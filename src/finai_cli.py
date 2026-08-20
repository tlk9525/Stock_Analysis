from __future__ import annotations

import argparse
import copy
import json
import shutil
import signal
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime
from io import StringIO
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from src.ai.ollama_report import analyze_report, apply_source_grounding, build_report_context
from src.config import PROJECT_ROOT, load_config, resolve_config
from src.main import run_once
from src.panel_main import resolve_panel_config, run_panel_once
from src.portfolio.service import create_portfolio, portfolio_summary, record_transaction
from src.reports.dashboard import enhance_dashboard_with_research
from src.research.news_history import (
    append_news_history,
    collect_live_news_history,
    export_news_history_from_reports,
    news_reader_snapshot_to_history_frame,
)
from src.research.live_web import (
    fetch_live_research,
    read_live_articles,
    write_live_research,
    write_news_reader,
)
from src.symbol_news_model import run_symbol_news_model
from src.web_server import serve as serve_workspace


app = typer.Typer(help="CLI nghiên cứu cổ phiếu Việt Nam có guard ML và portfolio ledger.")
portfolio_app = typer.Typer(help="Quản lý danh mục theo transaction ledger.")
ai_app = typer.Typer(help="Phân tích report đã có bằng Ollama local.")
app.add_typer(portfolio_app, name="portfolio")
app.add_typer(ai_app, name="ai")
console = Console()


@app.command("web")
def web_workspace(
    host: str = typer.Option("127.0.0.1", help="Host local để mở workspace."),
    port: int = typer.Option(8787, min=1024, max=65535, help="Cổng local của workspace."),
) -> None:
    """Mở web workspace local để nhập mã và chạy pipeline dưới dạng job nền."""

    serve_workspace(host=host, port=port)


class QuietStepError(Exception):
    def __init__(self, output: str, cause: BaseException) -> None:
        super().__init__(str(cause))
        self.output = output
        self.cause = cause


class StepTimeoutError(TimeoutError):
    pass


def _latest_report(symbol: str) -> Path:
    root = PROJECT_ROOT / "reports" / symbol.strip().upper()
    candidates = sorted(
        path
        for path in root.glob("*")
        if path.is_dir()
        and (
            (path / "signal_decision.json").exists()
            or (path / "all_files" / "signal_decision.json").exists()
        )
    )
    if not candidates:
        raise typer.BadParameter(
            f"Chưa có report cho {symbol.upper()}. Hãy chạy `finai analyze {symbol.upper()}` trước."
        )
    return candidates[-1]


def _artifact_directory(report_directory: Path) -> Path:
    if (report_directory / "signal_decision.json").exists():
        return report_directory
    nested = report_directory / "all_files"
    if (nested / "signal_decision.json").exists():
        return nested
    return report_directory


def _report_directories(report_directory: Path) -> tuple[Path, Path]:
    """Return the writable artifact directory and the user-facing dashboard directory.

    ``stockrun full`` moves the generated artifacts into ``all_files`` but
    leaves a compact ``dashboard_report`` beside it.  Follow-up commands must
    update the artifacts first, then refresh that compact copy; otherwise a
    later ``research`` or ``ai analyze`` appears to succeed but is invisible
    in the report users were told to open.
    """

    report_root = report_directory.parent if report_directory.name == "dashboard_report" else report_directory
    artifact_directory = _artifact_directory(report_root)
    dashboard_directory = report_root / "dashboard_report"
    if not dashboard_directory.is_dir():
        dashboard_directory = artifact_directory
    return artifact_directory, dashboard_directory


def _refresh_dashboard_copy(artifact_directory: Path, dashboard_directory: Path) -> None:
    """Synchronize the generated dashboard when a full report has been packaged."""

    if artifact_directory.resolve() != dashboard_directory.resolve():
        _copy_if_exists(artifact_directory / "dashboard.html", dashboard_directory / "dashboard.html")


def _run_quietly(operation, *, timeout_seconds: int | None = None):
    """Capture noisy providers so the one-command workflow only prints its report path."""

    output = StringIO()
    previous_handler = None

    def _timeout_handler(signum, frame):
        raise StepTimeoutError(f"Quá {timeout_seconds} giây.")

    try:
        if timeout_seconds is not None and timeout_seconds > 0:
            previous_handler = signal.signal(signal.SIGALRM, _timeout_handler)
            signal.setitimer(signal.ITIMER_REAL, timeout_seconds)
        with redirect_stdout(output), redirect_stderr(output):
            result = operation()
    except BaseException as exc:
        raise QuietStepError(output.getvalue(), exc) from exc
    finally:
        if timeout_seconds is not None and timeout_seconds > 0:
            signal.setitimer(signal.ITIMER_REAL, 0)
            if previous_handler is not None:
                signal.signal(signal.SIGALRM, previous_handler)
    return result, output.getvalue()


def _write_final_report(report_directory: Path, ai_result: dict) -> Path:
    """Combine the deterministic ML report with the grounded Ollama result."""

    base_path = report_directory / "analysis_report.md"
    base_report = base_path.read_text(encoding="utf-8").rstrip() if base_path.exists() else "# Báo cáo"
    sources = ai_result.get("sources", []) or []
    risks = ai_result.get("risks", []) or []
    evidence = ai_result.get("evidence", []) or []
    lines = [
        base_report,
        "",
        "---",
        "",
        "## Tổng hợp AI từ report và tin web",
        "",
        f"- Trạng thái quyết định: {ai_result.get('decision_status', 'UNKNOWN')}.",
        f"- Tóm tắt: {ai_result.get('summary', 'Không có tóm tắt.')}",
        f"- Góc nhìn kỹ thuật: {ai_result.get('technical_view', 'N/A')}",
        f"- Góc nhìn cơ bản: {ai_result.get('fundamental_view', 'N/A')}",
        f"- Tin doanh nghiệp: {ai_result.get('news_view', 'N/A')}",
        f"- Live research: {ai_result.get('live_research_view', 'N/A')}",
        "",
        "### Bằng chứng",
        "",
        *(f"- {item}" for item in evidence),
        "",
        "### Rủi ro cần kiểm chứng",
        "",
        *(f"- {item}" for item in risks),
        "",
        "### Nguồn live research",
        "",
        *(
            f"- [{item.get('publisher', 'Nguồn')}] {item.get('title', 'Không có tiêu đề')} "
            f"({item.get('published_at') or 'không rõ thời gian'}): {item.get('url', '')}"
            for item in sources
        ),
        "",
        f"Lưu ý: {ai_result.get('disclaimer', 'Không phải khuyến nghị mua/bán.')}",
        "",
    ]
    (report_directory / "ai_analysis.json").write_text(
        json.dumps(ai_result, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    output_path = report_directory / "final_report.md"
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def _append_symbol_news_model_section(
    final_report: Path,
    symbol_news_report: Path,
    impact_summary: dict | None = None,
    display_symbol_news_report: Path | None = None,
) -> None:
    summary_path = symbol_news_report / "symbol_news_model_summary.json"
    probabilities_path = symbol_news_report / "latest_probabilities.json"
    metrics_path = symbol_news_report / "model_metrics.json"
    if not summary_path.exists() or not probabilities_path.exists() or not metrics_path.exists():
        return
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    probabilities = json.loads(probabilities_path.read_text(encoding="utf-8"))
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    xgboost_metrics = metrics.get("xgboost", {}) or {}
    backtest = metrics.get("backtest", {}) or {}
    section = [
        "",
        "---",
        "",
        "## News model riêng từng mã",
        "",
        f"- Symbol-news report: `{display_symbol_news_report or symbol_news_report}`",
        f"- Số bài tin trong CSV cho mã: {summary.get('symbol_article_count', 0)}",
        f"- Số dòng giá có news feature: {summary.get('feature_rows_with_news', 0)}",
        f"- XGBoost probability mới nhất: {float(probabilities.get('xgboost', 0.0)):.3f}",
        f"- AUC OOS: {float(xgboost_metrics.get('roc_auc') or 0.0):.3f}",
        f"- Balanced accuracy OOS: {float(xgboost_metrics.get('balanced_accuracy') or 0.0):.3f}",
        f"- Backtest total return: {float(backtest.get('total_return') or 0.0):.3f}",
        *(
            [
                f"- Base XGBoost probability: {float(impact_summary.get('base_xgboost_probability') or 0.0):.3f}",
                f"- Chênh lệch News-adjusted - Base: {float(impact_summary.get('probability_delta') or 0.0):+.3f}",
                f"- Áp vào signal chính: {impact_summary.get('effect_on_primary_signal', 'not_applied')}",
                f"- Trạng thái news model: {impact_summary.get('status', 'research_only')}",
                f"- Gate chưa đạt: {', '.join(impact_summary.get('failed_gates') or []) or 'Không'}",
            ]
            if impact_summary
            else []
        ),
        "",
        "News-adjusted model hiện là lớp kiểm chứng/shadow; signal chính vẫn do `signal_decision.json` quyết định.",
        "",
        "Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.",
        "",
    ]
    with final_report.open("a", encoding="utf-8") as file:
        file.write("\n".join(section))


def _fallback_ai_result(report_directory: Path, reason: str | None = None) -> dict:
    context = build_report_context(_artifact_directory(report_directory))
    result = apply_source_grounding(
        {
            "summary": "",
            "technical_view": "",
            "fundamental_view": "",
            "news_view": "",
            "live_research_view": "",
            "risks": [],
            "decision_status": "NO_EDGE",
            "evidence": [],
            "sources": [],
            "disclaimer": "",
        },
        context,
    )
    if reason:
        result["risks"] = [
            *result.get("risks", []),
            f"Ollama AI chưa hoàn tất trong lệnh full: {reason}",
        ]
        result["live_research_view"] = (
            str(result.get("live_research_view") or "")
            + " Final report dùng fallback grounded từ artifact local."
        )
    return result


def _copy_if_exists(source: Path, destination: Path) -> None:
    if source.exists() and source.is_file():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def _read_json_file(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _to_float(value: object) -> float | None:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _write_news_impact_summary(
    report_directory: Path,
    symbol_news_report: Path | None,
    final_symbol_news_report: Path | None = None,
) -> dict | None:
    """Write an explicit shadow comparison between base ML and news-adjusted ML."""

    if symbol_news_report is None or not symbol_news_report.exists():
        return None
    summary = _read_json_file(symbol_news_report / "symbol_news_model_summary.json")
    probabilities = _read_json_file(symbol_news_report / "latest_probabilities.json")
    metrics = _read_json_file(symbol_news_report / "model_metrics.json")
    feature_importance = _read_json_file(symbol_news_report / "feature_importance.json")
    if not summary or not probabilities or not metrics:
        return None

    base_probabilities = _read_json_file(report_directory / "latest_probabilities.json")
    decision = _read_json_file(report_directory / "signal_decision.json")
    xgboost_metrics = metrics.get("xgboost", {}) or {}
    backtest = metrics.get("backtest", {}) or {}
    news_feature_importance = {
        key: _to_float(value) or 0.0
        for key, value in feature_importance.items()
        if str(key).startswith("news_")
    }
    sorted_news_importance = dict(
        sorted(news_feature_importance.items(), key=lambda item: item[1], reverse=True)
    )
    article_count = int(summary.get("symbol_article_count") or 0)
    feature_rows_with_news = int(summary.get("feature_rows_with_news") or 0)
    news_importance_gain_sum = float(sum(sorted_news_importance.values()))
    auc = _to_float(xgboost_metrics.get("roc_auc"))
    balanced_accuracy = _to_float(xgboost_metrics.get("balanced_accuracy"))
    base_xgb = _to_float(base_probabilities.get("xgboost"))
    news_xgb = _to_float(probabilities.get("xgboost"))

    gates = {
        "min_articles_60": article_count >= 60,
        "min_feature_rows_30": feature_rows_with_news >= 30,
        "news_feature_gain_positive": news_importance_gain_sum > 0,
        "auc_at_least_0_55": auc is not None and auc >= 0.55,
        "balanced_accuracy_at_least_0_52": balanced_accuracy is not None and balanced_accuracy >= 0.52,
    }
    failed_gates = [name for name, passed in gates.items() if not passed]
    readiness = "shadow_review" if not failed_gates else "research_only"
    impact = {
        "symbol": summary.get("symbol"),
        "status": readiness,
        "effect_on_primary_signal": "not_applied",
        "primary_signal_status": decision.get("status"),
        "base_xgboost_probability": base_xgb,
        "news_adjusted_xgboost_probability": news_xgb,
        "probability_delta": None if base_xgb is None or news_xgb is None else news_xgb - base_xgb,
        "news_model_auc": auc,
        "news_model_balanced_accuracy": balanced_accuracy,
        "news_model_backtest_total_return": _to_float(backtest.get("total_return")),
        "symbol_article_count": article_count,
        "feature_rows_with_news": feature_rows_with_news,
        "news_feature_importance_gain": sorted_news_importance,
        "news_feature_importance_gain_sum": news_importance_gain_sum,
        "gates": gates,
        "failed_gates": failed_gates,
        "artifact_paths": {
            "base_report": str(report_directory),
            "symbol_news_report": str(final_symbol_news_report or symbol_news_report),
            "news_articles_csv": str(summary.get("articles_csv")),
        },
        "recommendation": (
            "Chỉ hiển thị như shadow/research, chưa thay signal chính."
            if failed_gates
            else "Đủ điều kiện xem xét ở chế độ shadow; vẫn cần kiểm định thêm trước khi thay signal chính."
        ),
        "limitation": summary.get("limitation"),
    }
    (report_directory / "news_impact_summary.json").write_text(
        json.dumps(impact, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    return impact


def _organize_full_report(
    report_directory: Path,
    *,
    symbol_news_report: Path | None,
) -> tuple[Path, Path]:
    all_files = report_directory / "all_files"
    dashboard_report = report_directory / "dashboard_report"
    dashboard_report.mkdir(parents=True, exist_ok=True)

    if not all_files.exists():
        all_files.mkdir()
        for path in list(report_directory.iterdir()):
            if path.name in {"all_files", "dashboard_report"}:
                continue
            shutil.move(str(path), str(all_files / path.name))

    if symbol_news_report is not None and symbol_news_report.exists():
        target_news_dir = all_files / "symbol_news_model"
        if symbol_news_report.resolve() != target_news_dir.resolve():
            if target_news_dir.exists():
                shutil.rmtree(target_news_dir)
            shutil.move(str(symbol_news_report), str(target_news_dir))
        symbol_news_report = target_news_dir

    for name in [
        "dashboard.html",
        "final_report.md",
        "analysis_report.md",
        "stockrun.log",
        "technical_chart.png",
        "forecast_chart.png",
        "history_chart.png",
        "ai_analysis.json",
        "news_impact_summary.json",
    ]:
        _copy_if_exists(all_files / name, dashboard_report / name)
    if symbol_news_report is not None:
        _copy_if_exists(
            symbol_news_report / "symbol_news_model_summary.json",
            dashboard_report / "symbol_news_model_summary.json",
        )
        _copy_if_exists(
            symbol_news_report / "latest_probabilities.json",
            dashboard_report / "symbol_news_latest_probabilities.json",
        )
        _copy_if_exists(
            symbol_news_report / "model_metrics.json",
            dashboard_report / "symbol_news_model_metrics.json",
        )
        _copy_if_exists(
            symbol_news_report / "feature_importance.json",
            dashboard_report / "symbol_news_feature_importance.json",
        )
    return all_files, dashboard_report


@app.command()
def doctor() -> None:
    """Kiểm tra cấu hình local trước khi chạy phân tích."""

    config = load_config()
    table = Table(title="FinAI doctor")
    table.add_column("Hạng mục")
    table.add_column("Giá trị")
    table.add_row("Project", str(PROJECT_ROOT))
    table.add_row("PostgreSQL URL", str(config.get("database_url")))
    table.add_row("Nguồn VN", str(config.get("source")))
    table.add_row("Ollama model mặc định", "qwen3:1.7b")
    table.add_row("ML guard", "Bật: NO_EDGE được giữ nguyên")
    console.print(table)


@app.command()
def analyze(
    symbol: str = typer.Argument(..., help="Mã VN, ví dụ FPT/HPG/VCB."),
    source: str | None = typer.Option(None, help="Nguồn vnstock, ví dụ VCI."),
    forecast_sessions: int | None = typer.Option(None, min=1),
    no_postgres: bool = typer.Option(False, help="Không lưu report vào PostgreSQL."),
) -> Path:
    """Chạy pipeline ML hiện có cho một mã và in vị trí report."""

    args = argparse.Namespace(
        symbol=symbol,
        symbol_option=None,
        source=source,
        forecast_sessions=forecast_sessions,
        run_time=None,
        database_url=None,
        no_postgres=no_postgres,
    )
    config = resolve_config(load_config(), args)
    report_directory = run_once(config)
    decision = json.loads((report_directory / "signal_decision.json").read_text(encoding="utf-8"))
    console.print(f"[bold green]Đã tạo report:[/] {report_directory}")
    console.print(f"ML decision: [bold]{decision.get('status', 'UNKNOWN')}[/]")
    return report_directory


@app.command()
def rank(
    symbols: str | None = typer.Option(None, help="Danh sách ngăn cách bởi dấu phẩy."),
    universe: str | None = typer.Option(
        None,
        help="configured hoặc all-vietnam (snapshot HOSE/HNX/UPCOM).",
    ),
    universe_csv: Path | None = typer.Option(
        None, help="Registry point-in-time có available_at/listed_at/delisted_at."
    ),
    max_symbols: int | None = typer.Option(None, min=2, help="Chỉ dùng smoke test."),
    horizons: str | None = typer.Option(None, help="Ví dụ: 5,20."),
    top_k: int | None = typer.Option(None, min=1),
    news_articles_csv: Path | None = typer.Option(
        None,
        "--news-articles-csv",
        help="CSV lịch sử tin có available_at để huấn luyện Base + News.",
    ),
    use_news: bool = typer.Option(
        False,
        "--use-news",
        help="Bật feature tin; cần --news-articles-csv.",
    ),
    foreign_flow_csv: Path | None = typer.Option(
        None, help="CSV dòng vốn ngoại point-in-time."
    ),
    no_postgres: bool = typer.Option(False),
) -> None:
    """Chạy panel XGBoost/ranking trên nhiều mã VN."""

    args = argparse.Namespace(
        symbols=symbols.split(",") if symbols else None,
        benchmark=None,
        horizons=[int(value.strip()) for value in horizons.split(",")] if horizons else None,
        top_k=top_k,
        source=None,
        start_date=None,
        end_date=None,
        min_train_dates=None,
        validation_dates=None,
        test_dates=None,
        step_dates=None,
        max_folds=None,
        min_symbols_per_date=None,
        model_kind=None,
        transaction_cost_bps=None,
        news_articles_csv=news_articles_csv,
        use_news=use_news,
        database_url=None,
        no_postgres=no_postgres,
        universe=universe,
        universe_csv=universe_csv,
        exchanges=None,
        max_symbols=max_symbols,
        foreign_flow_csv=foreign_flow_csv,
        max_positions=None,
    )
    config = resolve_panel_config(copy.deepcopy(load_config()), args)
    report_directory = run_panel_once(config)
    console.print(f"[bold green]Đã tạo panel report:[/] {report_directory}")


@app.command("export-news-history")
def export_news_history(
    symbols: str | None = typer.Option(None, help="Danh sách mã ngăn cách bởi dấu phẩy."),
    output: Path = typer.Option(
        PROJECT_ROOT / "data" / "news_history.csv",
        "--output",
        help="CSV output cho --news-articles-csv.",
    ),
) -> None:
    """Xuất CSV news_history từ các News Reader snapshot đã lưu."""

    selected = [value.strip() for value in symbols.split(",")] if symbols else None
    frame = export_news_history_from_reports(
        PROJECT_ROOT / "reports",
        output,
        symbols=selected,
    )
    console.print(f"[green]Đã xuất {len(frame)} dòng news history:[/] {output}")
    console.print(
        "[yellow]Lưu ý:[/] dữ liệu này dựng từ live snapshot đã lưu, "
        "phù hợp để chạy thử Base + News; chưa phải bộ lịch sử production."
    )


@app.command("collect-news")
def collect_news(
    symbols: str = typer.Option(..., help="Danh sách mã ngăn cách bởi dấu phẩy."),
    output: Path = typer.Option(
        PROJECT_ROOT / "data" / "news_articles.csv",
        "--output",
        help="CSV tích lũy cho train-symbol-news hoặc --news-articles-csv.",
    ),
    hours: int = typer.Option(720, min=1, max=720),
    limit: int = typer.Option(20, min=1, max=30),
    read_limit: int = typer.Option(10, min=1, max=10),
) -> None:
    """Đọc tin nhiều mã và append vào CSV news tích lũy."""

    selected = [value.strip() for value in symbols.split(",") if value.strip()]
    frame, summaries = collect_live_news_history(
        selected,
        output,
        hours=hours,
        limit=limit,
        read_limit=read_limit,
    )
    table = Table(title="Collect news")
    table.add_column("Symbol")
    table.add_column("RSS")
    table.add_column("Read")
    table.add_column("Filtered")
    table.add_column("Exported")
    for item in summaries:
        table.add_row(
            item["symbol"],
            str(item["rss_article_count"]),
            str(item["read_article_count"]),
            str(item["failed_or_filtered_count"]),
            str(item["exported_rows"]),
        )
    console.print(table)
    console.print(f"[green]CSV hiện có {len(frame)} dòng:[/] {output}")
    console.print(
        "[yellow]Lưu ý:[/] đây là kho tin tích lũy từ live reads. "
        "Muốn production cần chạy đều mỗi ngày và lưu đủ lịch sử."
    )


@app.command("train-symbol-news")
def train_symbol_news(
    symbol: str = typer.Argument(..., help="Mã VN, ví dụ MBB/TCB/VCB."),
    news_articles_csv: Path = typer.Option(
        PROJECT_ROOT / "data" / "news_articles.csv",
        "--news-articles-csv",
        help="CSV tin đã có available_at.",
    ),
    lookback_days: int = typer.Option(5, min=1, max=60),
) -> None:
    """Train XGBoost riêng một mã với feature tin point-in-time."""

    report_directory = run_symbol_news_model(
        load_config(),
        symbol=symbol,
        news_articles_csv=news_articles_csv,
        lookback_days=lookback_days,
    )
    console.print(f"[bold green]Đã tạo symbol-news report:[/] {report_directory}")


@app.command()
def research(
    symbol: str = typer.Argument(..., help="Mã VN, ví dụ FPT/HPG/VCB."),
    limit: int = typer.Option(10, min=1, max=30),
    hours: int = typer.Option(72, min=1, max=720),
    read_articles: bool = typer.Option(True, "--read/--no-read", help="Đọc và trích đoạn bài gốc sau khi lấy RSS."),
    read_limit: int = typer.Option(5, min=1, max=10, help="Số bài gốc tối đa cần đọc."),
    report_dir: Path | None = typer.Option(None, exists=True, file_okay=False),
) -> None:
    """Lấy RSS, tùy chọn đọc bài gốc và lưu snapshot có nguồn vào report."""

    requested_directory = report_dir or _latest_report(symbol)
    directory, dashboard_directory = _report_directories(requested_directory)
    fundamentals_path = directory / "fundamental_summary.json"
    fundamentals = json.loads(fundamentals_path.read_text(encoding="utf-8")) if fundamentals_path.exists() else {}
    company = fundamentals.get("company", {}) or {}
    company_name = company.get("organ_name") or company.get("organ_short_name")
    try:
        snapshot = fetch_live_research(
            symbol,
            company_name=company_name,
            limit=limit,
            hours=hours,
        )
    except Exception as exc:
        console.print(f"[red]Không lấy được live research:[/] {exc}")
        raise typer.Exit(code=1) from exc
    output = write_live_research(directory, snapshot)
    enhance_dashboard_with_research(directory)
    _refresh_dashboard_copy(directory, dashboard_directory)
    table = Table(title=f"Live research: {symbol.upper()}")
    table.add_column("Publisher")
    table.add_column("Headline")
    table.add_column("Published")
    for article in snapshot["articles"]:
        table.add_row(article["publisher"], article["title"], article["published_at"] or "N/A")
    console.print(table)
    console.print(f"[green]Đã lưu {snapshot['article_count']} bài:[/] {output}")
    if not read_articles:
        return
    reader_snapshot = read_live_articles(snapshot, limit=read_limit)
    reader_output = write_news_reader(directory, reader_snapshot)
    enhance_dashboard_with_research(directory)
    _refresh_dashboard_copy(directory, dashboard_directory)
    reader_table = Table(title=f"News Reader: {symbol.upper()}")
    reader_table.add_column("Nguồn")
    reader_table.add_column("Tiêu đề")
    reader_table.add_column("Nhóm")
    for article in reader_snapshot["articles"]:
        reader_table.add_row(
            article["publisher"],
            article["title"],
            ", ".join(article["topics"]) or "khác",
        )
    console.print(reader_table)
    console.print(
        f"[green]Đã đọc/trích {reader_snapshot['read_article_count']} bài; "
        f"lọc/lỗi {reader_snapshot['failed_or_filtered_count']} bài:[/] {reader_output}"
    )


@portfolio_app.command("create")
def portfolio_create(
    name: str,
    base_currency: str = typer.Option("VND"),
) -> None:
    result = create_portfolio(name, base_currency)
    console.print(f"[green]Đã tạo portfolio[/] {result['name']} ({result['base_currency']})")


def _record_trade(
    side: str,
    portfolio: str,
    symbol: str,
    quantity: str,
    price: str,
    fee: str,
    market: str,
    currency: str,
    notes: str | None,
) -> None:
    result = record_transaction(
        portfolio,
        side=side,
        symbol=symbol,
        quantity=quantity,
        price=price,
        fee=fee,
        market=market,
        currency=currency,
        notes=notes,
        executed_at=datetime.now().astimezone(),
    )
    realized = result["realized_pnl"]
    suffix = "" if realized is None else f"; realized P/L={realized}"
    console.print(f"[green]Đã ghi {result['side']} {result['symbol']}[/]{suffix}")


@portfolio_app.command("buy")
def portfolio_buy(
    portfolio: str,
    symbol: str,
    quantity: str = typer.Option(..., "--qty"),
    price: str = typer.Option(...),
    fee: str = typer.Option("0"),
    market: str = typer.Option("VN"),
    currency: str = typer.Option("VND"),
    notes: str | None = typer.Option(None),
) -> None:
    _record_trade("BUY", portfolio, symbol, quantity, price, fee, market, currency, notes)


@portfolio_app.command("sell")
def portfolio_sell(
    portfolio: str,
    symbol: str,
    quantity: str = typer.Option(..., "--qty"),
    price: str = typer.Option(...),
    fee: str = typer.Option("0"),
    market: str = typer.Option("VN"),
    currency: str = typer.Option("VND"),
    notes: str | None = typer.Option(None),
) -> None:
    _record_trade("SELL", portfolio, symbol, quantity, price, fee, market, currency, notes)


@portfolio_app.command("summary")
def portfolio_summary_command(name: str) -> None:
    result = portfolio_summary(name)
    table = Table(title=f"Portfolio: {result['name']}")
    table.add_column("Mã")
    table.add_column("Market")
    table.add_column("Số lượng", justify="right")
    table.add_column("Giá vốn TB", justify="right")
    table.add_column("Cost basis", justify="right")
    for position in result["positions"]:
        table.add_row(
            position["symbol"],
            position["market"],
            str(position["quantity"]),
            str(position["average_cost"]),
            str(position["cost_basis"]),
        )
    console.print(table)
    console.print(f"Realized P/L: {result['realized_pnl']} | Giao dịch: {result['transaction_count']}")


@ai_app.command("analyze")
def ai_analyze(
    symbol: str,
    model: str = typer.Option("qwen3:1.7b"),
    report_dir: Path | None = typer.Option(None, exists=True, file_okay=False),
) -> dict:
    """Dùng Ollama để giải thích artifact report, không tạo dữ liệu thị trường mới."""

    directory, dashboard_directory = _report_directories(report_dir or _latest_report(symbol))
    try:
        result = analyze_report(directory, model=model)
    except (RuntimeError, ValueError) as exc:
        console.print(f"[red]AI analysis chưa chạy:[/] {exc}")
        raise typer.Exit(code=1) from exc
    (directory / "ai_analysis.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    enhance_dashboard_with_research(directory, result)
    _refresh_dashboard_copy(directory, dashboard_directory)
    console.print_json(json.dumps(result, ensure_ascii=False, default=str))
    return result


@app.command("full")
def full_analysis(
    symbol: str = typer.Argument(..., help="Mã VN, ví dụ FPT/HPG/VCB."),
    source: str | None = typer.Option(None, help="Nguồn vnstock, ví dụ VCI."),
    forecast_sessions: int | None = typer.Option(None, min=1),
    no_postgres: bool = typer.Option(False, help="Không lưu report vào PostgreSQL."),
    hours: int = typer.Option(168, min=1, max=720, help="Khoảng thời gian lấy tin, mặc định 7 ngày."),
    limit: int = typer.Option(10, min=1, max=30, help="Số headline tối đa cần lấy."),
    read_articles: bool = typer.Option(True, "--read/--no-read", help="Đọc bài gốc sau khi lấy RSS."),
    read_limit: int = typer.Option(5, min=1, max=10, help="Số bài gốc tối đa cần đọc."),
    train_news_model: bool = typer.Option(
        True,
        "--train-news-model/--no-train-news-model",
        help="Append tin vừa đọc vào CSV và train model riêng từng mã.",
    ),
    news_articles_csv: Path = typer.Option(
        PROJECT_ROOT / "data" / "news_articles.csv",
        "--news-articles-csv",
        help="CSV tích lũy cho symbol-news model.",
    ),
    news_lookback_days: int = typer.Option(5, min=1, max=60),
    model: str = typer.Option("qwen3:1.7b", help="Model Ollama dùng để đọc report."),
    ai_timeout_seconds: int = typer.Option(
        45,
        min=5,
        max=600,
        help="Timeout cho bước Ollama AI; quá hạn sẽ dùng fallback artifact local.",
    ),
) -> None:
    """Chạy ML, lấy tin, AI và news model riêng trong một lệnh."""

    normalized_symbol = symbol.strip().upper()
    report_directory: Path | None = None
    symbol_news_report: Path | None = None
    logs: list[str] = []
    current_step = "ML report"
    try:
        typer.echo(f"[1/4] ML report {normalized_symbol}...")
        report_directory, output = _run_quietly(
            lambda: analyze(
                normalized_symbol,
                source=source,
                forecast_sessions=forecast_sessions,
                no_postgres=no_postgres,
            )
        )
        logs.append("[ML report]\n" + output)
        current_step = "Live research"
        typer.echo(f"[2/4] Live research + News Reader {normalized_symbol}...")
        _, output = _run_quietly(
            lambda: research(
                normalized_symbol,
                limit=limit,
                hours=hours,
                read_articles=read_articles,
                read_limit=read_limit,
                report_dir=report_directory,
            )
        )
        logs.append("[Live research]\n" + output)
        if train_news_model:
            current_step = "Symbol news model"
            typer.echo(f"[3/4] Append news + train symbol-news model {normalized_symbol}...")
            news_reader_path = report_directory / "news_reader.json"
            if news_reader_path.exists():
                reader_snapshot = json.loads(news_reader_path.read_text(encoding="utf-8"))
                news_rows = news_reader_snapshot_to_history_frame(reader_snapshot)
                append_news_history(news_articles_csv, news_rows)
            symbol_news_report, output = _run_quietly(
                lambda: run_symbol_news_model(
                    load_config(),
                    symbol=normalized_symbol,
                    news_articles_csv=news_articles_csv,
                    lookback_days=news_lookback_days,
                )
            )
            logs.append("[Symbol news model]\n" + output)
        current_step = "Ollama AI"
        typer.echo(f"[4/4] AI summary {normalized_symbol}...")
        try:
            ai_result, output = _run_quietly(
                lambda: ai_analyze(normalized_symbol, model=model, report_dir=report_directory),
                timeout_seconds=ai_timeout_seconds,
            )
            logs.append("[Ollama AI]\n" + output)
        except QuietStepError as exc:
            reason = f"{type(exc.cause).__name__}: {exc.cause}"
            logs.append(f"[Ollama AI skipped]\n{exc.output}\n{reason}")
            ai_result = _fallback_ai_result(report_directory, reason)
            typer.echo("Ollama AI chưa hoàn tất; dùng fallback grounded từ artifact local.")
    except QuietStepError as exc:
        logs.append(f"[{current_step} failed]\n{exc.output}\n{type(exc.cause).__name__}: {exc.cause}")
        if report_directory is not None:
            (report_directory / "stockrun.log").write_text("\n\n".join(logs), encoding="utf-8")
            typer.echo(f"Không thể hoàn tất {current_step}. Chi tiết: {report_directory / 'stockrun.log'}")
        else:
            typer.echo(f"Không thể hoàn tất {current_step}: {exc.cause}", err=True)
        raise typer.Exit(code=1) from exc

    (report_directory / "stockrun.log").write_text("\n\n".join(logs), encoding="utf-8")
    final_symbol_news_report = (
        report_directory / "all_files" / "symbol_news_model"
        if symbol_news_report is not None
        else None
    )
    final_report = _write_final_report(report_directory, ai_result)
    news_impact_summary = _write_news_impact_summary(
        report_directory,
        symbol_news_report,
        final_symbol_news_report=final_symbol_news_report,
    )
    if train_news_model and symbol_news_report is not None:
        _append_symbol_news_model_section(
            final_report,
            symbol_news_report,
            news_impact_summary,
            display_symbol_news_report=final_symbol_news_report,
        )
    enhance_dashboard_with_research(report_directory, ai_result)
    all_files, dashboard_report = _organize_full_report(
        report_directory,
        symbol_news_report=symbol_news_report,
    )
    typer.echo(f"Báo cáo xem nhanh: {dashboard_report}")
    typer.echo(f"Toàn bộ artifact: {all_files}")


if __name__ == "__main__":
    app()
