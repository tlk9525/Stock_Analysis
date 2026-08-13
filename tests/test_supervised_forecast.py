from __future__ import annotations

import unittest

import numpy as np
import pandas as pd

from src.features.technical import MARKET_MODEL_FEATURES, MODEL_FEATURES, add_swing_target
from src.forecast.supervised import train_supervised_forecast
from src.reports.dashboard import _interactive_forecast_markup


class SupervisedForecastTests(unittest.TestCase):
    def _frame(self) -> pd.DataFrame:
        rng = np.random.default_rng(7)
        index = pd.bdate_range("2020-01-02", periods=520)
        stock_return = rng.normal(0.0005, 0.012, len(index))
        market_return = rng.normal(0.0003, 0.009, len(index))
        close = 50 * np.cumprod(1 + stock_return)
        market_close = 1000 * np.cumprod(1 + market_return)
        frame = pd.DataFrame(
            {
                "open": close * (1 + rng.normal(0, 0.002, len(index))),
                "close": close,
                "market_open": market_close * (1 + rng.normal(0, 0.001, len(index))),
                "market_close": market_close,
            },
            index=index,
        )
        for offset, feature in enumerate([*MODEL_FEATURES, *MARKET_MODEL_FEATURES]):
            frame[feature] = rng.normal(offset * 0.001, 1.0, len(index))
        frame = add_swing_target(frame, horizon_sessions=5)
        frame = add_swing_target(frame, horizon_sessions=10)
        return frame

    def test_quantile_forecast_has_calibrated_bands_and_direct_anchors(self) -> None:
        config = {
            "forecast_sessions": 10,
            "market_weekmask": "Mon Tue Wed Thu Fri",
            "market_holidays": [],
            "market_features": {"enabled": True},
            "xgboost": {
                "num_boost_round": 8,
                "early_stopping_rounds": 3,
                "max_depth": 2,
                "n_jobs": 1,
                "random_state": 11,
            },
            "forecast_model": {
                "horizons": [5, 10],
                "minimum_train_rows": 200,
                "validation_rows": 40,
                "frozen_holdout_rows": 80,
                "minimum_frozen_rows": 40,
                "conformal_coverage": 0.80,
                "num_boost_round": 8,
                "early_stopping_rounds": 3,
            },
        }
        forecast, metrics, models = train_supervised_forecast(self._frame(), config)

        self.assertEqual(len(forecast), 10)
        self.assertTrue((forecast["p10"] <= forecast["p50"]).all())
        self.assertTrue((forecast["p50"] <= forecast["p90"]).all())
        self.assertEqual(int(forecast["is_model_anchor"].sum()), 2)
        self.assertEqual(set(models), {5, 10})
        self.assertEqual(metrics["method"], "xgboost_direct_quantile_conformal")
        self.assertIn("baselines", metrics["by_horizon"]["5"])

        markup, scripts = _interactive_forecast_markup(forecast, "TEST")
        self.assertIn('id="future-forecast-canvas"', markup)
        self.assertIn("data-forecast-range=\"10\"", markup)
        self.assertIn('id="future-forecast-data"', scripts)


if __name__ == "__main__":
    unittest.main()
