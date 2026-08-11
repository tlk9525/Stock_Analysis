from __future__ import annotations

import numpy as np
import pandas as pd
import pandas.testing as pdt

from src.panel.data import assemble_price_panel, fetch_price_frames
from src.panel.features import PANEL_MODEL_FEATURES, add_panel_features
from src.panel.news import NEWS_MODEL_FEATURES, add_panel_news_features


def make_history(
    dates: pd.DatetimeIndex,
    *,
    start: float,
    daily_return: float,
) -> pd.DataFrame:
    close = start * np.cumprod(np.full(len(dates), 1 + daily_return))
    return pd.DataFrame(
        {
            "open": close * 0.997,
            "high": close * 1.01,
            "low": close * 0.99,
            "close": close,
            "volume": np.linspace(1_000_000, 2_000_000, len(dates)),
        },
        index=dates,
    )


def test_fetch_and_assemble_accept_injected_frames_without_network() -> None:
    dates = pd.bdate_range("2023-01-02", periods=80)
    frames = {
        "AAA": make_history(dates, start=10, daily_return=0.001),
        "BBB": make_history(dates, start=20, daily_return=0.002),
        "VNINDEX": make_history(dates[1:], start=1000, daily_return=0.0005),
    }

    stocks, benchmark = fetch_price_frames(
        ["aaa", "BBB", "AAA"],
        frames=frames,
    )
    panel = assemble_price_panel(stocks, benchmark)

    assert list(stocks) == ["AAA", "BBB"]
    assert panel.index.names == ["date", "symbol"]
    assert panel.index.get_level_values("date").min() == dates[1]
    assert len(panel) == 2 * (len(dates) - 1)
    for _, daily in panel.reset_index().groupby("date"):
        assert daily["market_close"].nunique() == 1
        assert daily["benchmark_symbol"].eq("VNINDEX").all()


def test_panel_features_are_point_in_time_and_labels_keep_unknown_tail_nan() -> None:
    dates = pd.bdate_range("2022-01-03", periods=130)
    stocks = {
        "AAA": make_history(dates, start=10, daily_return=0.0015),
        "BBB": make_history(dates, start=15, daily_return=-0.0002),
        "CCC": make_history(dates, start=30, daily_return=0.0008),
    }
    benchmark = make_history(dates, start=1000, daily_return=0.0005)
    prices = assemble_price_panel(stocks, benchmark)
    featured = add_panel_features(prices)

    assert set(PANEL_MODEL_FEATURES).issubset(featured.columns)
    expected_stock_return = (
        stocks["AAA"].loc[dates[5], "close"]
        / stocks["AAA"].loc[dates[1], "open"]
        - 1
    )
    expected_market_return = (
        benchmark.loc[dates[5], "close"] / benchmark.loc[dates[1], "open"] - 1
    )
    assert np.isclose(
        featured.loc[(dates[0], "AAA"), "target_return_5d"],
        expected_stock_return,
    )
    assert np.isclose(
        featured.loc[(dates[0], "AAA"), "target_market_return_5d"],
        expected_market_return,
    )
    for _, group in featured.groupby(level="symbol"):
        assert group["target_excess_return_5d"].tail(5).isna().all()
        assert group["target_excess_return_20d"].tail(20).isna().all()
        assert group["target_excess_return_5d"].iloc[-6:].notna().sum() == 1

    cutoff = dates[90]
    changed_stocks = {symbol: frame.copy() for symbol, frame in stocks.items()}
    changed_stocks["AAA"].loc[changed_stocks["AAA"].index > cutoff, "close"] *= 1.5
    changed_stocks["AAA"].loc[changed_stocks["AAA"].index > cutoff, "high"] *= 1.5
    changed = add_panel_features(assemble_price_panel(changed_stocks, benchmark))

    columns = [*PANEL_MODEL_FEATURES, "market_regime"]
    pdt.assert_series_equal(
        featured.loc[(cutoff, "AAA"), columns],
        changed.loc[(cutoff, "AAA"), columns],
        check_names=False,
    )
    assert (
        featured.loc[(cutoff, "AAA"), "target_excess_return_20d"]
        != changed.loc[(cutoff, "AAA"), "target_excess_return_20d"]
    )


def test_panel_news_features_respect_market_close_cutoff() -> None:
    dates = pd.bdate_range("2024-01-02", periods=8)
    stocks = {"AAA": make_history(dates, start=10, daily_return=0.001)}
    benchmark = make_history(dates, start=1000, daily_return=0.0005)
    featured = add_panel_features(
        assemble_price_panel(stocks, benchmark), horizons=[5]
    )
    articles = pd.DataFrame(
        {
            "symbol": ["AAA", "AAA", "AAA"],
            "available_at": [
                "2024-01-02T07:00:00Z",  # before 15:00 local: included on Jan 2
                "2024-01-02T09:00:00Z",  # after 16:00 local: excluded on Jan 2
                "2024-01-03T07:00:00Z",
            ],
            "sentiment_score": [1.0, -1.0, -1.0],
            "sentiment_label": ["positive", "negative", "negative"],
            "event_type": ["earnings", "legal", "legal"],
            "source_name": ["A", "B", "B"],
        }
    )
    enriched = add_panel_news_features(featured, articles, lookback_days=5)

    jan2 = enriched.loc[(pd.Timestamp("2024-01-02"), "AAA")]
    jan3 = enriched.loc[(pd.Timestamp("2024-01-03"), "AAA")]
    assert set(NEWS_MODEL_FEATURES).issubset(enriched.columns)
    assert jan2["news_count_lookback"] == 1
    assert jan2["news_sentiment_mean_lookback"] == 1.0
    assert jan2["news_legal_count_lookback"] == 0
    assert jan3["news_count_lookback"] == 3
    assert jan3["news_negative_count_lookback"] == 2
