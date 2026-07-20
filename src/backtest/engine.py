from __future__ import annotations

import math

import numpy as np
import pandas as pd


def _compound_return(returns: pd.Series) -> float:
    return float((1.0 + returns).prod() - 1.0)


def _annualized_return(returns: pd.Series, periods_per_year: int) -> float | None:
    if returns.empty:
        return None
    ending_equity = float((1.0 + returns).prod())
    if ending_equity <= 0:
        return None
    return float(ending_equity ** (periods_per_year / len(returns)) - 1.0)


def _sharpe_ratio(returns: pd.Series, periods_per_year: int) -> float | None:
    volatility = float(returns.std(ddof=1))
    if not np.isfinite(volatility) or volatility <= 0:
        return None
    return float(math.sqrt(periods_per_year) * returns.mean() / volatility)


def _max_drawdown(returns: pd.Series) -> float:
    equity = (1.0 + returns).cumprod()
    equity_with_start = pd.concat(
        [pd.Series([1.0], index=["__start__"]), equity],
    )
    drawdown = equity_with_start.div(equity_with_start.cummax()).sub(1.0)
    return float(drawdown.min())


def _cost_rates(
    round_trip_cost_bps: float | None,
    entry_cost_bps: float | None,
    exit_cost_bps: float | None,
) -> tuple[float, float]:
    if entry_cost_bps is None and exit_cost_bps is None:
        total = 40.0 if round_trip_cost_bps is None else float(round_trip_cost_bps)
        if total < 0:
            raise ValueError("round_trip_cost_bps không được âm.")
        return total / 2.0, total / 2.0
    if entry_cost_bps is None or exit_cost_bps is None:
        raise ValueError("Phải cung cấp cả entry_cost_bps và exit_cost_bps.")
    entry = float(entry_cost_bps)
    exit_ = float(exit_cost_bps)
    if entry < 0 or exit_ < 0:
        raise ValueError("Chi phí mua/bán không được âm.")
    return entry, exit_


def _round_trip_returns(
    details: pd.DataFrame,
    entry_rate: float,
    exit_rate: float,
    *,
    entry_price: pd.Series | None,
    volume: pd.Series | None,
    initial_capital: float | None,
    lot_size: int,
    max_volume_fraction: float,
    price_multiplier: float,
) -> tuple[int, int]:
    signal = details["executed_position"]
    asset_return = details["asset_return"]
    sizing_enabled = initial_capital is not None

    if not sizing_enabled:
        entry_turnover = signal
        exit_turnover = signal * (1.0 + asset_return)
        details["executed_shares"] = np.nan
        details["liquidity_cap_shares"] = np.nan
        details["capital_utilization"] = signal
        details["turnover"] = entry_turnover + exit_turnover
        details["transaction_cost"] = (
            entry_turnover * entry_rate + exit_turnover * exit_rate
        )
        details["gross_strategy_return"] = signal * asset_return
        details["net_strategy_return"] = (
            details["gross_strategy_return"] - details["transaction_cost"]
        )
        details["transaction_cost_value"] = np.nan
        details["gross_pnl"] = np.nan
        details["net_pnl"] = np.nan
        active_trades = int(signal.sum())
        return active_trades, 0

    assert entry_price is not None
    capital = float(initial_capital)
    equity = capital
    executed_shares: list[int] = []
    liquidity_caps: list[int] = []
    capital_utilization: list[float] = []
    turnover: list[float] = []
    costs_return: list[float] = []
    gross_returns: list[float] = []
    net_returns: list[float] = []
    costs_value: list[float] = []
    gross_pnl_values: list[float] = []
    net_pnl_values: list[float] = []
    liquidity_limited = 0

    for row_number in range(len(details)):
        current_signal = int(signal.iloc[row_number])
        price = float(entry_price.iloc[row_number])
        cash_price = price * price_multiplier
        current_return = float(asset_return.iloc[row_number])
        equity_before = equity
        affordable = int(
            math.floor(equity_before / (cash_price * (1.0 + entry_rate)) / lot_size)
            * lot_size
        )
        if volume is None:
            liquidity_cap = affordable
        else:
            liquidity_cap = int(
                math.floor(
                    float(volume.iloc[row_number]) * max_volume_fraction / lot_size
                )
                * lot_size
            )
        shares = min(affordable, liquidity_cap) if current_signal else 0
        if current_signal and liquidity_cap < affordable:
            liquidity_limited += 1

        entry_notional = shares * cash_price
        exit_notional = entry_notional * (1.0 + current_return)
        gross_pnl = entry_notional * current_return
        transaction_cost_value = entry_notional * entry_rate + exit_notional * exit_rate
        net_pnl = gross_pnl - transaction_cost_value
        gross_period_return = gross_pnl / equity_before
        net_period_return = net_pnl / equity_before
        equity += net_pnl

        executed_shares.append(shares)
        liquidity_caps.append(liquidity_cap)
        capital_utilization.append(entry_notional / equity_before)
        turnover.append((entry_notional + exit_notional) / equity_before)
        costs_return.append(transaction_cost_value / equity_before)
        gross_returns.append(gross_period_return)
        net_returns.append(net_period_return)
        costs_value.append(transaction_cost_value)
        gross_pnl_values.append(gross_pnl)
        net_pnl_values.append(net_pnl)

    details["executed_shares"] = executed_shares
    details["liquidity_cap_shares"] = liquidity_caps
    details["capital_utilization"] = capital_utilization
    details["turnover"] = turnover
    details["transaction_cost"] = costs_return
    details["gross_strategy_return"] = gross_returns
    details["net_strategy_return"] = net_returns
    details["transaction_cost_value"] = costs_value
    details["gross_pnl"] = gross_pnl_values
    details["net_pnl"] = net_pnl_values
    active_trades = int((details["executed_shares"] > 0).sum())
    return active_trades, liquidity_limited


def _position_returns(
    details: pd.DataFrame,
    entry_rate: float,
    exit_rate: float,
    force_close_at_end: bool,
) -> tuple[int, int, bool]:
    position_change = details["executed_position"].diff()
    position_change.iloc[0] = details["executed_position"].iloc[0]
    entry_turnover = position_change.clip(lower=0.0)
    exit_turnover = (-position_change.clip(upper=0.0)).astype(float)
    entries = int((position_change > 0).sum())
    exits = int((position_change < 0).sum())
    forced_exit = bool(force_close_at_end and details["executed_position"].iloc[-1] > 0)
    if forced_exit:
        exit_turnover.iloc[-1] += float(details["executed_position"].iloc[-1])
        exits += 1

    details["executed_shares"] = np.nan
    details["liquidity_cap_shares"] = np.nan
    details["capital_utilization"] = details["executed_position"]
    details["turnover"] = entry_turnover + exit_turnover
    details["transaction_cost"] = (
        entry_turnover * entry_rate + exit_turnover * exit_rate
    )
    details["gross_strategy_return"] = (
        details["executed_position"] * details["asset_return"]
    )
    details["net_strategy_return"] = (
        details["gross_strategy_return"] - details["transaction_cost"]
    )
    details["transaction_cost_value"] = np.nan
    details["gross_pnl"] = np.nan
    details["net_pnl"] = np.nan
    return entries, exits, forced_exit


def run_long_only_backtest(
    frame: pd.DataFrame,
    signal_column: str = "xgboost_prediction",
    return_column: str = "next_return",
    *,
    execution_lag: int = 1,
    round_trip_cost_bps: float | None = 40.0,
    entry_cost_bps: float | None = None,
    exit_cost_bps: float | None = None,
    periods_per_year: int = 252,
    force_close_at_end: bool = True,
    round_trip_each_signal: bool = False,
    entry_price_column: str | None = None,
    volume_column: str | None = None,
    initial_capital: float | None = None,
    lot_size: int = 1,
    max_volume_fraction: float = 1.0,
    price_multiplier: float = 1.0,
) -> tuple[dict, pd.DataFrame]:
    """Backtest long/cash có độ trễ, chi phí và tùy chọn lô/thanh khoản.

    ``execution_lag=1`` nghĩa là return dòng ``t`` nhận signal dòng ``t-1``.
    Khi ``round_trip_each_signal=True``, mỗi signal active là một giao dịch vào
    và ra trong chính period của ``return_column``; chi phí hai phía được tính
    trên từng giao dịch, không chỉ khi signal đổi trạng thái.
    ``volume_column`` phải là ước lượng thanh khoản đã biết tại lúc tạo signal,
    ví dụ ADV20 đến ngày t; không được truyền volume cả ngày giao dịch tương lai.
    """

    if frame.empty:
        raise ValueError("Không có dữ liệu để backtest.")
    required_columns = [signal_column, return_column]
    if initial_capital is not None:
        if entry_price_column is None:
            raise ValueError("Cần entry_price_column khi backtest theo vốn/lô.")
        required_columns.append(entry_price_column)
        if max_volume_fraction < 1.0:
            if volume_column is None:
                raise ValueError("Cần volume_column khi giới hạn thanh khoản.")
            required_columns.append(volume_column)
    missing = [column for column in required_columns if column not in frame.columns]
    if missing:
        raise ValueError(f"Thiếu cột backtest: {', '.join(missing)}")
    if execution_lag < 0:
        raise ValueError("execution_lag phải lớn hơn hoặc bằng 0.")
    if periods_per_year <= 0:
        raise ValueError("periods_per_year phải lớn hơn 0.")
    if initial_capital is not None and initial_capital <= 0:
        raise ValueError("initial_capital phải lớn hơn 0.")
    if lot_size < 1:
        raise ValueError("lot_size phải lớn hơn 0.")
    if price_multiplier <= 0:
        raise ValueError("price_multiplier phải lớn hơn 0.")
    if not 0 < max_volume_fraction <= 1:
        raise ValueError("max_volume_fraction phải nằm trong (0, 1].")
    if initial_capital is not None and not round_trip_each_signal:
        raise ValueError("Backtest theo vốn/lô cần round_trip_each_signal=True.")

    entry_bps, exit_bps = _cost_rates(
        round_trip_cost_bps,
        entry_cost_bps,
        exit_cost_bps,
    )
    entry_rate = entry_bps / 10_000.0
    exit_rate = exit_bps / 10_000.0

    signal = pd.to_numeric(frame[signal_column], errors="coerce")
    if signal.isna().any() or not signal.isin([0, 1]).all():
        raise ValueError("Signal backtest phải chỉ gồm 0/1 và không có NaN.")
    asset_return = pd.to_numeric(frame[return_column], errors="coerce")
    if asset_return.isna().any() or not np.isfinite(asset_return).all():
        raise ValueError("Cột return phải đầy đủ và hữu hạn.")
    if (asset_return <= -1).any():
        raise ValueError("Return backtest phải lớn hơn -100%.")

    entry_price = None
    volume = None
    if initial_capital is not None:
        entry_price = pd.to_numeric(frame[entry_price_column], errors="coerce")
        if entry_price.isna().any() or (entry_price <= 0).any():
            raise ValueError("Giá vào lệnh phải đầy đủ và lớn hơn 0.")
        if volume_column is not None:
            volume = pd.to_numeric(frame[volume_column], errors="coerce")
            if volume.isna().any() or (volume < 0).any():
                raise ValueError("Volume backtest phải đầy đủ và không âm.")

    details = pd.DataFrame(index=frame.index)
    details["raw_signal"] = signal.astype(int)
    details["executed_position"] = signal.shift(execution_lag).fillna(0.0).astype(float)
    details["asset_return"] = asset_return.astype(float)

    liquidity_limited_trades = 0
    if round_trip_each_signal:
        entries, liquidity_limited_trades = _round_trip_returns(
            details,
            entry_rate,
            exit_rate,
            entry_price=entry_price,
            volume=volume,
            initial_capital=initial_capital,
            lot_size=lot_size,
            max_volume_fraction=max_volume_fraction,
            price_multiplier=price_multiplier,
        )
        exits = entries
        forced_exit = False
    else:
        entries, exits, forced_exit = _position_returns(
            details,
            entry_rate,
            exit_rate,
            force_close_at_end,
        )

    details["equity_curve"] = (1.0 + details["net_strategy_return"]).cumprod()
    details["drawdown"] = (
        details["equity_curve"]
        .div(details["equity_curve"].cummax().clip(lower=1.0))
        .sub(1.0)
    )

    gross = details["gross_strategy_return"]
    net = details["net_strategy_return"]
    active = (
        details["executed_shares"].fillna(0) > 0
        if initial_capital is not None
        else details["executed_position"] > 0
    )
    active_returns = details.loc[active, "asset_return"]
    annualized_volatility = float(net.std(ddof=1) * math.sqrt(periods_per_year))
    if not np.isfinite(annualized_volatility):
        annualized_volatility = 0.0
    net_total_return = _compound_return(net)
    sharpe = _sharpe_ratio(net, periods_per_year)
    average_turnover = float(details["turnover"].mean())

    summary = {
        "strategy": (
            "single_period_round_trip" if round_trip_each_signal else "long_or_cash"
        ),
        "signal_column": signal_column,
        "return_column": return_column,
        "signal_timing": "signal[t] được áp vào return[t + execution_lag]",
        "return_alignment": "executed_position[t] * return_column[t]",
        "execution_lag_sessions": int(execution_lag),
        "round_trip_cost_bps": float(entry_bps + exit_bps),
        "entry_cost_bps": float(entry_bps),
        "exit_cost_bps": float(exit_bps),
        "one_way_cost_bps": (
            float(entry_bps) if math.isclose(entry_bps, exit_bps) else None
        ),
        "force_close_at_end": bool(force_close_at_end),
        "forced_exit": forced_exit,
        "round_trip_each_signal": bool(round_trip_each_signal),
        "periods_per_year": int(periods_per_year),
        "observations": int(len(details)),
        "active_sessions": int(active.sum()),
        "exposure": float(active.mean()),
        "entries": entries,
        "exits": exits,
        "completed_round_trips": int(min(entries, exits)),
        "gross_total_return": _compound_return(gross),
        "net_total_return": net_total_return,
        "total_return": net_total_return,
        "annualized_return": _annualized_return(net, periods_per_year),
        "annualized_volatility": annualized_volatility,
        "sharpe_ratio": sharpe,
        "sharpe": sharpe,
        "max_drawdown": _max_drawdown(net),
        "hit_rate": float((active_returns > 0).mean()) if len(active_returns) else None,
        "total_turnover": float(details["turnover"].sum()),
        "average_turnover_per_session": average_turnover,
        "average_turnover": average_turnover,
        "annualized_turnover": float(average_turnover * periods_per_year),
        "transaction_cost_sum": float(details["transaction_cost"].sum()),
        "transaction_cost_value_sum": (
            float(details["transaction_cost_value"].sum())
            if initial_capital is not None
            else None
        ),
        "buy_and_hold_total_return": _compound_return(details["asset_return"]),
        "initial_capital": (
            float(initial_capital) if initial_capital is not None else None
        ),
        "lot_size": int(lot_size) if initial_capital is not None else None,
        "max_volume_fraction": (
            float(max_volume_fraction) if initial_capital is not None else None
        ),
        "price_multiplier": (
            float(price_multiplier) if initial_capital is not None else None
        ),
        "liquidity_limited_trades": int(liquidity_limited_trades),
        "final_capital": (
            float(initial_capital * (1.0 + net_total_return))
            if initial_capital is not None
            else None
        ),
    }
    return summary, details
