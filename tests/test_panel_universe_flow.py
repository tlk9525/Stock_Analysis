from __future__ import annotations

import numpy as np
import pandas as pd

from src.panel.data import assemble_price_panel
from src.panel.features import add_panel_features
from src.panel.flows import FLOW_MODEL_FEATURES, add_foreign_flow_features
from src.panel.universe import (
    apply_point_in_time_eligibility,
    normalize_universe_registry,
    point_in_time_symbols,
)


def _history(dates: pd.DatetimeIndex, price: float, volume: float = 1_000_000) -> pd.DataFrame:
    close = price * np.cumprod(np.full(len(dates), 1.001))
    return pd.DataFrame(
        {
            "open": close * 0.999,
            "high": close * 1.01,
            "low": close * 0.99,
            "close": close,
            "volume": volume,
        },
        index=dates,
    )


def test_point_in_time_universe_excludes_future_and_delisted_symbols() -> None:
    registry = normalize_universe_registry(
        pd.DataFrame(
            {
                "symbol": ["AAA", "BBB", "CCC"],
                "exchange": ["HOSE", "HNX", "UPCOM"],
                "listed_at": ["2020-01-01", "2025-01-01", "2020-01-01"],
                "delisted_at": [None, None, "2023-01-01"],
                "available_at": ["2020-01-01", "2025-01-01", "2020-01-01"],
                "status": ["active", "active", "delisted"],
            }
        )
    )
    assert point_in_time_symbols(registry, "2024-01-01") == ["AAA"]
    assert point_in_time_symbols(registry, "2022-12-30") == ["AAA", "CCC"]

    dates = pd.bdate_range("2022-12-29", periods=5)
    panel = assemble_price_panel(
        {"AAA": _history(dates, 10), "CCC": _history(dates, 20)},
        _history(dates, 1000),
        universe_registry=registry,
    )
    eligible = apply_point_in_time_eligibility(panel, registry)
    assert (pd.Timestamp("2023-01-02"), "CCC") not in eligible.index
    assert (pd.Timestamp("2022-12-30"), "CCC") in eligible.index


def test_liquidity_breadth_net_targets_and_tradability_are_materialized() -> None:
    dates = pd.bdate_range("2022-01-03", periods=280)
    stocks = {
        "AAA": _history(dates, 20, 2_000_000),
        "BBB": _history(dates, 10, 100),
    }
    registry = pd.DataFrame(
        {"symbol": ["AAA", "BBB"], "sector": ["bank", "bank"]}
    )
    panel = assemble_price_panel(
        stocks,
        _history(dates, 1000, 10_000_000),
        universe_registry=registry,
    )
    featured = add_panel_features(panel, horizons=[5, 10, 20])
    latest = featured.xs(dates[-21], level="date")
    assert bool(latest.loc["AAA", "is_tradable"])
    assert not bool(latest.loc["BBB", "is_tradable"])
    assert latest.loc["BBB", "estimated_round_trip_cost"] > latest.loc["AAA", "estimated_round_trip_cost"]
    assert np.isclose(
        latest.loc["AAA", "target_net_excess_return_5d"],
        latest.loc["AAA", "target_excess_return_5d"]
        - latest.loc["AAA", "estimated_round_trip_cost"],
    )
    assert featured["market_breadth_advance_ratio"].dropna().between(0, 1).all()


def test_foreign_flow_respects_available_at_and_does_not_impute_missing() -> None:
    dates = pd.bdate_range("2024-01-02", periods=80)
    panel = assemble_price_panel(
        {"AAA": _history(dates, 10)}, _history(dates, 1000)
    )
    featured = add_panel_features(panel, horizons=[5])
    flows = pd.DataFrame(
        {
            "symbol": ["AAA", "AAA"],
            "date": ["2024-01-02", "2024-01-03"],
            "available_at": ["2024-01-02T07:00:00Z", "2024-01-03T09:00:00Z"],
            "foreign_buy_value": [200.0, 999.0],
            "foreign_sell_value": [50.0, 0.0],
        }
    )
    enriched = add_foreign_flow_features(featured, flows)
    assert enriched.loc[(dates[0], "AAA"), "foreign_net_value_1d"] == 150.0
    assert pd.isna(enriched.loc[(dates[1], "AAA"), "foreign_net_value_1d"])
    assert set(FLOW_MODEL_FEATURES).issubset(enriched.columns)
