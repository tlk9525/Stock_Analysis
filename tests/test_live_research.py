from __future__ import annotations

from datetime import datetime, timezone

import pytest

from src.research.live_web import (
    _public_redirect_target,
    build_live_research_snapshot,
    read_live_articles,
)


def test_news_reader_rejects_redirect_to_local_address() -> None:
    with pytest.raises(ValueError, match="HTTP\\(S\\) public"):
        _public_redirect_target("https://publisher.example/article", "http://127.0.0.1/private")

    assert _public_redirect_target(
        "https://publisher.example/article",
        "/market/update",
    ) == "https://publisher.example/market/update"


def test_live_research_keeps_attributable_recent_headlines_only() -> None:
    snapshot = build_live_research_snapshot(
        "fpt",
        [
            {
                "title": "FPT công bố kết quả kinh doanh",
                "link": "https://example.com/fpt-q2",
                "published": "Thu, 07 Aug 2026 09:00:00 GMT",
                "source": {"title": "Nguồn A"},
            },
            {
                "title": "FPT công bố kết quả kinh doanh",
                "link": "https://example.com/fpt-q2",
                "published": "Thu, 07 Aug 2026 09:00:00 GMT",
                "source": {"title": "Nguồn A"},
            },
            {
                "title": "Tin cũ",
                "link": "https://example.com/old",
                "published": "Thu, 01 Aug 2024 09:00:00 GMT",
                "source": {"title": "Nguồn B"},
            },
        ],
        query='"FPT" cổ phiếu',
        fetched_at=datetime(2026, 8, 7, 12, tzinfo=timezone.utc),
        hours=72,
    )

    assert snapshot["mode"] == "live_research_only"
    assert snapshot["article_count"] == 1
    assert snapshot["articles"][0]["publisher"] == "Nguồn A"
    assert snapshot["articles"][0]["url"] == "https://example.com/fpt-q2"


def test_news_reader_extracts_a_bounded_article_and_labels_topics() -> None:
    html = """
    <html><head><title>FPT công bố kết quả</title></head><body>
      <nav>Menu quảng cáo</nav><article>
        <p>FPT công bố kết quả kinh doanh quý mới với doanh thu và lợi nhuận được cập nhật trong báo cáo.</p>
        <p>Doanh nghiệp cũng công bố cổ tức tiền mặt cho cổ đông theo nghị quyết đã được thông qua.</p>
        <p>Thông tin được cung cấp nhằm giúp nhà đầu tư theo dõi tình hình doanh nghiệp và cần được đối chiếu với nguồn gốc.</p>
        <p>Các số liệu chi tiết cần được kiểm chứng cùng báo cáo tài chính và công bố thông tin chính thức của doanh nghiệp.</p>
      </article></body></html>
    """
    snapshot = {
        "symbol": "FPT",
        "fetched_at": "2026-08-07T12:00:00+00:00",
        "articles": [
            {
                "title": "FPT công bố kết quả",
                "publisher": "Nguồn A",
                "url": "https://news.google.com/rss/articles/example",
                "published_at": "2026-08-07T10:00:00+00:00",
            }
        ],
    }
    result = read_live_articles(
        snapshot,
        resolver=lambda url: "https://publisher.example/fpt",
        downloader=lambda url: (html, url),
    )

    assert result["read_article_count"] == 1
    article = result["articles"][0]
    assert article["final_url"] == "https://publisher.example/fpt"
    assert article["content_chars"] > 300
    assert "ket_qua_kinh_doanh" in article["topics"]
    assert "co_tuc_va_hanh_dong_doanh_nghiep" in article["topics"]
    assert any("GDKHQ" in item for item in article["review_implications"])
    assert "quảng cáo" not in article["content_excerpt"].casefold()
