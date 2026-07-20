from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from src.panel.features import PANEL_MODEL_FEATURES, target_horizon


@dataclass
class WalkForwardResult:
    """Các artifact do quá trình walk-forward panel tạo ra."""

    predictions: pd.DataFrame
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
    ):
        raise ValueError(
            "Cấu hình fold không hợp lệ: train>=2, validation/test>=1, "
            "step>=test, max_folds>=1 và min_symbols_per_date>=2."
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

    first_test = min_train_dates + purge + validation_dates + purge
    if len(labeled_dates) <= first_test:
        raise ValueError(
            "Không đủ ngày có nhãn cho walk-forward: "
            f"cần > {first_test}, hiện có {len(labeled_dates)}."
        )

    params, rounds, early_stopping_rounds = _xgboost_params(
        model_kind, xgboost_params
    )
    candidate_starts = list(range(first_test, len(labeled_dates), step))
    selected_starts = candidate_starts[-max_folds:]
    prediction_parts: list[pd.DataFrame] = []
    fold_records: list[dict[str, Any]] = []
    selected_rounds: list[int] = []

    for fold_number, test_start in enumerate(selected_starts, start=1):
        test_end = min(test_start + test_dates, len(labeled_dates))
        validation_end = test_start - purge
        validation_start = validation_end - validation_dates
        train_end = validation_start - purge
        train_date_values = labeled_dates[:train_end]
        validation_date_values = labeled_dates[validation_start:validation_end]
        held_out_dates = labeled_dates[test_start:test_end]
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

        _, best_rounds, history = _tune_with_validation(
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
        scored["actual_excess_return"] = scored[target]
        scored["actual_return"] = scored[f"target_return_{horizon}d"]
        scored["actual_market_return"] = scored[
            f"target_market_return_{horizon}d"
        ]
        keep = [
            "date",
            "symbol",
            "fold",
            "prediction",
            "prediction_score",
            "predicted_rank",
            "predicted_percentile",
            "actual_excess_return",
            "actual_return",
            "actual_market_return",
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
            }
        )

    if not prediction_parts:
        raise ValueError("Không tạo được fold walk-forward hợp lệ.")

    predictions = pd.concat(prediction_parts, ignore_index=True).sort_values(
        ["date", "predicted_rank"]
    )
    predictions = predictions.set_index(["date", "symbol"])
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
    latest_columns = [
        "date",
        "symbol",
        "prediction",
        "prediction_score",
        "predicted_rank",
        "predicted_percentile",
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
        "latest_feature_date": pd.Timestamp(latest_date),
        "execution": {
            "signal": "after_close_t",
            "entry": "open_t_plus_1",
            "exit": f"close_t_plus_{horizon}",
        },
    }
    return WalkForwardResult(
        predictions=predictions,
        latest_ranking=latest_ranking,
        folds=folds,
        feature_importance=importance,
        final_model=final_model,
        feature_columns=list(feature_columns),
        target_column=target,
        model_kind=model_kind,
        training_metadata=training_metadata,
    )
