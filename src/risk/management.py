from __future__ import annotations

import math

import pandas as pd

from src.utils import resolve_price_multiplier, safe_float


def build_risk_plan(levels: dict, forecast: pd.DataFrame, config: dict) -> dict:
    latest = levels["latest_close"]
    atr = levels.get("atr14")
    risk_pct = float(config.get("risk_per_trade_pct", 0.01))
    atr_multiplier = float(config.get("atr_stop_multiplier", 1.5))
    capital = float(config.get("risk_capital_vnd", 100_000_000))
    backtest_options = config.get("backtest", {})
    lot_size = max(int(backtest_options.get("lot_size", 100)), 1)
    max_volume_fraction = float(backtest_options.get("max_volume_fraction", 0.01))
    commission_bps = float(backtest_options.get("commission_bps_per_side", 0.0))
    sell_tax_bps = float(backtest_options.get("sell_tax_bps", 0.0))
    slippage_bps = float(backtest_options.get("slippage_bps_per_side", 0.0))
    buy_cost_rate = (commission_bps + slippage_bps) / 10_000
    sell_cost_rate = (commission_bps + slippage_bps + sell_tax_bps) / 10_000
    minimum_reward_risk = float(config.get("min_reward_risk", 1.5))
    price_multiplier = resolve_price_multiplier(config)

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

    effective_entry = latest * (1 + buy_cost_rate)
    effective_stop = (
        stop_loss * (1 - sell_cost_rate) if stop_loss is not None else None
    )
    risk_per_share = (
        effective_entry - effective_stop
        if effective_stop is not None
        else None
    )
    minimum_target = (
        (effective_entry + minimum_reward_risk * risk_per_share)
        / (1 - sell_cost_rate)
        if risk_per_share is not None
        and risk_per_share > 0
        and sell_cost_rate < 1
        else None
    )
    qualified_targets = [
        value
        for value in valid_targets
        if minimum_target is not None and value >= minimum_target
    ]
    target_1 = min(qualified_targets) if qualified_targets else None
    target_2 = max(valid_targets) if valid_targets else None
    effective_target = (
        target_1 * (1 - sell_cost_rate) if target_1 is not None else None
    )
    reward_per_share = (
        effective_target - effective_entry
        if effective_target is not None
        else None
    )
    reward_risk = (
        reward_per_share / risk_per_share
        if risk_per_share and reward_per_share and risk_per_share > 0
        else None
    )
    risk_budget = capital * risk_pct
    position_shares = None
    if risk_per_share and risk_per_share > 0 and reward_risk is not None:
        risk_cap = math.floor(risk_budget / (risk_per_share * price_multiplier))
        capital_cap = math.floor(capital / (latest * price_multiplier))
        liquidity = safe_float(levels.get("volume20"))
        liquidity_cap = (
            math.floor(liquidity * max_volume_fraction)
            if liquidity is not None and liquidity > 0 and max_volume_fraction > 0
            else capital_cap
        )
        raw_shares = min(risk_cap, capital_cap, liquidity_cap)
        rounded_shares = math.floor(raw_shares / lot_size) * lot_size
        if rounded_shares >= lot_size and reward_risk >= minimum_reward_risk:
            position_shares = rounded_shares
    position_value = (
        position_shares * effective_entry * price_multiplier
        if position_shares is not None
        else None
    )

    notes = [
        f"Rủi ro mỗi lệnh mặc định {risk_pct:.1%} trên vốn {capital:,.0f} VND.",
        "Không mua đuổi nếu giá đang dưới stop tham chiếu.",
        (
            "Đã tính commission/slippage hai chiều và thuế bên bán vào "
            "risk/reward."
        ),
    ]
    if reward_risk is not None and reward_risk < minimum_reward_risk:
        notes.append("Reward/risk thấp, nên đợi điểm vào tốt hơn.")
    elif reward_risk is not None:
        notes.append("Reward/risk đạt ngưỡng tối thiểu theo cấu hình.")
    else:
        notes.append("Không có target đạt ngưỡng reward/risk; không đề xuất vị thế.")

    return {
        "risk_per_trade_pct": risk_pct,
        "capital_reference_vnd": capital,
        "atr_stop_multiplier": atr_multiplier,
        "lot_size": lot_size,
        "max_volume_fraction": max_volume_fraction,
        "minimum_reward_risk": minimum_reward_risk,
        "price_multiplier": price_multiplier,
        "commission_bps_per_side": commission_bps,
        "sell_tax_bps": sell_tax_bps,
        "slippage_bps_per_side": slippage_bps,
        "effective_entry": safe_float(effective_entry),
        "effective_stop": safe_float(effective_stop),
        "minimum_target": safe_float(minimum_target),
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
