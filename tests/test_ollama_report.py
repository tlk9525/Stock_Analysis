from __future__ import annotations

import json

import pandas as pd

from src.ai.ollama_report import apply_source_grounding, build_messages, build_report_context
from src.reports.dashboard import enhance_dashboard_with_research, write_dashboard, write_report


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
    (tmp_path / "news_impact_summary.json").write_text(
        json.dumps(
            {
                "status": "research_only",
                "effect_on_primary_signal": "not_applied",
                "base_xgboost_probability": 0.61,
                "news_adjusted_xgboost_probability": 0.55,
                "probability_delta": -0.06,
                "symbol_article_count": 12,
                "news_feature_importance_gain": {"news_count_lookback": 0.0},
                "gates": {"min_articles_60": False},
                "failed_gates": ["min_articles_60"],
                "recommendation": "Chỉ hiển thị như shadow/research.",
            }
        ),
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
    assert "Tác động của tin lên model" in rendered
    assert "News-adjusted XGBoost" in rendered
    assert "not_applied" in rendered
    assert "Chi tiết báo cáo tài chính" in rendered
    assert "Đoạn trích &lt;đã escape&gt;." in rendered
    assert rendered.count("FinAI dynamic enrichment start") == 1


def test_report_and_dashboard_explain_positive_gross_but_negative_net_costs(tmp_path) -> None:
    index = pd.bdate_range("2026-01-01", periods=30)
    frame = pd.DataFrame(
        {
            "close": range(100, 130),
            "return_1d": [0.001] * 30,
            "sma_20": [110] * 30,
            "sma_60": [105] * 30,
            "volume": [1_000_000] * 30,
        },
        index=index,
    )
    forecast = pd.DataFrame(
        {
            "p10": [95, 96],
            "p25": [98, 99],
            "p50": [105, 106],
            "p75": [110, 111],
            "p90": [115, 116],
            "prob_end_above_latest": [0.55, 0.56],
        },
        index=pd.bdate_range("2026-02-12", periods=2),
    )
    levels = {
        "latest_close": 129,
        "latest_date": "2026-02-11",
        "sma20": 110,
        "sma60": 105,
        "rsi14": 55,
        "macd": 0.1,
        "macd_signal": 0.05,
        "macd_hist": 0.05,
        "atr14": 2,
        "atr_pct14": 0.02,
        "adx14": 20,
        "support20": 120,
        "resistance20": 140,
    }
    metrics = {
        "split": {"test_start": "2025-01-01", "test_end": "2026-01-01"},
        "xgboost": {
            "balanced_accuracy": 0.53,
            "roc_auc": 0.56,
            "log_loss": 0.69,
            "best_iteration": 10,
            "feature_importance_gain": {"return_1d": 1.2},
        },
        "logistic_baseline": {"balanced_accuracy": 0.51, "roc_auc": 0.52},
        "majority_baseline": {"balanced_accuracy": 0.50},
        "backtest": {
            "observations": 252,
            "active_sessions": 61,
            "completed_round_trips": 61,
            "gross_total_return": 0.18,
            "net_total_return": -0.12,
            "sharpe_ratio": -0.3,
            "max_drawdown": -0.2,
            "transaction_cost_sum": 0.30,
            "transaction_cost_value_sum": 28_000_000,
            "gross_pnl_sum": 16_000_000,
            "net_pnl_sum": -12_000_000,
            "initial_capital": 100_000_000,
            "entry_cost_bps": 20,
            "exit_cost_bps": 30,
            "round_trip_cost_bps": 50,
            "threshold_sensitivity": [
                {
                    "signal_threshold": 0.55,
                    "active_sessions": 61,
                    "completed_round_trips": 61,
                    "net_total_return": -0.12,
                    "transaction_cost_sum": 0.30,
                    "sharpe_ratio": -0.3,
                },
                {
                    "signal_threshold": 0.60,
                    "active_sessions": 30,
                    "completed_round_trips": 30,
                    "net_total_return": 0.02,
                    "transaction_cost_sum": 0.15,
                    "sharpe_ratio": 0.1,
                },
            ],
            "top_n_trade_sensitivity": [
                {
                    "top_n": 10,
                    "min_probability_included": 0.62,
                    "completed_round_trips": 10,
                    "gross_total_return": 0.08,
                    "net_total_return": 0.03,
                    "transaction_cost_sum": 0.05,
                    "sharpe_ratio": 0.2,
                },
                {
                    "top_n": 5,
                    "min_probability_included": 0.67,
                    "completed_round_trips": 5,
                    "gross_total_return": 0.05,
                    "net_total_return": 0.02,
                    "transaction_cost_sum": 0.025,
                    "sharpe_ratio": 0.15,
                },
                {
                    "top_n": 1,
                    "min_probability_included": 0.75,
                    "completed_round_trips": 1,
                    "gross_total_return": 0.01,
                    "net_total_return": 0.005,
                    "transaction_cost_sum": 0.005,
                    "sharpe_ratio": 0.05,
                },
            ],
        },
    }
    technical = {"bias": "Trung tính", "score": 2, "signals": []}
    fundamentals = {"company": {"organ_short_name": "Demo"}, "metrics": [], "notes": []}
    news = {"available": False, "notes": []}
    risk_plan = {
        "capital_reference_vnd": 100_000_000,
        "risk_per_trade_pct": 0.01,
        "stop_loss": 120,
        "target_1": 140,
        "target_2": 145,
        "reward_risk": 2,
        "position_shares": None,
        "risk_budget_vnd": 1_000_000,
        "risk_per_share": 9,
    }
    decision = {"status": "NO_EDGE", "failed_checks": ["backtest_net_edge"], "checks": {"backtest_net_edge": False}, "reasons": []}
    config = {"symbol": "HCM", "source": "VCI", "forecast_sessions": 2}

    write_report(
        config,
        frame,
        forecast,
        levels,
        metrics,
        {"xgboost": 0.53, "logistic_regression": 0.49},
        technical,
        fundamentals,
        news,
        risk_plan,
        decision,
        tmp_path / "analysis_report.md",
    )
    write_dashboard(
        config,
        frame,
        forecast,
        levels,
        metrics,
        {"xgboost": 0.53, "logistic_regression": 0.49},
        technical,
        fundamentals,
        news,
        risk_plan,
        decision,
        tmp_path / "dashboard.html",
    )

    markdown = (tmp_path / "analysis_report.md").read_text(encoding="utf-8")
    html = (tmp_path / "dashboard.html").read_text(encoding="utf-8")
    assert "Breakdown trước phí / sau phí" in markdown
    assert "Nếu chưa có cổ phiếu: WAIT" in markdown
    assert "Nếu đang nắm giữ" in markdown
    assert "Model health" in markdown
    assert "Khuyến nghị hành động sau phí" in markdown
    assert "Kịch bản trước chi phí" in markdown
    assert "Kịch bản sau chi phí" in markdown
    assert "Kiểm thử kịch bản lịch sử (không phải khuyến nghị giao dịch)" in markdown
    assert "Gross trước phí" in markdown
    assert "Net sau phí" in markdown
    assert "Ngưỡng 0.60" in markdown
    assert "Giới hạn 10 vòng" in markdown
    assert "Giới hạn 1 vòng" in markdown
    assert "mạnh nhất" not in markdown
    assert "Không mở vị thế mới" in markdown
    assert "Mua mới" in html
    assert "Đang giữ" in html
    assert "Khuyến nghị hành động sau phí" in html
    assert "WAIT" in html
    assert "Ngưỡng theo dõi" in html
    assert "Chi phí & vòng lệnh" not in html
    assert "Breakdown trước phí / sau phí" not in html
    assert "Kiểm thử kịch bản lịch sử (không phải khuyến nghị giao dịch)" not in html
    assert "nghiên cứu OOS" not in html
    assert "Giới hạn 10 vòng" not in html
    assert "mạnh nhất" not in html
    assert "+18.0%" in html
    assert "-12.0%" in html
    assert 'id="theme-toggle"' in html
    assert 'id="market-canvas"' in html
    assert 'id="market-chart-data"' in html
    assert 'data-mode="candle"' in html
    assert 'data-overlay="bollinger"' in html
    assert 'data-indicator="macd"' in html
    assert 'data-tool="trend"' in html
    assert 'data-tool="horizontal"' in html
    assert 'data-tool="fib"' in html
    assert "Cuộn để zoom" in html
    assert "https://cdn" not in html
    assert html.index('id="technical"') < html.index('id="overview"')
    assert "Lệnh mới hôm nay" in html
    assert "Vốn giả định" in html
    assert 'id="assumed-capital-input"' in html
    assert "Chỉ quy đổi tiền minh họa" in html
    assert "vn-stock-analysis-assumed-capital-vnd" in html
