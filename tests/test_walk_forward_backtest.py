from __future__ import annotations

import unittest

import numpy as np
import pandas as pd

from src.backtest import run_long_only_backtest
from src.features.technical import MODEL_FEATURES
from src.models.metrics import binary_metrics, classification_metrics_by_fold
from src.models.xgboost import (
    _split_data,
    build_walk_forward_splits,
    _liquidity_estimate_at_signal,
    resolve_walk_forward_settings,
    train_models,
)


def _model_frame(rows: int = 150) -> pd.DataFrame:
    index = pd.bdate_range("2024-01-02", periods=rows, name="time")
    position = np.arange(rows, dtype=float)
    frame = pd.DataFrame(index=index)
    for feature_number, feature in enumerate(MODEL_FEATURES, start=1):
        frame[feature] = (
            np.sin(position / (feature_number + 2))
            + feature_number * 0.01
            + position * 0.0001
        )
    target = ((np.sin(position / 4) + np.cos(position / 9)) > 0).astype(float)
    frame["target_next_up"] = target
    frame["next_return"] = np.where(target == 1, 0.01, -0.008)
    frame.loc[index[-1], ["target_next_up", "next_return"]] = np.nan
    return frame


class WalkForwardSplitTests(unittest.TestCase):
    def test_expanding_splits_have_two_gaps_and_keep_recent_folds(self) -> None:
        splits, settings = build_walk_forward_splits(
            120,
            {
                "walk_forward": {
                    "min_train_rows": 40,
                    "validation_rows": 10,
                    "test_rows": 15,
                    "gap_rows": 2,
                    "max_folds": 3,
                }
            },
        )

        self.assertEqual(settings["max_folds"], 3)
        self.assertEqual([split["test_start"] for split in splits], [84, 99, 114])
        self.assertEqual(splits[-1]["test_end"], 120)
        self.assertEqual([split["fold"] for split in splits], [1, 2, 3])
        for previous, current in zip(splits, splits[1:]):
            self.assertLessEqual(previous["test_end"], current["test_start"])
            self.assertLess(previous["train_end"], current["train_end"])
        for split in splits:
            self.assertEqual(
                split["validation_start"] - split["train_end"],
                2,
            )
            self.assertEqual(
                split["test_start"] - split["validation_end"],
                2,
            )

    def test_split_uses_real_latest_row_before_dropping_unknown_label(self) -> None:
        frame = _model_frame(100)
        train, validation, test, latest = _split_data(
            frame,
            {
                "walk_forward": {
                    "min_train_rows": 50,
                    "validation_rows": 10,
                    "test_rows": 10,
                    "gap": 1,
                    "max_folds": 2,
                }
            },
        )

        self.assertEqual(latest.index[0], frame.index[-1])
        self.assertNotIn(frame.index[-1], train.index)
        self.assertNotIn(frame.index[-1], validation.index)
        self.assertNotIn(frame.index[-1], test.index)

        stale = frame.copy()
        stale.loc[stale.index[-1], MODEL_FEATURES[0]] = np.nan
        with self.assertRaisesRegex(ValueError, MODEL_FEATURES[0]):
            _split_data(stale)

    def test_walk_forward_alias_priority_and_strict_purge(self) -> None:
        settings = resolve_walk_forward_settings(
            500,
            {
                "validation": {"min_train_rows": 100, "gap_rows": 1},
                "walk_forward": {"min_train_size": 200, "gap": 3},
            },
        )
        self.assertEqual(settings["min_train_rows"], 200)
        self.assertEqual(settings["gap_rows"], 3)

        with self.assertRaisesRegex(ValueError, "gap_rows"):
            resolve_walk_forward_settings(500, {"validation": {"gap_rows": 0}})
        with self.assertRaisesRegex(ValueError, "step_rows"):
            resolve_walk_forward_settings(
                500,
                {"validation": {"test_rows": 20, "step_rows": 30}},
            )


class MetricsTests(unittest.TestCase):
    def test_oos_metrics_are_reported_overall_and_per_fold(self) -> None:
        overall, per_fold = classification_metrics_by_fold(
            [0, 1, 0, 1],
            [0.1, 0.8, 0.7, 0.9],
            [1, 1, 2, 2],
        )

        self.assertEqual(overall["rows"], 4)
        self.assertEqual(len(per_fold), 2)
        self.assertEqual(per_fold[0]["fold"], 1)
        self.assertEqual(per_fold[0]["accuracy"], 1.0)
        self.assertEqual(per_fold[1]["accuracy"], 0.5)

    def test_metrics_reject_fractional_binary_values_before_cast(self) -> None:
        with self.assertRaisesRegex(ValueError, "Nhãn phân lớp"):
            classification_metrics_by_fold(
                [0.9, 1.0],
                [0.1, 0.9],
                [1, 1],
            )
        with self.assertRaisesRegex(ValueError, "Dự báo phân lớp"):
            binary_metrics([0, 1], [0.9, 1.0])


class BacktestTests(unittest.TestCase):
    def test_liquidity_estimate_does_not_use_next_day_volume(self) -> None:
        frame = pd.DataFrame(
            {"volume": [100.0, 100.0, 10_000.0]},
            index=pd.bdate_range("2026-01-05", periods=3),
        )

        estimate = _liquidity_estimate_at_signal(frame)

        self.assertEqual(estimate.iloc[1], 100.0)
        self.assertGreater(estimate.iloc[2], 100.0)

    def test_execution_lag_prevents_same_row_return_and_charges_round_trip(
        self,
    ) -> None:
        frame = pd.DataFrame(
            {
                "signal": [1, 1, 0, 0],
                "future_return": [0.10, 0.20, 0.30, 0.40],
            },
            index=pd.bdate_range("2026-01-05", periods=4),
        )
        summary, details = run_long_only_backtest(
            frame,
            "signal",
            "future_return",
            execution_lag=1,
            round_trip_cost_bps=100,
        )

        self.assertEqual(details["executed_position"].tolist(), [0.0, 1.0, 1.0, 0.0])
        self.assertAlmostEqual(details["transaction_cost"].sum(), 0.01)
        self.assertEqual(summary["entries"], 1)
        self.assertEqual(summary["exits"], 1)
        self.assertEqual(summary["completed_round_trips"], 1)
        self.assertEqual(summary["hit_rate"], 1.0)
        self.assertLess(summary["net_total_return"], summary["gross_total_return"])
        self.assertLessEqual(summary["max_drawdown"], 0.0)

    def test_force_close_charges_exit_for_open_position_at_sample_end(self) -> None:
        frame = pd.DataFrame(
            {"signal": [1, 1, 1], "ret": [0.0, 0.01, 0.01]},
            index=pd.bdate_range("2026-02-02", periods=3),
        )
        summary, details = run_long_only_backtest(
            frame,
            "signal",
            "ret",
            execution_lag=1,
            round_trip_cost_bps=40,
        )

        self.assertTrue(summary["forced_exit"])
        self.assertEqual(summary["exits"], 1)
        self.assertAlmostEqual(details["transaction_cost"].sum(), 0.004)

    def test_intraday_round_trips_respect_lot_and_liquidity_cap(self) -> None:
        frame = pd.DataFrame(
            {
                "signal": [1, 1],
                "next_intraday_return": [0.02, 0.01],
                "next_open": [20.0, 20.0],
                "next_volume": [20_000, 5_000],
            },
            index=pd.bdate_range("2026-03-02", periods=2),
        )
        summary, details = run_long_only_backtest(
            frame,
            "signal",
            "next_intraday_return",
            execution_lag=0,
            round_trip_cost_bps=None,
            entry_cost_bps=20,
            exit_cost_bps=30,
            round_trip_each_signal=True,
            entry_price_column="next_open",
            volume_column="next_volume",
            initial_capital=100_000_000,
            lot_size=100,
            max_volume_fraction=0.01,
            price_multiplier=1000,
        )

        self.assertEqual(details["executed_shares"].tolist(), [200, 0])
        self.assertTrue((details["executed_shares"] % 100 == 0).all())
        self.assertTrue(
            (
                details["executed_shares"]
                <= frame["next_volume"] * summary["max_volume_fraction"]
            ).all()
        )
        self.assertEqual(summary["completed_round_trips"], 1)
        self.assertEqual(summary["entry_cost_bps"], 20)
        self.assertEqual(summary["exit_cost_bps"], 30)
        self.assertEqual(summary["round_trip_cost_bps"], 50)
        self.assertEqual(summary["liquidity_limited_trades"], 2)


class TrainModelsTests(unittest.TestCase):
    def test_train_models_returns_contiguous_oos_and_legacy_keys(self) -> None:
        frame = _model_frame()
        config = {
            "xgboost": {
                "num_boost_round": 8,
                "early_stopping_rounds": 3,
                "max_depth": 2,
                "n_jobs": 1,
            },
            "walk_forward": {
                "min_train_rows": 60,
                "validation_rows": 15,
                "test_rows": 20,
                "gap_rows": 1,
                "max_folds": 3,
            },
            "backtest": {
                "execution_lag": 0,
                "round_trip_cost_bps": 40,
                "signal_threshold": 0.55,
            },
        }

        metrics, scored, latest, booster = train_models(frame, config)

        self.assertTrue(scored.index.is_monotonic_increasing)
        self.assertTrue(scored.index.is_unique)
        self.assertNotIn(frame.index[-1], scored.index)
        self.assertEqual(latest["as_of"], str(frame.index[-1].date()))
        self.assertIn("xgboost", latest)
        self.assertIn("logistic_regression", latest)
        self.assertEqual(metrics["split"]["strategy"], "expanding_walk_forward")
        self.assertEqual(metrics["xgboost"]["rows"], len(scored))
        self.assertEqual(len(metrics["xgboost"]["per_fold"]), 3)
        self.assertEqual(len(metrics["walk_forward"]["folds"]), 3)
        self.assertEqual(metrics["validation"]["scheme"], "expanding_walk_forward")
        self.assertIn("train_logloss_at_best", metrics["xgboost"])
        self.assertIn("validation_logloss_at_best", metrics["xgboost"])
        self.assertGreater(metrics["xgboost"]["scale_pos_weight"], 0)
        self.assertTrue(metrics["backtest"]["available"])
        self.assertEqual(metrics["backtest"]["execution_lag_sessions"], 0)
        self.assertEqual(metrics["xgboost"]["threshold"], 0.55)
        self.assertEqual(
            metrics["backtest"]["total_return"],
            metrics["backtest"]["net_total_return"],
        )
        self.assertEqual(
            metrics["backtest"]["sharpe"],
            metrics["backtest"]["sharpe_ratio"],
        )
        self.assertEqual(booster.feature_names, MODEL_FEATURES)


if __name__ == "__main__":
    unittest.main()
