from __future__ import annotations

from src.finai_cli import _refresh_dashboard_copy, _report_directories


def test_follow_up_commands_target_artifacts_and_refresh_compact_full_report(tmp_path) -> None:
    full_report = tmp_path / "2026-08-13_12-00-00"
    artifacts = full_report / "all_files"
    compact_dashboard = full_report / "dashboard_report"
    artifacts.mkdir(parents=True)
    compact_dashboard.mkdir()
    (artifacts / "signal_decision.json").write_text("{}", encoding="utf-8")
    (artifacts / "dashboard.html").write_text("<main>updated</main>", encoding="utf-8")

    resolved_artifacts, resolved_dashboard = _report_directories(full_report)
    assert resolved_artifacts == artifacts
    assert resolved_dashboard == compact_dashboard

    _refresh_dashboard_copy(resolved_artifacts, resolved_dashboard)
    assert (compact_dashboard / "dashboard.html").read_text(encoding="utf-8") == "<main>updated</main>"
