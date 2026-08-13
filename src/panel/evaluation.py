from __future__ import annotations

import math
from collections.abc import Sequence

import numpy as np
import pandas as pd


def _as_columns(predictions: pd.DataFrame) -> pd.DataFrame:
    if isinstance(predictions.index, pd.MultiIndex) and {"date", "symbol"}.issubset(
        predictions.index.names
    ):
        frame = predictions.reset_index()
    else:
        frame = predictions.copy()
    if not {"date", "symbol"}.issubset(frame.columns):
        raise ValueError("Predictions phải có date và symbol.")
    frame["date"] = pd.to_datetime(frame["date"]).dt.tz_localize(None)
    return frame.sort_values(["date", "symbol"])


def _filter_complete_universe_dates(
    frame: pd.DataFrame,
    *,
    required_columns: Sequence[str],
    min_symbols_per_date: int,
) -> pd.DataFrame:
    complete = frame.dropna(subset=list(required_columns)).copy()
    counts = complete.groupby("date")["symbol"].nunique()
    eligible = counts[counts >= min_symbols_per_date].index
    return complete[complete["date"].isin(eligible)]


def rank_ic_by_date(
    predictions: pd.DataFrame,
    *,
    prediction_column: str = "prediction",
    actual_column: str = "actual_excess_return",
    min_symbols_per_date: int = 2,
) -> pd.Series:
    """Tính Spearman Rank IC theo từng ngày trên universe đủ lớn."""

    if min_symbols_per_date < 2:
        raise ValueError("min_symbols_per_date phải >= 2 để tính Rank IC.")
    frame = _filter_complete_universe_dates(
        _as_columns(predictions),
        required_columns=[prediction_column, actual_column],
        min_symbols_per_date=min_symbols_per_date,
    )

    def spearman(group: pd.DataFrame) -> float:
        predicted_rank = group[prediction_column].rank(method="average")
        actual_rank = group[actual_column].rank(method="average")
        return float(predicted_rank.corr(actual_rank))

    values = {
        current_date: spearman(group)
        for current_date, group in frame.groupby("date", sort=True)
    }
    return pd.Series(values, dtype=float, name="rank_ic").dropna()


def _newey_west_t_stat(values: pd.Series, max_lag: int) -> float | None:
    """Tính t-stat HAC cho mean, phù hợp với forward return chồng lắp."""

    clean = pd.to_numeric(values, errors="coerce").dropna()
    if len(clean) < 3:
        return None
    residual = clean - clean.mean()
    observations = len(residual)
    lag = min(max(int(max_lag), 0), observations - 1)
    long_run_variance = float(np.dot(residual, residual) / observations)
    for offset in range(1, lag + 1):
        covariance = float(
            np.dot(residual.iloc[offset:], residual.iloc[:-offset]) / observations
        )
        bartlett_weight = 1.0 - offset / (lag + 1.0)
        long_run_variance += 2.0 * bartlett_weight * covariance
    if not np.isfinite(long_run_variance) or long_run_variance <= 0:
        return None
    standard_error = math.sqrt(long_run_variance / observations)
    return float(clean.mean() / standard_error)


def _weights(symbols: Sequence[str]) -> dict[str, float]:
    if not symbols:
        return {}
    weight = 1.0 / len(symbols)
    return {symbol: weight for symbol in symbols}


def _turnover(previous: dict[str, float], current: dict[str, float]) -> float:
    """Một nửa L1 dùng để đo mức thay đổi thành phần danh mục."""

    universe = set(previous) | set(current)
    return 0.5 * sum(
        abs(current.get(symbol, 0.0) - previous.get(symbol, 0.0))
        for symbol in universe
    )


def top_k_backtest(
    predictions: pd.DataFrame,
    *,
    top_k: int = 5,
    transaction_cost_bps: float = 50.0,
    rebalance_every: int = 1,
    min_symbols_per_date: int = 2,
    prediction_column: str = "prediction",
    return_column: str = "actual_return",
    force_liquidation: bool = True,
) -> pd.DataFrame:
    """Backtest equal-weight top-k với full round-trip cho mỗi cohort.

    ``transaction_cost_bps`` là tổng chi phí giả định cho một vòng mua + bán.
    Target hiện tại luôn vào ở open(t+1) và thoát ở close(t+h), nên toàn bộ
    danh mục phải chịu đúng một round-trip ở mỗi cohort, kể cả khi cùng mã được
    chọn lại. ``selection_turnover`` chỉ đo thay đổi thành phần, không dùng để
    giảm chi phí. ``force_liquidation`` được giữ để tương thích API; thanh lý đã
    nằm trong return/chi phí của từng cohort.
    """

    if (
        top_k <= 0
        or rebalance_every <= 0
        or transaction_cost_bps < 0
        or min_symbols_per_date < top_k
    ):
        raise ValueError(
            "top_k/rebalance_every phải > 0, phí không âm và "
            "min_symbols_per_date phải >= top_k."
        )
    frame = _filter_complete_universe_dates(
        _as_columns(predictions),
        required_columns=[prediction_column, return_column],
        min_symbols_per_date=min_symbols_per_date,
    )
    dates = frame["date"].drop_duplicates().sort_values().iloc[::rebalance_every]
    previous: dict[str, float] = {}
    records: list[dict] = []
    cost_rate = transaction_cost_bps / 10_000

    for current_date in dates:
        candidates = frame[frame["date"] == current_date].nlargest(
            top_k, prediction_column
        )
        if len(candidates) < top_k:
            continue
        symbols = candidates["symbol"].astype(str).tolist()
        current = _weights(symbols)
        selection_turnover = _turnover(previous, current)
        cost_turnover = 1.0
        gross_return = float(candidates[return_column].mean())
        market_return = (
            float(candidates["actual_market_return"].mean())
            if "actual_market_return" in candidates
            else float("nan")
        )
        cost = cost_turnover * cost_rate
        record = {
            "date": current_date,
            "symbols": ",".join(symbols),
            "positions": len(symbols),
            "gross_return": gross_return,
            "turnover": selection_turnover,
            "selection_turnover": selection_turnover,
            "cost_turnover": cost_turnover,
            "cost": cost,
            "net_return": gross_return - cost,
            "market_return": market_return,
        }
        record["net_excess_return"] = record["net_return"] - market_return
        if "market_regime" in candidates:
            modes = candidates["market_regime"].dropna().mode()
            record["market_regime"] = (
                modes.iloc[0] if not modes.empty else "unknown"
            )
        records.append(record)
        previous = current

    if not records:
        columns = [
            "symbols",
            "positions",
            "gross_return",
            "turnover",
            "selection_turnover",
            "cost_turnover",
            "cost",
            "net_return",
            "market_return",
            "net_excess_return",
        ]
        return pd.DataFrame(columns=columns, index=pd.DatetimeIndex([], name="date"))

    _ = force_liquidation
    return pd.DataFrame(records).set_index("date").sort_index()


def sparse_panel_backtest(
    predictions: pd.DataFrame,
    *,
    max_positions: int = 3,
    transaction_cost_bps: float = 50.0,
    horizon: int = 5,
    minimum_holding_sessions: int = 2,
    rebalance_every: int | None = None,
    min_symbols_per_date: int = 2,
    prediction_column: str = "prediction",
    return_column: str = "actual_return",
    market_return_column: str = "actual_market_return",
    entry_margin: float = 0.0,
    entry_margin_column: str | None = "entry_margin",
    rule_selected_column: str | None = "entry_rule_selected",
    cooldown_cohorts: int = 0,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Backtest sparse cohorts: 0..max_positions, cash is the default.

    A prediction must exceed full round-trip cost plus the fold-specific margin.
    Cohorts never overlap because the evaluation interval is at least ``horizon``.
    Each selected position receives ``1 / max_positions`` capital; unused slots
    remain in cash.  This makes Top-K a capacity cap rather than a trading quota.
    """

    interval = horizon if rebalance_every is None else int(rebalance_every)
    if (
        max_positions <= 0
        or horizon < minimum_holding_sessions
        or minimum_holding_sessions < 2
        or interval < horizon
        or transaction_cost_bps < 0
        or cooldown_cohorts < 0
        or min_symbols_per_date < max(2, max_positions)
    ):
        raise ValueError(
            "Cấu hình sparse backtest không hợp lệ: horizon phải tôn trọng T+2, "
            "rebalance_every >= horizon, phí/cooldown không âm và universe đủ lớn."
        )

    required = [prediction_column, return_column, market_return_column]
    frame = _filter_complete_universe_dates(
        _as_columns(predictions),
        required_columns=required,
        min_symbols_per_date=min_symbols_per_date,
    )
    dates = frame["date"].drop_duplicates().sort_values().iloc[::interval]
    cost_rate = transaction_cost_bps / 10_000
    slot_weight = 1.0 / max_positions
    cooldown_until: dict[str, int] = {}
    cohort_records: list[dict] = []
    trade_records: list[dict] = []

    for cohort_number, current_date in enumerate(dates):
        date_frame = frame[frame["date"] == current_date].copy()
        regime = None
        if "market_regime" in date_frame:
            modes = date_frame["market_regime"].dropna().mode()
            regime = str(modes.iloc[0]) if not modes.empty else None
        candidates = date_frame.copy()
        candidates["entry_margin_used"] = float(entry_margin)
        if entry_margin_column and entry_margin_column in candidates:
            candidates["entry_margin_used"] = pd.to_numeric(
                candidates[entry_margin_column], errors="coerce"
            )
        if rule_selected_column and rule_selected_column in candidates:
            candidates = candidates[candidates[rule_selected_column].fillna(False)]
        candidates["entry_threshold"] = (
            cost_rate + candidates["entry_margin_used"]
        )
        candidates["expected_net_edge"] = (
            pd.to_numeric(candidates[prediction_column], errors="coerce")
            - cost_rate
        )
        candidates = candidates[
            candidates[prediction_column] > candidates["entry_threshold"]
        ]
        if not candidates.empty:
            cooldown_mask = candidates["symbol"].map(
                lambda symbol: cohort_number >= cooldown_until.get(str(symbol), 0)
            ).astype(bool)
            candidates = candidates.loc[cooldown_mask].nlargest(
                max_positions, prediction_column
            )

        gross_return = 0.0
        market_return = 0.0
        winning_trades = 0
        symbols: list[str] = []
        margins: list[float] = []
        for row in candidates.to_dict("records"):
            symbol = str(row["symbol"])
            gross_trade_return = float(row[return_column])
            market_trade_return = float(row[market_return_column])
            net_trade_return = gross_trade_return - cost_rate
            gross_return += slot_weight * gross_trade_return
            market_return += slot_weight * market_trade_return
            winning_trades += int(net_trade_return > 0)
            symbols.append(symbol)
            margins.append(float(row["entry_margin_used"]))
            cooldown_until[symbol] = cohort_number + 1 + cooldown_cohorts
            trade_records.append(
                {
                    "signal_date": current_date,
                    "entry_date": row.get("entry_date"),
                    "exit_date": row.get("exit_date"),
                    "symbol": symbol,
                    "horizon": horizon,
                    "holding_sessions": horizon,
                    "prediction": float(row.get("prediction", row[prediction_column])),
                    "prediction_lower_bound": float(row[prediction_column]),
                    "prediction_haircut": row.get("prediction_haircut"),
                    "entry_price": row.get("entry_price"),
                    "exit_price": row.get("exit_price"),
                    "entry_margin": float(row["entry_margin_used"]),
                    "entry_threshold": float(row["entry_threshold"]),
                    "expected_net_edge": float(row["expected_net_edge"]),
                    "gross_return": gross_trade_return,
                    "cost": cost_rate,
                    "net_return": net_trade_return,
                    "market_return": market_trade_return,
                    "net_excess_return": net_trade_return - market_trade_return,
                    "fold": row.get("fold"),
                }
            )

        trade_count = len(symbols)
        invested_fraction = trade_count / max_positions
        cost = invested_fraction * cost_rate
        net_return = gross_return - cost
        cohort_record = {
                "date": current_date,
                "symbols": ",".join(symbols),
                "positions": trade_count,
                "completed_round_trips": trade_count,
                "gross_return": gross_return,
                "cost": cost,
                "net_return": net_return,
                "market_return": market_return,
                "net_excess_return": net_return - market_return,
                "invested_fraction": invested_fraction,
                "cash_fraction": 1.0 - invested_fraction,
                "round_trip_turnover": 2.0 * invested_fraction,
                "winning_trades": winning_trades,
                "entry_margin_min": min(margins) if margins else None,
                "entry_margin_max": max(margins) if margins else None,
            }
        if regime is not None:
            cohort_record["market_regime"] = regime
        cohort_records.append(cohort_record)

    cohort_columns = [
        "symbols", "positions", "completed_round_trips", "gross_return", "cost",
        "net_return", "market_return", "net_excess_return", "invested_fraction",
        "cash_fraction", "round_trip_turnover", "winning_trades",
        "entry_margin_min", "entry_margin_max",
    ]
    if not cohort_records:
        cohorts = pd.DataFrame(
            columns=cohort_columns, index=pd.DatetimeIndex([], name="date")
        )
    else:
        cohorts = pd.DataFrame(cohort_records).set_index("date").sort_index()
    trades = pd.DataFrame(trade_records)
    if not trades.empty:
        trades = trades.sort_values(["signal_date", "symbol"]).reset_index(drop=True)
    return cohorts, trades


def performance_metrics(
    returns: pd.Series,
    *,
    periods_per_year: float = 252.0,
) -> dict[str, float | int | None]:
    clean = pd.to_numeric(returns, errors="coerce").dropna()
    if clean.empty:
        return {
            "observations": 0,
            "total_return": None,
            "annualized_return": None,
            "annualized_volatility": None,
            "sharpe": None,
            "max_drawdown": None,
            "win_rate": None,
        }
    equity = (1 + clean).cumprod()
    running_peak = np.maximum.accumulate(
        np.concatenate(([1.0], equity.to_numpy(dtype=float)))
    )[1:]
    drawdown = equity / running_peak - 1
    observations = len(clean)
    total_return = float(equity.iloc[-1] - 1)
    annualized_return = (
        float(equity.iloc[-1] ** (periods_per_year / observations) - 1)
        if equity.iloc[-1] > 0
        else -1.0
    )
    standard_deviation = float(clean.std(ddof=1)) if observations > 1 else 0.0
    sharpe = (
        float(clean.mean() / standard_deviation * math.sqrt(periods_per_year))
        if standard_deviation > 0
        else None
    )
    return {
        "observations": observations,
        "total_return": total_return,
        "annualized_return": annualized_return,
        "annualized_volatility": float(
            standard_deviation * math.sqrt(periods_per_year)
        ),
        "sharpe": sharpe,
        "max_drawdown": float(drawdown.min()),
        "win_rate": float((clean > 0).mean()),
    }


def evaluate_panel_predictions(
    predictions: pd.DataFrame,
    *,
    top_k: int = 5,
    transaction_cost_bps: float = 50.0,
    horizon: int = 20,
    rebalance_every: int | None = None,
    min_symbols_per_date: int = 2,
    entry_margin: float = 0.0,
    entry_margin_column: str | None = "entry_margin",
    rule_selected_column: str | None = "entry_rule_selected",
    cooldown_cohorts: int = 0,
    minimum_holding_sessions: int = 2,
    cost_stress_multipliers: Sequence[float] = (1.0, 1.5, 2.0),
) -> tuple[dict, pd.DataFrame]:
    """Đánh giá Rank IC và chiến lược sparse sau phí.

    ``top_k`` được giữ để tương thích CLI, nhưng mang nghĩa số vị thế tối đa.
    Không có ứng viên vượt cost + margin thì cohort giữ 100% tiền mặt.
    """

    if horizon <= 0:
        raise ValueError("horizon phải > 0.")
    if min_symbols_per_date < max(2, top_k):
        raise ValueError("min_symbols_per_date phải >= max(2, top_k).")
    ic = rank_ic_by_date(
        predictions, min_symbols_per_date=min_symbols_per_date
    )
    ic_std = float(ic.std(ddof=1)) if len(ic) > 1 else 0.0
    hac_lag = max(horizon - 1, 0)
    rank_ic = {
        "observations": int(len(ic)),
        "mean": float(ic.mean()) if len(ic) else None,
        "std": ic_std if len(ic) else None,
        "information_ratio": (
            float(ic.mean() / ic_std) if len(ic) and ic_std > 0 else None
        ),
        "positive_rate": float((ic > 0).mean()) if len(ic) else None,
        "hac_lag": hac_lag,
        "hac_t_stat": _newey_west_t_stat(ic, hac_lag),
    }
    interval = horizon if rebalance_every is None else rebalance_every
    if interval < horizon:
        raise ValueError(
            "rebalance_every nhỏ hơn horizon sẽ tạo forward return chồng lắp."
        )
    execution_prediction_column = (
        "prediction_lower_bound"
        if "prediction_lower_bound" in _as_columns(predictions).columns
        else "prediction"
    )
    backtest, trades = sparse_panel_backtest(
        predictions,
        max_positions=top_k,
        transaction_cost_bps=transaction_cost_bps,
        horizon=horizon,
        minimum_holding_sessions=minimum_holding_sessions,
        rebalance_every=interval,
        min_symbols_per_date=min_symbols_per_date,
        prediction_column=execution_prediction_column,
        entry_margin=entry_margin,
        entry_margin_column=entry_margin_column,
        rule_selected_column=rule_selected_column,
        cooldown_cohorts=cooldown_cohorts,
    )
    backtest.attrs["trade_ledger"] = trades
    annual_periods = 252.0 / interval
    portfolio = performance_metrics(
        backtest.get("net_return", pd.Series(dtype=float)),
        periods_per_year=annual_periods,
    )
    portfolio.update(
        {
            "top_k": top_k,
            "max_positions": top_k,
            "transaction_cost_bps": transaction_cost_bps,
            "cost_convention": "full_round_trip_selected_positions_only",
            "full_round_trip_charged_each_cohort": False,
            "terminal_liquidation_charged": True,
            "rebalance_every": interval,
            "min_symbols_per_date": min_symbols_per_date,
            "entry_rule": "prediction > round_trip_cost + validation_selected_margin",
            "execution_prediction_column": execution_prediction_column,
            "cash_is_default": True,
            "cooldown_cohorts": cooldown_cohorts,
            "completed_round_trips": int(len(trades)),
            "average_holding_sessions": (
                float(trades["holding_sessions"].mean()) if not trades.empty else None
            ),
            "no_trade_cohorts": int(backtest["positions"].eq(0).sum())
            if not backtest.empty
            else 0,
            "no_trade_rate": float(backtest["positions"].eq(0).mean())
            if not backtest.empty
            else None,
            "average_invested_fraction": float(backtest["invested_fraction"].mean())
            if not backtest.empty
            else None,
            "total_cost": float(backtest["cost"].sum())
            if not backtest.empty
            else 0.0,
            "gross_compound_return": (
                float((1 + backtest["gross_return"]).prod() - 1)
                if not backtest.empty
                else None
            ),
            "average_gross_return_per_trade": (
                float(trades["gross_return"].mean()) if not trades.empty else None
            ),
            "average_net_return_per_trade": (
                float(trades["net_return"].mean()) if not trades.empty else None
            ),
            "profit_factor": (
                float(
                    trades.loc[trades["net_return"] > 0, "net_return"].sum()
                    / abs(trades.loc[trades["net_return"] < 0, "net_return"].sum())
                )
                if not trades.empty
                and trades.loc[trades["net_return"] < 0, "net_return"].sum() < 0
                else None
            ),
            "average_turnover": (
                float(backtest["round_trip_turnover"].mean())
                if not backtest.empty
                else None
            ),
            "total_turnover": (
                float(backtest["round_trip_turnover"].sum())
                if not backtest.empty
                else None
            ),
            "annualized_turnover": (
                float(backtest["round_trip_turnover"].mean() * annual_periods)
                if not backtest.empty
                else None
            ),
            "mean_net_excess_return": (
                float(backtest["net_excess_return"].mean())
                if not backtest.empty
                else None
            ),
        }
    )

    stress: dict[str, dict] = {}
    for multiplier in sorted({float(value) for value in cost_stress_multipliers}):
        if multiplier <= 0:
            raise ValueError("Mọi cost stress multiplier phải > 0.")
        stressed = backtest["gross_return"] - backtest["invested_fraction"] * (
            transaction_cost_bps / 10_000
        ) * multiplier
        stress_metrics = performance_metrics(stressed, periods_per_year=annual_periods)
        stress_metrics["multiplier"] = multiplier
        stress_metrics["transaction_cost_bps"] = transaction_cost_bps * multiplier
        stress[f"{multiplier:g}x"] = stress_metrics
    portfolio["cost_stress"] = stress

    regime: dict[str, dict] = {}
    if not backtest.empty and "market_regime" in backtest:
        prediction_frame = _as_columns(predictions)
        regime_by_date = (
            prediction_frame.dropna(subset=["market_regime"])
            .groupby("date")["market_regime"]
            .first()
        )
        for name, group in backtest.groupby("market_regime", dropna=False):
            result = performance_metrics(
                group["net_return"], periods_per_year=annual_periods
            )
            regime_dates = regime_by_date[regime_by_date == name].index
            regime_ic = ic[ic.index.isin(regime_dates)]
            result["rank_ic_observations"] = int(len(regime_ic))
            result["rank_ic_mean"] = (
                float(regime_ic.mean()) if len(regime_ic) else None
            )
            regime[str(name)] = result

    metrics = {
        "rank_ic": rank_ic,
        "sparse_portfolio": portfolio,
        # Backward-compatible alias for database/report consumers.
        "top_k_portfolio": portfolio,
        "by_regime": regime,
    }
    return metrics, backtest
