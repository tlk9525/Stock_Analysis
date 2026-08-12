from __future__ import annotations

import copy
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

from src.config import PROJECT_ROOT
from src.data.fetch import fetch_history
from src.features.technical import add_features, add_market_features
from src.models.xgboost import train_models
from src.panel.news import NEWS_MODEL_FEATURES, load_news_articles
from src.utils import write_json


def add_symbol_news_features(
    featured: pd.DataFrame,
    articles: pd.DataFrame,
    *,
    symbol: str,
    lookback_days: int = 5,
    timezone: str = "Asia/Ho_Chi_Minh",
    close_hour: int = 15,
) -> pd.DataFrame:
    if lookback_days <= 0:
        raise ValueError("lookback_days phải lớn hơn 0.")
    if not featured.index.is_monotonic_increasing or not featured.index.is_unique:
        raise ValueError("Dữ liệu feature phải tăng dần và không trùng ngày.")

    out = featured.copy()
    for column in NEWS_MODEL_FEATURES:
        out[column] = 0.0
    if articles.empty:
        return out

    news = articles.copy()
    news["symbol"] = news["symbol"].astype(str).str.upper().str.strip()
    news = news[news["symbol"] == symbol.strip().upper()]
    if news.empty:
        return out
    news["available_at"] = pd.to_datetime(news["available_at"], errors="coerce", utc=True)
    news = news.dropna(subset=["available_at"]).sort_values("available_at")
    news["sentiment_score"] = pd.to_numeric(news["sentiment_score"], errors="coerce").fillna(0.0)
    news["sentiment_label"] = news["sentiment_label"].astype(str).str.lower()
    news["event_type"] = news["event_type"].astype(str).str.lower()

    available = news["available_at"].astype("int64").to_numpy()
    sentiment = news["sentiment_score"].to_numpy(dtype=float)
    labels = news["sentiment_label"].to_numpy(dtype=str)
    events = news["event_type"].to_numpy(dtype=str)
    sources = (
        news["source_name"].fillna("").astype(str).to_numpy()
        if "source_name" in news
        else np.full(len(news), "", dtype=str)
    )
    cutoffs = (
        pd.to_datetime(out.index).tz_localize(timezone) + pd.Timedelta(hours=close_hour)
    ).tz_convert("UTC")
    lookback = pd.Timedelta(days=lookback_days)
    for position, cutoff in enumerate(cutoffs):
        start = np.searchsorted(available, (cutoff - lookback).value, side="right")
        end = np.searchsorted(available, cutoff.value, side="right")
        if end <= start:
            continue
        row_index = out.index[position]
        window_labels = labels[start:end]
        window_events = events[start:end]
        window_sources = sources[start:end]
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


def run_symbol_news_model(
    config: dict,
    *,
    symbol: str,
    news_articles_csv: Path,
    lookback_days: int = 5,
) -> Path:
    resolved = copy.deepcopy(config)
    resolved["symbol"] = symbol.strip().upper()
    resolved["save_to_postgres"] = False
    timezone = ZoneInfo(resolved.get("timezone", "Asia/Ho_Chi_Minh"))
    stamp = datetime.now(timezone).strftime("%Y-%m-%d_%H-%M-%S")
    run_directory = (
        PROJECT_ROOT
        / resolved.get("report_root", "reports")
        / resolved["symbol"]
        / f"{stamp}_news_model"
    )
    run_directory.mkdir(parents=True, exist_ok=True)

    history = fetch_history(resolved)
    featured = add_features(history)
    market_options = resolved.get("market_features", {}) or {}
    if bool(market_options.get("enabled", False)):
        benchmark_symbol = str(market_options.get("benchmark_symbol", "VNINDEX")).upper()
        benchmark = fetch_history({**resolved, "symbol": benchmark_symbol})
        featured = add_market_features(featured, benchmark)

    news_path = news_articles_csv
    if not news_path.is_absolute():
        news_path = PROJECT_ROOT / news_path
    articles = load_news_articles(news_path)
    featured = add_symbol_news_features(
        featured,
        articles,
        symbol=resolved["symbol"],
        lookback_days=lookback_days,
        timezone=resolved.get("timezone", "Asia/Ho_Chi_Minh"),
    )
    train_config = {
        **resolved,
        "extra_model_features": NEWS_MODEL_FEATURES,
        "news_model": {
            "enabled": True,
            "articles_csv": str(news_articles_csv),
            "lookback_days": lookback_days,
            "scope": "single_symbol",
        },
    }
    metrics, scored_test, latest_probabilities, booster = train_models(
        featured,
        train_config,
    )
    symbol_articles = articles[
        articles["symbol"].astype(str).str.upper().str.strip() == resolved["symbol"]
    ]
    summary = {
        "symbol": resolved["symbol"],
        "enabled": True,
        "articles_csv": str(news_articles_csv),
        "symbol_article_count": int(len(symbol_articles)),
        "feature_rows_with_news": int((featured["news_count_lookback"] > 0).sum()),
        "feature_columns": NEWS_MODEL_FEATURES,
        "target": "target_next_up",
        "execution": "signal after close t; entry open t+1; exit close t+1",
        "point_in_time_rule": "available_at <= local market close of date t",
        "limitation": (
            "CSV dựng từ live snapshots chỉ phù hợp smoke test/research; "
            "cần lịch sử available_at dài hơn trước khi dùng production."
        ),
    }

    featured.reset_index().rename(columns={"time": "date"}).to_csv(
        run_directory / "history_features_with_news.csv",
        index=False,
    )
    scored_test.reset_index().rename(columns={"time": "date"}).to_csv(
        run_directory / "model_test_predictions.csv",
        index=False,
    )
    booster.save_model(str(run_directory / "xgboost_symbol_news.json"))
    write_json(run_directory / "model_metrics.json", metrics)
    write_json(run_directory / "latest_probabilities.json", latest_probabilities)
    write_json(run_directory / "symbol_news_model_summary.json", summary)
    write_json(run_directory / "resolved_config.json", train_config)
    write_json(run_directory / "feature_importance.json", metrics["xgboost"].get("feature_importance_gain", {}))
    print(f"Xong symbol-news model. Báo cáo nằm ở: {run_directory}")
    return run_directory
