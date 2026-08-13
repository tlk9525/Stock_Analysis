from __future__ import annotations

import copy
import math

import numpy as np
import pandas as pd

from src.backtest import run_stateful_long_only_backtest
from src.features.technical import latest_model_features
from src.models.xgboost import build_walk_forward_splits, model_feature_columns
from src.utils import resolve_price_multiplier


def _regression_params(config: dict) -> tuple[dict, int, int]:
    options = config.get("xgboost", {}) or {}
    params = {
        "objective": "reg:squarederror",
        "eval_metric": "rmse",
        "tree_method": "hist",
        "eta": float(options.get("learning_rate", 0.03)),
        "max_depth": int(options.get("max_depth", 4)),
        "min_child_weight": float(options.get("min_child_weight", 3)),
        "subsample": float(options.get("subsample", 0.8)),
        "colsample_bytree": float(options.get("colsample_bytree", 0.8)),
        "lambda": float(options.get("reg_lambda", 1.0)),
        "alpha": float(options.get("reg_alpha", 0.05)),
        "seed": int(options.get("random_state", 42)),
        "nthread": int(options.get("n_jobs", 4)),
    }
    rounds = int(options.get("num_boost_round", 400))
    early_stopping = int(options.get("early_stopping_rounds", 40))
    if rounds < 1 or early_stopping < 1:
        raise ValueError("XGBoost rounds và early stopping phải dương.")
    return params, rounds, early_stopping


def _best_rounds(model, fallback: int) -> int:
    return max(1, int(getattr(model, "best_iteration", fallback - 1)) + 1)


def _regression_metrics(actual: pd.Series, predicted: np.ndarray) -> dict:
    y = pd.to_numeric(actual, errors="coerce").to_numpy(dtype=float)
    values = np.asarray(predicted, dtype=float)
    if len(y) != len(values) or not len(y) or not np.isfinite(y).all() or not np.isfinite(values).all():
        raise ValueError("Regression metrics cần nhãn và dự báo hữu hạn cùng độ dài.")
    errors = values - y
    return {
        "rows": int(len(y)),
        "mae": float(np.mean(np.abs(errors))),
        "rmse": float(math.sqrt(np.mean(errors**2))),
        "mean_actual_excess_return": float(np.mean(y)),
        "mean_predicted_excess_return": float(np.mean(values)),
        "directional_accuracy": float(np.mean((values > 0) == (y > 0))),
        "correlation": (
            float(np.corrcoef(y, values)[0, 1])
            if len(y) > 1 and np.std(y) > 0 and np.std(values) > 0
            else None
        ),
    }


def _finite_sample_quantile(values: np.ndarray, confidence: float) -> float:
    if not 0.5 < confidence < 1.0:
        raise ValueError("swing_strategy.lower_confidence_level phải nằm trong (0.5, 1).")
    if not len(values):
        raise ValueError("Không có OOS residual để hiệu chỉnh uncertainty.")
    level = min(1.0, math.ceil((len(values) + 1) * confidence) / len(values))
    return float(np.quantile(values, level, method="higher"))


def _baseline_metrics(actual: pd.Series, historical_mean: float) -> dict:
    rows = len(actual)
    return {
        "zero_excess_return": _regression_metrics(actual, np.zeros(rows)),
        "historical_mean": _regression_metrics(
            actual, np.full(rows, float(historical_mean))
        ),
    }


def _strategy_options(config: dict) -> dict:
    options = config.get("swing_strategy", {}) or {}
    if not isinstance(options, dict):
        raise ValueError("swing_strategy trong config phải là object.")
    return options


def _backtest_options(config: dict, strategy: dict) -> dict:
    options = config.get("backtest", {}) or {}
    commission = float(options.get("commission_bps_per_side", 15.0))
    slippage = float(options.get("slippage_bps_per_side", 5.0))
    return {
        "entry_cost_bps": commission + slippage,
        "exit_cost_bps": commission + slippage + float(options.get("sell_tax_bps", 10.0)),
        "periods_per_year": int(options.get("periods_per_year", 252)),
        "initial_capital": float(config.get("risk_capital_vnd", 100_000_000)),
        "lot_size": int(options.get("lot_size", 100)),
        "max_volume_fraction": float(options.get("max_volume_fraction", 0.01)),
        "price_multiplier": resolve_price_multiplier(config),
        "minimum_holding_sessions": int(strategy.get("minimum_holding_sessions", 2)),
    }


def _swing_backtest(
    scored: pd.DataFrame,
    config: dict,
    strategy: dict,
    *,
    entry_margin: float = 0.0,
    entry_margin_column: str | None = None,
    cost_multiplier: float = 1.0,
) -> tuple[dict, pd.DataFrame]:
    options = _backtest_options(config, strategy)
    horizon = int(strategy.get("horizon_sessions", 5))
    fixed_holding_sessions = horizon - 1
    if fixed_holding_sessions < options["minimum_holding_sessions"]:
        raise ValueError(
            "horizon_sessions phải đủ dài để vừa khớp target vừa tôn trọng minimum_holding_sessions."
        )
    execution = scored.copy()
    if "volume_sma_20" in execution:
        execution["swing_liquidity_estimate"] = pd.to_numeric(
            execution["volume_sma_20"], errors="coerce"
        )
    else:
        execution["swing_liquidity_estimate"] = pd.to_numeric(
            execution["volume"], errors="coerce"
        ).rolling(20, min_periods=1).mean()
    return run_stateful_long_only_backtest(
        execution,
        prediction_column="predicted_excess_return_5d",
        entry_price_column="swing_execution_open",
        mark_price_column="swing_execution_close",
        volume_column="swing_liquidity_estimate",
        entry_margin=entry_margin,
        entry_margin_column=entry_margin_column,
        minimum_holding_sessions=options["minimum_holding_sessions"],
        fixed_holding_sessions=fixed_holding_sessions,
        entry_cost_bps=options["entry_cost_bps"] * cost_multiplier,
        exit_cost_bps=options["exit_cost_bps"] * cost_multiplier,
        periods_per_year=options["periods_per_year"],
        initial_capital=options["initial_capital"],
        lot_size=options["lot_size"],
        max_volume_fraction=options["max_volume_fraction"],
        price_multiplier=options["price_multiplier"],
        force_close_at_end=True,
    )


def _select_margin(
    validation: pd.DataFrame,
    predicted: np.ndarray,
    config: dict,
    strategy: dict,
) -> tuple[float, bool]:
    candidates = strategy.get("entry_margin_candidates", [0.0, 0.0025, 0.005])
    candidates = sorted({float(value) for value in candidates})
    minimum_trades = int(strategy.get("min_completed_round_trips", 10))
    scored = validation.copy()
    scored["predicted_excess_return_5d"] = predicted
    viable: list[tuple[float, float, float]] = []
    for margin in candidates:
        summary, _ = _swing_backtest(scored, config, strategy, entry_margin=margin)
        net = float(summary.get("net_total_return") or -np.inf)
        sharpe = float(summary.get("sharpe_ratio") or -np.inf)
        if summary["completed_round_trips"] >= minimum_trades:
            viable.append((net, sharpe, margin))
    if not viable:
        # Keep a no-entry fallback for auditability, but record that no rule
        # was selected.  It must never be interpreted as a validated margin.
        return float(max(candidates)), False
    return float(sorted(viable, key=lambda item: (item[0], item[1], -item[2]), reverse=True)[0][2]), True


def train_swing_strategy(
    frame: pd.DataFrame,
    config: dict,
) -> tuple[dict, pd.DataFrame, dict, object]:
    """Train 5D excess-return regression with inner margin tuning and holdout.

    The frozen holdout is never used to select boosting rounds or entry margin.
    The returned final booster can use all historical labels only *after* that
    holdout evaluation has been captured.
    """

    try:
        import xgboost as xgb
    except Exception as exc:
        raise RuntimeError("Không nạp được XGBoost cho swing strategy.") from exc

    strategy = _strategy_options(config)
    horizon = int(strategy.get("horizon_sessions", 5))
    if horizon < 2:
        raise ValueError("swing_strategy.horizon_sessions phải >= 2.")
    target = f"target_excess_return_{horizon}d"
    feature_columns = model_feature_columns(config)
    required = [
        *feature_columns,
        target,
        "swing_execution_open",
        "swing_execution_close",
        "volume",
    ]
    missing = [column for column in required if column not in frame]
    if missing:
        raise ValueError("Thiếu dữ liệu swing strategy: " + ", ".join(missing))
    latest_features = latest_model_features(frame, feature_columns)
    labeled = frame.dropna(subset=required).copy()
    numeric = labeled[feature_columns].apply(pd.to_numeric, errors="coerce")
    finite = np.isfinite(numeric.to_numpy(dtype=float)).all(axis=1)
    labeled = labeled.loc[finite].copy()
    labeled[feature_columns] = numeric.loc[finite]
    if labeled.empty:
        raise ValueError("Không có dữ liệu swing labeled hợp lệ.")

    frozen_rows = int(strategy.get("frozen_holdout_rows", 126))
    if frozen_rows < 20 or len(labeled) <= frozen_rows + horizon + 60:
        raise ValueError("Không đủ dữ liệu cho swing frozen holdout.")
    development = labeled.iloc[: -(frozen_rows + horizon)].copy()
    frozen_holdout = labeled.iloc[-frozen_rows:].copy()
    split_config = copy.deepcopy(config)
    validation = split_config.setdefault("validation", {})
    validation["gap_rows"] = max(int(validation.get("gap_rows", 1)), horizon)
    splits, walk_settings = build_walk_forward_splits(len(development), split_config)
    minimum_test_rows = int(
        strategy.get("minimum_test_rows", walk_settings["test_rows"])
    )
    if minimum_test_rows < 1 or minimum_test_rows > walk_settings["test_rows"]:
        raise ValueError(
            "swing_strategy.minimum_test_rows phải nằm trong [1, validation.test_rows]."
        )
    splits = [
        split
        for split in splits
        if split["test_end"] - split["test_start"] >= minimum_test_rows
    ]
    if not splits:
        raise ValueError("Không còn walk-forward fold đủ số dòng test tối thiểu.")
    params, rounds, early_stopping = _regression_params(config)

    oos_parts: list[pd.DataFrame] = []
    fold_records: list[dict] = []
    selected_rounds: list[int] = []
    selected_margins: list[float] = []
    valid_margin_selections: list[bool] = []
    for split in splits:
        train = development.iloc[split["train_start"] : split["train_end"]]
        validation_frame = development.iloc[
            split["validation_start"] : split["validation_end"]
        ]
        test = development.iloc[split["test_start"] : split["test_end"]]
        train_matrix = xgb.DMatrix(train[feature_columns], label=train[target], feature_names=feature_columns)
        validation_matrix = xgb.DMatrix(validation_frame[feature_columns], label=validation_frame[target], feature_names=feature_columns)
        history: dict = {}
        tuning = xgb.train(
            params=params,
            dtrain=train_matrix,
            num_boost_round=rounds,
            evals=[(train_matrix, "train"), (validation_matrix, "validation")],
            evals_result=history,
            early_stopping_rounds=early_stopping,
            verbose_eval=False,
        )
        best_rounds = _best_rounds(tuning, rounds)
        selected_rounds.append(best_rounds)
        validation_prediction = tuning.predict(validation_matrix)
        selected_margin, margin_selected = _select_margin(
            validation_frame, validation_prediction, config, strategy
        )
        selected_margins.append(selected_margin)
        valid_margin_selections.append(margin_selected)
        pool = pd.concat([train, validation_frame])
        model = xgb.train(
            params=params,
            dtrain=xgb.DMatrix(pool[feature_columns], label=pool[target], feature_names=feature_columns),
            num_boost_round=best_rounds,
            verbose_eval=False,
        )
        scored = test.copy()
        scored["predicted_excess_return_5d"] = model.predict(
            xgb.DMatrix(test[feature_columns], feature_names=feature_columns)
        )
        scored["entry_margin"] = selected_margin
        scored["fold"] = int(split["fold"])
        oos_parts.append(scored)
        fold_records.append(
            {
                "fold": int(split["fold"]),
                "train_rows": int(len(train)),
                "validation_rows": int(len(validation_frame)),
                "test_rows": int(len(test)),
                "selected_num_boost_round": int(best_rounds),
                "selected_entry_margin": float(selected_margin),
                "entry_margin_selected_from_validation": bool(margin_selected),
                "test_metrics": _regression_metrics(test[target], scored["predicted_excess_return_5d"].to_numpy()),
            }
        )

    development_oos = pd.concat(oos_parts).sort_index()
    dev_metrics = _regression_metrics(
        development_oos[target], development_oos["predicted_excess_return_5d"].to_numpy()
    )
    development_baselines = _baseline_metrics(
        development_oos[target], float(development[target].mean())
    )
    dev_backtest, dev_details = _swing_backtest(
        development_oos,
        config,
        strategy,
        entry_margin_column="entry_margin",
    )
    dev_backtest["entry_margin"] = "fold-specific"
    dev_backtest["validated_entry_margin_folds"] = int(sum(valid_margin_selections))
    dev_backtest["total_entry_margin_folds"] = int(len(valid_margin_selections))
    chosen_rounds = max(1, int(round(float(np.median(selected_rounds)))))
    chosen_margin = float(np.median(selected_margins))
    margin_selection_valid = bool(valid_margin_selections) and all(valid_margin_selections)
    development_model = xgb.train(
        params=params,
        dtrain=xgb.DMatrix(development[feature_columns], label=development[target], feature_names=feature_columns),
        num_boost_round=chosen_rounds,
        verbose_eval=False,
    )
    frozen_scored = frozen_holdout.copy()
    frozen_scored["predicted_excess_return_5d"] = development_model.predict(
        xgb.DMatrix(frozen_holdout[feature_columns], feature_names=feature_columns)
    )
    frozen_scored["entry_margin"] = chosen_margin
    frozen_regression = _regression_metrics(
        frozen_scored[target], frozen_scored["predicted_excess_return_5d"].to_numpy()
    )
    frozen_baselines = _baseline_metrics(
        frozen_scored[target], float(development[target].mean())
    )
    confidence = float(strategy.get("lower_confidence_level", 0.80))
    residuals = np.abs(
        development_oos[target].to_numpy(dtype=float)
        - development_oos["predicted_excess_return_5d"].to_numpy(dtype=float)
    )
    conformal_radius = _finite_sample_quantile(residuals, confidence)
    frozen_lower = (
        frozen_scored["predicted_excess_return_5d"].to_numpy(dtype=float)
        - conformal_radius
    )
    frozen_actual = frozen_scored[target].to_numpy(dtype=float)
    frozen_lower_coverage = float(np.mean(frozen_actual >= frozen_lower))
    frozen_backtest, frozen_details = _swing_backtest(
        frozen_scored, config, strategy, entry_margin=chosen_margin
    )
    stress = []
    for multiplier in strategy.get("cost_stress_multipliers", [1.0, 1.5, 2.0]):
        value = float(multiplier)
        summary, _ = _swing_backtest(
            frozen_scored,
            config,
            strategy,
            entry_margin=chosen_margin,
            cost_multiplier=value,
        )
        stress.append(
            {
                "cost_multiplier": value,
                "net_total_return": summary["net_total_return"],
                "sharpe_ratio": summary["sharpe_ratio"],
                "completed_round_trips": summary["completed_round_trips"],
                "max_drawdown": summary["max_drawdown"],
            }
        )
    stress_15 = next((item for item in stress if math.isclose(item["cost_multiplier"], 1.5)), None)
    minimum_trades = int(strategy.get("min_completed_round_trips", 10))
    gate = {
        "frozen_holdout": True,
        "margin_selected_in_validation": margin_selection_valid,
        "development_sufficient_trades": dev_backtest["completed_round_trips"] >= minimum_trades,
        "sufficient_trades": frozen_backtest["completed_round_trips"] >= minimum_trades,
        "development_ranking_edge": (dev_metrics.get("correlation") or 0.0) > 0.0,
        "frozen_ranking_edge": (frozen_regression.get("correlation") or 0.0) > 0.0,
        "net_edge": frozen_backtest["net_total_return"] > 0 and (frozen_backtest["sharpe_ratio"] or 0) > 0,
        "cost_stress_1_5x": bool(stress_15) and stress_15["net_total_return"] > 0 and (stress_15["sharpe_ratio"] or 0) > 0,
        "settlement_aware": frozen_backtest["minimum_holding_sessions"] >= 2,
        "uncertainty_calibrated": len(development_oos)
        >= int(strategy.get("minimum_calibration_rows", 126)),
        "beats_zero_baseline_mae": frozen_regression["mae"]
        < frozen_baselines["zero_excess_return"]["mae"],
    }
    gate["passed"] = all(gate.values())

    final_model = xgb.train(
        params=params,
        dtrain=xgb.DMatrix(labeled[feature_columns], label=labeled[target], feature_names=feature_columns),
        num_boost_round=chosen_rounds,
        verbose_eval=False,
    )
    latest_prediction = float(
        final_model.predict(xgb.DMatrix(latest_features, feature_names=feature_columns))[0]
    )
    latest_lower_bound = latest_prediction - conformal_radius
    importance = final_model.get_score(importance_type="gain")
    metrics = {
        "available": True,
        "target": target,
        "target_definition": frame.attrs.get("swing_target_definition"),
        "feature_columns": feature_columns,
        "horizon_sessions": horizon,
        "min_completed_round_trips": minimum_trades,
        "validation": {
            "scheme": "nested_expanding_walk_forward_plus_frozen_holdout",
            "development_rows": int(len(development)),
            "purged_rows_before_holdout": horizon,
            "frozen_holdout_rows": int(len(frozen_holdout)),
            "gap_rows": int(walk_settings["gap_rows"]),
            "minimum_test_rows": minimum_test_rows,
            "folds": fold_records,
        },
        "development_oos": {
            "regression": dev_metrics,
            "baselines": development_baselines,
            "backtest": dev_backtest,
        },
        "frozen_holdout": {
            "regression": frozen_regression,
            "baselines": frozen_baselines,
            "lower_bound_coverage": frozen_lower_coverage,
            "backtest": frozen_backtest,
        },
        "cost_stress": stress,
        "selected_num_boost_round": chosen_rounds,
        "selected_entry_margin": chosen_margin,
        "latest_expected_excess_return": latest_prediction,
        "latest_expected_excess_return_lower_bound": latest_lower_bound,
        "uncertainty": {
            "method": "split_conformal_absolute_oos_residual",
            "confidence_level": confidence,
            "calibration_rows": int(len(development_oos)),
            "radius": conformal_radius,
            "frozen_lower_bound_coverage": frozen_lower_coverage,
        },
        "publish_gate": gate,
        "feature_importance_gain": dict(
            sorted(
                (
                    (feature, float(importance.get(feature, 0.0)))
                    for feature in feature_columns
                ),
                key=lambda item: item[1],
                reverse=True,
            )
        ),
    }
    development_oos.attrs["backtest_details"] = dev_details
    development_oos.attrs["backtest_trades"] = dev_details.attrs.get("trades")
    frozen_scored.attrs["backtest_details"] = frozen_details
    frozen_scored.attrs["backtest_trades"] = frozen_details.attrs.get("trades")
    latest = {
        "expected_excess_return_5d": latest_prediction,
        "expected_excess_return_5d_lower_bound": latest_lower_bound,
        "selected_entry_margin": chosen_margin,
        "as_of": str(latest_features.index[0].date()),
    }
    return metrics, development_oos, {"latest": latest, "frozen_scored": frozen_scored}, final_model
