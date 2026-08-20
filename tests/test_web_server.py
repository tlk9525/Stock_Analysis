from pathlib import Path

import pytest

from src.web_server import (
    chat_report_directory,
    dashboard_file,
    inject_report_chat_widget,
    list_reports,
    normalize_symbol,
    report_url,
)


def test_normalize_symbol_rejects_non_ticker_input() -> None:
    assert normalize_symbol(" vcb ") == "VCB"
    for value in ("", "VCB; rm -rf /", "VCB1", "FPT/../"):
        with pytest.raises(ValueError):
            normalize_symbol(value)


def test_report_listing_only_exposes_dashboard_files(tmp_path: Path) -> None:
    report = tmp_path / "reports" / "VCB" / "2026-08-19_15-30-00"
    dashboard = report / "dashboard_report" / "dashboard.html"
    dashboard.parent.mkdir(parents=True)
    dashboard.write_text("<html>dashboard</html>", encoding="utf-8")
    (tmp_path / "reports" / "VCB" / "incomplete").mkdir()

    assert dashboard_file(report) == dashboard
    assert report_url(tmp_path, report) == (
        "/reports/VCB/2026-08-19_15-30-00/dashboard_report/dashboard.html"
    )
    assert list_reports(tmp_path, "vcb") == [
        {
            "symbol": "VCB",
            "run_id": "2026-08-19_15-30-00",
            "dashboard_url": "/reports/VCB/2026-08-19_15-30-00/dashboard_report/dashboard.html",
        }
    ]


def test_chat_report_directory_uses_artifact_directory_and_rejects_path_escape(tmp_path: Path) -> None:
    report_root = tmp_path / "reports" / "HPG" / "2026-08-19_15-30-00"
    dashboard = report_root / "dashboard_report" / "dashboard.html"
    dashboard.parent.mkdir(parents=True)
    dashboard.write_text("<html>dashboard</html>", encoding="utf-8")
    artifacts = report_root / "all_files"
    artifacts.mkdir()
    (artifacts / "signal_decision.json").write_text("{}", encoding="utf-8")

    assert chat_report_directory(
        tmp_path,
        "/reports/HPG/2026-08-19_15-30-00/dashboard_report/dashboard.html",
    ) == artifacts
    with pytest.raises(ValueError):
        chat_report_directory(tmp_path, "../../outside/dashboard.html")


def test_old_dashboard_gets_chat_widget_only_once() -> None:
    original = "<html><style>.x{}</style><body><main>Report</main></body></html>"
    rendered = inject_report_chat_widget(original)

    assert 'id="report-chat-launcher"' in rendered
    assert "/api/chat" in rendered
    assert inject_report_chat_widget(rendered) == rendered
