from __future__ import annotations

import argparse
import copy
import json
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


app = typer.Typer(help="CLI nghiên cứu cổ phiếu Việt Nam có guard ML và portfolio ledger.")
portfolio_app = typer.Typer(help="Quản lý danh mục theo transaction ledger.")
ai_app = typer.Typer(help="Phân tích report đã có bằng Ollama local.")
app.add_typer(portfolio_app, name="portfolio")
app.add_typer(ai_app, name="ai")
console = Console()


class QuietStepError(Exception):
    def __init__(self, output: str, cause: BaseException) -> None:
        super().__init__(str(cause))
        self.output = output
        self.cause = cause


def _latest_report(symbol: str) -> Path:
    root = PROJECT_ROOT / "reports" / symbol.strip().upper()
    candidates = sorted(path for path in root.glob("*") if path.is_dir())
    if not candidates:
        raise typer.BadParameter(
            f"Chưa có report cho {symbol.upper()}. Hãy chạy `finai analyze {symbol.upper()}` trước."
        )
    return candidates[-1]


def _run_quietly(operation):
    """Capture noisy providers so the one-command workflow only prints its report path."""

    output = StringIO()
    try:
        with redirect_stdout(output), redirect_stderr(output):
            result = operation()
    except BaseException as exc:
        raise QuietStepError(output.getvalue(), exc) from exc
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
        f"- Symbol-news report: `{symbol_news_report}`",
        f"- Số bài tin trong CSV cho mã: {summary.get('symbol_article_count', 0)}",
        f"- Số dòng giá có news feature: {summary.get('feature_rows_with_news', 0)}",
        f"- XGBoost probability mới nhất: {float(probabilities.get('xgboost', 0.0)):.3f}",
        f"- AUC OOS: {float(xgboost_metrics.get('roc_auc') or 0.0):.3f}",
        f"- Balanced accuracy OOS: {float(xgboost_metrics.get('balanced_accuracy') or 0.0):.3f}",
        f"- Backtest total return: {float(backtest.get('total_return') or 0.0):.3f}",
        "",
        "Lưu ý: news model dùng dữ liệu `available_at` point-in-time trong CSV tích lũy; nếu lịch sử tin còn mỏng thì chỉ xem là research/smoke test.",
        "",
    ]
    with final_report.open("a", encoding="utf-8") as file:
        file.write("\n".join(section))


def _fallback_ai_result(report_directory: Path, reason: str | None = None) -> dict:
    context = build_report_context(report_directory)
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

    directory = report_dir or _latest_report(symbol)
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

    directory = report_dir or _latest_report(symbol)
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
                lambda: ai_analyze(normalized_symbol, model=model, report_dir=report_directory)
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
    final_report = _write_final_report(report_directory, ai_result)
    if train_news_model and symbol_news_report is not None:
        _append_symbol_news_model_section(final_report, symbol_news_report)
    typer.echo(f"Báo cáo: {final_report}")


if __name__ == "__main__":
    app()
