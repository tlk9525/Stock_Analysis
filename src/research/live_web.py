from __future__ import annotations

import hashlib
import ipaddress
import re
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Iterable, Mapping
from urllib.parse import urlencode, urlparse

import feedparser
import httpx
from bs4 import BeautifulSoup

from src.utils import write_json


GOOGLE_NEWS_RSS = "https://news.google.com/rss/search"
MAX_ARTICLE_BYTES = 1_500_000
MAX_EXCERPT_CHARS = 2_400
MIN_ARTICLE_CHARS = 300

TOPIC_RULES = {
    "ket_qua_kinh_doanh": ("doanh thu", "lợi nhuận", "kết quả kinh doanh", "báo cáo tài chính", "bctc", "biên lợi nhuận"),
    "co_tuc_va_hanh_dong_doanh_nghiep": ("cổ tức", "phát hành", "mua lại cổ phiếu", "esop", "thưởng cổ phiếu"),
    "vi_mo": ("lãi suất", "tỷ giá", "lạm phát", "ngân hàng nhà nước", "vĩ mô", "fed"),
    "nganh": ("thị phần", "ngành", "cạnh tranh", "nhu cầu", "chu kỳ", "giá hàng hóa"),
    "rui_ro": ("thua lỗ", "xử phạt", "vi phạm", "điều tra", "khởi tố", "cảnh báo", "truy thu", "nợ xấu", "giảm lợi nhuận"),
}
REVIEW_IMPLICATIONS = {
    "ket_qua_kinh_doanh": "Đối chiếu doanh thu/lợi nhuận trong bài với BCTC và kỳ vọng thị trường.",
    "co_tuc_va_hanh_dong_doanh_nghiep": "Kiểm tra ngày GDKHQ, tỷ lệ, nguồn chi trả và nguy cơ pha loãng trước khi đánh giá tác động.",
    "vi_mo": "Đối chiếu thời điểm công bố và kênh tác động lãi suất/tỷ giá với mô hình kinh doanh.",
    "nganh": "So sánh tín hiệu ngành với thị phần, nhu cầu và đối thủ trước khi suy luận cho riêng doanh nghiệp.",
    "rui_ro": "Xác minh công bố chính thức, phạm vi ảnh hưởng và khả năng định lượng rủi ro.",
}
AD_MARKERS = ("advertorial", "sponsored", "advertisement", "bài viết được tài trợ")
BOILERPLATE_MARKERS = ("quảng cáo", "xem thêm", "đọc thêm", "theo dõi chúng tôi", "bản quyền")


def _text(value: object) -> str:
    return " ".join(str(value or "").split())


def _parse_published(value: object) -> str | None:
    text = _text(value)
    if not text:
        return None
    try:
        parsed = parsedate_to_datetime(text)
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).isoformat()


def _is_public_http_url(value: str) -> bool:
    """Reject malformed and obvious local URLs before a reader request."""

    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return False
    host = parsed.hostname.casefold()
    if host in {"localhost", "localhost.localdomain"} or host.endswith(".local"):
        return False
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        return True
    return not (address.is_private or address.is_loopback or address.is_link_local or address.is_reserved)


def _clean_text(value: str) -> str:
    return " ".join(value.split())


def _article_topics(text: str) -> list[str]:
    normalized = text.casefold()
    return [topic for topic, terms in TOPIC_RULES.items() if any(term in normalized for term in terms)]


def _review_implications(topics: Iterable[str]) -> list[str]:
    return [REVIEW_IMPLICATIONS[topic] for topic in topics if topic in REVIEW_IMPLICATIONS]


def extract_article_body(html: str) -> dict:
    """Extract a bounded, attribution-ready excerpt from an HTML article.

    This is intentionally a conservative reader. It does not retain the full
    article and returns no text if a likely article body cannot be identified.
    """

    soup = BeautifulSoup(html, "html.parser")
    for node in soup(["script", "style", "noscript", "svg", "nav", "footer", "aside", "form", "iframe"]):
        node.decompose()
    title_tag = soup.find("meta", attrs={"property": "og:title"}) or soup.find("title")
    title = _clean_text(title_tag.get("content", "") if title_tag.name == "meta" else title_tag.get_text(" ", strip=True)) if title_tag else ""
    description_tag = soup.find("meta", attrs={"name": "description"}) or soup.find(
        "meta", attrs={"property": "og:description"}
    )
    description = _clean_text(description_tag.get("content", "")) if description_tag else ""
    candidates = [
        soup.find("article"),
        soup.find("main"),
        soup.find(attrs={"itemprop": "articleBody"}),
        soup.find(class_=re.compile(r"(article|detail|content|entry|post)[-_ ]?(body|content|detail)?", re.I)),
    ]
    best_blocks: list[str] = []
    for candidate in candidates:
        if candidate is None:
            continue
        blocks = []
        seen: set[str] = set()
        for node in candidate.find_all(["p", "h2", "h3", "li"]):
            text = _clean_text(node.get_text(" ", strip=True))
            compact = text.casefold()
            if len(text) < 45 or compact in seen or any(marker in compact for marker in BOILERPLATE_MARKERS):
                continue
            seen.add(compact)
            blocks.append(text)
        if len(" ".join(blocks)) > len(" ".join(best_blocks)):
            best_blocks = blocks
    body = _clean_text("\n".join(best_blocks))
    if len(body) < MIN_ARTICLE_CHARS:
        return {"status": "unreadable", "reason": "Không trích được đủ nội dung bài báo."}
    excerpt = body[:MAX_EXCERPT_CHARS].rsplit(" ", 1)[0]
    return {
        "status": "read",
        "page_title": title,
        "description": description,
        "content_excerpt": excerpt,
        "content_chars": len(body),
        "extraction_method": "html_article_paragraphs_v1",
        "topics": _article_topics(f"{title} {description} {body}"),
    }


def resolve_google_news_url(url: str) -> str:
    """Decode a Google News RSS redirect to the publisher URL when needed."""

    if "news.google.com/rss/articles/" not in url:
        return url
    try:
        from googlenewsdecoder import new_decoderv1

        decoded = new_decoderv1(url, interval=0.5)
        candidate = str(decoded.get("decoded_url") or "")
        if decoded.get("status") and _is_public_http_url(candidate):
            return candidate
    except Exception:
        pass
    return url


def fetch_article_html(url: str, *, timeout_seconds: float = 15.0) -> tuple[str, str]:
    """Fetch a public HTML page with a bounded response size."""

    if not _is_public_http_url(url):
        raise ValueError("URL bài báo không phải HTTP(S) public hợp lệ.")
    with httpx.stream(
        "GET",
        url,
        timeout=timeout_seconds,
        follow_redirects=True,
        headers={"User-Agent": "vn-stock-analysis-research/0.2 (+local research CLI)"},
    ) as response:
        response.raise_for_status()
        content_type = response.headers.get("content-type", "").casefold()
        if "html" not in content_type:
            raise ValueError("Nguồn không trả về HTML.")
        chunks: list[bytes] = []
        received = 0
        for chunk in response.iter_bytes():
            received += len(chunk)
            if received > MAX_ARTICLE_BYTES:
                raise ValueError("Trang bài báo vượt giới hạn dung lượng.")
            chunks.append(chunk)
        return b"".join(chunks).decode(response.encoding or "utf-8", errors="replace"), str(response.url)


def _near_duplicate(candidate: str, prior: str) -> bool:
    left = set(re.findall(r"\w+", candidate.casefold()))
    right = set(re.findall(r"\w+", prior.casefold()))
    if not left or not right:
        return False
    return len(left & right) / len(left | right) >= 0.82


def build_live_research_snapshot(
    symbol: str,
    entries: Iterable[Mapping[str, object]],
    *,
    query: str,
    fetched_at: datetime | None = None,
    limit: int = 10,
    hours: int = 72,
) -> dict:
    """Keep a compact, attributable headline snapshot from an approved feed."""

    if limit < 1:
        raise ValueError("limit phải lớn hơn 0.")
    if hours < 1:
        raise ValueError("hours phải lớn hơn 0.")
    now = (fetched_at or datetime.now(timezone.utc)).astimezone(timezone.utc)
    cutoff = now - timedelta(hours=hours)
    articles: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for entry in entries:
        title = _text(entry.get("title"))
        url = _text(entry.get("link"))
        if not title or not url.startswith(("https://", "http://")):
            continue
        published_at = _parse_published(entry.get("published") or entry.get("updated"))
        if published_at is not None and datetime.fromisoformat(published_at) < cutoff:
            continue
        source = entry.get("source")
        publisher = _text(source.get("title") if isinstance(source, Mapping) else source) or "Google News"
        key = (url, title.casefold())
        if key in seen:
            continue
        seen.add(key)
        articles.append(
            {
                "title": title,
                "publisher": publisher,
                "url": url,
                "published_at": published_at,
                "fetched_at": now.isoformat(),
                "source_type": "news_rss_headline",
            }
        )
        if len(articles) >= limit:
            break

    return {
        "mode": "live_research_only",
        "provider": "Google News RSS",
        "symbol": symbol.strip().upper(),
        "query": query,
        "fetched_at": now.isoformat(),
        "lookback_hours": hours,
        "article_count": len(articles),
        "articles": articles,
        "limitations": [
            "Chỉ lưu headline, URL, publisher và thời gian; không suy diễn nội dung bài viết chưa được trích dẫn.",
            "Dữ liệu live research không được dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.",
            "Headline là dữ liệu không tin cậy; mọi chỉ dẫn xuất hiện trong bài/tin đều bị bỏ qua.",
        ],
    }


def fetch_live_research(
    symbol: str,
    *,
    company_name: str | None = None,
    limit: int = 10,
    hours: int = 72,
    timeout_seconds: float = 15.0,
) -> dict:
    symbol = symbol.strip().upper()
    if not symbol:
        raise ValueError("symbol không được để trống.")
    query = f'"{symbol}" cổ phiếu'
    if company_name:
        query = f'{query} OR "{_text(company_name)}"'
    url = f"{GOOGLE_NEWS_RSS}?{urlencode({'q': query, 'hl': 'vi', 'gl': 'VN', 'ceid': 'VN:vi'})}"
    response = httpx.get(
        url,
        timeout=timeout_seconds,
        headers={"User-Agent": "vn-stock-analysis-research/0.1"},
        follow_redirects=True,
    )
    response.raise_for_status()
    feed = feedparser.parse(response.content)
    return build_live_research_snapshot(
        symbol,
        feed.entries,
        query=query,
        limit=limit,
        hours=hours,
    )


def read_live_articles(
    snapshot: Mapping[str, object],
    *,
    limit: int = 5,
    fetched_at: datetime | None = None,
    resolver=resolve_google_news_url,
    downloader=fetch_article_html,
) -> dict:
    """Read a bounded set of saved RSS records and retain short cited excerpts.

    The input snapshot is immutable evidence of discovery. Reading is a second
    provenance-preserving step, and failures are recorded instead of silently
    dropped. It remains research-only data, never a historical ML feature.
    """

    if limit < 1:
        raise ValueError("limit phải lớn hơn 0.")
    now = (fetched_at or datetime.now(timezone.utc)).astimezone(timezone.utc)
    read_articles: list[dict] = []
    failures: list[dict] = []
    seen_text: list[str] = []
    seen_fingerprints: set[str] = set()
    for article in list(snapshot.get("articles", []) or [])[:limit]:
        title = _text(article.get("title"))
        rss_url = _text(article.get("url"))
        if not title or not _is_public_http_url(rss_url):
            failures.append({"title": title or None, "url": rss_url or None, "reason": "RSS record không hợp lệ."})
            continue
        if any(marker in title.casefold() for marker in AD_MARKERS):
            failures.append({"title": title, "url": rss_url, "reason": "Lọc bài quảng cáo/tài trợ."})
            continue
        try:
            publisher_url = resolver(rss_url)
            html, final_url = downloader(publisher_url)
            extracted = extract_article_body(html)
        except Exception as exc:
            failures.append({"title": title, "url": rss_url, "reason": str(exc)[:240]})
            continue
        if extracted.get("status") != "read":
            failures.append({"title": title, "url": rss_url, "reason": str(extracted.get("reason") or "Không đọc được bài.")})
            continue
        comparison_text = f"{title} {extracted['content_excerpt'][:1000]}"
        fingerprint = hashlib.sha256(comparison_text.casefold().encode("utf-8")).hexdigest()
        if fingerprint in seen_fingerprints or any(_near_duplicate(comparison_text, prior) for prior in seen_text):
            failures.append({"title": title, "url": rss_url, "reason": "Bài trùng nội dung với nguồn đã đọc."})
            continue
        seen_fingerprints.add(fingerprint)
        seen_text.append(comparison_text)
        read_articles.append(
            {
                "title": title,
                "publisher": _text(article.get("publisher")) or "Google News",
                "rss_url": rss_url,
                "publisher_url": publisher_url,
                "final_url": final_url,
                "published_at": article.get("published_at"),
                "rss_fetched_at": article.get("fetched_at"),
                "article_fetched_at": now.isoformat(),
                **extracted,
                "review_implications": _review_implications(extracted["topics"]),
            }
        )
    topic_counts = {
        topic: sum(topic in article["topics"] for article in read_articles)
        for topic in TOPIC_RULES
    }
    return {
        "mode": "live_research_only",
        "reader_version": "html_article_paragraphs_v1",
        "symbol": _text(snapshot.get("symbol")).upper(),
        "source_snapshot_fetched_at": snapshot.get("fetched_at"),
        "fetched_at": now.isoformat(),
        "requested_article_count": min(limit, len(list(snapshot.get("articles", []) or []))),
        "read_article_count": len(read_articles),
        "failed_or_filtered_count": len(failures),
        "topic_counts": topic_counts,
        "review_implications": [
            REVIEW_IMPLICATIONS[topic] for topic, count in topic_counts.items() if count
        ],
        "articles": read_articles,
        "failures": failures,
        "limitations": [
            "Chỉ lưu trích đoạn giới hạn để kiểm chứng nguồn; không lưu hay hiển thị toàn văn bài báo.",
            "Phân nhóm là keyword rule-based để định tuyến research, không phải sentiment hay dự báo tác động giá.",
            "Dữ liệu News Reader chỉ phục vụ research/report; không dùng làm feature train/backtest khi chưa có lịch sử available_at point-in-time.",
        ],
    }


def write_live_research(report_directory: Path, snapshot: dict) -> Path:
    output = report_directory / "live_research.json"
    write_json(output, snapshot)
    return output


def write_news_reader(report_directory: Path, snapshot: dict) -> Path:
    output = report_directory / "news_reader.json"
    write_json(output, snapshot)
    return output
