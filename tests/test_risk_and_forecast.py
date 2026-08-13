from __future__ import annotations

import unittest

import numpy as np
import pandas as pd

from src.forecast.monte_carlo import simulate_forecast
from src.risk.decision import build_signal_decision, enforce_signal_decision
from src.risk.management import build_risk_plan


class RiskPlanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.levels = {
            "latest_close": 100.0,
            "atr14": 2.0,
            "support20": 95.0,
            "sma60": 90.0,
            "resistance20": 120.0,
            "volume20": 100_000.0,
        }
        index = pd.date_range("2026-01-01", periods=5, freq="B")
        self.forecast = pd.DataFrame(
            {
                "p50": [101, 103, 105, 108, 110],
                "p90": [104, 108, 112, 120, 125],
            },
            index=index,
        )
        self.config = {
            "risk_per_trade_pct": 0.01,
            "risk_capital_vnd": 100_000_000,
            "atr_stop_multiplier": 1.5,
            "min_reward_risk": 1.5,
            "backtest": {
                "lot_size": 100,
                "max_volume_fraction": 0.01,
                "commission_bps_per_side": 15,
                "sell_tax_bps": 10,
                "slippage_bps_per_side": 5,
            },
        }

    def test_position_is_rounded_and_requires_reward_risk(self) -> None:
        plan = build_risk_plan(self.levels, self.forecast, self.config)
        self.assertEqual(plan["stop_loss"], 97.0)
        self.assertEqual(plan["target_1"], 110.0)
        self.assertEqual(plan["position_shares"], 200)
        self.assertGreaterEqual(plan["reward_risk"], 1.5)

    def test_close_target_is_rejected(self) -> None:
        forecast = self.forecast.copy()
        forecast.loc[:, "p50"] = 101.0
        forecast.loc[:, "p90"] = 102.0
        levels = dict(self.levels, resistance20=102.0)
        plan = build_risk_plan(levels, forecast, self.config)
        self.assertIsNone(plan["target_1"])
        self.assertIsNone(plan["position_shares"])

    def test_price_multiplier_can_be_set_for_absolute_vnd_prices(self) -> None:
        levels = {
            "latest_close": 25_500.0,
            "atr14": 500.0,
            "support20": 25_000.0,
            "sma60": 24_000.0,
            "resistance20": 28_000.0,
            "volume20": 1_000_000.0,
        }
        config = {
            **self.config,
            "backtest": {**self.config["backtest"], "price_multiplier": 1},
        }

        plan = build_risk_plan(levels, self.forecast, config)

        self.assertEqual(plan["price_multiplier"], 1.0)
        self.assertEqual(plan["position_shares"], 1100)
        self.assertLess(plan["position_value_vnd"], config["risk_capital_vnd"])

    def test_publish_guard_clears_position_when_model_has_no_edge(self) -> None:
        plan = build_risk_plan(self.levels, self.forecast, self.config)
        metrics = {
            "xgboost": {"roc_auc": 0.51, "balanced_accuracy": 0.51},
        }
        decision = build_signal_decision(
            metrics,
            {"xgboost": 0.60},
            {"score": 5},
            plan,
            str(pd.Timestamp.today().date()),
            self.config,
        )
        guarded = enforce_signal_decision(plan, decision)
        self.assertEqual(decision["status"], "NO_EDGE")
        self.assertIsNone(guarded["position_shares"])

    def test_publish_guard_rejects_negative_cost_aware_backtest(self) -> None:
        plan = build_risk_plan(self.levels, self.forecast, self.config)
        metrics = {
            "xgboost": {"roc_auc": 0.62, "balanced_accuracy": 0.58},
            "backtest": {
                "available": True,
                "observations": 252,
                "completed_round_trips": 30,
                "net_total_return": -0.08,
                "sharpe_ratio": -0.4,
            },
        }

        decision = build_signal_decision(
            metrics,
            {"xgboost": 0.62},
            {"score": 5},
            plan,
            str(pd.Timestamp.today().date()),
            self.config,
        )

        self.assertEqual(decision["status"], "NO_EDGE")
        self.assertFalse(decision["checks"]["backtest_net_edge"])

    def test_publish_guard_allows_only_a_positive_oos_edge(self) -> None:
        plan = build_risk_plan(self.levels, self.forecast, self.config)
        metrics = {
            "xgboost": {"roc_auc": 0.62, "balanced_accuracy": 0.58},
            "logistic_baseline": {"roc_auc": 0.55},
            "backtest": {
                "available": True,
                "observations": 252,
                "completed_round_trips": 30,
                "net_total_return": 0.12,
                "sharpe_ratio": 0.8,
            },
        }

        decision = build_signal_decision(
            metrics,
            {"xgboost": 0.62},
            {"score": 5},
            plan,
            str(pd.Timestamp.today().date()),
            self.config,
        )

        self.assertEqual(decision["status"], "ACTIONABLE")
        self.assertTrue(all(decision["checks"].values()))

    def test_near_threshold_candidate_is_watch_without_position(self) -> None:
        plan = build_risk_plan(self.levels, self.forecast, self.config)
        metrics = {
            "xgboost": {"roc_auc": 0.521, "balanced_accuracy": 0.53},
            "logistic_baseline": {"roc_auc": 0.51},
            "backtest": {
                "available": True,
                "observations": 252,
                "completed_round_trips": 30,
                "net_total_return": 0.12,
                "sharpe_ratio": 0.8,
            },
        }
        config = {
            **self.config,
            "signal_guard": {
                "enable_near_threshold_watch": True,
                "max_auc_shortfall_for_watch": 0.02,
                "max_balanced_accuracy_shortfall_for_watch": 0.01,
                "max_probability_shortfall_for_watch": 0.02,
            },
        }

        decision = build_signal_decision(
            metrics,
            {"xgboost": 0.535},
            {"score": 5},
            plan,
            str(pd.Timestamp.today().date()),
            config,
        )
        guarded = enforce_signal_decision(plan, decision)

        self.assertEqual(decision["status"], "WATCH")
        self.assertEqual(decision["direction"], "NONE")
        self.assertEqual(decision["failed_checks"], ["model_auc", "probability_edge"])
        self.assertIsNone(guarded["position_shares"])

    def test_swing_contract_ignores_positive_legacy_classifier_when_holdout_is_empty(self) -> None:
        plan = build_risk_plan(self.levels, self.forecast, self.config)
        config = {
            **self.config,
            "swing_strategy": {
                "enabled": True,
                "min_completed_round_trips": 10,
            },
        }
        metrics = {
            # These legacy metrics must not turn a 5D strategy actionable.
            "xgboost": {"roc_auc": 0.99, "balanced_accuracy": 0.99},
            "backtest": {
                "available": True,
                "observations": 999,
                "completed_round_trips": 99,
                "net_total_return": 0.99,
                "sharpe_ratio": 9.0,
            },
            "swing_strategy": {
                "available": True,
                "selected_entry_margin": 0.005,
                "latest_expected_excess_return": 0.02,
                "development_oos": {"backtest": {"completed_round_trips": 1}},
                "frozen_holdout": {
                    "backtest": {
                        "completed_round_trips": 0,
                        "round_trip_cost_bps": 50,
                    }
                },
                "publish_gate": {
                    "margin_selected_in_validation": False,
                    "development_sufficient_trades": False,
                    "sufficient_trades": False,
                    "development_ranking_edge": False,
                    "frozen_ranking_edge": False,
                    "net_edge": False,
                    "cost_stress_1_5x": False,
                },
            },
        }

        decision = build_signal_decision(
            metrics,
            {"xgboost": 0.99},
            {"score": 5},
            plan,
            str(pd.Timestamp.today().date()),
            config,
        )

        self.assertEqual(decision["status"], "NO_EDGE")
        self.assertEqual(decision["execution_contract"], "fixed_horizon_swing_5d")
        self.assertFalse(decision["checks"]["swing_frozen_holdout"])


class MonteCarloTests(unittest.TestCase):
    def test_block_bootstrap_is_reproducible_and_uses_market_holidays(self) -> None:
        index = pd.bdate_range("2025-08-01", periods=120)
        returns = np.tile([0.01, -0.005, 0.002, -0.003], 30)
        close = 100 * np.cumprod(1 + returns)
        frame = pd.DataFrame({"close": close, "return_1d": returns}, index=index)
        next_business_day = pd.bdate_range(index[-1] + pd.Timedelta(days=1), periods=1)[0]
        config = {
            "forecast_sessions": 10,
            "simulations": 500,
            "lookback_sessions": 100,
            "random_seed": 7,
            "monte_carlo_method": "moving_block_bootstrap",
            "monte_carlo_block_size": 4,
            "monte_carlo_drift_shrinkage": 0.0,
            "market_holidays": [str(next_business_day.date())],
        }
        first = simulate_forecast(frame, config)
        second = simulate_forecast(frame, config)
        pd.testing.assert_frame_equal(first, second)
        self.assertNotIn(next_business_day, first.index)
        self.assertEqual(first.attrs["method"], "moving_block_bootstrap")
        self.assertTrue(first["prob_end_above_latest"].between(0, 1).all())

    def test_forecast_uses_default_vietnam_market_holidays(self) -> None:
        index = pd.bdate_range("2026-07-06", periods=40)
        returns = np.tile([0.01, -0.005, 0.002, -0.003], 10)
        close = 100 * np.cumprod(1 + returns)
        frame = pd.DataFrame({"close": close, "return_1d": returns}, index=index)
        config = {
            "forecast_sessions": 8,
            "simulations": 200,
            "lookback_sessions": 40,
            "random_seed": 7,
            "monte_carlo_method": "moving_block_bootstrap",
            "monte_carlo_block_size": 4,
            "monte_carlo_drift_shrinkage": 0.0,
        }

        forecast = simulate_forecast(frame, config)

        self.assertNotIn(pd.Timestamp("2026-08-31"), forecast.index)
        self.assertNotIn(pd.Timestamp("2026-09-01"), forecast.index)
        self.assertNotIn(pd.Timestamp("2026-09-02"), forecast.index)
        self.assertTrue((forecast.index.dayofweek < 5).all())
        self.assertIn("Thứ Bảy/Chủ Nhật", forecast.attrs["market_calendar_note"])


if __name__ == "__main__":
    unittest.main()
