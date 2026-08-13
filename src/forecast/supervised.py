from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import pandas as pd

from src.features.technical import latest_model_features
from src.market_calendar import build_market_calendar, market_calendar_note, market_holidays
from src.models.xgboost import model_feature_columns


@dataclass(frozen=True)
class _HorizonResult:
    horizon: int
    lower_return: float
    median_return: float
    upper_return: float
    probability_positive: float
    metrics: dict
    model: object


def _options(config: dict) -> dict:
    raw = config.get("forecast_model", {}) or {}
    if not isinstance(raw, dict):
        raise ValueError("forecast_model trong config phải là object.")
    horizons = sorted({int(value) for value in raw.get("horizons", [5, 10, 20])})
    if not horizons or any(value < 2 for value in horizons):
        raise ValueError("forecast_model.horizons phải chứa các số nguyên >= 2.")
    quantiles = [float(value) for value in raw.get("quantiles", [0.10, 0.50, 0.90])]
    if quantiles != sorted(quantiles) or len(quantiles) != 3 or not math.isclose(quantiles[1], 0.5):
        raise ValueError("forecast_model.quantiles phải gồm 3 mức tăng dần và mức giữa là 0.5.")
    if quantiles[0] <= 0 or quantiles[-1] >= 1:
        raise ValueError("forecast_model.quantiles phải nằm trong khoảng (0, 1).")
    return {
        **raw,
        "horizons": horizons,
        "quantiles": quantiles,
        "validation_rows": int(raw.get("validation_rows", 126)),
        "frozen_holdout_rows": int(raw.get("frozen_holdout_rows", 252)),
        "minimum_train_rows": int(raw.get("minimum_train_rows", 756)),
        "conformal_coverage": float(raw.get("conformal_coverage", 0.80)),
        "minimum_frozen_rows": int(raw.get("minimum_frozen_rows", 126)),
    }


def _quantile(values: np.ndarray, probability: float) -> float:
    if not len(values):
        raise ValueError("Không có residual để conformal calibration.")
    level = min(1.0, math.ceil((len(values) + 1) * probability) / len(values))
    return float(np.quantile(values, level, method="higher"))


def _point_metrics(actual: np.ndarray, predicted: np.ndarray) -> dict:
    error = predicted - actual
    return {
        "rows": int(len(actual)),
        "mae": float(np.mean(np.abs(error))),
        "rmse": float(np.sqrt(np.mean(error**2))),
        "directional_accuracy": float(np.mean((predicted > 0) == (actual > 0))),
        "correlation": (
            float(np.corrcoef(actual, predicted)[0, 1])
            if len(actual) > 1 and np.std(actual) > 0 and np.std(predicted) > 0
            else None
        ),
    }


def _pinball(actual: np.ndarray, predicted: np.ndarray, alpha: float) -> float:
    error = actual - predicted
    return float(np.mean(np.maximum(alpha * error, (alpha - 1.0) * error)))


def _xgb_params(config: dict, quantiles: list[float]) -> tuple[dict, int, int]:
    options = config.get("xgboost", {}) or {}
    forecast = config.get("forecast_model", {}) or {}
    params = {
        "objective": "reg:quantileerror",
        "quantile_alpha": quantiles,
        "tree_method": "hist",
        "eta": float(forecast.get("learning_rate", options.get("learning_rate", 0.03))),
        "max_depth": int(forecast.get("max_depth", min(int(options.get("max_depth", 4)), 4))),
        "min_child_weight": float(options.get("min_child_weight", 3)),
        "subsample": float(options.get("subsample", 0.8)),
        "colsample_bytree": float(options.get("colsample_bytree", 0.8)),
        "lambda": float(options.get("reg_lambda", 1.0)),
        "alpha": float(options.get("reg_alpha", 0.05)),
        "seed": int(options.get("random_state", 42)),
        "nthread": int(options.get("n_jobs", 4)),
    }
    return (
        params,
        int(forecast.get("num_boost_round", options.get("num_boost_round", 400))),
        int(forecast.get("early_stopping_rounds", options.get("early_stopping_rounds", 40))),
    )


def _train_horizon(frame: pd.DataFrame, config: dict, horizon: int, options: dict) -> _HorizonResult:
    try:
        import xgboost as xgb
    except Exception as exc:
        raise RuntimeError("Không nạp được XGBoost cho supervised forecast.") from exc

    features = model_feature_columns(config)
    target = f"target_return_{horizon}d"
    required = [*features, target]
    missing = [column for column in required if column not in frame]
    if missing:
        raise ValueError(f"Thiếu dữ liệu forecast {horizon}D: {', '.join(missing)}")
    latest = latest_model_features(frame, features)
    labeled = frame.dropna(subset=required).copy()
    numeric = labeled[required].apply(pd.to_numeric, errors="coerce")
    finite = np.isfinite(numeric.to_numpy(dtype=float)).all(axis=1)
    labeled = labeled.loc[finite].copy()
    labeled[required] = numeric.loc[finite]

    frozen_rows = options["frozen_holdout_rows"]
    validation_rows = options["validation_rows"]
    train_end = len(labeled) - frozen_rows - horizon - validation_rows - horizon
    validation_start = train_end + horizon
    validation_end = validation_start + validation_rows
    frozen_start = validation_end + horizon
    if train_end < options["minimum_train_rows"] or len(labeled) - frozen_start < options["minimum_frozen_rows"]:
        raise ValueError(
            f"Không đủ dữ liệu cho forecast {horizon}D: train={train_end}, "
            f"frozen={len(labeled) - frozen_start}."
        )
    train = labeled.iloc[:train_end]
    validation = labeled.iloc[validation_start:validation_end]
    frozen = labeled.iloc[frozen_start:]
    quantiles = options["quantiles"]
    params, rounds, early_stopping = _xgb_params(config, quantiles)
    train_matrix = xgb.QuantileDMatrix(train[features], label=train[target], feature_names=features)
    validation_matrix = xgb.QuantileDMatrix(
        validation[features], label=validation[target], feature_names=features, ref=train_matrix
    )
    tuning = xgb.train(
        params,
        train_matrix,
        num_boost_round=rounds,
        evals=[(validation_matrix, "validation")],
        early_stopping_rounds=early_stopping,
        verbose_eval=False,
    )
    selected_rounds = max(1, int(getattr(tuning, "best_iteration", rounds - 1)) + 1)
    validation_prediction = np.asarray(tuning.predict(validation_matrix), dtype=float)
    if validation_prediction.ndim != 2 or validation_prediction.shape[1] != 3:
        raise RuntimeError("XGBoost quantile forecast không trả về đủ P10/P50/P90.")
    validation_actual = validation[target].to_numpy(dtype=float)
    interval_error = np.maximum.reduce(
        [validation_prediction[:, 0] - validation_actual,
         validation_actual - validation_prediction[:, 2],
         np.zeros(len(validation_actual))]
    )
    conformal_adjustment = _quantile(interval_error, options["conformal_coverage"])

    development = labeled.iloc[:validation_end]
    development_matrix = xgb.QuantileDMatrix(
        development[features], label=development[target], feature_names=features
    )
    model = xgb.train(params, development_matrix, num_boost_round=selected_rounds, verbose_eval=False)
    frozen_prediction = np.asarray(
        model.predict(xgb.DMatrix(frozen[features], feature_names=features)), dtype=float
    )
    frozen_actual = frozen[target].to_numpy(dtype=float)
    frozen_lower = frozen_prediction[:, 0] - conformal_adjustment
    frozen_upper = frozen_prediction[:, 2] + conformal_adjustment
    frozen_median = frozen_prediction[:, 1]
    point = _point_metrics(frozen_actual, frozen_median)
    zero = _point_metrics(frozen_actual, np.zeros(len(frozen_actual)))
    historical_mean_value = float(train[target].mean())
    historical_mean = _point_metrics(
        frozen_actual, np.full(len(frozen_actual), historical_mean_value)
    )
    best_baseline_mae = min(zero["mae"], historical_mean["mae"])
    coverage = float(np.mean((frozen_actual >= frozen_lower) & (frozen_actual <= frozen_upper)))

    final_matrix = xgb.QuantileDMatrix(labeled[features], label=labeled[target], feature_names=features)
    final_model = xgb.train(params, final_matrix, num_boost_round=selected_rounds, verbose_eval=False)
    latest_prediction = np.asarray(
        final_model.predict(xgb.DMatrix(latest, feature_names=features)), dtype=float
    ).reshape(-1)
    lower = float(latest_prediction[0] - conformal_adjustment)
    median = float(latest_prediction[1])
    upper = float(latest_prediction[2] + conformal_adjustment)
    lower, median, upper = sorted((lower, median, upper))
    residuals = frozen_actual - frozen_median
    probability_positive = float(np.mean(median + residuals > 0))
    metrics = {
        "horizon_sessions": horizon,
        "target": target,
        "train_rows": int(len(train)),
        "validation_rows": int(len(validation)),
        "purge_rows": horizon,
        "frozen_holdout_rows": int(len(frozen)),
        "selected_num_boost_round": selected_rounds,
        "quantiles": quantiles,
        "conformal_coverage_target": options["conformal_coverage"],
        "conformal_adjustment_return": conformal_adjustment,
        "frozen_interval_coverage": coverage,
        "frozen_average_interval_width": float(np.mean(frozen_upper - frozen_lower)),
        "frozen_point_metrics": point,
        "baselines": {"zero_return": zero, "historical_mean": historical_mean},
        "pinball_loss": {
            str(alpha): _pinball(frozen_actual, frozen_prediction[:, index], alpha)
            for index, alpha in enumerate(quantiles)
        },
        "beats_best_baseline_mae": point["mae"] < best_baseline_mae,
        "frozen_ranking_edge": (point["correlation"] or 0.0) > 0.0,
        "latest_return_quantiles": {"p10": lower, "p50": median, "p90": upper},
        "latest_probability_positive": probability_positive,
    }
    metrics["publish_ready"] = bool(
        metrics["beats_best_baseline_mae"]
        and metrics["frozen_ranking_edge"]
        and coverage >= max(0.0, options["conformal_coverage"] - 0.10)
    )
    return _HorizonResult(
        horizon=horizon,
        lower_return=max(lower, -0.95),
        median_return=max(median, -0.95),
        upper_return=max(upper, -0.95),
        probability_positive=probability_positive,
        metrics=metrics,
        model=final_model,
    )


def _interpolate_anchor(values: dict[int, float], sessions: int) -> np.ndarray:
    anchors = sorted(values)
    x = np.arange(1, sessions + 1, dtype=float)
    return np.interp(x, anchors, [values[key] for key in anchors])


def train_supervised_forecast(
    frame: pd.DataFrame,
    config: dict,
) -> tuple[pd.DataFrame, dict, dict[int, object]]:
    """Direct multi-horizon quantile forecast with purging and conformal bands.

    Targets follow the same executable convention as the swing model: the
    signal is known after close[t], entry is open[t+1], and the horizon exit is
    close[t+h].  Frozen holdout rows are never used for round selection or
    conformal calibration.
    """

    options = _options(config)
    results = [_train_horizon(frame, config, horizon, options) for horizon in options["horizons"]]
    latest_close = float(pd.to_numeric(frame["close"], errors="coerce").iloc[-1])
    sessions = int(config.get("forecast_sessions", max(options["horizons"])))
    if sessions < 1:
        raise ValueError("forecast_sessions phải dương.")
    anchors = {
        "p10": {0: latest_close},
        "p50": {0: latest_close},
        "p90": {0: latest_close},
        "probability": {0: 0.5},
    }
    for result in results:
        anchors["p10"][result.horizon] = latest_close * (1.0 + result.lower_return)
        anchors["p50"][result.horizon] = latest_close * (1.0 + result.median_return)
        anchors["p90"][result.horizon] = latest_close * (1.0 + result.upper_return)
        anchors["probability"][result.horizon] = result.probability_positive
    market_calendar = build_market_calendar(config)
    future_dates = pd.date_range(
        frame.index[-1] + market_calendar,
        periods=sessions,
        freq=market_calendar,
    )
    p10 = _interpolate_anchor(anchors["p10"], sessions)
    p50 = _interpolate_anchor(anchors["p50"], sessions)
    p90 = _interpolate_anchor(anchors["p90"], sessions)
    ordered = np.sort(np.column_stack([p10, p50, p90]), axis=1)
    forecast = pd.DataFrame(
        {
            "p10": ordered[:, 0],
            "p25": (ordered[:, 0] + ordered[:, 1]) / 2.0,
            "p50": ordered[:, 1],
            "p75": (ordered[:, 1] + ordered[:, 2]) / 2.0,
            "p90": ordered[:, 2],
            "prob_end_above_latest": np.clip(
                _interpolate_anchor(anchors["probability"], sessions), 0.0, 1.0
            ),
            "latest_close": latest_close,
            "is_model_anchor": [session in options["horizons"] for session in range(1, sessions + 1)],
        },
        index=future_dates,
    )
    metrics = {
        "available": True,
        "method": "xgboost_direct_quantile_conformal",
        "execution_contract": "signal_close_t_entry_open_t_plus_1_exit_close_t_plus_h",
        "horizons": options["horizons"],
        "interpolation": "linear_between_direct_model_horizons",
        "all_horizons_publish_ready": all(result.metrics["publish_ready"] for result in results),
        "by_horizon": {str(result.horizon): result.metrics for result in results},
    }
    forecast.attrs["method"] = metrics["method"]
    forecast.attrs["forecast_model_metrics"] = metrics
    forecast.attrs["market_calendar_note"] = market_calendar_note(config)
    forecast.attrs["market_holidays"] = market_holidays(config)
    return forecast, metrics, {result.horizon: result.model for result in results}
