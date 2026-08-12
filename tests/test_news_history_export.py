from __future__ import annotations

import json

import pandas as pd

from src.research.news_history import (
    append_news_history,
    export_news_history_from_reports,
    news_reader_snapshot_to_history_frame,
)


def test_export_news_history_from_news_reader_snapshots(tmp_path) -> None:
    reader_dir = tmp_path / "reports" / "MBB" / "2026-08-11_12-03-45"
    reader_dir.mkdir(parents=True)
    (reader_dir / "news_reader.json").write_text(
        json.dumps(
            {
                "mode": "live_research_only",
                "symbol": "MBB",
                "fetched_at": "2026-08-11T05:03:57+00:00",
                "articles": [
                    {
                        "title": "MBB lãi tăng mạnh và trả cổ tức 15%",
                        "publisher": "Test News",
                        "final_url": "https://example.test/mbb",
                        "published_at": "2026-08-04T08:39:02+00:00",
                        "description": "Lợi nhuận tăng trưởng, phát hành cổ phiếu trả cổ tức.",
                    },
                    {
                        "title": "Bài thiếu thời gian bị bỏ qua",
                        "publisher": "Test News",
                    },
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    output_csv = tmp_path / "data" / "news_history.csv"

    frame = export_news_history_from_reports(
        tmp_path / "reports",
        output_csv,
        symbols=["MBB"],
    )

    assert output_csv.exists()
    saved = pd.read_csv(output_csv)
    assert len(frame) == 1
    assert len(saved) == 1
    assert saved.loc[0, "symbol"] == "MBB"
    assert saved.loc[0, "sentiment_label"] == "positive"
    assert saved.loc[0, "event_type"] == "earnings"
    assert saved.loc[0, "snapshot_mode"] == "live_research_only"


def test_news_reader_snapshot_to_history_frame_and_append_dedupe(tmp_path) -> None:
    snapshot = {
        "mode": "live_research_only",
        "symbol": "TCB",
        "fetched_at": "2026-08-11T05:03:57+00:00",
        "articles": [
            {
                "title": "TCB lợi nhuận tăng trưởng",
                "publisher": "Test News",
                "final_url": "https://example.test/tcb",
                "published_at": "2026-08-04T08:39:02+00:00",
                "description": "Lợi nhuận tăng.",
            }
        ],
    }
    frame = news_reader_snapshot_to_history_frame(snapshot)
    output = tmp_path / "news_articles.csv"

    first = append_news_history(output, frame)
    second = append_news_history(output, frame)

    assert len(frame) == 1
    assert len(first) == 1
    assert len(second) == 1
    assert second.loc[0, "symbol"] == "TCB"
