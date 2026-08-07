from __future__ import annotations

import unittest

import pandas as pd

from src.data.news import build_asof_news_features, normalize_news_frame
from src.features.fundamental import summarize_financial_statements


class FundamentalStatementTests(unittest.TestCase):
    def test_summarizes_cash_flow_and_balance_sheet_without_publication_time(self) -> None:
        frames = {
            "income_statement": pd.DataFrame(
                {
                    "item_id": ["net_profit_loss_after_tax", "operating_profit_loss", "interest_expenses"],
                    "2026-Q1": [100.0, 160.0, 20.0],
                }
            ),
            "balance_sheet": pd.DataFrame(
                {
                    "item_id": [
                        "cash_and_cash_equivalents",
                        "short_term_borrowings",
                        "long_term_borrowings",
                        "total_assets",
                        "liabilities",
                        "owners_equity",
                        "accounts_receivable",
                    ],
                    "2026-Q1": [50.0, 20.0, 30.0, 300.0, 120.0, 180.0, 30.0],
                }
            ),
            "cash_flow": pd.DataFrame(
                {
                    "item_id": [
                        "net_cash_inflows_outflows_from_operating_activities",
                        "purchases_of_fixed_assets_and_other_long_term_assets",
                    ],
                    "2026-Q1": [120.0, -25.0],
                }
            ),
        }

        metrics, quality = summarize_financial_statements(frames)
        lookup = {item["metric_name"]: item["metric_value"] for item in metrics}

        self.assertEqual(lookup["free_cash_flow"], 95.0)
        self.assertEqual(lookup["cash_conversion"], 1.2)
        self.assertEqual(lookup["net_debt"], 0.0)
        self.assertAlmostEqual(lookup["interest_coverage"], 8.0)
        self.assertEqual(quality["available_at_status"], "unverified_publication_time")
        self.assertEqual(quality["balance_check_relative_error"], 0.0)


class NewsPointInTimeTests(unittest.TestCase):
    def test_missing_publication_time_is_not_available_for_asof_features(self) -> None:
        raw = pd.DataFrame(
            {
                "news_id": ["1", "2"],
                "news_title": ["FPT: Lợi nhuận tăng", "FPT: thông tin chưa có giờ công bố"],
                "public_date": ["2026-08-07T14:00:00", None],
            }
        )

        articles = normalize_news_frame(
            raw,
            symbol="FPT",
            provider="vnstock:VCI",
            fetched_at=pd.Timestamp("2026-08-07T16:00:00+07:00"),
        )
        self.assertEqual(articles["availability_basis"].tolist(), ["published_at", "unknown"])
        self.assertEqual(int(articles["available_at"].notna().sum()), 1)

        features = build_asof_news_features(
            articles,
            ["2026-08-07T15:00:00+07:00"],
            lookback_days=5,
        )
        self.assertEqual(int(features.iloc[0]["news_count_lookback"]), 1)
        self.assertGreater(float(features.iloc[0]["news_sentiment_mean_lookback"]), 0)

    def test_future_news_is_excluded_at_earlier_cutoff(self) -> None:
        raw = pd.DataFrame(
            {
                "news_id": ["early", "future"],
                "news_title": ["FPT: tăng trưởng", "FPT: xử phạt"],
                "public_date": ["2026-08-07T09:00:00", "2026-08-07T16:00:00"],
            }
        )
        articles = normalize_news_frame(raw, symbol="FPT", provider="vnstock:VCI")

        features = build_asof_news_features(
            articles,
            ["2026-08-07T15:00:00+07:00"],
            lookback_days=1,
        )
        self.assertEqual(int(features.iloc[0]["news_count_lookback"]), 1)
        self.assertEqual(int(features.iloc[0]["news_negative_count_lookback"]), 0)


if __name__ == "__main__":
    unittest.main()
