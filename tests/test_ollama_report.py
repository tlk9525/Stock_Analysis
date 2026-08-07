from __future__ import annotations

import json

from src.ai.ollama_report import apply_source_grounding, build_messages, build_report_context
from src.reports.dashboard import enhance_dashboard_with_research


def test_report_context_and_prompt_keep_decision_status(tmp_path) -> None:
    (tmp_path / "signal_decision.json").write_text(
        json.dumps({"status": "NO_EDGE", "reasons": ["No net edge"]}), encoding="utf-8"
    )
    (tmp_path / "latest_levels.json").write_text(json.dumps({"latest_close": 100}), encoding="utf-8")

    context = build_report_context(tmp_path)
    messages = build_messages(context)

    assert context["levels"]["latest_close"] == 100
    assert "NO_EDGE" in messages[0]["content"]
    assert "Không bịa số liệu" in messages[0]["content"]
    assert "mỗi headline chỉ chứng minh" in messages[0]["content"]


def test_live_research_sources_and_evidence_are_replaced_with_saved_snapshot() -> None:
    result = apply_source_grounding(
        {"sources": [{"title": "Model invented", "url": "https://bad.example"}], "evidence": ["Model claim"]},
        {
            "decision": {"status": "NO_EDGE", "reasons": ["Net return < 0"]},
            "live_research": {
                "fetched_at": "2026-08-07T06:00:00+00:00",
                "articles": [
                    {
                        "title": "FPT published headline",
                        "publisher": "Example News",
                        "url": "https://example.com/fpt",
                        "published_at": "2026-08-07T05:00:00+00:00",
                    }
                ],
            },
        },
    )

    assert result["sources"] == [
        {
            "title": "FPT published headline",
            "publisher": "Example News",
            "url": "https://example.com/fpt",
            "published_at": "2026-08-07T05:00:00+00:00",
        }
    ]
    assert result["evidence"][0] == "ML decision artifact: NO_EDGE. Net return < 0"
    assert result["summary"].startswith("ML decision hiện giữ nguyên NO_EDGE")
    assert "không được diễn giải là tin tích cực/tiêu cực" in result["news_view"]


def test_news_reader_is_preferred_over_headlines_for_ai_citations() -> None:
    result = apply_source_grounding(
        {},
        {
            "decision": {"status": "NO_EDGE", "reasons": []},
            "live_research": {"fetched_at": "2026-08-07T06:00:00+00:00", "articles": []},
            "news_reader": {
                "topic_counts": {"ket_qua_kinh_doanh": 1},
                "review_implications": ["Đối chiếu doanh thu/lợi nhuận trong bài với BCTC."],
                "articles": [
                    {
                        "title": "Nguồn gốc",
                        "publisher": "Publisher",
                        "final_url": "https://publisher.example/article",
                        "published_at": "2026-08-07T05:00:00+00:00",
                        "topics": ["ket_qua_kinh_doanh"],
                    }
                ],
            },
        },
    )

    assert result["sources"][0]["url"] == "https://publisher.example/article"
    assert "News Reader [Publisher]" in result["evidence"][0]
    assert "phân nhóm rule-based" in result["news_view"]
    assert "Tác động cần kiểm chứng" in result["news_view"]


def test_grounding_replaces_every_user_visible_model_claim_without_news() -> None:
    result = apply_source_grounding(
        {
            "summary": "Mô hình bịa tóm tắt",
            "technical_view": "Mô hình bịa kỹ thuật",
            "fundamental_view": "Mô hình bịa cơ bản",
            "news_view": "Mô hình bịa tin",
            "live_research_view": "Mô hình bịa research",
            "risks": ["Mô hình bịa rủi ro"],
            "decision_status": "ACTIONABLE",
            "evidence": ["Mô hình bịa bằng chứng"],
            "sources": [{"title": "Mô hình bịa nguồn"}],
            "disclaimer": "Mô hình bịa disclaimer",
        },
        {
            "decision": {"status": "NO_EDGE", "reasons": ["Net return < 0"]},
            "technical": {
                "bias": "Trung tính",
                "score": 0,
                "signals": [{"name": "MACD", "status": "Cẩn thận", "detail": "Histogram âm."}],
            },
            "fundamentals": {
                "available": True,
                "symbol": "HCM",
                "latest_period": "2026-Q2",
                "metrics": [{"metric_name": "roe", "metric_label": "ROE", "metric_value": 0.1, "metric_unit": "percent"}],
            },
        },
    )

    rendered = json.dumps(result, ensure_ascii=False)
    assert "Mô hình bịa" not in rendered
    assert result["decision_status"] == "NO_EDGE"
    assert result["sources"] == []
    assert result["evidence"] == ["ML decision artifact: NO_EDGE. Net return < 0"]
    assert result["risks"] == ["ML guard: Net return < 0"]
    assert "bias Trung tính" in result["technical_view"]
    assert "ROE 10.0%" in result["fundamental_view"]
    assert "không phải khuyến nghị mua/bán" in result["disclaimer"]


def test_dashboard_enrichment_adds_ai_news_reader_and_financial_details(tmp_path) -> None:
    (tmp_path / "dashboard.html").write_text("<html><main><p>Base</p></main></html>", encoding="utf-8")
    (tmp_path / "live_research.json").write_text(
        json.dumps({"articles": [{"publisher": "Example", "title": "Headline", "published_at": "2026-08-07", "url": "https://example.com/live"}]}),
        encoding="utf-8",
    )
    (tmp_path / "news_reader.json").write_text(
        json.dumps({"articles": [{"publisher": "Reader", "title": "Read article", "topics": ["nganh"], "published_at": "2026-08-07", "final_url": "https://example.com/read", "content_excerpt": "Đoạn trích <đã escape>."}]}),
        encoding="utf-8",
    )
    (tmp_path / "income_statement.csv").write_text(
        "item,2026-Q2,2026-Q1,2025-Q4,2025-Q3\nDoanh thu,1000000000,900000000,800000000,700000000\n",
        encoding="utf-8",
    )

    enhance_dashboard_with_research(
        tmp_path,
        {
            "decision_status": "NO_EDGE",
            "summary": "Tóm tắt đã kiểm chứng",
            "risks": ["Rủi ro artifact"],
            "evidence": ["Bằng chứng artifact"],
            "disclaimer": "Không phải khuyến nghị mua/bán.",
        },
    )

    rendered = (tmp_path / "dashboard.html").read_text(encoding="utf-8")
    assert "Phân tích AI có kiểm chứng" in rendered
    assert "Tin web đã lấy" in rendered
    assert "News Reader: bài đã đọc và trích đoạn" in rendered
    assert "Chi tiết báo cáo tài chính" in rendered
    assert "Đoạn trích &lt;đã escape&gt;." in rendered
    assert rendered.count("FinAI dynamic enrichment start") == 1
