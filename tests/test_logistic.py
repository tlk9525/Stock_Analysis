from __future__ import annotations

import unittest

import numpy as np
import pandas as pd

from src.models.logistic import fit_logistic


class LogisticModelTests(unittest.TestCase):
    def test_l2_regularization_shrinks_non_bias_weights(self) -> None:
        signal = np.tile(np.array([-2.0, -1.0, 1.0, 2.0]), 60)
        noise = np.sin(np.arange(len(signal)) / 5)
        features = pd.DataFrame({"signal": signal, "noise": noise})
        labels = pd.Series((signal > 0).astype(float))

        without_regularization = fit_logistic(
            features,
            labels,
            iterations=3000,
            learning_rate=0.05,
            l2=0.0,
        )
        with_regularization = fit_logistic(
            features,
            labels,
            iterations=3000,
            learning_rate=0.05,
            l2=0.1,
        )

        self.assertLess(
            np.linalg.norm(with_regularization["weights"][1:]),
            np.linalg.norm(without_regularization["weights"][1:]),
        )


if __name__ == "__main__":
    unittest.main()
