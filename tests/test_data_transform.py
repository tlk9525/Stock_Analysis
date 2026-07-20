from __future__ import annotations

import unittest

import pandas as pd

from src.data.transform import clean_history


class CleanHistoryTests(unittest.TestCase):
    def test_quarantines_invalid_ohlcv_and_reports_reasons(self) -> None:
        raw = pd.DataFrame(
            [
                ["2026-01-01", 10, 11, 9, 10.5, 1000],
                ["2026-01-02", 10, 9.5, 9, 9.3, 1000],
                ["2026-01-03", 10, 12, 10.8, 10.5, 1000],
                ["2026-01-04", 0, 11, 9, 10, 1000],
                ["2026-01-05", 10, 11, 9, 10, -1],
                ["2026-01-06", 10, 11, 9, 10, 0],
                ["2026-01-07", 10, 11, 9, "bad", 1000],
                ["2026-01-08", 11, 12, 10, 11.5, 2000],
            ],
            columns=["time", "open", "high", "low", "close", "volume"],
        )

        cleaned = clean_history(raw, "hcm")

        self.assertEqual(
            list(cleaned.index),
            [pd.Timestamp("2026-01-01"), pd.Timestamp("2026-01-08")],
        )
        report = cleaned.attrs["data_quality_report"]
        self.assertEqual(report["symbol"], "HCM")
        self.assertEqual(report["source_rows"], 8)
        self.assertEqual(report["cleaned_rows"], 2)
        self.assertEqual(report["quarantined_rows"], 6)
        self.assertEqual(report["zero_volume_policy"], "quarantine")
        self.assertEqual(report["reason_counts"]["zero_volume"], 1)
        self.assertEqual(report["reason_counts"]["negative_volume"], 1)
        self.assertEqual(report["reason_counts"]["non_positive_price"], 1)
        self.assertEqual(
            report["reason_counts"]["missing_or_non_finite_ohlcv"],
            1,
        )
        quarantined_reasons = {
            reason for record in report["quarantine"] for reason in record["reasons"]
        }
        self.assertIn("high_below_open_or_close", quarantined_reasons)
        self.assertIn("low_above_open_or_close", quarantined_reasons)

    def test_invalid_time_and_duplicate_are_quarantined(self) -> None:
        raw = pd.DataFrame(
            [
                ["2026-99-99", 10, 11, 9, 10, 1000],
                ["2026-01-02", 10, 11, 9, 10, 1000],
                ["2026-01-01", 8, 9, 7, 8, 800],
                ["2026-01-02", 20, 21, 19, 20, 2000],
            ],
            columns=["time", "open", "high", "low", "close", "volume"],
        )

        cleaned = clean_history(raw, "TCB")

        self.assertTrue(cleaned.index.is_monotonic_increasing)
        self.assertTrue(cleaned.index.is_unique)
        self.assertEqual(cleaned.loc[pd.Timestamp("2026-01-02"), "open"], 20)
        report = cleaned.attrs["data_quality_report"]
        self.assertEqual(report["source_rows"], 4)
        self.assertEqual(report["cleaned_rows"], 2)
        self.assertEqual(report["quarantined_rows"], 2)
        self.assertEqual(report["reason_counts"]["invalid_time"], 1)
        self.assertEqual(report["reason_counts"]["duplicate_time"], 1)

    def test_rejects_missing_columns_or_fully_invalid_data(self) -> None:
        missing_volume = pd.DataFrame(
            {
                "time": ["2026-01-01"],
                "open": [10],
                "high": [11],
                "low": [9],
                "close": [10],
            }
        )
        with self.assertRaisesRegex(ValueError, "volume"):
            clean_history(missing_volume, "FPT")

        zero_volume_only = pd.DataFrame(
            [["2026-01-01", 10, 11, 9, 10, 0]],
            columns=["time", "open", "high", "low", "close", "volume"],
        )
        with self.assertRaisesRegex(ValueError, "Không có dòng giá hợp lệ"):
            clean_history(zero_volume_only, "FPT")


if __name__ == "__main__":
    unittest.main()
