from __future__ import annotations

import html
import os
import tempfile
from pathlib import Path
from typing import Any, Mapping

os.environ.setdefault(
    "MPLCONFIGDIR",
    str(Path(tempfile.gettempdir()) / "vn_stock_analysis_matplotlib"),
)

import matplotlib.pyplot as plt
import pandas as pd

from src.plotting_backend import configure_publication_style, has_cnsplots, save_figure
from src.utils import safe_float

configure_publication_style()


def _percent(value: Any) -> str:
    number = safe_float(value)
    return "N/A" if number is None else f"{number:.2%}"


def _number(value: Any, decimals: int = 3) -> str:
    number = safe_float(value)
    return "N/A" if number is None else f"{number:.{decimals}f}"


def _escape(value: Any) -> str:
    return html.escape(str(value), quote=True)


def build_panel_publish_guard(metrics: dict, config: dict) -> dict:
    """Decide whether OOS evidence is strong enough to publish as research.

    A passing result exposes a ranking, not an automatic buy order.  The guard
    deliberately requires positive cross-sectional skill and positive net
    portfolio performance after the configured round-trip cost.
    """

    options = (config.get("panel", {}) or {}).get("publish_guard", {}) or {}
    ic = metrics.get("rank_ic", {}) or {}
    portfolio = metrics.get("top_k_portfolio", {}) or {}
    thresholds = {
        "min_rank_ic_observations": int(
            options.get("min_rank_ic_observations", 20)
        ),
        "min_portfolio_observations": int(
            options.get("min_portfolio_observations", 12)
        ),
        "min_mean_rank_ic": float(options.get("min_mean_rank_ic", 0.0)),
        "min_rank_ic_hac_t_stat": float(
            options.get("min_rank_ic_hac_t_stat", 1.96)
        ),
        "min_total_return": float(options.get("min_total_return", 0.0)),
        "min_sharpe": float(options.get("min_sharpe", 0.0)),
    }
    checks = {
        "rank_ic_sample": int(ic.get("observations") or 0)
        >= thresholds["min_rank_ic_observations"],
        "portfolio_sample": int(portfolio.get("observations") or 0)
        >= thresholds["min_portfolio_observations"],
        "positive_rank_ic": safe_float(ic.get("mean")) is not None
        and float(ic["mean"]) > thresholds["min_mean_rank_ic"],
        "rank_ic_hac_significance": safe_float(ic.get("hac_t_stat")) is not None
        and float(ic["hac_t_stat"]) >= thresholds["min_rank_ic_hac_t_stat"],
        "positive_net_return": safe_float(portfolio.get("total_return")) is not None
        and float(portfolio["total_return"]) > thresholds["min_total_return"],
        "positive_sharpe": safe_float(portfolio.get("sharpe")) is not None
        and float(portfolio["sharpe"]) > thresholds["min_sharpe"],
    }
    failed = [name for name, passed in checks.items() if not passed]
    return {
        "status": "RESEARCH_OK" if not failed else "NO_EDGE",
        "checks": checks,
        "failed_checks": failed,
        "thresholds": thresholds,
        "meaning": "Chỉ là bảng xếp hạng nghiên cứu; không tự động đặt lệnh.",
    }


def make_panel_performance_chart(
    artifacts: Mapping[int, Mapping[str, Any]], output_path: Path
) -> None:
    if has_cnsplots():
        import cnsplots as cns

        mp = cns.multipanel(max_width=540, title="OOS performance", loc="left")
        plotted = False
        for horizon, artifact in sorted(artifacts.items()):
            backtest = artifact["backtest"]
            if backtest.empty:
                continue

            equity = (1 + backtest["net_return"].fillna(0)).cumprod()
            drawdown = equity / equity.cummax().clip(lower=1.0) - 1

            equity_label = f"h{horizon}_equity"
            drawdown_label = f"h{horizon}_drawdown"

            mp.panel(equity_label, width=240, height=120, pad_top=10)
            ax_equity = mp.get_axes(equity_label)
            ax_equity.plot(equity.index, equity, label=f"Top-k {horizon}d", linewidth=1.6)
            ax_equity.set_title(f"{horizon}d OOS equity")
            ax_equity.set_ylabel("Hệ số tài sản")
            ax_equity.grid(alpha=0.25)
            ax_equity.legend(loc="best")

            mp.panel(drawdown_label, width=240, height=120, pad_top=10)
            ax_drawdown = mp.get_axes(drawdown_label)
            ax_drawdown.plot(drawdown.index, drawdown, label=f"{horizon}d", linewidth=1.3)
            ax_drawdown.set_title(f"{horizon}d OOS drawdown")
            ax_drawdown.set_ylabel("Drawdown")
            ax_drawdown.grid(alpha=0.25)
            ax_drawdown.legend(loc="best")
            plotted = True

        if plotted:
            save_figure(mp.fig, output_path)
            return

    figure, axes = plt.subplots(2, 1, figsize=(13, 8), sharex=False)
    plotted = False
    for horizon, artifact in sorted(artifacts.items()):
        backtest = artifact["backtest"]
        if backtest.empty:
            continue
        equity = (1 + backtest["net_return"].fillna(0)).cumprod()
        axes[0].plot(equity.index, equity, label=f"Top-k {horizon}d", linewidth=1.6)
        drawdown = equity / equity.cummax().clip(lower=1.0) - 1
        axes[1].plot(drawdown.index, drawdown, label=f"{horizon}d", linewidth=1.3)
        plotted = True
    axes[0].set_title("OOS equity sau chi phí")
    axes[0].set_ylabel("Hệ số tài sản")
    axes[1].set_title("OOS drawdown")
    axes[1].set_ylabel("Drawdown")
    for axis in axes:
        axis.grid(alpha=0.25)
        if plotted:
            axis.legend(loc="best")
    figure.tight_layout()
    save_figure(figure, output_path)
    plt.close(figure)


def _ranking_rows(ranking: pd.DataFrame, limit: int = 10) -> list[dict]:
    frame = ranking.reset_index().sort_values("predicted_rank").head(limit)
    return frame.to_dict("records")


def _regime_rows(metrics: dict) -> list[tuple[str, dict]]:
    return sorted((metrics.get("by_regime", {}) or {}).items())


def _prediction_label(result: Any) -> str:
    return "Dự báo excess return" if result.model_kind == "regression" else "Điểm ranking"


def _prediction_text(result: Any, row: dict) -> str:
    if result.model_kind == "regression":
        return _percent(row["prediction"])
    return _number(row["prediction"], 5)


def write_panel_report(
    config: dict,
    price_panel: pd.DataFrame,
    artifacts: Mapping[int, Mapping[str, Any]],
    data_quality: dict,
    output_path: Path,
) -> None:
    panel_options = config["panel"]
    dates = price_panel.index.get_level_values("date")
    symbols = sorted(price_panel.index.get_level_values("symbol").unique())
    lines = [
        "# Báo cáo panel cổ phiếu Việt Nam",
        "",
        f"- Dữ liệu: {dates.min().date()} -> {dates.max().date()}.",
        f"- Universe ({len(symbols)} mã): {', '.join(symbols)}.",
        f"- Benchmark: {panel_options['benchmark_symbol']}.",
        "- Timing: feature sau close t; vào lệnh open t+1; thoát close t+h.",
        f"- Chi phí: {panel_options['transaction_cost_bps']:.1f} bps full round-trip cho từng cohort.",
        f"- Data quarantine: {data_quality.get('quarantined_rows', 0)} dòng.",
        "- Cảnh báo: universe cố định theo cấu hình hiện tại nên vẫn có survivorship bias; cần universe point-in-time trước khi dùng cho nghiên cứu production.",
        "- Cần xác minh dữ liệu giá đã điều chỉnh corporate action nhất quán giữa các mã.",
    ]
    for horizon, artifact in sorted(artifacts.items()):
        metrics = artifact["metrics"]
        guard = metrics["publish_guard"]
        ic = metrics["rank_ic"]
        portfolio = metrics["top_k_portfolio"]
        lines.extend(
            [
                "",
                f"## Horizon {horizon} phiên - {guard['status']}",
                "",
                f"- OOS Rank IC mean: {_number(ic.get('mean'))} ({ic.get('observations', 0)} ngày); HAC t-stat {_number(ic.get('hac_t_stat'), 2)} với lag {ic.get('hac_lag', 0)}.",
                f"- Top-{portfolio.get('top_k')} net return: {_percent(portfolio.get('total_return'))}; Sharpe {_number(portfolio.get('sharpe'), 2)}; max drawdown {_percent(portfolio.get('max_drawdown'))}.",
                f"- Selection turnover trung bình: {_percent(portfolio.get('average_turnover'))}; {portfolio.get('observations', 0)} cohort, mỗi cohort chịu full round-trip cost.",
                f"- Guard fail: {', '.join(guard['failed_checks']) or 'không'}.",
                "",
                f"| Rank | Mã | {_prediction_label(artifact['result'])} | Percentile |",
                "|---:|---|---:|---:|",
            ]
        )
        for row in _ranking_rows(artifact["result"].latest_ranking):
            lines.append(
                f"| {int(row['predicted_rank'])} | {row['symbol']} | "
                f"{_prediction_text(artifact['result'], row)} | {_percent(row['predicted_percentile'])} |"
            )
        if _regime_rows(metrics):
            lines.extend(["", "### Kết quả theo market regime", ""])
            for regime, regime_metrics in _regime_rows(metrics):
                lines.append(
                    f"- {regime}: net return {_percent(regime_metrics.get('total_return'))}; "
                    f"Sharpe {_number(regime_metrics.get('sharpe'), 2)}; "
                    f"Rank IC {_number(regime_metrics.get('rank_ic_mean'))}."
                )
    lines.extend(
        [
            "",
            "Lưu ý: ranking chỉ được xem là bảng xếp hạng nghiên cứu khi guard đạt; không phải khuyến nghị mua/bán.",
        ]
    )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_panel_dashboard(
    config: dict,
    price_panel: pd.DataFrame,
    artifacts: Mapping[int, Mapping[str, Any]],
    output_path: Path,
) -> None:
    dates = price_panel.index.get_level_values("date")
    sections: list[str] = []
    cards: list[str] = []
    for horizon, artifact in sorted(artifacts.items()):
        metrics = artifact["metrics"]
        portfolio = metrics["top_k_portfolio"]
        ic = metrics["rank_ic"]
        guard = metrics["publish_guard"]
        cards.append(
            '<div class="card">'
            f"<small>{horizon} phiên</small><strong>{_escape(guard['status'])}</strong>"
            f"<span>Rank IC {_number(ic.get('mean'))} · HAC t {_number(ic.get('hac_t_stat'), 2)} · Net {_percent(portfolio.get('total_return'))} · Sharpe {_number(portfolio.get('sharpe'), 2)}</span>"
            "</div>"
        )
        rows = "".join(
            "<tr>"
            f"<td>{int(row['predicted_rank'])}</td><td>{_escape(row['symbol'])}</td>"
            f"<td>{_prediction_text(artifact['result'], row)}</td><td>{_percent(row['predicted_percentile'])}</td>"
            "</tr>"
            for row in _ranking_rows(artifact["result"].latest_ranking)
        )
        regime_rows = "".join(
            "<tr>"
            f"<td>{_escape(regime)}</td>"
            f"<td>{_percent(values.get('total_return'))}</td>"
            f"<td>{_number(values.get('sharpe'), 2)}</td>"
            f"<td>{_number(values.get('rank_ic_mean'))}</td>"
            "</tr>"
            for regime, values in _regime_rows(metrics)
        )
        sections.append(
            f"<section><h2>Ranking {horizon} phiên</h2>"
            f"<p>Guard fail: {_escape(', '.join(guard['failed_checks']) or 'không')}</p>"
            f"<table><thead><tr><th>Rank</th><th>Mã</th><th>{_escape(_prediction_label(artifact['result']))}</th><th>Percentile</th></tr></thead>"
            f"<tbody>{rows}</tbody></table>"
            "<h3>Kết quả theo market regime</h3>"
            "<table><thead><tr><th>Regime</th><th>Net return</th><th>Sharpe</th><th>Rank IC</th></tr></thead>"
            f"<tbody>{regime_rows}</tbody></table></section>"
        )
    document = f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>VN Stock Panel Dashboard</title>
<style>
body{{margin:0;background:#f4f6f3;color:#1f2933;font-family:Inter,system-ui,sans-serif}}header,main{{padding:28px clamp(18px,4vw,48px)}}header{{background:#fff;border-bottom:1px solid #d6ddd5}}h1{{margin:6px 0}}.muted,small{{color:#687382}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}}.card,section{{background:#fff;border:1px solid #d6ddd5;border-radius:9px;padding:18px}}.card strong,.card span{{display:block;margin-top:9px}}main{{display:grid;gap:18px}}img{{width:100%;border:1px solid #d6ddd5;border-radius:7px}}table{{width:100%;border-collapse:collapse}}th,td{{padding:10px;text-align:left;border-top:1px solid #e2e8e2}}.note{{color:#687382}}
</style></head><body><header><small>WALK-FORWARD PANEL RESEARCH</small><h1>Bảng xếp hạng cổ phiếu Việt Nam</h1>
<p class="muted">{dates.min().date()} → {dates.max().date()} · Benchmark {_escape(config['panel']['benchmark_symbol'])} · vào open t+1, thoát close t+h.</p></header>
<main><div class="cards">{''.join(cards)}</div><section><h2>OOS performance</h2><img src="panel_performance.png" alt="Panel performance"></section>
{''.join(sections)}<p class="note">Chỉ dùng cho nghiên cứu. NO_EDGE nghĩa là không đủ bằng chứng OOS sau chi phí. Universe cố định vẫn có survivorship bias; cần universe point-in-time và dữ liệu corporate action đáng tin cậy trước khi dùng ở production.</p></main></body></html>"""
    output_path.write_text(document, encoding="utf-8")
