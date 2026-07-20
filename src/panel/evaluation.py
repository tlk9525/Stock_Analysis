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
) -> tuple[dict, pd.DataFrame]:
    """Đánh giá kỹ năng cross-sectional và top-k có thể đầu tư."""

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
    backtest = top_k_backtest(
        predictions,
        top_k=top_k,
        transaction_cost_bps=transaction_cost_bps,
        rebalance_every=interval,
        min_symbols_per_date=min_symbols_per_date,
    )
    annual_periods = 252.0 / interval
    portfolio = performance_metrics(
        backtest.get("net_return", pd.Series(dtype=float)),
        periods_per_year=annual_periods,
    )
    portfolio.update(
        {
            "top_k": top_k,
            "transaction_cost_bps": transaction_cost_bps,
            "cost_convention": "full_round_trip_each_cohort",
            "full_round_trip_charged_each_cohort": True,
            "terminal_liquidation_charged": True,
            "rebalance_every": interval,
            "min_symbols_per_date": min_symbols_per_date,
            "average_turnover": (
                float(backtest["turnover"].mean()) if not backtest.empty else None
            ),
            "total_turnover": (
                float(backtest["turnover"].sum()) if not backtest.empty else None
            ),
            "average_cost_turnover": (
                float(backtest["cost_turnover"].mean())
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
        "top_k_portfolio": portfolio,
        "by_regime": regime,
    }
    return metrics, backtest
