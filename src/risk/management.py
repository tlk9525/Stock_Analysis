from __future__ import annotations

import math

import pandas as pd

from src.utils import safe_float


def build_risk_plan(levels: dict, forecast: pd.DataFrame, config: dict) -> dict:
    latest = levels["latest_close"]
    atr = levels.get("atr14")
    risk_pct = float(config.get("risk_per_trade_pct", 0.01))
    atr_multiplier = float(config.get("atr_stop_multiplier", 1.5))
    capital = float(config.get("risk_capital_vnd", 100_000_000))

    stop_candidates = []
    if atr is not None and atr > 0:
        stop_candidates.append(latest - atr_multiplier * atr)
    if levels.get("support20") is not None:
        stop_candidates.append(levels["support20"] * 0.99)
    if levels.get("sma60") is not None:
        stop_candidates.append(levels["sma60"] * 0.99)
    valid_stops = [value for value in stop_candidates if 0 < value < latest]
    stop_loss = max(valid_stops) if valid_stops else None

    forecast_end = forecast.iloc[-1]
    target_candidates = [
        levels.get("resistance20"),
        safe_float(forecast_end.get("p50")),
        safe_float(forecast_end.get("p90")),
    ]
    valid_targets = [value for value in target_candidates if value and value > latest]
    target_1 = min(valid_targets) if valid_targets else levels.get("resistance20")
    target_2 = max(valid_targets) if valid_targets else safe_float(forecast_end.get("p90"))

    risk_per_share = latest - stop_loss if stop_loss is not None else None
    reward_per_share = target_1 - latest if target_1 is not None else None
    reward_risk = (
        reward_per_share / risk_per_share
        if risk_per_share and reward_per_share and risk_per_share > 0
        else None
    )
    risk_budget = capital * risk_pct
    position_shares = (
        math.floor(risk_budget / (risk_per_share * 1000))
        if risk_per_share and risk_per_share > 0
        else None
    )
    position_value = (
        position_shares * latest * 1000
        if position_shares is not None
        else None
    )

    notes = [
        f"Rui ro moi lenh mac dinh {risk_pct:.1%} tren von {capital:,.0f} VND.",
        "Khong mua duoi neu gia dang duoi stop tham chieu.",
    ]
    minimum_reward_risk = float(config.get("min_reward_risk", 1.5))
    if reward_risk is not None and reward_risk < minimum_reward_risk:
        notes.append("Reward/risk thap, nen doi diem vao tot hon.")
    elif reward_risk is not None:
        notes.append("Reward/risk dat nguong toi thieu theo cau hinh.")

    return {
        "risk_per_trade_pct": risk_pct,
        "capital_reference_vnd": capital,
        "atr_stop_multiplier": atr_multiplier,
        "stop_loss": safe_float(stop_loss),
        "target_1": safe_float(target_1),
        "target_2": safe_float(target_2),
        "risk_per_share": safe_float(risk_per_share),
        "reward_per_share": safe_float(reward_per_share),
        "reward_risk": safe_float(reward_risk),
        "risk_budget_vnd": safe_float(risk_budget),
        "position_shares": int(position_shares) if position_shares is not None else None,
        "position_value_vnd": safe_float(position_value),
        "notes": notes,
    }

