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


def run_stateful_long_only_backtest(
    frame: pd.DataFrame,
    *,
    prediction_column: str = "predicted_excess_return",
    entry_price_column: str = "swing_execution_open",
    mark_price_column: str = "swing_execution_close",
    volume_column: str | None = None,
    entry_margin: float = 0.0,
    entry_margin_column: str | None = None,
    exit_threshold: float = 0.0,
    fixed_holding_sessions: int | None = None,
    minimum_holding_sessions: int = 2,
    entry_cost_bps: float = 20.0,
    exit_cost_bps: float = 30.0,
    periods_per_year: int = 252,
    initial_capital: float = 100_000_000,
    lot_size: int = 100,
    max_volume_fraction: float = 0.01,
    price_multiplier: float = 1000.0,
    force_close_at_end: bool = True,
) -> tuple[dict, pd.DataFrame]:
    """Backtest one cash/long position with settlement-aware holding rules.

    Decisions are made after the signal-date close and executed at the next
    session open supplied by ``entry_price_column``.  A newly bought position
    cannot be sold until ``minimum_holding_sessions`` later signal sessions;
    use at least two for Vietnamese cash equities.  This is deliberately a
    separate engine from the legacy one-period round-trip simulator.

    When ``fixed_holding_sessions`` is supplied, the backtest exits at the
    row's close/mark price exactly after that many sessions.  This is the
    correct mode for validating a fixed-horizon return target; score-based
    exits are deliberately disabled so the executed return matches the label.
    """

    if frame.empty:
        raise ValueError("Không có dữ liệu để backtest stateful.")
    if minimum_holding_sessions < 2:
        raise ValueError(
            "minimum_holding_sessions phải >= 2 cho cổ phiếu cơ sở T+2."
        )
    if fixed_holding_sessions is not None and fixed_holding_sessions < minimum_holding_sessions:
        raise ValueError(
            "fixed_holding_sessions phải >= minimum_holding_sessions để tôn trọng T+2."
        )
    if initial_capital <= 0 or lot_size < 1 or price_multiplier <= 0:
        raise ValueError("Vốn, lot_size và price_multiplier phải dương.")
    if not 0 < max_volume_fraction <= 1:
        raise ValueError("max_volume_fraction phải nằm trong (0, 1].")
    required = [prediction_column, entry_price_column, mark_price_column]
    if entry_margin_column:
        required.append(entry_margin_column)
    if volume_column:
        required.append(volume_column)
    missing = [column for column in required if column not in frame]
    if missing:
        raise ValueError("Thiếu cột stateful backtest: " + ", ".join(missing))

    predictions = pd.to_numeric(frame[prediction_column], errors="coerce")
    entries = pd.to_numeric(frame[entry_price_column], errors="coerce")
    marks = pd.to_numeric(frame[mark_price_column], errors="coerce")
    if predictions.isna().any() or entries.isna().any() or marks.isna().any():
        raise ValueError("Prediction/giá execution stateful không được thiếu.")
    if (entries <= 0).any() or (marks <= 0).any():
        raise ValueError("Giá execution stateful phải dương.")
    volumes = None
    if volume_column:
        volumes = pd.to_numeric(frame[volume_column], errors="coerce")
        if volumes.isna().any() or (volumes < 0).any():
            raise ValueError("Ước lượng thanh khoản stateful không hợp lệ.")

    entry_rate = float(entry_cost_bps) / 10_000.0
    exit_rate = float(exit_cost_bps) / 10_000.0
    if entry_rate < 0 or exit_rate < 0:
        raise ValueError("Chi phí stateful không được âm.")
    margins = (
        pd.to_numeric(frame[entry_margin_column], errors="coerce")
        if entry_margin_column
        else pd.Series(float(entry_margin), index=frame.index)
    )
    if margins.isna().any():
        raise ValueError("entry margin stateful không được thiếu.")

    cash = float(initial_capital)
    gross_cash = float(initial_capital)
    shares = 0
    entry_row: int | None = None
    entry_date = None
    entry_price = None
    entry_notional = 0.0
    entry_cost_value = 0.0
    total_cost = 0.0
    liquidity_limited = 0
    trade_records: list[dict] = []
    rows: list[dict] = []
    previous_equity = float(initial_capital)

    for row_number, (current_date, prediction) in enumerate(predictions.items()):
        execution_price = float(entries.loc[current_date]) * price_multiplier
        mark_price = float(marks.loc[current_date]) * price_multiplier
        margin = float(margins.loc[current_date])
        volume_cap = None
        if volumes is not None:
            volume_cap = int(
                math.floor(
                    float(volumes.loc[current_date]) * max_volume_fraction / lot_size
                )
                * lot_size
            )

        action = "HOLD"
        realized_trade_return = np.nan
        transaction_cost_value = 0.0
        sell_eligible = (
            shares > 0
            and entry_row is not None
            and row_number - entry_row >= minimum_holding_sessions
        )

        fixed_exit_due = (
            fixed_holding_sessions is not None
            and shares > 0
            and entry_row is not None
            and row_number - entry_row >= fixed_holding_sessions
        )
        # Fixed-horizon validation exits at the stated close.  Otherwise an
        # exit signal known after close[t] is executed at open[t+1].
        model_exit_due = fixed_holding_sessions is None and float(prediction) <= float(exit_threshold)
        if sell_eligible and (fixed_exit_due or model_exit_due):
            sell_shares = shares if volume_cap is None or volume_cap >= shares else 0
            if sell_shares <= 0:
                liquidity_limited += 1
            else:
                exit_price = mark_price if fixed_exit_due else execution_price
                proceeds = sell_shares * exit_price
                exit_cost_value = proceeds * exit_rate
                cash += proceeds - exit_cost_value
                gross_cash += proceeds
                shares -= sell_shares
                total_cost += exit_cost_value
                transaction_cost_value += exit_cost_value
                action = "SELL"
                if shares == 0 and entry_price is not None:
                    gross_pnl = proceeds - entry_notional
                    net_pnl = cash - gross_cash + gross_pnl
                    # net_pnl above would include earlier trades; derive per-trade
                    # costs directly to keep the audit record independent.
                    net_pnl = gross_pnl - entry_cost_value - exit_cost_value
                    realized_trade_return = net_pnl / max(
                        entry_notional + entry_cost_value, 1e-12
                    )
                    trade_records.append(
                        {
                            "entry_date": entry_date,
                            "exit_date": current_date,
                            "entry_price": entry_price / price_multiplier,
                            "exit_price": exit_price / price_multiplier,
                            "shares": sell_shares,
                            "holding_sessions": int(row_number - entry_row),
                            "gross_pnl": gross_pnl,
                            "net_pnl": net_pnl,
                            "net_return": realized_trade_return,
                            "exit_reason": "fixed_horizon_exit" if fixed_exit_due else "model_exit",
                        }
                    )
                    entry_row = None
                    entry_date = None
                    entry_price = None
                    entry_notional = 0.0
                    entry_cost_value = 0.0

        # Never reverse from LONG to LONG in one session: a sale settles first.
        if shares == 0 and action == "HOLD":
            threshold = entry_rate + exit_rate + margin
            if float(prediction) > threshold:
                affordable = int(
                    math.floor(cash / (execution_price * (1.0 + entry_rate)) / lot_size)
                    * lot_size
                )
                buy_shares = affordable if volume_cap is None else min(affordable, volume_cap)
                if buy_shares <= 0:
                    if affordable > 0:
                        liquidity_limited += 1
                else:
                    if volume_cap is not None and buy_shares < affordable:
                        liquidity_limited += 1
                    notional = buy_shares * execution_price
                    buy_cost = notional * entry_rate
                    cash -= notional + buy_cost
                    gross_cash -= notional
                    shares = buy_shares
                    entry_row = row_number
                    entry_date = current_date
                    entry_price = execution_price
                    entry_notional = notional
                    entry_cost_value = buy_cost
                    total_cost += buy_cost
                    transaction_cost_value += buy_cost
                    action = "BUY"

        equity = cash + shares * mark_price
        gross_equity = gross_cash + shares * mark_price
        net_return = equity / previous_equity - 1.0 if previous_equity > 0 else 0.0
        previous_equity = equity
        rows.append(
            {
                "prediction": float(prediction),
                "entry_margin": margin,
                "action": action,
                "position_shares": int(shares),
                "sell_eligible": bool(sell_eligible),
                "holding_sessions": (
                    int(row_number - entry_row) if entry_row is not None else 0
                ),
                "transaction_cost_value": transaction_cost_value,
                "transaction_cost": transaction_cost_value / max(initial_capital, 1e-12),
                "equity_curve": equity / initial_capital,
                "gross_equity_curve": gross_equity / initial_capital,
                "net_strategy_return": net_return,
                "realized_trade_return": realized_trade_return,
            }
        )

    forced_exit = False
    unsettled_position_at_end = shares > 0
    if shares and force_close_at_end and entry_row is not None:
        last_row = len(rows) - 1
        if last_row - entry_row >= minimum_holding_sessions:
            forced_exit = True
            final_price = float(marks.iloc[-1]) * price_multiplier
            proceeds = shares * final_price
            exit_cost_value = proceeds * exit_rate
            cash += proceeds - exit_cost_value
            gross_cash += proceeds
            total_cost += exit_cost_value
            gross_pnl = proceeds - entry_notional
            net_pnl = gross_pnl - entry_cost_value - exit_cost_value
            trade_records.append(
                {
                    "entry_date": entry_date,
                    "exit_date": frame.index[-1],
                    "entry_price": entry_price / price_multiplier,
                    "exit_price": final_price / price_multiplier,
                    "shares": shares,
                    "holding_sessions": int(last_row - entry_row),
                    "gross_pnl": gross_pnl,
                    "net_pnl": net_pnl,
                    "net_return": net_pnl / max(entry_notional + entry_cost_value, 1e-12),
                    "exit_reason": "forced_terminal_exit",
                }
            )
            shares = 0
            unsettled_position_at_end = False
            rows[-1]["action"] = "FORCED_SELL"
            rows[-1]["transaction_cost_value"] += exit_cost_value
            rows[-1]["transaction_cost"] += exit_cost_value / initial_capital
            rows[-1]["position_shares"] = 0
            rows[-1]["equity_curve"] = cash / initial_capital
            rows[-1]["gross_equity_curve"] = gross_cash / initial_capital
            rows[-1]["net_strategy_return"] = cash / max(
                initial_capital * (rows[-2]["equity_curve"] if len(rows) > 1 else 1.0),
                1e-12,
            ) - 1.0

    details = pd.DataFrame(rows, index=frame.index)
    trades = pd.DataFrame(trade_records)
    net_returns = details["net_strategy_return"].replace([np.inf, -np.inf], np.nan).fillna(0.0)
    gross_total_return = float(details["gross_equity_curve"].iloc[-1] - 1.0)
    net_total_return = float(details["equity_curve"].iloc[-1] - 1.0)
    holdings = trades["holding_sessions"] if not trades.empty else pd.Series(dtype=float)
    trade_returns = trades["net_return"] if not trades.empty else pd.Series(dtype=float)
    closed_gross_pnl = float(trades["gross_pnl"].sum()) if not trades.empty else 0.0
    closed_net_pnl = float(trades["net_pnl"].sum()) if not trades.empty else 0.0
    positive_pnl = (
        float(trades.loc[trades["net_pnl"] > 0, "net_pnl"].sum())
        if not trades.empty
        else 0.0
    )
    negative_pnl = (
        float(-trades.loc[trades["net_pnl"] < 0, "net_pnl"].sum())
        if not trades.empty
        else 0.0
    )
    summary = {
        "strategy": "stateful_cash_long_swing",
        "execution_rule": "signal after close[t]; execute next-session open; cash -> long -> cash",
        "settlement_rule": f"minimum holding {minimum_holding_sessions} sessions before sale eligibility",
        "minimum_holding_sessions": int(minimum_holding_sessions),
        "entry_margin": float(entry_margin),
        "exit_threshold": float(exit_threshold),
        "exit_rule": (
            f"fixed close exit after {fixed_holding_sessions} sessions"
            if fixed_holding_sessions is not None
            else "score-based next-open exit"
        ),
        "fixed_holding_sessions": fixed_holding_sessions,
        "entry_cost_bps": float(entry_cost_bps),
        "exit_cost_bps": float(exit_cost_bps),
        "round_trip_cost_bps": float(entry_cost_bps + exit_cost_bps),
        "periods_per_year": int(periods_per_year),
        "observations": int(len(details)),
        "entries": int(len(trades) + (1 if unsettled_position_at_end else 0)),
        "exits": int(len(trades)),
        "completed_round_trips": int(len(trades)),
        "active_sessions": int((details["position_shares"] > 0).sum()),
        "exposure": float((details["position_shares"] > 0).mean()),
        "gross_total_return": gross_total_return,
        "net_total_return": net_total_return,
        "total_return": net_total_return,
        "annualized_return": _annualized_return(net_returns, periods_per_year),
        "annualized_volatility": float(net_returns.std(ddof=1) * math.sqrt(periods_per_year)) if len(net_returns) > 1 else 0.0,
        "sharpe_ratio": _sharpe_ratio(net_returns, periods_per_year),
        "sharpe": _sharpe_ratio(net_returns, periods_per_year),
        "max_drawdown": _max_drawdown(net_returns),
        "hit_rate": float((trade_returns > 0).mean()) if len(trade_returns) else None,
        "profit_factor": positive_pnl / negative_pnl if negative_pnl > 0 else None,
        "average_holding_sessions": float(holdings.mean()) if len(holdings) else None,
        "median_holding_sessions": float(holdings.median()) if len(holdings) else None,
        "gross_pnl_sum": closed_gross_pnl,
        "net_pnl_sum": closed_net_pnl,
        "transaction_cost_value_sum": float(total_cost),
        "transaction_cost_sum": float(total_cost / initial_capital),
        "total_turnover": None,
        "annualized_turnover": None,
        "liquidity_limited_trades": int(liquidity_limited),
        "forced_exit": bool(forced_exit),
        "unsettled_position_at_end": bool(unsettled_position_at_end),
        "initial_capital": float(initial_capital),
        "final_capital": float(details["equity_curve"].iloc[-1] * initial_capital),
        "lot_size": int(lot_size),
        "max_volume_fraction": float(max_volume_fraction),
        "price_multiplier": float(price_multiplier),
    }
    details.attrs["trades"] = trades
    return summary, details
