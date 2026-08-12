from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import pandas as pd

from src.data.news import _event_type, _sentiment
from src.research.live_web import fetch_live_research, read_live_articles


NEWS_HISTORY_COLUMNS = [
    "symbol",
    "available_at",
    "published_at",
    "sentiment_score",
    "sentiment_label",
    "event_type",
    "source_name",
    "title",
    "source_url",
    "fetched_at",
    "analysis_method",
    "snapshot_mode",
]


def _normalize_symbols(symbols: Iterable[str] | None) -> set[str] | None:
    if symbols is None:
        return None
    normalized = {str(symbol).strip().upper() for symbol in symbols if str(symbol).strip()}
    return normalized or None


def news_reader_snapshot_to_history_frame(snapshot: dict) -> pd.DataFrame:
    rows: list[dict] = []
    symbol = str(snapshot.get("symbol") or "").strip().upper()
    snapshot_mode = str(snapshot.get("mode") or "unknown")
    snapshot_fetched_at = snapshot.get("fetched_at") or snapshot.get("source_snapshot_fetched_at")
    for article in snapshot.get("articles", []) or []:
        published_at = article.get("published_at")
        if not symbol or not published_at:
            continue
        title = str(article.get("title") or "").strip()
        excerpt = str(article.get("description") or article.get("content_excerpt") or "").strip()
        text = " ".join(value for value in [title, excerpt] if value)
        score, label = _sentiment(text)
        rows.append(
            {
                "symbol": symbol,
                "available_at": published_at,
                "published_at": published_at,
                "sentiment_score": score,
                "sentiment_label": label,
                "event_type": _event_type(text),
                "source_name": article.get("publisher"),
                "title": title or None,
                "source_url": article.get("final_url")
                or article.get("publisher_url")
                or article.get("rss_url")
                or article.get("url"),
                "fetched_at": article.get("article_fetched_at")
                or article.get("fetched_at")
                or snapshot_fetched_at,
                "analysis_method": "keyword_heuristic_from_news_reader_snapshot_v1",
                "snapshot_mode": snapshot_mode,
            }
        )
    return _finalize_history_frame(pd.DataFrame(rows, columns=NEWS_HISTORY_COLUMNS))


def _finalize_history_frame(frame: pd.DataFrame) -> pd.DataFrame:
    output = frame.copy()
    for column in NEWS_HISTORY_COLUMNS:
        if column not in output:
            output[column] = pd.NA
    output = output[NEWS_HISTORY_COLUMNS]
    if not output.empty:
        output["symbol"] = output["symbol"].astype(str).str.upper().str.strip()
        output["available_at"] = pd.to_datetime(
            output["available_at"], errors="coerce", utc=True
        )
        output["published_at"] = pd.to_datetime(
            output["published_at"], errors="coerce", utc=True
        )
        output = output.dropna(subset=["symbol", "available_at"])
        output = output.drop_duplicates(
            subset=["symbol", "available_at", "title", "source_url"],
            keep="last",
        ).sort_values(["symbol", "available_at", "title"], na_position="last")
    return output.reset_index(drop=True)


def append_news_history(output_csv: Path, new_rows: pd.DataFrame) -> pd.DataFrame:
    if output_csv.exists():
        existing = pd.read_csv(output_csv)
        combined = pd.concat([existing, new_rows], ignore_index=True)
    else:
        combined = new_rows
    output = _finalize_history_frame(combined)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(output_csv, index=False)
    return output


def collect_live_news_history(
    symbols: Iterable[str],
    output_csv: Path,
    *,
    hours: int = 720,
    limit: int = 20,
    read_limit: int = 10,
) -> tuple[pd.DataFrame, list[dict]]:
    collected: list[pd.DataFrame] = []
    summaries: list[dict] = []
    for symbol in sorted(_normalize_symbols(symbols) or []):
        snapshot = fetch_live_research(symbol, hours=hours, limit=limit)
        reader_snapshot = read_live_articles(snapshot, limit=read_limit)
        frame = news_reader_snapshot_to_history_frame(reader_snapshot)
        collected.append(frame)
        summaries.append(
            {
                "symbol": symbol,
                "rss_article_count": int(snapshot.get("article_count", 0)),
                "read_article_count": int(reader_snapshot.get("read_article_count", 0)),
                "failed_or_filtered_count": int(
                    reader_snapshot.get("failed_or_filtered_count", 0)
                ),
                "exported_rows": int(len(frame)),
            }
        )
    non_empty = [frame for frame in collected if not frame.empty]
    new_rows = (
        pd.concat(non_empty, ignore_index=True)
        if non_empty
        else pd.DataFrame(columns=NEWS_HISTORY_COLUMNS)
    )
    return append_news_history(output_csv, new_rows), summaries


def export_news_history_from_reports(
    reports_root: Path,
    output_csv: Path,
    *,
    symbols: Iterable[str] | None = None,
) -> pd.DataFrame:
    """Build a model-ready CSV from saved News Reader snapshots.

    This is a convenience export for local experiments. The source snapshots are
    still live-research artifacts, so the output should not be treated as a
    production historical news dataset.
    """

    selected_symbols = _normalize_symbols(symbols)
    frames: list[pd.DataFrame] = []
    for reader_path in sorted(reports_root.glob("*/**/news_reader.json")):
        try:
            snapshot = json.loads(reader_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        symbol = str(snapshot.get("symbol") or reader_path.parts[-3]).upper()
        if selected_symbols is not None and symbol not in selected_symbols:
            continue
        frames.append(news_reader_snapshot_to_history_frame({**snapshot, "symbol": symbol}))
    non_empty = [frame for frame in frames if not frame.empty]
    output = (
        _finalize_history_frame(pd.concat(non_empty, ignore_index=True))
        if non_empty
        else pd.DataFrame(columns=NEWS_HISTORY_COLUMNS)
    )
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(output_csv, index=False)
    return output
