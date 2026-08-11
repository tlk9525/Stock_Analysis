from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import numpy as np
import pandas as pd


NEWS_MODEL_FEATURES = [
    "news_count_lookback",
    "news_sentiment_mean_lookback",
    "news_positive_count_lookback",
    "news_negative_count_lookback",
    "news_earnings_count_lookback",
    "news_corporate_action_count_lookback",
    "news_legal_count_lookback",
    "news_source_count_lookback",
]


def load_news_articles(path: str | Path) -> pd.DataFrame:
    """Load a provenance-first historical news CSV for an explicit panel run."""

    csv_path = Path(path)
    if not csv_path.exists() or not csv_path.is_file():
        raise FileNotFoundError(f"Không tìm thấy news CSV: {csv_path}")
    articles = pd.read_csv(csv_path)
    required = {"symbol", "available_at", "sentiment_score", "sentiment_label", "event_type"}
    missing = sorted(required - set(articles.columns))
    if missing:
        raise ValueError(f"News CSV thiếu cột: {', '.join(missing)}")
    articles = articles.copy()
    articles["symbol"] = articles["symbol"].astype(str).str.upper().str.strip()
    articles["available_at"] = pd.to_datetime(
        articles["available_at"], errors="coerce", utc=True
    )
    articles["sentiment_score"] = pd.to_numeric(
        articles["sentiment_score"], errors="coerce"
    ).fillna(0.0)
    articles["sentiment_label"] = articles["sentiment_label"].astype(str).str.lower()
    articles["event_type"] = articles["event_type"].astype(str).str.lower()
    return articles.dropna(subset=["available_at"]).drop_duplicates(
        subset=["symbol", "available_at", "title", "source_url"],
        keep="last",
    )


def _empty_features(index: pd.MultiIndex) -> pd.DataFrame:
    return pd.DataFrame(0.0, index=index, columns=NEWS_MODEL_FEATURES)


def add_panel_news_features(
    featured_panel: pd.DataFrame,
    articles: pd.DataFrame,
    *,
    lookback_days: int = 5,
    timezone: str = "Asia/Ho_Chi_Minh",
    close_hour: int = 15,
) -> pd.DataFrame:
    """Attach point-in-time news aggregates to a (date, symbol) panel.

    The cutoff is the local market close on date *t*. Articles published after
    that cutoff cannot affect features at *t*. Missing news is represented by
    zeroes so the baseline panel remains trainable.
    """

    if lookback_days <= 0:
        raise ValueError("lookback_days phải lớn hơn 0.")
    if not isinstance(featured_panel.index, pd.MultiIndex) or not {
        "date",
        "symbol",
    }.issubset(featured_panel.index.names):
        raise ValueError("featured_panel phải có MultiIndex (date, symbol).")

    out = featured_panel.copy()
    empty = _empty_features(out.index)
    for column in NEWS_MODEL_FEATURES:
        out[column] = empty[column]
    if articles is None or articles.empty:
        return out

    required = {"symbol", "available_at", "sentiment_score", "sentiment_label", "event_type"}
    missing = sorted(required - set(articles.columns))
    if missing:
        raise ValueError(f"Articles thiếu cột: {', '.join(missing)}")
    news = articles.copy()
    news["symbol"] = news["symbol"].astype(str).str.upper().str.strip()
    news["available_at"] = pd.to_datetime(news["available_at"], errors="coerce", utc=True)
    news = news.dropna(subset=["available_at"])
    news["sentiment_score"] = pd.to_numeric(news["sentiment_score"], errors="coerce").fillna(0.0)
    news["sentiment_label"] = news["sentiment_label"].astype(str).str.lower()
    news["event_type"] = news["event_type"].astype(str).str.lower()

    dates = pd.to_datetime(out.index.get_level_values("date"), errors="coerce")
    symbols = out.index.get_level_values("symbol").astype(str).str.upper()
    cutoffs = (
        dates.tz_localize(timezone) + pd.Timedelta(hours=close_hour)
    ).tz_convert("UTC")
    lookback = pd.Timedelta(days=lookback_days)

    for symbol in symbols.unique():
        row_positions = np.flatnonzero(symbols == symbol)
        symbol_news = news[news["symbol"] == symbol].sort_values("available_at")
        if symbol_news.empty:
            continue
        available = symbol_news["available_at"].astype("int64").to_numpy()
        sentiment = symbol_news["sentiment_score"].to_numpy(dtype=float)
        labels = symbol_news["sentiment_label"].to_numpy(dtype=str)
        events = symbol_news["event_type"].to_numpy(dtype=str)
        source_values = (
            symbol_news["source_name"].fillna("").astype(str).to_numpy()
            if "source_name" in symbol_news
            else np.full(len(symbol_news), "", dtype=str)
        )
        for position in row_positions:
            cutoff_ns = cutoffs[position].value
            start = np.searchsorted(available, (cutoffs[position] - lookback).value, side="right")
            end = np.searchsorted(available, cutoff_ns, side="right")
            if end <= start:
                continue
            window_labels = labels[start:end]
            window_events = events[start:end]
            window_sources = source_values[start:end]
            row_index = out.index[position]
            out.at[row_index, "news_count_lookback"] = float(end - start)
            out.at[row_index, "news_sentiment_mean_lookback"] = float(sentiment[start:end].mean())
            out.at[row_index, "news_positive_count_lookback"] = float(np.sum(window_labels == "positive"))
            out.at[row_index, "news_negative_count_lookback"] = float(np.sum(window_labels == "negative"))
            out.at[row_index, "news_earnings_count_lookback"] = float(np.sum(window_events == "earnings"))
            out.at[row_index, "news_corporate_action_count_lookback"] = float(
                np.sum(window_events == "corporate_action")
            )
            out.at[row_index, "news_legal_count_lookback"] = float(np.sum(window_events == "legal"))
            out.at[row_index, "news_source_count_lookback"] = float(
                len({source for source in window_sources if source})
            )
    return out
