from __future__ import annotations

import math
import re
from collections.abc import Sequence

import numpy as np
import pandas as pd

from src.features.technical import MODEL_FEATURES, add_features


DEFAULT_HORIZONS = (5, 20)
MARKET_FEATURES = [
    "market_return_1d",
    "market_return_5d",
    "market_return_20d",
    "market_volatility_20d",
    "excess_return_1d",
    "excess_return_5d",
    "excess_return_20d",
    "relative_strength_20d",
    "beta_60d",
    "corr_60d",
]
PANEL_MODEL_FEATURES = [*MODEL_FEATURES, *MARKET_FEATURES]


def target_horizon(target_column: str) -> int:
    """Extract the session horizon from a target such as ``..._20d``."""

    match = re.search(r"_(\d+)d$", target_column)
    if not match:
        raise ValueError(
            f"Không suy ra được horizon từ target '{target_column}'. "
            "Tên target phải kết thúc bằng _Nd."
        )
    return int(match.group(1))


def _as_columns(panel: pd.DataFrame) -> pd.DataFrame:
    if isinstance(panel.index, pd.MultiIndex) and {"date", "symbol"}.issubset(
        panel.index.names
    ):
        out = panel.reset_index()
    else:
        out = panel.copy()
    missing = {"date", "symbol", "open", "high", "low", "close", "volume", "market_close"} - set(
        out.columns
    )
    if missing:
        raise ValueError(f"Panel thiếu cột: {', '.join(sorted(missing))}")
    out["date"] = pd.to_datetime(out["date"]).dt.tz_localize(None)
    out["symbol"] = out["symbol"].astype(str).str.upper()
    return out.sort_values(["symbol", "date"]).drop_duplicates(
        ["date", "symbol"], keep="last"
    )


def _market_features(panel: pd.DataFrame) -> pd.DataFrame:
    market = (
        panel.sort_values("date")
        .drop_duplicates("date", keep="last")
        .set_index("date")[["market_open", "market_close"]]
    )
    for horizon in (1, 5, 20):
        market[f"market_return_{horizon}d"] = market["market_close"].pct_change(
            horizon, fill_method=None
        )
    market["market_volatility_20d"] = (
        market["market_return_1d"].rolling(20).std() * math.sqrt(252)
    )
    market["market_regime"] = np.select(
        [market["market_return_20d"] > 0.03, market["market_return_20d"] < -0.03],
        ["bull", "bear"],
        default="sideways",
    )
    market.loc[market["market_return_20d"].isna(), "market_regime"] = "unknown"
    return market


def _future_value_on_market_calendar(
    values: pd.Series,
    market_dates: pd.DatetimeIndex,
    horizon: int,
) -> pd.Series:
    """Look up a symbol value exactly ``horizon`` benchmark sessions ahead."""

    future_dates = pd.Series(market_dates, index=market_dates).shift(-horizon)
    requested_dates = future_dates.reindex(values.index)
    looked_up = requested_dates.map(values)
    looked_up.index = values.index
    return looked_up


def add_panel_features(
    price_panel: pd.DataFrame,
    *,
    horizons: Sequence[int] = DEFAULT_HORIZONS,
    beta_window: int = 60,
) -> pd.DataFrame:
    """Create leakage-safe stock, market and cross-asset panel features.

    Feature columns at date *t* only use observations up to the close of *t*.
    A tradable target enters at the open of benchmark session *t+1* and exits
    at the close of session *t+h*. Future values are confined to explicit
    ``target_*`` columns, whose last ``h`` rows remain missing.
    """

    if beta_window < 2:
        raise ValueError("beta_window phải >= 2.")
    clean_horizons = tuple(sorted({int(value) for value in horizons}))
    if not clean_horizons or any(value <= 0 for value in clean_horizons):
        raise ValueError("horizons phải chứa số phiên dương.")

    panel = _as_columns(price_panel)
    market = _market_features(panel)
    outputs: list[pd.DataFrame] = []

    passthrough_market = [
        column
        for column in panel.columns
        if column.startswith("market_") and column != "market_close"
    ]
    passthrough = ["benchmark_symbol", *passthrough_market]

    for symbol, symbol_rows in panel.groupby("symbol", sort=True):
        rows = symbol_rows.sort_values("date").set_index("date")
        technical_input = rows[["open", "high", "low", "close", "volume"]]
        featured = add_features(technical_input).drop(
            columns=["target_next_up", "next_return"], errors="ignore"
        )
        featured["symbol"] = symbol
        for column in passthrough:
            if column in rows.columns:
                featured[column] = rows[column]

        featured = featured.join(
            market.drop(columns=["market_open", "market_close"]),
            how="left",
        )
        featured["market_close"] = rows["market_close"]
        featured["excess_return_1d"] = (
            featured["return_1d"] - featured["market_return_1d"]
        )
        featured["excess_return_5d"] = (
            featured["return_5d"] - featured["market_return_5d"]
        )
        featured["excess_return_20d"] = (
            featured["return_20d"] - featured["market_return_20d"]
        )
        featured["relative_strength_20d"] = (
            (1 + featured["return_20d"])
            / (1 + featured["market_return_20d"])
            - 1
        )
        rolling_market_variance = featured["market_return_1d"].rolling(
            beta_window
        ).var()
        rolling_covariance = featured["return_1d"].rolling(beta_window).cov(
            featured["market_return_1d"]
        )
        featured["beta_60d"] = rolling_covariance / rolling_market_variance.replace(
            0, np.nan
        )
        featured["corr_60d"] = featured["return_1d"].rolling(beta_window).corr(
            featured["market_return_1d"]
        )

        for horizon in clean_horizons:
            next_open = _future_value_on_market_calendar(
                featured["open"], market.index, 1
            )
            future_close = _future_value_on_market_calendar(
                featured["close"], market.index, horizon
            )
            next_market_open = market["market_open"].shift(-1).reindex(
                featured.index
            )
            future_market_close = market["market_close"].shift(-horizon).reindex(
                featured.index
            )
            future_return = future_close / next_open - 1
            future_market_return = future_market_close / next_market_open - 1
            featured[f"target_entry_open_{horizon}d"] = next_open
            featured[f"target_exit_close_{horizon}d"] = future_close
            featured[f"target_return_{horizon}d"] = future_return
            featured[f"target_market_return_{horizon}d"] = future_market_return
            featured[f"target_excess_return_{horizon}d"] = (
                future_return - future_market_return
            )

        outputs.append(featured.reset_index())

    result = pd.concat(outputs, ignore_index=True)
    return result.set_index(["date", "symbol"]).sort_index()


def model_frame(
    featured_panel: pd.DataFrame,
    target: str = "target_excess_return_20d",
    feature_columns: Sequence[str] = PANEL_MODEL_FEATURES,
) -> pd.DataFrame:
    """Return fully observed training rows while preserving panel identifiers."""

    required = [*feature_columns, target]
    missing = [column for column in required if column not in featured_panel.columns]
    if missing:
        raise ValueError(f"Feature panel thiếu cột: {', '.join(missing)}")
    return featured_panel.dropna(subset=required).copy()
