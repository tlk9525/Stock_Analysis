from __future__ import annotations

import unittest

import numpy as np
import pandas as pd

from src.features.technical import (
    MARKET_MODEL_FEATURES,
    add_features,
    add_market_features,
    latest_model_features,
)


def _feature_ready_history(rows: int = 100) -> pd.DataFrame:
    position = np.arange(rows, dtype=float)
    close = 100 + 0.08 * position + 2 * np.sin(position / 3)
    open_price = close + 0.25 * np.cos(position / 4)
    return pd.DataFrame(
        {
            "open": open_price,
            "high": np.maximum(open_price, close) + 0.8,
            "low": np.minimum(open_price, close) - 0.8,
            "close": close,
            "volume": 1000 + (position % 17) * 37,
        },
        index=pd.date_range("2025-01-01", periods=rows, freq="B", name="time"),
    )


class TechnicalFeatureTests(unittest.TestCase):
    def test_future_label_and_return_are_unknown_on_latest_row(self) -> None:
        history = pd.DataFrame(
            {
                "open": [10, 11, 10],
                "high": [11, 13, 11],
                "low": [9, 10, 8],
                "close": [10, 12, 9],
                "volume": [1000, 1200, 900],
            },
            index=pd.date_range("2026-01-01", periods=3, name="time"),
        )
        history.attrs["data_quality_report"] = {"cleaned_rows": 3}

        featured = add_features(history)

        self.assertAlmostEqual(featured["next_return"].iloc[0], 12 / 11 - 1)
        self.assertAlmostEqual(featured["next_return"].iloc[1], 9 / 10 - 1)
        self.assertTrue(pd.isna(featured["next_return"].iloc[-1]))
        self.assertEqual(featured["target_next_up"].iloc[0], 1.0)
        self.assertEqual(featured["target_next_up"].iloc[1], 0.0)
        self.assertTrue(pd.isna(featured["target_next_up"].iloc[-1]))
        self.assertEqual(
            featured.attrs["data_quality_report"],
            history.attrs["data_quality_report"],
        )

    def test_latest_model_features_returns_actual_latest_complete_row(self) -> None:
        featured = add_features(_feature_ready_history())

        latest = latest_model_features(featured)

        self.assertEqual(len(latest), 1)
        self.assertEqual(latest.index[0], featured.index[-1])
        self.assertTrue(np.isfinite(latest.to_numpy(dtype=float)).all())

    def test_macd_model_features_are_scale_invariant(self) -> None:
        base = _feature_ready_history()
        scaled = base.copy()
        for column in ["open", "high", "low", "close"]:
            scaled[column] = scaled[column] * 10

        base_featured = add_features(base)
        scaled_featured = add_features(scaled)
        comparable = base_featured[["macd_pct", "macd_hist_pct"]].dropna().index

        np.testing.assert_allclose(
            base_featured.loc[comparable, "macd_pct"],
            scaled_featured.loc[comparable, "macd_pct"],
        )
        np.testing.assert_allclose(
            base_featured.loc[comparable, "macd_hist_pct"],
            scaled_featured.loc[comparable, "macd_hist_pct"],
        )
        self.assertFalse(
            np.allclose(
                base_featured.loc[comparable, "macd"],
                scaled_featured.loc[comparable, "macd"],
            )
        )

    def test_latest_model_features_include_new_lag_calendar_and_moments(self) -> None:
        featured = add_features(_feature_ready_history())

        latest = latest_model_features(featured)

        for column in [
            "return_2d",
            "return_3d",
            "return_10d",
            "return_skew_20d",
            "return_kurtosis_20d",
            "day_of_week",
            "month_of_year",
        ]:
            self.assertIn(column, latest.columns)
            self.assertTrue(np.isfinite(latest.iloc[0][column]))

    def test_market_features_use_only_benchmark_data_available_at_each_date(self) -> None:
        history = _feature_ready_history()
        benchmark = history.copy()
        benchmark["close"] = 200 + np.arange(len(benchmark), dtype=float)
        featured = add_market_features(add_features(history), benchmark)

        changed_future = benchmark.copy()
        changed_future.loc[changed_future.index[-1], "close"] *= 10
        changed = add_market_features(add_features(history), changed_future)

        self.assertTrue(set(MARKET_MODEL_FEATURES).issubset(featured.columns))
        pd.testing.assert_frame_equal(
            featured.loc[featured.index[:-1], MARKET_MODEL_FEATURES],
            changed.loc[changed.index[:-1], MARKET_MODEL_FEATURES],
        )
        self.assertNotEqual(
            featured.iloc[-1]["market_return_1d"],
            changed.iloc[-1]["market_return_1d"],
        )

    def test_latest_model_features_rejects_leakage_and_invalid_features(self) -> None:
        featured = add_features(_feature_ready_history())
        featured.loc[featured.index[-1], "target_next_up"] = 1.0
        with self.assertRaisesRegex(ValueError, "dữ liệu tương lai"):
            latest_model_features(featured)

        featured = add_features(_feature_ready_history())
        featured.loc[featured.index[-1], "rsi_14"] = np.nan
        with self.assertRaisesRegex(ValueError, "rsi_14"):
            latest_model_features(featured)

    def test_latest_model_features_rejects_unsorted_index(self) -> None:
        featured = add_features(_feature_ready_history()).iloc[::-1]
        with self.assertRaisesRegex(ValueError, "sắp xếp tăng dần"):
            latest_model_features(featured)

    def test_quarantine_barrier_does_not_create_a_bridged_next_target(self) -> None:
        history = pd.DataFrame(
            {
                "open": [10.0, 12.0, 13.0],
                "high": [11.0, 13.0, 14.0],
                "low": [9.0, 11.0, 12.0],
                "close": [10.5, 12.5, 13.5],
                "volume": [1000, 1000, 1000],
            },
            index=pd.to_datetime(["2026-01-01", "2026-01-03", "2026-01-04"]),
        )
        history.attrs["data_quality_report"] = {
            "quarantine": [
                {
                    "time": "2026-01-02T00:00:00",
                    "reasons": ["zero_volume"],
                }
            ]
        }

        featured = add_features(history)

        self.assertTrue(pd.isna(featured.loc["2026-01-01", "next_return"]))
        self.assertTrue(pd.isna(featured.loc["2026-01-01", "target_next_up"]))
        self.assertEqual(featured.attrs["targets_invalidated_by_quarantine"], 1)


if __name__ == "__main__":
    unittest.main()
