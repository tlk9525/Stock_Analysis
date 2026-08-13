from __future__ import annotations

import unittest

import numpy as np
import pandas as pd

from src.backtest import run_stateful_long_only_backtest
from src.features.technical import MARKET_MODEL_FEATURES, MODEL_FEATURES, add_swing_target
from src.strategy import train_swing_strategy


class SwingTargetTests(unittest.TestCase):
    def test_target_uses_next_open_and_fifth_future_close(self) -> None:
        index = pd.bdate_range("2026-01-05", periods=12)
        frame = pd.DataFrame(
            {
                "open": np.arange(10, 22, dtype=float),
                "close": np.arange(10.5, 22.5, dtype=float),
                "market_open": np.arange(100, 112, dtype=float),
                "market_close": np.arange(100.5, 112.5, dtype=float),
            },
            index=index,
        )

        featured = add_swing_target(frame, horizon_sessions=5)

        self.assertAlmostEqual(featured.loc[index[0], "target_entry_open_5d"], 11.0)
        self.assertAlmostEqual(featured.loc[index[0], "target_exit_close_5d"], 15.5)
        self.assertAlmostEqual(
            featured.loc[index[0], "target_return_5d"], 15.5 / 11.0 - 1
        )
        self.assertTrue(featured["target_excess_return_5d"].tail(5).isna().all())


class StatefulBacktestTests(unittest.TestCase):
    def test_position_cannot_sell_before_minimum_t_plus_two_holding(self) -> None:
        index = pd.bdate_range("2026-01-05", periods=5)
        frame = pd.DataFrame(
            {
                "prediction": [0.02, -0.02, -0.02, -0.02, -0.02],
                "next_open": [10.0] * 5,
                "next_close": [10.1, 10.2, 10.3, 10.4, 10.5],
                "adv": [1_000_000] * 5,
            },
            index=index,
        )

        summary, details = run_stateful_long_only_backtest(
            frame,
            prediction_column="prediction",
            entry_price_column="next_open",
            mark_price_column="next_close",
            volume_column="adv",
            minimum_holding_sessions=2,
            initial_capital=1_000_000,
            price_multiplier=1,
        )

        self.assertEqual(details["action"].tolist()[:3], ["BUY", "HOLD", "SELL"])
        self.assertEqual(summary["completed_round_trips"], 1)
        self.assertEqual(summary["average_holding_sessions"], 2.0)
        with self.assertRaisesRegex(ValueError, r"T\+2"):
            run_stateful_long_only_backtest(
                frame,
                prediction_column="prediction",
                entry_price_column="next_open",
                mark_price_column="next_close",
                minimum_holding_sessions=1,
            )

    def test_fixed_horizon_exits_at_mark_close_not_a_later_score_exit(self) -> None:
        index = pd.bdate_range("2026-01-05", periods=7)
        frame = pd.DataFrame(
            {
                "prediction": [0.02] * 7,
                "next_open": [10.0] * 7,
                "next_close": [10.1, 10.2, 10.3, 10.4, 11.0, 12.0, 13.0],
                "adv": [1_000_000] * 7,
            },
            index=index,
        )

        summary, details = run_stateful_long_only_backtest(
            frame,
            prediction_column="prediction",
            entry_price_column="next_open",
            mark_price_column="next_close",
            volume_column="adv",
            minimum_holding_sessions=2,
            fixed_holding_sessions=4,
            initial_capital=1_000_000,
            price_multiplier=1,
        )

        self.assertEqual(details["action"].tolist()[:5], ["BUY", "HOLD", "HOLD", "HOLD", "SELL"])
        self.assertEqual(summary["completed_round_trips"], 1)
        self.assertEqual(summary["exit_rule"], "fixed close exit after 4 sessions")
        self.assertAlmostEqual(details.attrs["trades"].iloc[0]["exit_price"], 11.0)


class SwingTrainingTests(unittest.TestCase):
    def test_training_reserves_frozen_holdout_and_cost_stress(self) -> None:
        rows = 190
        index = pd.bdate_range("2024-01-02", periods=rows, name="time")
        position = np.arange(rows, dtype=float)
        frame = pd.DataFrame(index=index)
        for number, column in enumerate([*MODEL_FEATURES, *MARKET_MODEL_FEATURES], start=1):
            frame[column] = np.sin(position / (number + 2)) + number * 0.01
        frame["volume"] = 500_000.0
        frame["volume_sma_20"] = 500_000.0
        frame["swing_execution_open"] = 10.0 + position * 0.01
        frame["swing_execution_close"] = frame["swing_execution_open"] * (
            1 + 0.004 * np.sin(position / 3)
        )
        frame["target_excess_return_5d"] = 0.01 * np.sin(position / 3)
        frame.loc[index[-1], "target_excess_return_5d"] = np.nan
        config = {
            "market_features": {"enabled": True},
            "xgboost": {
                "num_boost_round": 8,
                "early_stopping_rounds": 3,
                "max_depth": 2,
                "n_jobs": 1,
            },
            "validation": {
                "min_train_rows": 60,
                "validation_rows": 15,
                "test_rows": 20,
                "step_rows": 20,
                "gap_rows": 1,
                "max_folds": 3,
            },
            "backtest": {
                "commission_bps_per_side": 15,
                "slippage_bps_per_side": 5,
                "sell_tax_bps": 10,
                "price_multiplier": 1,
                "lot_size": 100,
                "max_volume_fraction": 0.01,
            },
            "risk_capital_vnd": 1_000_000,
            "swing_strategy": {
                "enabled": True,
                "horizon_sessions": 5,
                "minimum_holding_sessions": 2,
                "entry_margin_candidates": [0.0, 0.0025],
                "frozen_holdout_rows": 25,
                "min_completed_round_trips": 1,
                "cost_stress_multipliers": [1.0, 1.5, 2.0],
            },
        }

        metrics, oos, latest, booster = train_swing_strategy(frame, config)

        self.assertTrue(metrics["available"])
        self.assertEqual(metrics["validation"]["frozen_holdout_rows"], 25)
        self.assertEqual(metrics["validation"]["gap_rows"], 5)
        self.assertEqual(len(metrics["cost_stress"]), 3)
        self.assertTrue(oos.index.is_monotonic_increasing)
        self.assertIn("expected_excess_return_5d", latest["latest"])
        self.assertEqual(booster.feature_names, [*MODEL_FEATURES, *MARKET_MODEL_FEATURES])


if __name__ == "__main__":
    unittest.main()
