from __future__ import annotations

import numpy as np
import pandas as pd
from pandas.tseries.offsets import CustomBusinessDay


def _moving_block_bootstrap(
    returns: np.ndarray,
    simulations: int,
    sessions: int,
    block_size: int,
    random_generator: np.random.Generator,
    drift_shrinkage: float,
) -> np.ndarray:
    """Resample contiguous historical blocks to retain tails and short memory."""

    block_size = max(1, min(block_size, len(returns)))
    block_count = int(np.ceil(sessions / block_size))
    maximum_start = len(returns) - block_size + 1
    starts = random_generator.integers(
        0,
        maximum_start,
        size=(simulations, block_count),
    )
    offsets = np.arange(block_size)
    indices = starts[..., None] + offsets
    sampled = returns[indices].reshape(simulations, -1)[:, :sessions]
    historical_mean = float(np.mean(returns))
    return sampled - historical_mean + historical_mean * drift_shrinkage


def simulate_forecast(frame: pd.DataFrame, config: dict) -> pd.DataFrame:
    sessions = int(config["forecast_sessions"])
    simulations = int(config["simulations"])
    lookback = int(config["lookback_sessions"])
    returns = frame["return_1d"].dropna().tail(lookback)
    latest_close = frame["close"].iloc[-1]
    if len(returns) < 30:
        raise ValueError("Không đủ return để chạy Monte Carlo.")

    random_generator = np.random.default_rng(int(config.get("random_seed", 42)))
    method = str(config.get("monte_carlo_method", "moving_block_bootstrap"))
    drift_shrinkage = float(config.get("monte_carlo_drift_shrinkage", 0.0))
    return_values = returns.to_numpy(dtype=float)
    if method == "moving_block_bootstrap":
        simulated_returns = _moving_block_bootstrap(
            return_values,
            simulations,
            sessions,
            int(config.get("monte_carlo_block_size", 5)),
            random_generator,
            drift_shrinkage,
        )
    elif method == "normal":
        simulated_returns = random_generator.normal(
            loc=float(returns.mean()) * drift_shrinkage,
            scale=float(returns.std()),
            size=(simulations, sessions),
        )
    else:
        raise ValueError(f"Phương pháp Monte Carlo không hợp lệ: {method}")

    simulated_returns = np.clip(simulated_returns, -0.99, None)
    simulated_prices = latest_close * np.cumprod(1 + simulated_returns, axis=1)
    percentiles = np.percentile(simulated_prices, [10, 25, 50, 75, 90], axis=0)
    market_calendar = CustomBusinessDay(
        holidays=pd.to_datetime(config.get("market_holidays", []))
    )
    future_dates = pd.date_range(
        frame.index[-1] + market_calendar,
        periods=sessions,
        freq=market_calendar,
    )
    forecast = pd.DataFrame(
        {
            "p10": percentiles[0],
            "p25": percentiles[1],
            "p50": percentiles[2],
            "p75": percentiles[3],
            "p90": percentiles[4],
        },
        index=future_dates,
    )
    forecast["prob_end_above_latest"] = (
        simulated_prices > latest_close
    ).mean(axis=0)
    forecast["latest_close"] = latest_close
    forecast.attrs["method"] = method
    forecast.attrs["drift_shrinkage"] = drift_shrinkage
    return forecast
