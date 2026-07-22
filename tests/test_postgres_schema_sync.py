from __future__ import annotations

from datetime import date
import unittest

import pandas as pd

from src.database.postgres import _infer_postgres_type, _missing_column_statements


class PostgresSchemaSyncTests(unittest.TestCase):
    def test_infer_postgres_type_for_new_feature_columns(self) -> None:
        self.assertEqual(_infer_postgres_type(pd.Series([0.1, 0.2])), "DOUBLE PRECISION")
        self.assertEqual(_infer_postgres_type(pd.Series([1, 2], dtype="Int64")), "BIGINT")
        self.assertEqual(_infer_postgres_type(pd.Series([date(2026, 7, 22), None])), "DATE")
        self.assertEqual(_infer_postgres_type(pd.Series(["HCM", "VIC"])), "TEXT")

    def test_missing_column_statements_only_add_unknown_columns(self) -> None:
        frame = pd.DataFrame(
            {
                "run_id": ["r1"],
                "trade_date": [date(2026, 7, 22)],
                "return_2d": [0.02],
                "month_of_year": [7.0],
            }
        )

        statements = _missing_column_statements(
            "history_features",
            frame,
            {"run_id", "trade_date"},
        )

        self.assertEqual(len(statements), 2)
        self.assertIn('ADD COLUMN IF NOT EXISTS "return_2d" DOUBLE PRECISION', statements[0])
        self.assertIn('ADD COLUMN IF NOT EXISTS "month_of_year" DOUBLE PRECISION', statements[1])


if __name__ == "__main__":
    unittest.main()
