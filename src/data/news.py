from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Iterable
from zoneinfo import ZoneInfo

import pandas as pd


NEWS_COLUMNS = [
    "article_key",
    "symbol",
    "provider",
    "source_name",
    "source_url",
    "title",
    "content_excerpt",
    "published_at",
    "available_at",
    "fetched_at",
    "availability_basis",
    "entity_match_method",
    "entity_confidence",
    "event_type",
    "sentiment_score",
    "sentiment_label",
    "analysis_method",
]


POSITIVE_TERMS = (
    "tăng trưởng",
    "tăng",
    "lãi",
    "lợi nhuận",
    "vượt kế hoạch",
    "cổ tức",
    "mở rộng",
    "hợp tác",
    "được cấp",
)
NEGATIVE_TERMS = (
    "thua lỗ",
    "lỗ",
    "giảm",
    "xử phạt",
    "bị phạt",
    "vi phạm",
    "cảnh báo",
    "truy thu",
    "khởi tố",
    "đình chỉ",
)


def _text(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()


def _first_value(row: pd.Series, candidates: Iterable[str]) -> str:
    for name in candidates:
        if name in row.index:
            value = _text(row[name])
            if value:
                return value
    return ""


def _to_utc(value: object, timezone: str) -> pd.Timestamp | pd.NaT:
    if not _text(value):
        return pd.NaT
    parsed = pd.to_datetime(value, errors="coerce")
    if pd.isna(parsed):
        return pd.NaT
    timestamp = pd.Timestamp(parsed)
    if timestamp.tzinfo is None:
        timestamp = timestamp.tz_localize(timezone)
    return timestamp.tz_convert("UTC")


def _sentiment(text: str) -> tuple[float, str]:
    """Transparent baseline only; it is not a trained Vietnamese NLP model."""

    normalized = text.casefold()
    positive = sum(term in normalized for term in POSITIVE_TERMS)
    negative = sum(term in normalized for term in NEGATIVE_TERMS)
    if positive == negative:
        return 0.0, "neutral"
    score = float((positive - negative) / max(positive + negative, 1))
    return score, "positive" if score > 0 else "negative"


def _event_type(text: str) -> str:
    normalized = text.casefold()
    if any(term in normalized for term in ("bctc", "báo cáo tài chính", "lợi nhuận", "doanh thu")):
        return "earnings"
    if any(term in normalized for term in ("cổ tức", "phát hành", "mua lại cổ phiếu", "esop")):
        return "corporate_action"
    if any(term in normalized for term in ("m&a", "sáp nhập", "thâu tóm", "mua cổ phần")):
        return "ma"
    if any(term in normalized for term in ("nghị quyết", "hđqt", "quản trị", "bổ nhiệm")):
        return "governance"
    if any(term in normalized for term in ("xử phạt", "vi phạm", "khởi tố", "truy thu", "đình chỉ")):
        return "legal"
    return "other"


def normalize_news_frame(
    raw: pd.DataFrame,
    symbol: str,
    provider: str,
    fetched_at: datetime | pd.Timestamp | None = None,
    timezone: str = "Asia/Ho_Chi_Minh",
) -> pd.DataFrame:
    """Normalize provider news into a provenance-first, deduplicated table.

    A missing publication time deliberately leaves ``available_at`` empty. Such
    an article can be shown in a report but must not become a historical model
    feature because its availability is unknown.
    """

    if raw.empty:
        return pd.DataFrame(columns=NEWS_COLUMNS)
    fetched = pd.Timestamp(fetched_at or datetime.now(ZoneInfo(timezone)))
    if fetched.tzinfo is None:
        fetched = fetched.tz_localize(timezone)
    fetched = fetched.tz_convert("UTC")
    rows: list[dict] = []
    for index, row in raw.iterrows():
        title = _first_value(row, ("news_title", "title", "friendly_title", "head"))
        excerpt = _first_value(
            row,
            ("news_short_content", "news_full_content", "friendly_sub_title", "news_sub_title"),
        )
        published = _to_utc(_first_value(row, ("public_date", "publish_time", "published_at")), timezone)
        source_url = _first_value(row, ("news_source_link", "url", "link"))
        source_name = _first_value(row, ("news_source", "source")) or provider
        external_id = _first_value(row, ("id", "news_id", "article_id"))
        identity = external_id or source_url or f"{title}|{published}|{index}"
        article_key = hashlib.sha256(f"{provider}|{identity}".encode("utf-8")).hexdigest()
        text = " ".join(value for value in (title, excerpt) if value)
        score, label = _sentiment(text)
        rows.append(
            {
                "article_key": article_key,
                "symbol": symbol.upper(),
                "provider": provider,
                "source_name": source_name,
                "source_url": source_url or None,
                "title": title or None,
                "content_excerpt": excerpt or None,
                "published_at": published,
                "available_at": published,
                "fetched_at": fetched,
                "availability_basis": "published_at" if not pd.isna(published) else "unknown",
                # Company.news is queried by ticker. This is traceable but less
                # certain than an explicit ticker inside the article itself.
                "entity_match_method": "provider_symbol_query",
                "entity_confidence": 0.8,
                "event_type": _event_type(text),
                "sentiment_score": score,
                "sentiment_label": label,
                "analysis_method": "keyword_heuristic_v1",
            }
        )
    out = pd.DataFrame(rows, columns=NEWS_COLUMNS)
    out = out.drop_duplicates(subset=["article_key"], keep="last")
    return out.sort_values(["published_at", "article_key"], na_position="last").reset_index(drop=True)


def fetch_company_news(config: dict) -> tuple[dict, pd.DataFrame]:
    """Fetch company news through the existing vnstock dependency.

    Provider failures are returned as report notes so a price-analysis run does
    not fail solely because optional news research is unavailable.
    """

    options = config.get("news", {}) or {}
    symbol = str(config["symbol"]).upper()
    provider = str(options.get("source") or config.get("source", "VCI")).upper()
    summary = {
        "available": False,
        "symbol": symbol,
        "provider": provider,
        "mode": options.get("mode", "research_only"),
        "analysis_method": "keyword_heuristic_v1",
        "notes": [],
    }
    if not bool(options.get("enabled", False)):
        summary["notes"].append("Pipeline tin tức đang tắt trong config.")
        return summary, pd.DataFrame(columns=NEWS_COLUMNS)
    try:
        from vnstock import Company

        raw = Company(source=provider, symbol=symbol, show_log=False).news()
        articles = normalize_news_frame(
            pd.DataFrame(raw),
            symbol=symbol,
            provider=f"vnstock:{provider}",
            timezone=config.get("timezone", "Asia/Ho_Chi_Minh"),
        )
    except Exception as exc:
        summary["notes"].append(f"Không lấy được tin tức: {exc}")
        return summary, pd.DataFrame(columns=NEWS_COLUMNS)

    dated = articles.dropna(subset=["available_at"])
    summary.update(
        {
            "available": not articles.empty,
            "article_count": int(len(articles)),
            "eligible_article_count": int(len(dated)),
            "latest_published_at": (
                dated["published_at"].max().isoformat() if not dated.empty else None
            ),
            "mean_sentiment": (
                float(dated["sentiment_score"].mean()) if not dated.empty else None
            ),
            "event_counts": articles["event_type"].value_counts().to_dict(),
        }
    )
    summary["notes"].extend(
        [
            "Sentiment hiện là keyword heuristic, chỉ phục vụ research/dashboard; cần tập gán nhãn tiếng Việt trước khi dùng cho model.",
            "Chỉ bài có published_at/available_at mới đủ điều kiện tạo feature point-in-time.",
        ]
    )
    return summary, articles


def build_asof_news_features(
    articles: pd.DataFrame,
    cutoffs: Iterable[object],
    lookback_days: int = 5,
    timezone: str = "Asia/Ho_Chi_Minh",
) -> pd.DataFrame:
    """Build research features using only articles available by each cutoff."""

    if lookback_days <= 0:
        raise ValueError("lookback_days phải lớn hơn 0.")
    prepared = articles.copy()
    if "available_at" not in prepared:
        prepared = pd.DataFrame(columns=NEWS_COLUMNS)
    else:
        prepared["available_at"] = pd.to_datetime(prepared["available_at"], errors="coerce", utc=True)
        prepared = prepared.dropna(subset=["available_at"])
    rows: list[dict] = []
    for cutoff_value in cutoffs:
        cutoff = _to_utc(cutoff_value, timezone)
        if pd.isna(cutoff):
            continue
        eligible = prepared[
            (prepared["available_at"] <= cutoff)
            & (prepared["available_at"] > cutoff - pd.Timedelta(days=lookback_days))
        ]
        rows.append(
            {
                "cutoff": cutoff,
                "news_count_lookback": int(len(eligible)),
                "news_sentiment_mean_lookback": (
                    float(eligible["sentiment_score"].mean()) if not eligible.empty else 0.0
                ),
                "news_negative_count_lookback": int(
                    (eligible.get("sentiment_label", pd.Series(dtype=str)) == "negative").sum()
                ),
                "news_earnings_count_lookback": int(
                    (eligible.get("event_type", pd.Series(dtype=str)) == "earnings").sum()
                ),
            }
        )
    return pd.DataFrame(rows).set_index("cutoff") if rows else pd.DataFrame()
