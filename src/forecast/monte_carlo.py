from __future__ import annotations

import numpy as np
import pandas as pd


def simulate_forecast(frame: pd.DataFrame, config: dict) -> pd.DataFrame:
    sessions = int(config["forecast_sessions"])
    simulations = int(config["simulations"])
    lookback = int(config["lookback_sessions"])
    returns = frame["return_1d"].dropna().tail(lookback)
    latest_close = frame["close"].iloc[-1]
    if len(returns) < 30:
        raise ValueError("Khong du return de chay Monte Carlo.")

    random_generator = np.random.default_rng(int(config.get("random_seed", 42)))
    drift = returns.mean() * 0.35
    volatility = returns.std()
    simulated_returns = random_generator.normal(
        loc=drift,
        scale=volatility,
        size=(simulations, sessions),
    )
    simulated_prices = latest_close * np.cumprod(1 + simulated_returns, axis=1)
    percentiles = np.percentile(simulated_prices, [10, 25, 50, 75, 90], axis=0)
    future_dates = pd.bdate_range(
        frame.index[-1] + pd.Timedelta(days=1),
        periods=sessions,
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
    forecast["prob_end_above_latest"] = float(
        (simulated_prices[:, -1] > latest_close).mean()
    )
    forecast["latest_close"] = latest_close
    return forecast

