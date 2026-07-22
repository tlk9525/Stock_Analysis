from __future__ import annotations

import numpy as np
import pandas as pd

from src.backtest import run_long_only_backtest
from src.features.technical import MODEL_FEATURES, latest_model_features
from src.models.logistic import fit_logistic, predict_logistic
from src.models.metrics import (
    binary_metrics,
    classification_metrics_by_fold,
)
from src.utils import resolve_price_multiplier


def _integer_option(
    options: dict,
    names: tuple[str, ...],
    default: int,
    *,
    minimum: int,
) -> int:
    raw_value = next((options[name] for name in names if name in options), default)
    value = int(raw_value)
    if value < minimum:
        joined = "/".join(names)
        raise ValueError(f"{joined} phải lớn hơn hoặc bằng {minimum}.")
    return value


def _section_option(
    primary: dict,
    fallback: dict,
    names: tuple[str, ...],
    default,
):
    for section in (primary, fallback):
        for name in names:
            if name in section:
                return section[name]
    return default


def resolve_walk_forward_settings(row_count: int, config: dict) -> dict:
    """Lấy cấu hình walk-forward, có mặc định hợp lý khi config cũ chưa có mục này."""

    validation_options = config.get("validation", {}) or {}
    walk_forward_options = config.get("walk_forward", {}) or {}
    if not isinstance(validation_options, dict) or not isinstance(
        walk_forward_options, dict
    ):
        raise ValueError("validation/walk_forward trong config phải là object.")
    default_min_train = max(60, min(504, int(row_count * 0.50)))
    default_validation = max(20, min(126, int(row_count * 0.10)))
    default_test = max(20, min(126, int(row_count * 0.10)))
    options = {
        "min_train_rows": _section_option(
            walk_forward_options,
            validation_options,
            ("min_train_rows", "min_train_size"),
            default_min_train,
        ),
        "validation_rows": _section_option(
            walk_forward_options,
            validation_options,
            ("validation_rows", "validation_size"),
            default_validation,
        ),
        "test_rows": _section_option(
            walk_forward_options,
            validation_options,
            ("test_rows", "test_size"),
            default_test,
        ),
        "gap_rows": _section_option(
            walk_forward_options,
            validation_options,
            ("gap_rows", "gap"),
            1,
        ),
        "max_folds": _section_option(
            walk_forward_options,
            validation_options,
            ("max_folds",),
            5,
        ),
        "step_rows": _section_option(
            walk_forward_options,
            validation_options,
            ("step_rows",),
            None,
        ),
    }
    settings = {
        "min_train_rows": _integer_option(
            options,
            ("min_train_rows", "min_train_size"),
            default_min_train,
            minimum=20,
        ),
        "validation_rows": _integer_option(
            options,
            ("validation_rows", "validation_size"),
            default_validation,
            minimum=1,
        ),
        "test_rows": _integer_option(
            options,
            ("test_rows", "test_size"),
            default_test,
            minimum=1,
        ),
        "gap_rows": _integer_option(
            options,
            ("gap_rows",),
            1,
            minimum=1,
        ),
        "max_folds": _integer_option(
            options,
            ("max_folds",),
            5,
            minimum=1,
        ),
    }
    if options["step_rows"] is None:
        options["step_rows"] = settings["test_rows"]
    settings["step_rows"] = _integer_option(
        options,
        ("step_rows",),
        settings["test_rows"],
        minimum=1,
    )
    if settings["step_rows"] != settings["test_rows"]:
        raise ValueError(
            "step_rows phải bằng test_rows để chuỗi OOS/backtest không bị trùng "
            "hoặc bỏ trống phiên."
        )
    return settings


def build_walk_forward_splits(row_count: int, config: dict) -> tuple[list[dict], dict]:
    """Tạo expanding folds: train -> gap -> validation -> gap -> test.

    Các test block không trùng nhau. Nếu số fold vượt ``max_folds``, chỉ giữ
    các fold mới nhất để OOS metrics phản ánh giai đoạn gần hiện tại hơn.
    """

    settings = resolve_walk_forward_settings(row_count, config)
    min_train = settings["min_train_rows"]
    validation_rows = settings["validation_rows"]
    test_rows = settings["test_rows"]
    step_rows = settings["step_rows"]
    gap = settings["gap_rows"]
    first_test_start = min_train + gap + validation_rows + gap
    if first_test_start >= row_count:
        required = first_test_start + 1
        raise ValueError(
            "Không đủ dữ liệu để tạo walk-forward fold: "
            f"cần tối thiểu {required} dòng labeled, hiện có {row_count}."
        )

    candidates: list[dict] = []
    for test_start in range(first_test_start, row_count, step_rows):
        test_end = min(test_start + test_rows, row_count)
        validation_end = test_start - gap
        validation_start = validation_end - validation_rows
        train_end = validation_start - gap
        candidates.append(
            {
                "train_start": 0,
                "train_end": train_end,
                "validation_start": validation_start,
                "validation_end": validation_end,
                "test_start": test_start,
                "test_end": test_end,
            }
        )

    selected = candidates[-settings["max_folds"] :]
    for fold_number, split in enumerate(selected, start=1):
        split["fold"] = fold_number
    return selected, settings


def _prepare_model_data(
    frame: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    missing = [
        column
        for column in [*MODEL_FEATURES, "target_next_up"]
        if column not in frame.columns
    ]
    if missing:
        raise ValueError(f"Thiếu cột để train model: {', '.join(missing)}")

    # Helper này lấy frame.iloc[-1] trước khi target bị drop và từ chối stale row.
    latest_features = latest_model_features(frame, MODEL_FEATURES)
    if latest_features.index[0] != frame.index[-1]:
        raise AssertionError("Feature latest không trùng với dòng cuối của frame.")

    labeled = frame.dropna(subset=[*MODEL_FEATURES, "target_next_up"]).copy()
    numeric_features = labeled[MODEL_FEATURES].apply(pd.to_numeric, errors="coerce")
    finite_rows = np.isfinite(numeric_features.to_numpy(dtype=float)).all(axis=1)
    labeled = labeled.loc[finite_rows].copy()
    labeled[MODEL_FEATURES] = numeric_features.loc[finite_rows]
    labeled["target_next_up"] = pd.to_numeric(
        labeled["target_next_up"], errors="coerce"
    )
    valid_target = labeled["target_next_up"].isin([0, 1])
    labeled = labeled.loc[valid_target].copy()
    labeled["target_next_up"] = labeled["target_next_up"].astype(int)
    if labeled.empty:
        raise ValueError("Không có dòng labeled hợp lệ để train model.")
    return labeled, latest_features


def _split_data(
    frame: pd.DataFrame,
    config: dict | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Compatibility helper: trả về train/validation/test của fold mới nhất."""

    labeled, latest_features = _prepare_model_data(frame)
    splits, _ = build_walk_forward_splits(len(labeled), config or {})
    latest_split = splits[-1]
    return (
        labeled.iloc[latest_split["train_start"] : latest_split["train_end"]],
        labeled.iloc[latest_split["validation_start"] : latest_split["validation_end"]],
        labeled.iloc[latest_split["test_start"] : latest_split["test_end"]],
        latest_features,
    )


def _xgboost_params(config: dict, labels: pd.Series) -> tuple[dict, dict]:
    options = config.get("xgboost", {})
    positives = max(float(labels.sum()), 1.0)
    negatives = max(float(len(labels) - labels.sum()), 1.0)
    scale_pos_weight = negatives / positives
    params = {
        "objective": "binary:logistic",
        "eval_metric": "logloss",
        "tree_method": "hist",
        "eta": float(options.get("learning_rate", 0.03)),
        "max_depth": int(options.get("max_depth", 4)),
        "min_child_weight": float(options.get("min_child_weight", 3)),
        "subsample": float(options.get("subsample", 0.8)),
        "colsample_bytree": float(options.get("colsample_bytree", 0.8)),
        "lambda": float(options.get("reg_lambda", 1.0)),
        "alpha": float(options.get("reg_alpha", 0.05)),
        "scale_pos_weight": scale_pos_weight,
        "seed": int(options.get("random_state", 42)),
        "nthread": int(options.get("n_jobs", 4)),
    }
    training = {
        "num_boost_round": int(options.get("num_boost_round", 400)),
        "early_stopping_rounds": int(options.get("early_stopping_rounds", 40)),
        "scale_pos_weight": float(scale_pos_weight),
    }
    if training["num_boost_round"] < 1 or training["early_stopping_rounds"] < 1:
        raise ValueError("Số boosting round và early stopping phải lớn hơn 0.")
    return params, training


def _best_iteration(booster, default_rounds: int) -> int:
    try:
        return int(booster.best_iteration)
    except (AttributeError, TypeError):
        return default_rounds - 1


def _date_text(value) -> str:
    timestamp = pd.Timestamp(value)
    return str(timestamp.date())


def _liquidity_estimate_at_signal(frame: pd.DataFrame) -> pd.Series:
    """Trả về ADV đã biết ở close[t], không dùng volume tương lai."""

    if "volume_sma_20" in frame:
        return pd.to_numeric(frame["volume_sma_20"], errors="coerce")
    return pd.to_numeric(frame["volume"], errors="coerce").rolling(
        20, min_periods=1
    ).mean()


def _fold_metadata(
    split: dict,
    train: pd.DataFrame,
    validation: pd.DataFrame,
    test: pd.DataFrame,
    gap_rows: int,
) -> dict:
    return {
        "fold": int(split["fold"]),
        "train_start": _date_text(train.index.min()),
        "train_end": _date_text(train.index.max()),
        "validation_start": _date_text(validation.index.min()),
        "validation_end": _date_text(validation.index.max()),
        "test_start": _date_text(test.index.min()),
        "test_end": _date_text(test.index.max()),
        "train_rows": int(len(train)),
        "validation_rows": int(len(validation)),
        "test_rows": int(len(test)),
        "gap_rows_each_boundary": int(gap_rows),
    }


def train_models(
    frame: pd.DataFrame,
    config: dict,
) -> tuple[dict, pd.DataFrame, dict, object]:
    try:
        import xgboost as xgb
    except Exception as exc:
        raise RuntimeError(
            "Không nạp được XGBoost. Hãy chạy ./setup_env.sh và cài OpenMP trên macOS."
        ) from exc

    labeled, latest_features = _prepare_model_data(frame)
    splits, walk_forward_settings = build_walk_forward_splits(len(labeled), config)
    validation_options = config.get("validation", {}) or {}
    walk_forward_options = config.get("walk_forward", {}) or {}
    backtest_options = config.get("backtest", {}) or {}
    decision_threshold = float(
        walk_forward_options.get(
            "decision_threshold",
            validation_options.get(
                "decision_threshold",
                backtest_options.get("signal_threshold", 0.5),
            ),
        )
    )
    if not 0 < decision_threshold < 1:
        raise ValueError("decision_threshold phải nằm trong khoảng (0, 1).")

    scored_folds: list[pd.DataFrame] = []
    fold_ids: list[int] = []
    fold_records: list[dict] = []
    best_rounds_by_fold: list[int] = []
    majority_classes: list[int] = []

    for split in splits:
        train = labeled.iloc[split["train_start"] : split["train_end"]]
        validation = labeled.iloc[split["validation_start"] : split["validation_end"]]
        test = labeled.iloc[split["test_start"] : split["test_end"]]

        params, training_options = _xgboost_params(config, train["target_next_up"])
        train_matrix = xgb.DMatrix(
            train[MODEL_FEATURES],
            label=train["target_next_up"],
            feature_names=MODEL_FEATURES,
        )
        validation_matrix = xgb.DMatrix(
            validation[MODEL_FEATURES],
            label=validation["target_next_up"],
            feature_names=MODEL_FEATURES,
        )
        evaluation_history: dict = {}
        tuning_booster = xgb.train(
            params=params,
            dtrain=train_matrix,
            num_boost_round=training_options["num_boost_round"],
            evals=[(train_matrix, "train"), (validation_matrix, "validation")],
            evals_result=evaluation_history,
            early_stopping_rounds=training_options["early_stopping_rounds"],
            verbose_eval=False,
        )
        best_iteration = _best_iteration(
            tuning_booster,
            training_options["num_boost_round"],
        )
        best_rounds = best_iteration + 1
        best_rounds_by_fold.append(best_rounds)

        # Refit trên train + validation; hai embargo gap vẫn bị loại khỏi fold.
        training_pool = pd.concat([train, validation])
        evaluation_params, _ = _xgboost_params(
            config,
            training_pool["target_next_up"],
        )
        pool_matrix = xgb.DMatrix(
            training_pool[MODEL_FEATURES],
            label=training_pool["target_next_up"],
            feature_names=MODEL_FEATURES,
        )
        evaluation_booster = xgb.train(
            params=evaluation_params,
            dtrain=pool_matrix,
            num_boost_round=best_rounds,
            verbose_eval=False,
        )
        test_matrix = xgb.DMatrix(
            test[MODEL_FEATURES],
            label=test["target_next_up"],
            feature_names=MODEL_FEATURES,
        )
        xgboost_probability = evaluation_booster.predict(test_matrix)

        logistic_model = fit_logistic(
            training_pool[MODEL_FEATURES],
            training_pool["target_next_up"],
        )
        logistic_probability = predict_logistic(
            logistic_model,
            test[MODEL_FEATURES],
        )
        majority_class = int(training_pool["target_next_up"].mode().iloc[0])
        majority_classes.append(majority_class)

        scored = test.copy()
        scored["xgboost_prediction"] = (
            xgboost_probability >= decision_threshold
        ).astype(int)
        scored["xgboost_prob_up"] = xgboost_probability
        scored["logistic_prediction"] = (
            logistic_probability >= decision_threshold
        ).astype(int)
        scored["logistic_prob_up"] = logistic_probability
        scored_folds.append(scored)
        fold_ids.extend([int(split["fold"])] * len(test))

        metadata = _fold_metadata(
            split,
            train,
            validation,
            test,
            walk_forward_settings["gap_rows"],
        )
        metadata.update(
            {
                "best_iteration": int(best_iteration),
                "num_boost_round": int(best_rounds),
                "majority_class": majority_class,
                "scale_pos_weight": float(training_options["scale_pos_weight"]),
                "train_logloss_at_best": float(
                    evaluation_history["train"]["logloss"][best_iteration]
                ),
                "validation_logloss_at_best": float(
                    evaluation_history["validation"]["logloss"][best_iteration]
                ),
            }
        )
        fold_records.append(metadata)

    scored_test = pd.concat(scored_folds).sort_index()
    fold_id_array = np.asarray(fold_ids, dtype=int)
    y_oos = scored_test["target_next_up"]
    xgboost_metrics, xgboost_per_fold = classification_metrics_by_fold(
        y_oos,
        scored_test["xgboost_prob_up"].to_numpy(),
        fold_id_array,
        decision_threshold,
    )
    logistic_metrics, logistic_per_fold = classification_metrics_by_fold(
        y_oos,
        scored_test["logistic_prob_up"].to_numpy(),
        fold_id_array,
        decision_threshold,
    )

    majority_predictions = np.concatenate(
        [
            np.full(record["test_rows"], record["majority_class"], dtype=int)
            for record in fold_records
        ]
    )
    majority_metrics = binary_metrics(y_oos, majority_predictions)
    majority_per_fold: list[dict] = []
    for record in fold_records:
        selected = fold_id_array == record["fold"]
        prediction = np.full(selected.sum(), record["majority_class"], dtype=int)
        majority_per_fold.append(
            {
                "fold": record["fold"],
                "class": record["majority_class"],
                **binary_metrics(y_oos.to_numpy()[selected], prediction),
            }
        )

    selected_rounds = max(1, int(round(float(np.median(best_rounds_by_fold)))))
    final_params, _ = _xgboost_params(config, labeled["target_next_up"])
    final_matrix = xgb.DMatrix(
        labeled[MODEL_FEATURES],
        label=labeled["target_next_up"],
        feature_names=MODEL_FEATURES,
    )
    final_booster = xgb.train(
        params=final_params,
        dtrain=final_matrix,
        num_boost_round=selected_rounds,
        verbose_eval=False,
    )
    latest_matrix = xgb.DMatrix(latest_features, feature_names=MODEL_FEATURES)
    latest_xgboost_probability = float(final_booster.predict(latest_matrix)[0])

    final_logistic = fit_logistic(
        labeled[MODEL_FEATURES],
        labeled["target_next_up"],
    )
    latest_logistic_probability = float(
        predict_logistic(final_logistic, latest_features)[0]
    )

    importance = final_booster.get_score(importance_type="gain")
    feature_importance = {
        feature: float(importance.get(feature, 0.0)) for feature in MODEL_FEATURES
    }
    feature_importance = dict(
        sorted(feature_importance.items(), key=lambda item: item[1], reverse=True)
    )
    xgboost_metrics.update(
        {
            "best_iteration": int(selected_rounds - 1),
            "selected_num_boost_round": int(selected_rounds),
            "best_round_selection": "median_num_boost_round_across_walk_forward_folds",
            "scale_pos_weight": float(final_params["scale_pos_weight"]),
            "feature_importance_gain": feature_importance,
            # Giữ các key cũ cho report/downstream hiện tại.
            "train_logloss_at_best": fold_records[-1]["train_logloss_at_best"],
            "validation_logloss_at_best": fold_records[-1][
                "validation_logloss_at_best"
            ],
            "per_fold": xgboost_per_fold,
        }
    )
    logistic_metrics["per_fold"] = logistic_per_fold
    majority_metrics.update(
        {
            "class": int(majority_classes[-1]),
            "classes_by_fold": majority_classes,
            "per_fold": majority_per_fold,
        }
    )

    for record, xgb_fold, logistic_fold, majority_fold in zip(
        fold_records,
        xgboost_per_fold,
        logistic_per_fold,
        majority_per_fold,
    ):
        record["xgboost_metrics"] = xgb_fold
        record["logistic_metrics"] = logistic_fold
        record["majority_metrics"] = majority_fold

    latest_fold = fold_records[-1]
    validation_summary = {
        "scheme": "expanding_walk_forward",
        "fold_count": int(len(fold_records)),
        "gap_rows": walk_forward_settings["gap_rows"],
        "min_train_rows": walk_forward_settings["min_train_rows"],
        "validation_rows": walk_forward_settings["validation_rows"],
        "test_rows": walk_forward_settings["test_rows"],
        "step_rows": walk_forward_settings["step_rows"],
        "max_folds": walk_forward_settings["max_folds"],
        "layout": "train -> gap -> validation -> gap -> test",
        "folds": fold_records,
    }
    metrics = {
        "split": {
            "strategy": "expanding_walk_forward",
            "train_start": latest_fold["train_start"],
            "train_end": latest_fold["train_end"],
            "validation_start": latest_fold["validation_start"],
            "validation_end": latest_fold["validation_end"],
            "test_start": _date_text(scored_test.index.min()),
            "test_end": _date_text(scored_test.index.max()),
            "train_rows": latest_fold["train_rows"],
            "validation_rows": latest_fold["validation_rows"],
            "test_rows": int(len(scored_test)),
            "oos_rows": int(len(scored_test)),
            "fold_count": int(len(fold_records)),
            "gap_rows_each_boundary": walk_forward_settings["gap_rows"],
            "latest_feature_date": _date_text(latest_features.index[0]),
        },
        "walk_forward": {
            **walk_forward_settings,
            "layout": "train -> gap -> validation -> gap -> test",
            "folds": fold_records,
        },
        # Compatibility key được dashboard/PostgreSQL hiện tại sử dụng.
        "validation": validation_summary,
        "xgboost": xgboost_metrics,
        "logistic_baseline": logistic_metrics,
        "majority_baseline": majority_metrics,
    }

    if "next_return" in scored_test and scored_test["next_return"].notna().any():
        backtest_signal_threshold = float(
            backtest_options.get("signal_threshold", decision_threshold)
        )
        if not 0 < backtest_signal_threshold < 1:
            raise ValueError("backtest.signal_threshold phải nằm trong khoảng (0, 1).")
        backtest_frame = scored_test.copy()
        backtest_frame["backtest_signal"] = (
            backtest_frame["xgboost_prob_up"] >= backtest_signal_threshold
        ).astype(int)
        commission_bps = float(backtest_options.get("commission_bps_per_side", 15.0))
        slippage_bps = float(backtest_options.get("slippage_bps_per_side", 5.0))
        sell_tax_bps = float(backtest_options.get("sell_tax_bps", 10.0))
        explicit_round_trip_cost = backtest_options.get(
            "round_trip_cost_bps",
            config.get("round_trip_cost_bps"),
        )
        if explicit_round_trip_cost is None:
            round_trip_cost_bps = None
            entry_cost_bps = commission_bps + slippage_bps
            exit_cost_bps = commission_bps + slippage_bps + sell_tax_bps
        else:
            round_trip_cost_bps = float(explicit_round_trip_cost)
            entry_cost_bps = None
            exit_cost_bps = None

        has_execution_data = {"open", "volume"}.issubset(frame.columns)
        if has_execution_data:
            backtest_frame["execution_open"] = (
                frame["open"].shift(-1).reindex(backtest_frame.index)
            )
            known_volume_estimate = _liquidity_estimate_at_signal(frame)
            backtest_frame["execution_volume_estimate"] = (
                known_volume_estimate.reindex(backtest_frame.index)
            )
        initial_capital = (
            float(config.get("risk_capital_vnd", 100_000_000))
            if has_execution_data
            else None
        )
        execution_lag = int(backtest_options.get("execution_lag", 0))
        if execution_lag != 0:
            raise ValueError(
                "backtest.execution_lag phải bằng 0 vì next_return đã được gắn "
                "forward tại ngày phát tín hiệu."
            )
        backtest_metrics, backtest_details = run_long_only_backtest(
            backtest_frame,
            signal_column="backtest_signal",
            return_column="next_return",
            execution_lag=execution_lag,
            round_trip_cost_bps=round_trip_cost_bps,
            entry_cost_bps=entry_cost_bps,
            exit_cost_bps=exit_cost_bps,
            periods_per_year=int(backtest_options.get("periods_per_year", 252)),
            round_trip_each_signal=True,
            entry_price_column="execution_open" if has_execution_data else None,
            volume_column=(
                "execution_volume_estimate" if has_execution_data else None
            ),
            initial_capital=initial_capital,
            lot_size=int(backtest_options.get("lot_size", 100)),
            max_volume_fraction=float(
                backtest_options.get("max_volume_fraction", 0.01)
            ),
            price_multiplier=resolve_price_multiplier(config),
        )
        if explicit_round_trip_cost is None:
            cost_components = {
                "source": "commission_slippage_sell_tax",
                "entry_total": backtest_metrics["entry_cost_bps"],
                "exit_total": backtest_metrics["exit_cost_bps"],
                "commission_per_side": commission_bps,
                "slippage_per_side": slippage_bps,
                "sell_tax": sell_tax_bps,
            }
        else:
            cost_components = {
                "source": "round_trip_cost_bps_override",
                "entry_total": backtest_metrics["entry_cost_bps"],
                "exit_total": backtest_metrics["exit_cost_bps"],
            }
        metrics["backtest"] = {
            "available": True,
            "signal_threshold": backtest_signal_threshold,
            "target_return_definition": ("next_return[t] = close[t+1] / open[t+1] - 1"),
            "execution_rule": (
                "Tín hiệu sau close[t], mua open[t+1], bán close[t+1]; "
                "forward return gắn tại dòng signal nên execution_lag=0"
            ),
            "liquidity_capacity_definition": (
                "ADV20 tính đến close[t], đã biết khi tạo tín hiệu; không dùng "
                "volume cả ngày t+1"
            ),
            "cost_components_bps": cost_components,
            **backtest_metrics,
        }
        scored_test.attrs["backtest_details"] = backtest_details
    else:
        metrics["backtest"] = {
            "available": False,
            "reason": "Không có next_return OOS để backtest.",
        }

    latest_probabilities = {
        "xgboost": latest_xgboost_probability,
        "logistic_regression": latest_logistic_probability,
        "as_of": _date_text(latest_features.index[0]),
    }
    return metrics, scored_test, latest_probabilities, final_booster
