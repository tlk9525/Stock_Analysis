from __future__ import annotations

from datetime import date

import pandas as pd

from src.utils import safe_float


def _metric(metrics: dict, model: str, name: str) -> float | None:
    return safe_float(metrics.get(model, {}).get(name))


def build_signal_decision(
    metrics: dict,
    latest_probabilities: dict,
    technical: dict,
    risk_plan: dict,
    latest_date: str,
    config: dict,
) -> dict:
    """Kiểm duyệt output trước khi trình bày như một tín hiệu có thể hành động.

    Project chỉ giữ vị thế mua. Tín hiệu chỉ ACTIONABLE khi mô hình OOS, xác
    suất, bối cảnh kỹ thuật, reward/risk, độ mới dữ liệu và backtest đều đạt.
    """

    options = config.get("signal_guard", {})
    min_auc = float(options.get("min_roc_auc", 0.54))
    min_balanced_accuracy = float(options.get("min_balanced_accuracy", 0.52))
    min_probability = float(options.get("min_probability_up", 0.55))
    min_technical_score = int(options.get("min_technical_score", 2))
    max_data_age_days = int(options.get("max_data_age_days", 5))
    require_model_outperform_baseline = bool(
        options.get("require_model_outperform_baseline", True)
    )
    min_auc_improvement = float(
        options.get("min_auc_improvement_over_logistic", 0.0)
    )
    require_profitable_backtest = bool(
        options.get("require_profitable_backtest", True)
    )
    min_backtest_observations = int(options.get("min_backtest_observations", 126))
    min_completed_round_trips = int(options.get("min_completed_round_trips", 5))
    min_backtest_total_return = float(
        options.get("min_backtest_total_return", 0.0)
    )
    min_backtest_sharpe = float(options.get("min_backtest_sharpe", 0.0))
    min_reward_risk = float(config.get("min_reward_risk", 1.5))

    auc = _metric(metrics, "xgboost", "roc_auc")
    balanced_accuracy = _metric(metrics, "xgboost", "balanced_accuracy")
    logistic_auc = _metric(metrics, "logistic_baseline", "roc_auc")
    probability = safe_float(latest_probabilities.get("xgboost"))
    reward_risk = safe_float(risk_plan.get("reward_risk"))
    technical_score = int(technical.get("score", 0))
    backtest = metrics.get("backtest", {}) or {}
    backtest_available = bool(backtest.get("available", False))
    backtest_observations = int(backtest.get("observations") or 0)
    completed_round_trips = int(backtest.get("completed_round_trips") or 0)
    backtest_total_return = safe_float(
        backtest.get("net_total_return", backtest.get("total_return"))
    )
    backtest_sharpe = safe_float(
        backtest.get("sharpe_ratio", backtest.get("sharpe"))
    )

    observation_date = pd.Timestamp(latest_date).date()
    age_days = max((date.today() - observation_date).days, 0)
    checks = {
        "model_auc": auc is not None and auc >= min_auc,
        "model_balanced_accuracy": (
            balanced_accuracy is not None
            and balanced_accuracy >= min_balanced_accuracy
        ),
        "model_beats_logistic": (not require_model_outperform_baseline)
        or (
            auc is not None
            and logistic_auc is not None
            and auc > logistic_auc + min_auc_improvement
        ),
        "probability_edge": probability is not None and probability >= min_probability,
        "technical_context": technical_score >= min_technical_score,
        "reward_risk": reward_risk is not None and reward_risk >= min_reward_risk,
        "fresh_data": age_days <= max_data_age_days,
        "position_available": risk_plan.get("position_shares") is not None,
        "backtest_available": (not require_profitable_backtest) or backtest_available,
        "backtest_sample": (not require_profitable_backtest)
        or (
            backtest_observations >= min_backtest_observations
            and completed_round_trips >= min_completed_round_trips
        ),
        "backtest_net_edge": (not require_profitable_backtest)
        or (
            backtest_total_return is not None
            and backtest_total_return > min_backtest_total_return
            and backtest_sharpe is not None
            and backtest_sharpe > min_backtest_sharpe
        ),
    }

    failures = [name for name, passed in checks.items() if not passed]
    model_is_credible = all(
        checks[name]
        for name in (
            "model_auc",
            "model_balanced_accuracy",
            "model_beats_logistic",
        )
    )
    backtest_is_credible = all(
        checks[name]
        for name in ("backtest_available", "backtest_sample", "backtest_net_edge")
    )
    if not failures:
        status = "ACTIONABLE"
    elif model_is_credible and backtest_is_credible:
        status = "WATCH"
    else:
        status = "NO_EDGE"

    reasons = {
        "model_auc": f"AUC {auc:.3f} < {min_auc:.3f}" if auc is not None else "Không có AUC",
        "model_balanced_accuracy": (
            f"Balanced accuracy {balanced_accuracy:.3f} < {min_balanced_accuracy:.3f}"
            if balanced_accuracy is not None
            else "Không có balanced accuracy"
        ),
        "model_beats_logistic": (
            "XGBoost chưa vượt logistic baseline: "
            f"AUC XGBoost={auc if auc is not None else 'N/A'}, "
            f"AUC logistic={logistic_auc if logistic_auc is not None else 'N/A'}"
        ),
        "probability_edge": (
            f"Probability {probability:.1%} < {min_probability:.1%}"
            if probability is not None
            else "Không có xác suất"
        ),
        "technical_context": f"Technical score {technical_score} < {min_technical_score}",
        "reward_risk": (
            f"Reward/risk {reward_risk:.2f} < {min_reward_risk:.2f}"
            if reward_risk is not None
            else "Không có target vượt cổng reward/risk"
        ),
        "fresh_data": f"Dữ liệu mới nhất đã cách {age_days} ngày lịch",
        "position_available": "Không còn vị thế theo lô hợp lệ sau giới hạn rủi ro và thanh khoản",
        "backtest_available": "Không có backtest OOS sau chi phí",
        "backtest_sample": (
            f"Mẫu backtest {backtest_observations} dòng/{completed_round_trips} giao dịch; "
            f"cần >= {min_backtest_observations}/{min_completed_round_trips}"
        ),
        "backtest_net_edge": (
            "Lợi thế OOS ròng không đạt: "
            f"return={backtest_total_return if backtest_total_return is not None else 'N/A'}, "
            f"Sharpe={backtest_sharpe if backtest_sharpe is not None else 'N/A'}"
        ),
    }

    return {
        "status": status,
        "direction": "LONG" if status == "ACTIONABLE" else "NONE",
        "checks": checks,
        "failed_checks": failures,
        "reasons": [reasons[name] for name in failures],
        "latest_data_age_days": age_days,
        "allowed_position_shares": (
            risk_plan.get("position_shares") if status == "ACTIONABLE" else None
        ),
        "thresholds": {
            "min_roc_auc": min_auc,
            "min_balanced_accuracy": min_balanced_accuracy,
            "min_probability_up": min_probability,
            "min_technical_score": min_technical_score,
            "min_reward_risk": min_reward_risk,
            "max_data_age_days": max_data_age_days,
            "require_model_outperform_baseline": require_model_outperform_baseline,
            "min_auc_improvement_over_logistic": min_auc_improvement,
            "require_profitable_backtest": require_profitable_backtest,
            "min_backtest_observations": min_backtest_observations,
            "min_completed_round_trips": min_completed_round_trips,
            "min_backtest_total_return": min_backtest_total_return,
            "min_backtest_sharpe": min_backtest_sharpe,
        },
    }


def enforce_signal_decision(risk_plan: dict, decision: dict) -> dict:
    """Ẩn position sizing khi tín hiệu chưa vượt toàn bộ publish guard."""

    guarded = dict(risk_plan)
    guarded["signal_status"] = decision["status"]
    if decision["status"] != "ACTIONABLE":
        guarded["position_shares"] = None
        guarded["position_value_vnd"] = None
        guarded["notes"] = list(guarded.get("notes", [])) + [
            f"Signal {decision['status']}: ẩn vị thế vì chưa qua publish guard."
        ]
    return guarded
