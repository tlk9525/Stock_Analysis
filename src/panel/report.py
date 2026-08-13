from __future__ import annotations

import html
import json
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
from src.utils import clean_json_value, safe_float

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
    frozen = metrics.get("frozen", {}) or {}
    evidence = frozen if frozen else metrics
    ic = evidence.get("rank_ic", {}) or {}
    portfolio = evidence.get("sparse_portfolio", evidence.get("top_k_portfolio", {})) or {}
    development = metrics.get("development", {}) or {}
    development_portfolio = development.get(
        "sparse_portfolio", development.get("top_k_portfolio", {})
    ) or {}
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
        "min_completed_round_trips": int(
            options.get("min_completed_round_trips", 20)
        ),
        "required_cost_stress_multiplier": float(
            options.get("required_cost_stress_multiplier", 1.5)
        ),
        "require_frozen_holdout": bool(
            options.get("require_frozen_holdout", True)
        ),
    }
    stress_key = f"{thresholds['required_cost_stress_multiplier']:g}x"
    stress_metrics = (portfolio.get("cost_stress", {}) or {}).get(stress_key, {})
    checks = {
        "point_in_time_universe": bool(
            (config.get("panel", {}) or {}).get(
                "_universe_point_in_time_complete", False
            )
        ),
        "frozen_holdout_present": bool(frozen)
        or not thresholds["require_frozen_holdout"],
        "entry_rule_selected": int(portfolio.get("completed_round_trips") or 0) > 0,
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
        "enough_completed_round_trips": int(
            portfolio.get("completed_round_trips") or 0
        )
        >= thresholds["min_completed_round_trips"],
        "positive_cost_stress_return": safe_float(
            stress_metrics.get("total_return")
        )
        is not None
        and float(stress_metrics["total_return"]) > thresholds["min_total_return"],
        "positive_cost_stress_sharpe": safe_float(stress_metrics.get("sharpe"))
        is not None
        and float(stress_metrics["sharpe"]) > thresholds["min_sharpe"],
    }
    if development:
        checks["positive_development_net_return"] = safe_float(
            development_portfolio.get("total_return")
        ) is not None and float(development_portfolio["total_return"]) > thresholds[
            "min_total_return"
        ]
    failed = [name for name, passed in checks.items() if not passed]
    return {
        "status": "RESEARCH_OK" if not failed else "NO_EDGE",
        "checks": checks,
        "failed_checks": failed,
        "thresholds": thresholds,
        "evidence_sample": "frozen" if frozen else "development",
        "meaning": "Chỉ phát BUY_CANDIDATE khi frozen gate đạt; hệ thống không tự đặt lệnh.",
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
        f"- Chi phí: {panel_options['transaction_cost_bps']:.1f} bps cho mỗi vị thế mua-bán hoàn tất.",
        f"- Tối đa {panel_options.get('max_positions', panel_options['top_k'])} vị thế; tiền mặt là mặc định nếu không mã nào vượt phí + margin.",
        f"- Data quarantine: {data_quality.get('quarantined_rows', 0)} dòng.",
        (
            "- Universe point-in-time: ĐẠT."
            if (data_quality.get("universe", {}) or {}).get("point_in_time_complete")
            else "- Cảnh báo universe: snapshot/config hiện tại chưa bao gồm đầy đủ mã hủy niêm yết lịch sử; còn survivorship bias."
        ),
        "- Cần xác minh dữ liệu giá đã điều chỉnh corporate action nhất quán giữa các mã.",
    ]
    for horizon, artifact in sorted(artifacts.items()):
        metrics = artifact["metrics"]
        guard = metrics["publish_guard"]
        evidence = metrics.get("frozen", {}) or metrics
        portfolio = evidence.get("sparse_portfolio", evidence["top_k_portfolio"])
        ic = evidence["rank_ic"]
        lines.extend(
            [
                "",
                f"## Horizon {horizon} phiên - {guard['status']}",
                "",
                f"- OOS Rank IC mean: {_number(ic.get('mean'))} ({ic.get('observations', 0)} ngày); HAC t-stat {_number(ic.get('hac_t_stat'), 2)} với lag {ic.get('hac_lag', 0)}.",
                f"- Sparse portfolio net return: {_percent(portfolio.get('total_return'))}; Sharpe {_number(portfolio.get('sharpe'), 2)}; max drawdown {_percent(portfolio.get('max_drawdown'))}.",
                f"- {portfolio.get('completed_round_trips', 0)} vòng hoàn tất; no-trade {_percent(portfolio.get('no_trade_rate'))}; nắm giữ trung bình {_number(portfolio.get('average_holding_sessions'), 1)} phiên.",
                f"- Turnover năm: {_number(portfolio.get('annualized_turnover'), 2)}x; chi phí chỉ tính cho vị thế thật sự được mở.",
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
        if _regime_rows(evidence):
            lines.extend(["", "### Kết quả theo market regime", ""])
            for regime, regime_metrics in _regime_rows(evidence):
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
    dashboard: dict[str, Any] = {
        "meta": {
            "from": str(pd.Timestamp(dates.min()).date()),
            "to": str(pd.Timestamp(dates.max()).date()),
            "benchmark": config["panel"]["benchmark_symbol"],
            "costBps": float(config["panel"]["transaction_cost_bps"]),
            "maxPositions": int(
                config["panel"].get("max_positions", config["panel"]["top_k"])
            ),
            "universePointInTime": bool(
                config["panel"].get("_universe_point_in_time_complete", False)
            ),
        },
        "horizons": {},
    }
    for horizon, artifact in sorted(artifacts.items()):
        metrics = artifact["metrics"]
        evidence = metrics.get("frozen", {}) or metrics
        portfolio = evidence.get(
            "sparse_portfolio", evidence.get("top_k_portfolio", {})
        )
        ic = evidence.get("rank_ic", {})
        guard = metrics["publish_guard"]
        backtest = artifact.get("frozen_backtest")
        sample = "frozen"
        if backtest is None or backtest.empty:
            backtest = artifact["backtest"]
            sample = "development"
        trades = artifact.get("frozen_trades")
        if trades is None or trades.empty:
            trades = artifact.get("trades", pd.DataFrame())

        series: list[dict[str, Any]] = []
        if not backtest.empty:
            net_equity = (1 + backtest["net_return"].fillna(0)).cumprod()
            gross_equity = (1 + backtest["gross_return"].fillna(0)).cumprod()
            drawdown = net_equity / net_equity.cummax().clip(lower=1.0) - 1
            for date_value, net, gross, dd in zip(
                backtest.index, net_equity, gross_equity, drawdown, strict=False
            ):
                series.append(
                    {
                        "date": str(pd.Timestamp(date_value).date()),
                        "net": float(net),
                        "gross": float(gross),
                        "drawdown": float(dd),
                    }
                )

        ranking_rows = []
        for row in _ranking_rows(artifact["result"].latest_ranking, limit=50):
            ranking_rows.append(
                {
                    "rank": int(row["predicted_rank"]),
                    "symbol": str(row["symbol"]),
                    "prediction": safe_float(row.get("prediction")),
                    "lowerBound": safe_float(row.get("prediction_lower_bound")),
                    "percentile": safe_float(row.get("predicted_percentile")),
                    "netEdge": safe_float(row.get("expected_net_edge")),
                    "threshold": safe_float(row.get("entry_threshold")),
                    "decision": str(row.get("decision", "WAIT")),
                    "tradable": bool(row.get("is_tradable", False)),
                    "costBps": safe_float(row.get("estimated_round_trip_cost_bps")),
                }
            )

        trade_rows: list[dict[str, Any]] = []
        if trades is not None and not trades.empty:
            for row in trades.tail(100).to_dict("records"):
                trade_rows.append(
                    {
                        "date": str(pd.Timestamp(row["signal_date"]).date()),
                        "entryDate": (
                            str(pd.Timestamp(row["entry_date"]).date())
                            if pd.notna(row.get("entry_date"))
                            else None
                        ),
                        "exitDate": (
                            str(pd.Timestamp(row["exit_date"]).date())
                            if pd.notna(row.get("exit_date"))
                            else None
                        ),
                        "symbol": str(row["symbol"]),
                        "prediction": safe_float(row.get("prediction")),
                        "gross": safe_float(row.get("gross_return")),
                        "cost": safe_float(row.get("cost")),
                        "net": safe_float(row.get("net_return")),
                        "holding": int(row.get("holding_sessions", horizon)),
                        "entryPrice": safe_float(row.get("entry_price")),
                        "exitPrice": safe_float(row.get("exit_price")),
                    }
                )
        stress = [
            {
                "label": label,
                "return": safe_float(values.get("total_return")),
                "sharpe": safe_float(values.get("sharpe")),
                "costBps": safe_float(values.get("transaction_cost_bps")),
            }
            for label, values in (portfolio.get("cost_stress", {}) or {}).items()
        ]
        importance = [
            {"feature": feature, "gain": float(gain)}
            for feature, gain in list(artifact["result"].feature_importance.items())[:10]
        ]
        dashboard["horizons"][str(horizon)] = {
            "horizon": horizon,
            "sample": sample,
            "status": guard["status"],
            "failed": guard["failed_checks"],
            "metrics": {
                "netReturn": safe_float(portfolio.get("total_return")),
                "grossReturn": safe_float(portfolio.get("gross_compound_return")),
                "sharpe": safe_float(portfolio.get("sharpe")),
                "maxDrawdown": safe_float(portfolio.get("max_drawdown")),
                "trades": int(portfolio.get("completed_round_trips") or 0),
                "noTradeRate": safe_float(portfolio.get("no_trade_rate")),
                "annualTurnover": safe_float(portfolio.get("annualized_turnover")),
                "avgHolding": safe_float(portfolio.get("average_holding_sessions")),
                "totalCost": safe_float(portfolio.get("total_cost")),
                "profitFactor": safe_float(portfolio.get("profit_factor")),
                "rankIc": safe_float(ic.get("mean")),
                "hacT": safe_float(ic.get("hac_t_stat")),
            },
            "series": series,
            "ranking": ranking_rows,
            "trades": trade_rows,
            "stress": stress,
            "importance": importance,
        }

    embedded = json.dumps(
        clean_json_value(dashboard), ensure_ascii=False, separators=(",", ":")
    ).replace("</", "<\\/")
    template = r'''<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>VN Stock Decision BI</title>
<style>
:root{--navy:#0b1739;--navy2:#142653;--blue:#2f6bff;--cyan:#16b7c9;--green:#13a976;--amber:#f2a93b;--red:#e05260;--ink:#16213a;--muted:#66748e;--line:#e5eaf2;--paper:#fff;--bg:#f3f6fb;--shadow:0 8px 28px rgba(20,38,83,.08)}
[data-theme="dark"]{--ink:#e8eefc;--muted:#99a8c2;--line:#26344c;--paper:#111c2f;--bg:#08111f;--shadow:0 8px 28px rgba(0,0,0,.25)}[data-theme="dark"] .topbar,[data-theme="dark"] .btn,[data-theme="dark"] th{background:var(--paper);color:var(--ink)}[data-theme="dark"] .audit{background:var(--bg)}[data-theme="dark"] tbody tr:hover{background:#17243a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}.app{min-height:100vh;display:grid;grid-template-columns:244px 1fr}.sidebar{background:linear-gradient(180deg,var(--navy),#081127);color:#fff;padding:26px 20px;position:sticky;top:0;height:100vh}.brand{display:flex;gap:12px;align-items:center}.logo{width:42px;height:42px;border-radius:12px;background:linear-gradient(135deg,var(--blue),var(--cyan));display:grid;place-items:center;font-weight:900}.brand strong{display:block;font-size:15px}.brand small{color:#9eacd0}.nav{margin-top:34px;display:grid;gap:8px}.nav a{color:#aab6d5;text-decoration:none;padding:11px 12px;border-radius:9px}.nav a:hover,.nav a.active{background:rgba(255,255,255,.09);color:#fff}.side-note{position:absolute;left:20px;right:20px;bottom:24px;padding:14px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.08);border-radius:12px;color:#afbad6;font-size:12px}.content{min-width:0}.topbar{height:72px;background:#fff;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;padding:0 clamp(20px,3vw,42px);position:sticky;top:0;z-index:10}.eyebrow{font-size:11px;font-weight:800;letter-spacing:.12em;color:var(--blue)}h1{font-size:20px;margin:2px 0}.top-meta{color:var(--muted);font-size:12px;text-align:right}.main{padding:26px clamp(18px,3vw,42px) 50px;display:grid;gap:20px}.toolbar,.panel,.kpi{background:var(--paper);border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow)}.toolbar{padding:14px 16px;display:flex;gap:12px;align-items:center;justify-content:space-between}.horizon-buttons,.chart-buttons{display:flex;gap:7px;flex-wrap:wrap}.btn{border:1px solid var(--line);background:#fff;color:var(--muted);border-radius:9px;padding:8px 12px;font-weight:700;cursor:pointer}.btn:hover,.btn.active{color:#fff;background:var(--navy2);border-color:var(--navy2)}.status{display:flex;align-items:center;gap:9px;font-weight:800}.dot{width:9px;height:9px;border-radius:50%}.status.ok .dot{background:var(--green)}.status.bad .dot{background:var(--red)}.kpis{display:grid;grid-template-columns:repeat(6,minmax(130px,1fr));gap:12px}.kpi{padding:16px}.kpi .label{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.07em}.kpi .value{font-size:23px;font-weight:800;margin-top:7px}.kpi .sub{font-size:11px;color:var(--muted);margin-top:4px}.positive{color:var(--green)!important}.negative{color:var(--red)!important}.grid{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(300px,.8fr);gap:16px}.panel{padding:18px;min-width:0}.panel-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-bottom:14px}.panel h2{font-size:15px;margin:0}.panel p{margin:3px 0 0;color:var(--muted);font-size:12px}.chart-wrap{height:330px;position:relative}.chart-wrap canvas{width:100%;height:100%}.tooltip{display:none;position:absolute;pointer-events:none;background:#0b1739;color:#fff;padding:8px 10px;border-radius:8px;font-size:11px;box-shadow:var(--shadow)}.stress{display:grid;gap:14px;margin-top:8px}.stress-row{display:grid;grid-template-columns:42px 1fr 64px;gap:10px;align-items:center}.bar-bg{height:10px;background:#edf1f7;border-radius:99px;overflow:hidden}.bar{height:100%;border-radius:99px;background:var(--blue)}.audit{padding:12px 14px;border-radius:10px;background:#f8f9fc;border:1px solid var(--line);margin-top:16px;color:var(--muted);font-size:12px}.table-wrap{overflow:auto;max-height:430px}table{width:100%;border-collapse:collapse;white-space:nowrap}th{position:sticky;top:0;background:#f7f9fc;color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.05em;text-align:left}th,td{padding:11px 12px;border-bottom:1px solid var(--line)}tbody tr:hover{background:#f7f9ff}.badge{display:inline-flex;padding:4px 8px;border-radius:99px;font-size:10px;font-weight:800}.badge.wait{background:#eef1f6;color:#647089}.badge.buy{background:#dff7ee;color:#087c58}.rank{font-weight:800;color:var(--blue)}.bottom-grid{display:grid;grid-template-columns:1.2fr .8fr;gap:16px}.feature{display:grid;grid-template-columns:145px 1fr 52px;gap:9px;align-items:center;margin:9px 0;font-size:12px}.feature .bar{background:linear-gradient(90deg,var(--blue),var(--cyan))}.empty{padding:40px;text-align:center;color:var(--muted)}.foot{color:var(--muted);font-size:11px;padding:0 4px}.mobile-menu{display:none}
@media(max-width:1180px){.kpis{grid-template-columns:repeat(3,1fr)}.grid,.bottom-grid{grid-template-columns:1fr}}
@media(max-width:760px){.app{display:block}.sidebar{display:none}.topbar{height:auto;padding:14px 18px}.top-meta{display:none}.main{padding:16px}.toolbar{align-items:flex-start;flex-direction:column}.kpis{grid-template-columns:repeat(2,1fr)}.kpi .value{font-size:19px}.chart-wrap{height:270px}.panel{padding:14px}}
</style></head>
<body><div class="app">
<aside class="sidebar"><div class="brand"><div class="logo">VN</div><div><strong>Stock Decision BI</strong><small>Cost-aware research</small></div></div><nav class="nav"><a class="active" href="#overview">Tổng quan</a><a href="#signals">Tín hiệu</a><a href="#trades">Nhật ký vòng lệnh</a><a href="#model">Model audit</a></nav><div class="side-note">Không tự động đặt lệnh. BUY chỉ xuất hiện khi frozen holdout và stress phí đều đạt.</div></aside>
<div class="content"><header class="topbar"><div><div class="eyebrow">SPARSE PANEL · WALK-FORWARD</div><h1>Vietnam Equity Decision Dashboard</h1></div><div><button class="btn" id="themeToggle" type="button">◐ Sáng/tối</button><div class="top-meta" id="meta"></div></div></header>
<main class="main"><section class="toolbar" id="overview"><div><b>Khung dự báo</b><div class="horizon-buttons" id="horizonButtons"></div></div><div class="status bad" id="status"><span class="dot"></span><span id="statusText">NO_EDGE</span></div></section>
<section class="kpis"><div class="kpi"><div class="label">Net sau phí</div><div class="value" id="netReturn">—</div><div class="sub" id="sampleLabel"></div></div><div class="kpi"><div class="label">Sharpe</div><div class="value" id="sharpe">—</div><div class="sub">sau chi phí</div></div><div class="kpi"><div class="label">Max drawdown</div><div class="value" id="drawdown">—</div><div class="sub">frozen / OOS</div></div><div class="kpi"><div class="label">Vòng hoàn tất</div><div class="value" id="tradesCount">—</div><div class="sub" id="holding"></div></div><div class="kpi"><div class="label">Không giao dịch</div><div class="value" id="noTrade">—</div><div class="sub">cash là mặc định</div></div><div class="kpi"><div class="label">Turnover năm</div><div class="value" id="turnover">—</div><div class="sub">mua + bán</div></div></section>
<section class="grid"><div class="panel"><div class="panel-head"><div><h2>Hiệu suất chiến lược</h2><p>Gross, net sau phí và drawdown theo cohort không chồng lắp</p></div><div class="chart-buttons"><button class="btn active" data-chart="net">Net</button><button class="btn" data-chart="gross">Gross</button><button class="btn" data-chart="drawdown">Drawdown</button></div></div><div class="chart-wrap"><canvas id="performanceChart"></canvas><div class="tooltip" id="tooltip"></div></div></div><div class="panel"><div class="panel-head"><div><h2>Stress chi phí</h2><p>Giữ nguyên lệnh, chỉ tăng chi phí thực thi</p></div></div><div class="stress" id="stressChart"></div><div class="audit"><b>Guard chưa đạt</b><div id="failedChecks"></div></div></div></section>
<section class="panel" id="signals"><div class="panel-head"><div><h2>Bảng quyết định hôm nay</h2><p>Mã không đạt thanh khoản/PIT luôn WAIT dù prediction cao</p></div><div class="eyebrow" id="rankIc"></div></div><div class="table-wrap"><table><thead><tr><th>Rank</th><th>Mã</th><th>Dự báo net</th><th>Cận dưới</th><th>Net edge</th><th>Chi phí</th><th>Thanh khoản</th><th>Quyết định</th></tr></thead><tbody id="rankingBody"></tbody></table></div></section>
<section class="bottom-grid"><div class="panel" id="trades"><div class="panel-head"><div><h2>Nhật ký vòng lệnh</h2><p>Mỗi dòng là một mua–bán hoàn tất, đã trừ full round-trip cost</p></div></div><div class="table-wrap"><table><thead><tr><th>Mã</th><th>Mua</th><th>Giá mua</th><th>Bán</th><th>Giá bán</th><th>Gross</th><th>Phí</th><th>Net</th></tr></thead><tbody id="tradeBody"></tbody></table></div></div><div class="panel" id="model"><div class="panel-head"><div><h2>Feature importance</h2><p>XGBoost gain · không phải quan hệ nhân quả</p></div></div><div id="importance"></div></div></section>
<div class="foot" id="footnote"></div>
</main></div></div>
<script>const DATA=__DATA__;
const fmtPct=v=>v==null?'N/A':new Intl.NumberFormat('vi-VN',{style:'percent',minimumFractionDigits:1,maximumFractionDigits:1}).format(v);const fmt=v=>v==null?'N/A':Number(v).toFixed(2);const fmtPrice=v=>v==null?'N/A':new Intl.NumberFormat('vi-VN',{maximumFractionDigits:2}).format(v);const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));let active=Object.keys(DATA.horizons)[0],chartMode='net';
const el=id=>document.getElementById(id);el('meta').innerHTML=`${DATA.meta.from} → ${DATA.meta.to}<br>${esc(DATA.meta.benchmark)} · ${DATA.meta.costBps} bps/vòng`;document.documentElement.dataset.theme=localStorage.getItem('panel-theme')||'light';el('themeToggle').onclick=()=>{const next=document.documentElement.dataset.theme==='dark'?'light':'dark';document.documentElement.dataset.theme=next;localStorage.setItem('panel-theme',next);drawChart()};el('footnote').textContent=DATA.meta.universePointInTime?'Universe PIT đã lọc theo available_at/listed_at/delisted_at. RESEARCH_OK vẫn không phải lệnh tự động.':'Research-only. Universe chưa point-in-time đầy đủ nên publish guard bắt buộc NO_EDGE để tránh survivorship bias.';
Object.keys(DATA.horizons).forEach((h,i)=>{const b=document.createElement('button');b.className='btn'+(i===0?' active':'');b.textContent=`${h} phiên`;b.onclick=()=>{active=h;document.querySelectorAll('#horizonButtons .btn').forEach(x=>x.classList.toggle('active',x===b));render()};el('horizonButtons').appendChild(b)});
document.querySelectorAll('[data-chart]').forEach(b=>b.onclick=()=>{chartMode=b.dataset.chart;document.querySelectorAll('[data-chart]').forEach(x=>x.classList.toggle('active',x===b));drawChart()});
function tone(node,v,inverse=false){node.classList.remove('positive','negative');if(v==null)return;node.classList.add((inverse?v<=0:v>=0)?'positive':'negative')}
function render(){const d=DATA.horizons[active],m=d.metrics;el('status').className='status '+(d.status==='RESEARCH_OK'?'ok':'bad');el('statusText').textContent=d.status;el('netReturn').textContent=fmtPct(m.netReturn);tone(el('netReturn'),m.netReturn);el('sharpe').textContent=fmt(m.sharpe);tone(el('sharpe'),m.sharpe);el('drawdown').textContent=fmtPct(m.maxDrawdown);tone(el('drawdown'),m.maxDrawdown);el('tradesCount').textContent=m.trades;el('noTrade').textContent=fmtPct(m.noTradeRate);el('turnover').textContent=m.annualTurnover==null?'N/A':`${fmt(m.annualTurnover)}x`;el('holding').textContent=m.avgHolding==null?'chưa có vòng':`giữ TB ${fmt(m.avgHolding)} phiên`;el('sampleLabel').textContent=d.sample==='frozen'?'frozen holdout':'development OOS';el('rankIc').textContent=`Rank IC ${fmt(m.rankIc)} · HAC t ${fmt(m.hacT)}`;el('failedChecks').textContent=d.failed.length?d.failed.join(' · '):'Không';renderStress(d);renderRanking(d);renderTrades(d);renderImportance(d);drawChart()}
function renderStress(d){const rows=d.stress||[],max=Math.max(...rows.map(x=>Math.abs(x.return||0)),.01);el('stressChart').innerHTML=rows.map(x=>`<div class="stress-row"><b>${esc(x.label)}</b><div class="bar-bg"><div class="bar" style="width:${Math.min(100,Math.abs(x.return||0)/max*100)}%;background:${(x.return||0)>=0?'var(--green)':'var(--red)'}"></div></div><span class="${(x.return||0)>=0?'positive':'negative'}">${fmtPct(x.return)}</span></div>`).join('')||'<div class="empty">Chưa có dữ liệu stress</div>'}
function renderRanking(d){el('rankingBody').innerHTML=d.ranking.map(r=>`<tr><td class="rank">#${r.rank}</td><td><b>${esc(r.symbol)}</b></td><td>${fmtPct(r.prediction)}</td><td>${fmtPct(r.lowerBound)}</td><td class="${(r.netEdge||0)>=0?'positive':'negative'}">${fmtPct(r.netEdge)}</td><td>${r.costBps==null?'N/A':fmt(r.costBps)+' bps'}</td><td><span class="badge ${r.tradable?'buy':'wait'}">${r.tradable?'ĐẠT':'LOẠI'}</span></td><td><span class="badge ${r.decision==='BUY_CANDIDATE'?'buy':'wait'}">${esc(r.decision)}</span></td></tr>`).join('')}
function renderTrades(d){el('tradeBody').innerHTML=d.trades.length?d.trades.slice().reverse().map(r=>`<tr><td><b>${esc(r.symbol)}</b></td><td>${esc(r.entryDate||r.date)}</td><td>${fmtPrice(r.entryPrice)}</td><td>${esc(r.exitDate||'N/A')}</td><td>${fmtPrice(r.exitPrice)}</td><td>${fmtPct(r.gross)}</td><td class="negative">-${fmtPct(r.cost)}</td><td class="${(r.net||0)>=0?'positive':'negative'}">${fmtPct(r.net)}</td></tr>`).join(''):'<tr><td colspan="8" class="empty">Không có vòng lệnh — hệ thống giữ tiền mặt</td></tr>'}
function renderImportance(d){const rows=d.importance||[],max=Math.max(...rows.map(x=>x.gain),1e-9);el('importance').innerHTML=rows.map(x=>`<div class="feature"><span title="${esc(x.feature)}">${esc(x.feature)}</span><div class="bar-bg"><div class="bar" style="width:${x.gain/max*100}%"></div></div><b>${fmt(x.gain)}</b></div>`).join('')||'<div class="empty">Chưa có feature importance</div>'}
function drawChart(){const canvas=el('performanceChart'),wrap=canvas.parentElement,dpr=window.devicePixelRatio||1,w=wrap.clientWidth,h=wrap.clientHeight;canvas.width=w*dpr;canvas.height=h*dpr;const c=canvas.getContext('2d');c.scale(dpr,dpr);c.clearRect(0,0,w,h);const rows=DATA.horizons[active].series;if(!rows.length){c.fillStyle='#7b879e';c.font='14px system-ui';c.fillText('Không có giao dịch trong mẫu đánh giá',24,h/2);return}const vals=rows.map(x=>x[chartMode]);let min=Math.min(...vals),max=Math.max(...vals);if(max===min){max+=.01;min-=.01}const pad={l:54,r:18,t:18,b:34},x=i=>pad.l+i/(Math.max(rows.length-1,1))*(w-pad.l-pad.r),y=v=>pad.t+(max-v)/(max-min)*(h-pad.t-pad.b);c.strokeStyle='#e7ebf2';c.fillStyle='#7c889d';c.font='11px system-ui';for(let i=0;i<5;i++){const yy=pad.t+i/4*(h-pad.t-pad.b),v=max-i/4*(max-min);c.beginPath();c.moveTo(pad.l,yy);c.lineTo(w-pad.r,yy);c.stroke();c.fillText(chartMode==='drawdown'?fmtPct(v):v.toFixed(2)+'x',4,yy+4)}const color=chartMode==='drawdown'?'#e05260':chartMode==='gross'?'#16b7c9':'#2f6bff';c.beginPath();rows.forEach((r,i)=>i?c.lineTo(x(i),y(r[chartMode])):c.moveTo(x(i),y(r[chartMode])));c.strokeStyle=color;c.lineWidth=2.4;c.stroke();c.lineTo(x(rows.length-1),h-pad.b);c.lineTo(x(0),h-pad.b);c.closePath();const g=c.createLinearGradient(0,pad.t,0,h-pad.b);g.addColorStop(0,color+'33');g.addColorStop(1,color+'00');c.fillStyle=g;c.fill();c.fillStyle='#7c889d';c.fillText(rows[0].date,pad.l,h-10);c.textAlign='right';c.fillText(rows.at(-1).date,w-pad.r,h-10);c.textAlign='left';canvas.onmousemove=e=>{const rect=canvas.getBoundingClientRect(),idx=Math.max(0,Math.min(rows.length-1,Math.round((e.clientX-rect.left-pad.l)/(w-pad.l-pad.r)*(rows.length-1)))),r=rows[idx],tip=el('tooltip');tip.style.display='block';tip.style.left=Math.min(w-145,Math.max(8,e.clientX-rect.left+10))+'px';tip.style.top=Math.max(8,e.clientY-rect.top-52)+'px';tip.innerHTML=`<b>${r.date}</b><br>${chartMode}: ${chartMode==='drawdown'?fmtPct(r[chartMode]):r[chartMode].toFixed(3)+'x'}`};canvas.onmouseleave=()=>el('tooltip').style.display='none'}
window.addEventListener('resize',drawChart);render();</script></body></html>'''
    output_path.write_text(template.replace("__DATA__", embedded), encoding="utf-8")
