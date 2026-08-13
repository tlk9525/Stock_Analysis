from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from src.panel.features import PANEL_MODEL_FEATURES, target_horizon
from src.panel.evaluation import performance_metrics, sparse_panel_backtest


@dataclass
class WalkForwardResult:
    """Các artifact do quá trình walk-forward panel tạo ra."""

    predictions: pd.DataFrame
    frozen_predictions: pd.DataFrame
    latest_ranking: pd.DataFrame
    folds: pd.DataFrame
    feature_importance: dict[str, float]
    final_model: Any
    feature_columns: list[str]
    target_column: str
    model_kind: str
    training_metadata: dict[str, Any]


def _panel_as_columns(panel: pd.DataFrame) -> pd.DataFrame:
    if isinstance(panel.index, pd.MultiIndex) and {"date", "symbol"}.issubset(
        panel.index.names
    ):
        frame = panel.reset_index()
    else:
        frame = panel.copy()
    if not {"date", "symbol"}.issubset(frame.columns):
        raise ValueError("Feature panel phải có date và symbol.")
    frame["date"] = pd.to_datetime(frame["date"]).dt.tz_localize(None)
    frame["symbol"] = frame["symbol"].astype(str).str.upper()
    return frame.sort_values(["date", "symbol"]).reset_index(drop=True)


def _xgboost_params(
    model_kind: str,
    options: Mapping[str, Any] | None,
) -> tuple[dict[str, Any], int, int]:
    supplied = dict(options or {})
    rounds = int(supplied.pop("num_boost_round", 150))
    early_stopping_rounds = int(supplied.pop("early_stopping_rounds", 30))
    if rounds <= 0 or early_stopping_rounds <= 0:
        raise ValueError("num_boost_round và early_stopping_rounds phải > 0.")
    aliases = {
        "learning_rate": "eta",
        "reg_lambda": "lambda",
        "reg_alpha": "alpha",
        "random_state": "seed",
        "n_jobs": "nthread",
    }
    for old_name, xgb_name in aliases.items():
        if old_name in supplied:
            supplied[xgb_name] = supplied.pop(old_name)
    defaults: dict[str, Any] = {
        "objective": (
            "reg:squarederror" if model_kind == "regression" else "rank:pairwise"
        ),
        "eval_metric": "rmse" if model_kind == "regression" else "ndcg",
        "tree_method": "hist",
        "eta": 0.05,
        "max_depth": 4,
        "min_child_weight": 3,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "lambda": 1.0,
        "alpha": 0.05,
        "seed": 42,
        "nthread": 4,
    }
    defaults.update(supplied)
    return defaults, rounds, early_stopping_rounds


def _relevance_labels(values: pd.Series, bins: int = 5) -> np.ndarray:
    """Đổi return liên tục thành relevance label theo từng ngày."""

    ranks = values.rank(method="average", pct=True)
    return np.minimum(
        (ranks * bins).apply(np.ceil).astype(int) - 1, bins - 1
    ).to_numpy()


def _matrix(
    xgb,
    frame: pd.DataFrame,
    feature_columns: Sequence[str],
    target: str | None,
    model_kind: str,
):
    ordered = frame.sort_values(["date", "symbol"])
    labels = None
    qid = None
    if target is not None:
        if model_kind == "ranking":
            labels = np.concatenate(
                [
                    _relevance_labels(group[target])
                    for _, group in ordered.groupby("date", sort=True)
                ]
            )
        else:
            labels = ordered[target].to_numpy(dtype=float)
    if model_kind == "ranking":
        qid = pd.factorize(ordered["date"], sort=True)[0]
    matrix = xgb.DMatrix(
        ordered[list(feature_columns)],
        label=labels,
        qid=qid,
        feature_names=list(feature_columns),
    )
    return matrix, ordered


def _fit(
    xgb,
    frame: pd.DataFrame,
    feature_columns: Sequence[str],
    target: str,
    model_kind: str,
    params: Mapping[str, Any],
    rounds: int,
):
    matrix, _ = _matrix(xgb, frame, feature_columns, target, model_kind)
    return xgb.train(
        params=dict(params),
        dtrain=matrix,
        num_boost_round=rounds,
        verbose_eval=False,
    )


def _tune_with_validation(
    xgb,
    train: pd.DataFrame,
    validation: pd.DataFrame,
    feature_columns: Sequence[str],
    target: str,
    model_kind: str,
    params: Mapping[str, Any],
    rounds: int,
    early_stopping_rounds: int,
) -> tuple[Any, int, dict]:
    train_matrix, _ = _matrix(
        xgb, train, feature_columns, target, model_kind
    )
    validation_matrix, _ = _matrix(
        xgb, validation, feature_columns, target, model_kind
    )
    history: dict = {}
    model = xgb.train(
        params=dict(params),
        dtrain=train_matrix,
        num_boost_round=rounds,
        evals=[(train_matrix, "train"), (validation_matrix, "validation")],
        evals_result=history,
        early_stopping_rounds=early_stopping_rounds,
        verbose_eval=False,
    )
    best_iteration = getattr(model, "best_iteration", rounds - 1)
    best_rounds = max(1, int(best_iteration) + 1)
    return model, best_rounds, history


def _score(
    xgb,
    model,
    frame: pd.DataFrame,
    feature_columns: Sequence[str],
    model_kind: str,
) -> pd.DataFrame:
    matrix, ordered = _matrix(
        xgb,
        frame,
        feature_columns,
        target=None,
        model_kind=model_kind,
    )
    scored = ordered.copy()
    scored["prediction"] = model.predict(matrix)
    scored["prediction_score"] = scored["prediction"]
    if model_kind == "regression":
        scored["predicted_excess_return"] = scored["prediction"]
    scored["predicted_rank"] = scored.groupby("date")["prediction"].rank(
        ascending=False, method="first"
    )
    scored["predicted_percentile"] = scored.groupby("date")["prediction"].rank(
        ascending=True, pct=True, method="average"
    )
    return scored


def _select_entry_margin(
    scored_validation: pd.DataFrame,
    *,
    candidates: Sequence[float],
    transaction_cost_bps: float,
    horizon: int,
    max_positions: int,
    min_symbols_per_date: int,
    minimum_trades: int,
    cooldown_cohorts: int,
) -> tuple[float | None, dict[str, Any]]:
    """Select the no-trade margin using validation data only."""

    trials: list[dict[str, Any]] = []
    annual_periods = 252.0 / horizon
    for raw_margin in sorted({float(value) for value in candidates}):
        if raw_margin < 0:
            raise ValueError("entry_margin_candidates không được âm.")
        cohorts, trades = sparse_panel_backtest(
            scored_validation,
            max_positions=max_positions,
            transaction_cost_bps=transaction_cost_bps,
            horizon=horizon,
            rebalance_every=horizon,
            min_symbols_per_date=min_symbols_per_date,
            prediction_column=(
                "prediction_lower_bound"
                if "prediction_lower_bound" in scored_validation
                else "prediction"
            ),
            entry_margin=raw_margin,
            entry_margin_column=None,
            rule_selected_column=None,
            cooldown_cohorts=cooldown_cohorts,
        )
        performance = performance_metrics(
            cohorts.get("net_return", pd.Series(dtype=float)),
            periods_per_year=annual_periods,
        )
        trial = {
            "margin": raw_margin,
            "completed_round_trips": int(len(trades)),
            "net_return": performance.get("total_return"),
            "sharpe": performance.get("sharpe"),
        }
        trials.append(trial)

    viable = [
        trial
        for trial in trials
        if trial["completed_round_trips"] >= minimum_trades
        and trial["net_return"] is not None
        and float(trial["net_return"]) > 0
    ]
    if not viable:
        return None, {"selected": False, "trials": trials}
    best = max(
        viable,
        key=lambda trial: (
            float(trial["net_return"]),
            float(trial["sharpe"] or float("-inf")),
            -int(trial["completed_round_trips"]),
            float(trial["margin"]),
        ),
    )
    return float(best["margin"]), {
        "selected": True,
        "selected_margin": float(best["margin"]),
        "trials": trials,
    }


def _eligible_dates(
    frame: pd.DataFrame,
    *,
    min_symbols_per_date: int,
) -> pd.Index:
    counts = frame.groupby("date")["symbol"].nunique()
    return pd.Index(counts[counts >= min_symbols_per_date].index).sort_values()


def walk_forward_predict(
    featured_panel: pd.DataFrame,
    *,
    target: str = "target_excess_return_20d",
    feature_columns: Sequence[str] = PANEL_MODEL_FEATURES,
    min_train_dates: int = 252,
    validation_dates: int = 5,
    test_dates: int = 20,
    step_dates: int | None = None,
    max_folds: int = 6,
    min_symbols_per_date: int = 2,
    gap: int | None = None,
    model_kind: str = "regression",
    xgboost_params: Mapping[str, Any] | None = None,
    transaction_cost_bps: float = 50.0,
    max_positions: int = 2,
    entry_margin_candidates: Sequence[float] = (0.0, 0.0025, 0.005, 0.01),
    minimum_validation_trades: int = 3,
    cooldown_cohorts: int = 0,
    frozen_holdout_dates: int = 0,
    lower_confidence_level: float = 0.80,
) -> WalkForwardResult:
    """Chạy expanding walk-forward có purge và validation độc lập.

    Mỗi fold có dạng ``train -> purge -> validation -> purge -> test``. Purge
    mặc định bằng horizon của target để nhãn train/validation không nhìn xuyên
    vào block kế tiếp. Phần đuôi chưa có nhãn không được đưa vào OOS test; nó
    chỉ được chấm riêng để tạo ranking mới nhất.
    """

    try:
        import xgboost as xgb
    except Exception as exc:
        raise RuntimeError("Không nạp được XGBoost cho panel model.") from exc

    if model_kind not in {"regression", "ranking"}:
        raise ValueError("model_kind chỉ nhận 'regression' hoặc 'ranking'.")
    step = test_dates if step_dates is None else int(step_dates)
    if (
        min_train_dates < 2
        or validation_dates < 1
        or test_dates < 1
        or step < test_dates
        or max_folds < 1
        or min_symbols_per_date < 2
        or max_positions < 1
        or max_positions > min_symbols_per_date
        or transaction_cost_bps < 0
        or minimum_validation_trades < 1
        or cooldown_cohorts < 0
        or frozen_holdout_dates < 0
        or not 0.5 <= lower_confidence_level < 1.0
    ):
        raise ValueError(
            "Cấu hình fold không hợp lệ: train>=2, validation/test>=1, "
            "step>=test, max_folds>=1, universe/position hợp lệ và phí không âm."
        )

    horizon = target_horizon(target)
    purge = horizon if gap is None else int(gap)
    if purge < horizon:
        raise ValueError(
            f"gap={purge} nhỏ hơn horizon={horizon}, có nguy cơ rò rỉ nhãn."
        )

    frame = _panel_as_columns(featured_panel)
    required = [*feature_columns, target]
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError(f"Feature panel thiếu cột: {', '.join(missing)}")

    predictable = frame.dropna(subset=list(feature_columns)).copy()
    predictable_dates = _eligible_dates(
        predictable, min_symbols_per_date=min_symbols_per_date
    )
    predictable = predictable[predictable["date"].isin(predictable_dates)]
    labeled = predictable.dropna(subset=[target]).copy()
    labeled_dates = _eligible_dates(
        labeled, min_symbols_per_date=min_symbols_per_date
    )
    labeled = labeled[labeled["date"].isin(labeled_dates)]

    if frozen_holdout_dates:
        minimum_required = (
            min_train_dates
            + purge
            + validation_dates
            + purge
            + test_dates
            + purge
            + frozen_holdout_dates
        )
        if len(labeled_dates) < minimum_required:
            raise ValueError(
                "Không đủ ngày cho frozen holdout tách biệt: "
                f"cần >= {minimum_required}, hiện có {len(labeled_dates)}."
            )
        frozen_dates_index = labeled_dates[-frozen_holdout_dates:]
        development_dates = labeled_dates[: -(frozen_holdout_dates + purge)]
    else:
        frozen_dates_index = pd.Index([])
        development_dates = labeled_dates

    first_test = min_train_dates + purge + validation_dates + purge
    if len(development_dates) <= first_test:
        raise ValueError(
            "Không đủ ngày có nhãn cho walk-forward: "
            f"cần > {first_test}, hiện có {len(development_dates)}."
        )

    params, rounds, early_stopping_rounds = _xgboost_params(
        model_kind, xgboost_params
    )
    candidate_starts = list(range(first_test, len(development_dates), step))
    selected_starts = candidate_starts[-max_folds:]
    prediction_parts: list[pd.DataFrame] = []
    fold_records: list[dict[str, Any]] = []
    selected_rounds: list[int] = []
    selected_margins: list[float] = []
    selected_haircuts: list[float] = []

    for fold_number, test_start in enumerate(selected_starts, start=1):
        test_end = min(test_start + test_dates, len(development_dates))
        validation_end = test_start - purge
        validation_start = validation_end - validation_dates
        train_end = validation_start - purge
        train_date_values = development_dates[:train_end]
        validation_date_values = development_dates[validation_start:validation_end]
        held_out_dates = development_dates[test_start:test_end]
        train = labeled[labeled["date"].isin(train_date_values)]
        validation = labeled[labeled["date"].isin(validation_date_values)]
        test = labeled[labeled["date"].isin(held_out_dates)]
        if train.empty or validation.empty or test.empty:
            continue
        if model_kind == "ranking":
            smallest_group = min(
                train.groupby("date")["symbol"].nunique().min(),
                validation.groupby("date")["symbol"].nunique().min(),
            )
            if smallest_group < 2:
                raise ValueError("Ranking model cần ít nhất hai mã mỗi ngày.")

        tuning_model, best_rounds, history = _tune_with_validation(
            xgb,
            train,
            validation,
            feature_columns,
            target,
            model_kind,
            params,
            rounds,
            early_stopping_rounds,
        )
        selected_rounds.append(best_rounds)
        validation_scored = _score(
            xgb, tuning_model, validation, feature_columns, model_kind
        )
        validation_scored["actual_excess_return"] = validation_scored[target]
        validation_scored["actual_return"] = validation_scored[
            f"target_return_{horizon}d"
        ]
        validation_scored["actual_market_return"] = validation_scored[
            f"target_market_return_{horizon}d"
        ]
        validation_overprediction = (
            validation_scored["prediction"]
            - validation_scored["actual_excess_return"]
        )
        prediction_haircut = max(
            0.0,
            float(validation_overprediction.quantile(lower_confidence_level)),
        )
        validation_scored["prediction_lower_bound"] = (
            validation_scored["prediction"] - prediction_haircut
        )
        selected_haircuts.append(prediction_haircut)
        if model_kind == "regression":
            selected_margin, margin_audit = _select_entry_margin(
                validation_scored,
                candidates=entry_margin_candidates,
                transaction_cost_bps=transaction_cost_bps,
                horizon=horizon,
                max_positions=max_positions,
                min_symbols_per_date=min_symbols_per_date,
                minimum_trades=minimum_validation_trades,
                cooldown_cohorts=cooldown_cohorts,
            )
        else:
            selected_margin, margin_audit = None, {
                "selected": False,
                "reason": "ranking_score_has_no_absolute_return_scale",
                "trials": [],
            }
        if selected_margin is not None:
            selected_margins.append(selected_margin)
        training_pool = pd.concat([train, validation], ignore_index=True)
        model = _fit(
            xgb,
            training_pool,
            feature_columns,
            target,
            model_kind,
            params,
            best_rounds,
        )
        scored = _score(xgb, model, test, feature_columns, model_kind)
        scored["fold"] = fold_number
        scored["entry_margin"] = (
            float(selected_margin) if selected_margin is not None else np.nan
        )
        scored["prediction_haircut"] = prediction_haircut
        scored["prediction_lower_bound"] = (
            scored["prediction"] - prediction_haircut
        )
        scored["entry_rule_selected"] = selected_margin is not None
        scored["entry_threshold"] = (
            transaction_cost_bps / 10_000 + selected_margin
            if selected_margin is not None
            else np.nan
        )
        scored["expected_net_edge"] = scored["prediction_lower_bound"] - (
            transaction_cost_bps / 10_000
        )
        scored["actual_excess_return"] = scored[target]
        scored["actual_return"] = scored[f"target_return_{horizon}d"]
        scored["actual_market_return"] = scored[
            f"target_market_return_{horizon}d"
        ]
        for output_name, source_name in {
            "entry_date": f"target_entry_date_{horizon}d",
            "exit_date": f"target_exit_date_{horizon}d",
            "entry_price": f"target_entry_open_{horizon}d",
            "exit_price": f"target_exit_close_{horizon}d",
        }.items():
            scored[output_name] = scored.get(source_name, np.nan)
        keep = [
            "date",
            "symbol",
            "fold",
            "prediction",
            "prediction_score",
            "predicted_rank",
            "predicted_percentile",
            "prediction_haircut",
            "prediction_lower_bound",
            "entry_margin",
            "entry_rule_selected",
            "entry_threshold",
            "expected_net_edge",
            "actual_excess_return",
            "actual_return",
            "actual_market_return",
            "entry_date",
            "exit_date",
            "entry_price",
            "exit_price",
        ]
        if model_kind == "regression":
            keep.append("predicted_excess_return")
        if "market_regime" in scored:
            keep.append("market_regime")
        prediction_parts.append(scored[keep])

        metric_name = "rmse" if model_kind == "regression" else "ndcg"
        fold_records.append(
            {
                "fold": fold_number,
                "train_start": train["date"].min(),
                "train_end": train["date"].max(),
                "validation_start": validation["date"].min(),
                "validation_end": validation["date"].max(),
                "test_start": test["date"].min(),
                "test_end": test["date"].max(),
                "train_dates": int(train["date"].nunique()),
                "train_rows": int(len(train)),
                "validation_dates": int(validation["date"].nunique()),
                "validation_rows": int(len(validation)),
                "test_dates": int(test["date"].nunique()),
                "test_rows": int(len(test)),
                "gap": purge,
                "best_iteration": best_rounds - 1,
                "num_boost_round": best_rounds,
                "validation_metric": metric_name,
                "validation_score_at_best": float(
                    history["validation"][metric_name][best_rounds - 1]
                ),
                "entry_margin_selected": selected_margin,
                "entry_rule_selected": selected_margin is not None,
                "entry_margin_audit": margin_audit,
                "prediction_haircut": prediction_haircut,
                "lower_confidence_level": lower_confidence_level,
            }
        )

    if not prediction_parts:
        raise ValueError("Không tạo được fold walk-forward hợp lệ.")

    predictions = pd.concat(prediction_parts, ignore_index=True).sort_values(
        ["date", "predicted_rank"]
    )
    predictions = predictions.set_index(["date", "symbol"])

    frozen_predictions = pd.DataFrame()
    frozen_audit: dict[str, Any] = {
        "enabled": bool(frozen_holdout_dates),
        "dates": int(frozen_holdout_dates),
        "entry_rule_selected": False,
    }
    if frozen_holdout_dates:
        pre_frozen_dates = labeled_dates[: -(frozen_holdout_dates + purge)]
        frozen_validation_end = len(pre_frozen_dates)
        frozen_validation_start = frozen_validation_end - validation_dates
        frozen_train_end = frozen_validation_start - purge
        frozen_train_dates = pre_frozen_dates[:frozen_train_end]
        frozen_validation_dates_index = pre_frozen_dates[
            frozen_validation_start:frozen_validation_end
        ]
        frozen_train = labeled[labeled["date"].isin(frozen_train_dates)]
        frozen_validation = labeled[
            labeled["date"].isin(frozen_validation_dates_index)
        ]
        frozen_test = labeled[labeled["date"].isin(frozen_dates_index)]
        tuning_model, frozen_rounds, _ = _tune_with_validation(
            xgb,
            frozen_train,
            frozen_validation,
            feature_columns,
            target,
            model_kind,
            params,
            rounds,
            early_stopping_rounds,
        )
        frozen_validation_scored = _score(
            xgb, tuning_model, frozen_validation, feature_columns, model_kind
        )
        frozen_validation_scored["actual_excess_return"] = (
            frozen_validation_scored[target]
        )
        frozen_validation_scored["actual_return"] = frozen_validation_scored[
            f"target_return_{horizon}d"
        ]
        frozen_validation_scored["actual_market_return"] = (
            frozen_validation_scored[f"target_market_return_{horizon}d"]
        )
        frozen_overprediction = (
            frozen_validation_scored["prediction"]
            - frozen_validation_scored["actual_excess_return"]
        )
        frozen_haircut = max(
            0.0,
            float(frozen_overprediction.quantile(lower_confidence_level)),
        )
        frozen_validation_scored["prediction_lower_bound"] = (
            frozen_validation_scored["prediction"] - frozen_haircut
        )
        if model_kind == "regression":
            frozen_margin, frozen_margin_audit = _select_entry_margin(
                frozen_validation_scored,
                candidates=entry_margin_candidates,
                transaction_cost_bps=transaction_cost_bps,
                horizon=horizon,
                max_positions=max_positions,
                min_symbols_per_date=min_symbols_per_date,
                minimum_trades=minimum_validation_trades,
                cooldown_cohorts=cooldown_cohorts,
            )
        else:
            frozen_margin, frozen_margin_audit = None, {
                "selected": False,
                "reason": "ranking_score_has_no_absolute_return_scale",
                "trials": [],
            }
        frozen_model = _fit(
            xgb,
            pd.concat([frozen_train, frozen_validation], ignore_index=True),
            feature_columns,
            target,
            model_kind,
            params,
            frozen_rounds,
        )
        frozen_scored = _score(
            xgb, frozen_model, frozen_test, feature_columns, model_kind
        )
        frozen_scored["fold"] = "frozen"
        frozen_scored["entry_margin"] = frozen_margin
        frozen_scored["prediction_haircut"] = frozen_haircut
        frozen_scored["prediction_lower_bound"] = (
            frozen_scored["prediction"] - frozen_haircut
        )
        frozen_scored["entry_rule_selected"] = frozen_margin is not None
        frozen_scored["entry_threshold"] = (
            transaction_cost_bps / 10_000 + frozen_margin
            if frozen_margin is not None
            else np.nan
        )
        frozen_scored["expected_net_edge"] = frozen_scored[
            "prediction_lower_bound"
        ] - (
            transaction_cost_bps / 10_000
        )
        frozen_scored["actual_excess_return"] = frozen_scored[target]
        frozen_scored["actual_return"] = frozen_scored[
            f"target_return_{horizon}d"
        ]
        frozen_scored["actual_market_return"] = frozen_scored[
            f"target_market_return_{horizon}d"
        ]
        for output_name, source_name in {
            "entry_date": f"target_entry_date_{horizon}d",
            "exit_date": f"target_exit_date_{horizon}d",
            "entry_price": f"target_entry_open_{horizon}d",
            "exit_price": f"target_exit_close_{horizon}d",
        }.items():
            frozen_scored[output_name] = frozen_scored.get(source_name, np.nan)
        frozen_keep = [
            "date", "symbol", "fold", "prediction", "prediction_score",
            "predicted_rank", "predicted_percentile", "entry_margin",
            "prediction_haircut", "prediction_lower_bound",
            "entry_rule_selected", "entry_threshold", "expected_net_edge",
            "actual_excess_return", "actual_return", "actual_market_return",
            "entry_date", "exit_date", "entry_price", "exit_price",
        ]
        if model_kind == "regression":
            frozen_keep.append("predicted_excess_return")
        if "market_regime" in frozen_scored:
            frozen_keep.append("market_regime")
        frozen_predictions = frozen_scored[frozen_keep].set_index(
            ["date", "symbol"]
        ).sort_index()
        frozen_audit = {
            "enabled": True,
            "dates": int(frozen_holdout_dates),
            "start": pd.Timestamp(frozen_dates_index.min()),
            "end": pd.Timestamp(frozen_dates_index.max()),
            "purge_before_frozen": int(purge),
            "selected_num_boost_round": int(frozen_rounds),
            "entry_margin": frozen_margin,
            "prediction_haircut": frozen_haircut,
            "lower_confidence_level": lower_confidence_level,
            "entry_rule_selected": frozen_margin is not None,
            "entry_margin_audit": frozen_margin_audit,
        }
    final_rounds = max(1, int(round(float(np.median(selected_rounds)))))
    final_model = _fit(
        xgb,
        labeled,
        feature_columns,
        target,
        model_kind,
        params,
        final_rounds,
    )

    latest_date = predictable_dates.max()
    latest = predictable[predictable["date"] == latest_date]
    if latest["symbol"].nunique() < min_symbols_per_date:
        raise ValueError("Ngày mới nhất không đủ số mã để xuất ranking.")
    latest_scored = _score(
        xgb,
        final_model,
        latest,
        feature_columns,
        model_kind,
    )
    live_margin = (
        float(np.median(selected_margins)) if selected_margins else None
    )
    live_haircut = (
        float(np.median(selected_haircuts)) if selected_haircuts else 0.0
    )
    latest_scored["entry_margin"] = live_margin
    latest_scored["prediction_haircut"] = live_haircut
    latest_scored["prediction_lower_bound"] = (
        latest_scored["prediction"] - live_haircut
    )
    latest_scored["entry_rule_selected"] = live_margin is not None
    latest_scored["entry_threshold"] = (
        transaction_cost_bps / 10_000 + live_margin
        if live_margin is not None
        else np.nan
    )
    latest_scored["expected_net_edge"] = latest_scored[
        "prediction_lower_bound"
    ] - (
        transaction_cost_bps / 10_000
    )
    latest_scored["candidate_decision"] = np.where(
        latest_scored["entry_rule_selected"]
        & (
            latest_scored["prediction_lower_bound"]
            > latest_scored["entry_threshold"]
        ),
        "BUY_CANDIDATE",
        "WAIT",
    )
    latest_columns = [
        "date",
        "symbol",
        "prediction",
        "prediction_score",
        "predicted_rank",
        "predicted_percentile",
        "prediction_haircut",
        "prediction_lower_bound",
        "entry_margin",
        "entry_rule_selected",
        "entry_threshold",
        "expected_net_edge",
        "candidate_decision",
    ]
    if model_kind == "regression":
        latest_columns.append("predicted_excess_return")
    latest_ranking = latest_scored[latest_columns].set_index(["date", "symbol"])
    latest_ranking = latest_ranking.sort_values("predicted_rank")

    raw_importance = final_model.get_score(importance_type="gain")
    importance = {
        feature: float(raw_importance.get(feature, 0.0))
        for feature in feature_columns
    }
    importance = dict(
        sorted(importance.items(), key=lambda item: item[1], reverse=True)
    )
    folds = pd.DataFrame(fold_records).set_index("fold")
    training_metadata = {
        "layout": "train -> purge -> validation -> purge -> test",
        "horizon": horizon,
        "gap": purge,
        "fold_count": int(len(folds)),
        "min_symbols_per_date": min_symbols_per_date,
        "selected_num_boost_round": final_rounds,
        "entry_margin_candidates": [float(value) for value in entry_margin_candidates],
        "selected_entry_margin_median": live_margin,
        "valid_margin_selections": int(len(selected_margins)),
        "selected_prediction_haircut_median": live_haircut,
        "lower_confidence_level": float(lower_confidence_level),
        "transaction_cost_bps": float(transaction_cost_bps),
        "max_positions": int(max_positions),
        "cooldown_cohorts": int(cooldown_cohorts),
        "frozen_holdout": frozen_audit,
        "latest_feature_date": pd.Timestamp(latest_date),
        "execution": {
            "signal": "after_close_t",
            "entry": "open_t_plus_1",
            "exit": f"close_t_plus_{horizon}",
        },
    }
    return WalkForwardResult(
        predictions=predictions,
        frozen_predictions=frozen_predictions,
        latest_ranking=latest_ranking,
        folds=folds,
        feature_importance=importance,
        final_model=final_model,
        feature_columns=list(feature_columns),
        target_column=target,
        model_kind=model_kind,
        training_metadata=training_metadata,
    )
