from __future__ import annotations

import html
import os
import tempfile
from datetime import datetime
from pathlib import Path

os.environ.setdefault(
    "MPLCONFIGDIR",
    str(Path(tempfile.gettempdir()) / "vn_stock_analysis_matplotlib"),
)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.utils import safe_float


SIGNAL_STATUS_LABELS = {
    "ACTIONABLE": "CÓ THỂ HÀNH ĐỘNG (ACTIONABLE)",
    "WATCH": "THEO DÕI (WATCH)",
    "NO_EDGE": "CHƯA CÓ LỢI THẾ (NO_EDGE)",
}

SIGNAL_CHECK_LABELS = {
    "model_auc": "AUC của mô hình",
    "model_balanced_accuracy": "Độ chính xác cân bằng của mô hình",
    "model_beats_logistic": "XGBoost vượt mô hình Logistic đối chứng",
    "probability_edge": "Xác suất tăng đạt ngưỡng",
    "technical_context": "Bối cảnh kỹ thuật đạt ngưỡng",
    "reward_risk": "Tỷ lệ lợi nhuận/rủi ro đạt ngưỡng",
    "fresh_data": "Dữ liệu còn mới",
    "position_available": "Có khối lượng vị thế hợp lệ",
    "backtest_available": "Có kết quả kiểm thử chiến lược ngoài mẫu",
    "backtest_sample": "Mẫu kiểm thử chiến lược đủ lớn",
    "backtest_net_edge": "Kiểm thử chiến lược có lợi thế ròng",
}


def signal_status_label(status: object) -> str:
    """Đổi mã trạng thái nội bộ thành nhãn tiếng Việt để hiển thị."""

    value = str(status)
    return SIGNAL_STATUS_LABELS.get(value, value)


def signal_check_label(check: object) -> str:
    """Đổi tên điều kiện nội bộ thành nhãn tiếng Việt để hiển thị."""

    value = str(check)
    return SIGNAL_CHECK_LABELS.get(value, value.replace("_", " "))


def format_price(value: float | None) -> str:
    return "N/A" if value is None else f"{value:,.2f}"


def format_number(value: float | None, decimals: int = 2) -> str:
    return "N/A" if value is None else f"{value:,.{decimals}f}"


def format_percent(value: float | None, decimals: int = 1) -> str:
    return "N/A" if value is None else f"{value:.{decimals}%}"


def format_metric(value: float | None, unit: str = "number") -> str:
    if value is None:
        return "N/A"
    if unit == "percent":
        return format_percent(value)
    if unit == "money":
        return f"{value / 1_000_000_000:,.1f} tỷ"
    return format_number(value)


def make_history_chart(frame: pd.DataFrame, output_path: Path) -> None:
    returns = frame["return_1d"]
    equity = (1 + returns.fillna(0)).cumprod()
    drawdown = equity / equity.cummax() - 1
    figure, axes = plt.subplots(
        3,
        1,
        figsize=(13, 9),
        sharex=True,
        height_ratios=[2.2, 1, 1],
    )
    axes[0].plot(frame.index, frame["close"], label="Giá đóng cửa", color="#1f4d7a", linewidth=1.4)
    axes[0].plot(frame.index, frame["sma_20"], label="SMA20", color="#d97706", linewidth=1.0)
    axes[0].plot(frame.index, frame["sma_60"], label="SMA60", color="#16806a", linewidth=1.0)
    axes[0].set_title("Giá lịch sử và đường trung bình")
    axes[0].set_ylabel("Nghìn VND/cp")
    axes[0].legend(loc="upper left")
    axes[0].grid(alpha=0.25)
    axes[1].bar(frame.index, frame["volume"] / 1_000_000, color="#64748b", width=1.0)
    axes[1].set_title("Khối lượng giao dịch")
    axes[1].set_ylabel("Triệu cp")
    axes[1].grid(alpha=0.25)
    axes[2].fill_between(frame.index, drawdown, 0, color="#b42318", alpha=0.35)
    axes[2].set_title("Mức sụt giảm của tài sản")
    axes[2].set_ylabel("Mức sụt giảm")
    axes[2].grid(alpha=0.25)
    figure.tight_layout()
    figure.savefig(output_path, dpi=170)
    plt.close(figure)


def make_forecast_chart(
    frame: pd.DataFrame,
    forecast: pd.DataFrame,
    levels: dict,
    output_path: Path,
) -> None:
    chart_frame = frame.tail(260)
    figure, axis = plt.subplots(figsize=(13, 7))
    axis.plot(chart_frame.index, chart_frame["close"], label="Giá đóng cửa", color="#1f4d7a", linewidth=1.5)
    axis.plot(chart_frame.index, chart_frame["sma_20"], label="SMA20", color="#d97706", linewidth=1.1)
    axis.plot(chart_frame.index, chart_frame["sma_60"], label="SMA60", color="#16806a", linewidth=1.1)
    axis.plot(forecast.index, forecast["p50"], label="Dự báo P50", color="#111827", linewidth=1.6)
    axis.fill_between(forecast.index, forecast["p25"], forecast["p75"], color="#7dd3c7", alpha=0.35, label="P25-P75")
    axis.fill_between(forecast.index, forecast["p10"], forecast["p90"], color="#bae6fd", alpha=0.45, label="P10-P90")
    axis.axhline(levels["support20"], color="#b42318", linestyle="--", linewidth=1, label="Hỗ trợ 20")
    axis.axhline(levels["resistance20"], color="#7c3aed", linestyle="--", linewidth=1, label="Kháng cự 20")
    axis.axhline(levels["latest_close"], color="#475569", linestyle=":", linewidth=1, label="Giá đóng cửa mới nhất")
    axis.set_title("Dự báo Monte Carlo")
    axis.set_ylabel("Nghìn VND/cp")
    axis.grid(alpha=0.25)
    axis.legend(loc="upper left", ncol=2)
    figure.tight_layout()
    figure.savefig(output_path, dpi=170)
    plt.close(figure)


def make_technical_chart(frame: pd.DataFrame, output_path: Path) -> None:
    chart_frame = frame.tail(220)
    figure, axes = plt.subplots(
        4,
        1,
        figsize=(13, 10),
        sharex=True,
        height_ratios=[2.2, 1.1, 1, 1],
    )
    axes[0].plot(chart_frame.index, chart_frame["close"], label="Giá đóng cửa", color="#172554", linewidth=1.5)
    axes[0].plot(chart_frame.index, chart_frame["sma_20"], label="SMA20", color="#d97706", linewidth=1.0)
    axes[0].plot(chart_frame.index, chart_frame["sma_60"], label="SMA60", color="#16806a", linewidth=1.0)
    axes[0].fill_between(chart_frame.index, chart_frame["bb_lower_20"], chart_frame["bb_upper_20"], color="#bae6fd", alpha=0.35, label="Bollinger 20")
    axes[0].set_title("Giá, SMA và dải Bollinger")
    axes[0].set_ylabel("Nghìn VND/cp")
    axes[0].legend(loc="upper left", ncol=2)
    axes[0].grid(alpha=0.25)

    histogram_colors = np.where(chart_frame["macd_hist"] >= 0, "#16806a", "#b42318")
    axes[1].bar(chart_frame.index, chart_frame["macd_hist"], color=histogram_colors, width=1.0, alpha=0.55, label="Biểu đồ cột MACD")
    axes[1].plot(chart_frame.index, chart_frame["macd"], color="#2563a8", linewidth=1.2, label="MACD")
    axes[1].plot(chart_frame.index, chart_frame["macd_signal"], color="#d97706", linewidth=1.1, label="Tín hiệu")
    axes[1].axhline(0, color="#64748b", linewidth=0.8)
    axes[1].set_title("MACD")
    axes[1].legend(loc="upper left", ncol=3)
    axes[1].grid(alpha=0.25)

    axes[2].plot(chart_frame.index, chart_frame["rsi_14"], color="#7c3aed", linewidth=1.2, label="RSI14")
    axes[2].axhline(70, color="#b42318", linestyle="--", linewidth=0.8)
    axes[2].axhline(30, color="#16806a", linestyle="--", linewidth=0.8)
    axes[2].set_ylim(0, 100)
    axes[2].set_title("RSI")
    axes[2].legend(loc="upper left")
    axes[2].grid(alpha=0.25)

    axes[3].plot(chart_frame.index, chart_frame["atr_pct_14"] * 100, color="#0f766e", linewidth=1.1, label="ATR%")
    axes[3].plot(chart_frame.index, chart_frame["adx_14"], color="#be123c", linewidth=1.1, label="ADX14")
    axes[3].axhline(25, color="#64748b", linestyle="--", linewidth=0.8)
    axes[3].set_title("Biến động và độ mạnh xu hướng")
    axes[3].legend(loc="upper left", ncol=2)
    axes[3].grid(alpha=0.25)
    figure.tight_layout()
    figure.savefig(output_path, dpi=170)
    plt.close(figure)


def _scenario_text(
    levels: dict,
    forecast: pd.DataFrame,
    latest_probabilities: dict,
    technical: dict,
    risk_plan: dict,
    decision: dict,
) -> list[str]:
    latest = levels["latest_close"]
    forecast_end = forecast.iloc[-1]
    if latest > levels["sma20"] > levels["sma60"]:
        trend = "Xu hướng ngắn hạn thuận: giá trên SMA20 và SMA60."
    elif latest > levels["sma60"]:
        trend = "Trung hạn chưa xấu, ngắn hạn yếu vì giá dưới SMA20."
    else:
        trend = "Xu hướng yếu: giá dưới SMA60, ưu tiên quản trị rủi ro."
    return [
        f"Trạng thái tín hiệu: {signal_status_label(decision['status'])}.",
        *[f"Điều kiện phát hành tín hiệu: {reason}." for reason in decision.get("reasons", [])],
        trend,
        f"Xu hướng kỹ thuật nghiêng về: {technical['bias']}.",
        f"XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: {latest_probabilities['xgboost']:.1%}.",
        f"Mô hình Logistic đối chứng: {latest_probabilities['logistic_regression']:.1%}.",
        f"Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: {forecast_end['prob_end_above_latest']:.1%}.",
        f"Mức dừng lỗ tham chiếu {format_price(risk_plan['stop_loss'])}, mục tiêu 1 {format_price(risk_plan['target_1'])}, tỷ lệ lợi nhuận/rủi ro {format_number(risk_plan['reward_risk'])}.",
    ]


def write_report(
    config: dict,
    frame: pd.DataFrame,
    forecast: pd.DataFrame,
    levels: dict,
    metrics: dict,
    latest_probabilities: dict,
    technical: dict,
    fundamentals: dict,
    risk_plan: dict,
    decision: dict,
    output_path: Path,
) -> None:
    latest = levels["latest_close"]
    forecast_end = forecast.iloc[-1]
    lines = [
        f"# Báo cáo ngày {datetime.now().date()} - {config['symbol']}",
        "",
        "## Tổng quan",
        "",
        f"- Dữ liệu: {frame.index.min().date()} -> {frame.index.max().date()}, {len(frame):,} phiên.",
        f"- Giá đóng cửa: {latest:.2f} nghìn VND/cp.",
        f"- Xu hướng kỹ thuật nghiêng về: {technical['bias']} (điểm {technical['score']}).",
        f"- Xác suất XGBoost để giá đóng cửa phiên tới cao hơn giá mở cửa: {latest_probabilities['xgboost']:.1%}.",
        f"- Trạng thái tín hiệu: {signal_status_label(decision['status'])}.",
        "",
        "## Phân tích kỹ thuật",
        "",
        f"- SMA20 {levels['sma20']:.2f}; SMA60 {levels['sma60']:.2f}; RSI14 {levels['rsi14']:.1f}.",
        f"- MACD {format_number(levels['macd'], 3)}; đường tín hiệu {format_number(levels['macd_signal'], 3)}; biểu đồ cột {format_number(levels['macd_hist'], 3)}.",
        f"- ATR14 {format_price(levels['atr14'])}; ATR% {format_percent(levels['atr_pct14'])}; ADX14 {format_number(levels['adx14'], 1)}.",
    ]
    lines.extend(
        f"- {item['name']}: {item['status']} - {item['detail']}"
        for item in technical["signals"]
    )

    lines.extend(["", "## Phân tích cơ bản", ""])
    company = fundamentals.get("company", {})
    if company:
        lines.append(
            f"- Doanh nghiệp: {company.get('organ_short_name') or company.get('organ_name') or config['symbol']}."
        )
        if company.get("sector"):
            lines.append(f"- Ngành: {company['sector']}.")
    if fundamentals.get("latest_period"):
        lines.append(f"- Kỳ tỷ số mới nhất: {fundamentals['latest_period']}.")
    fundamental_lookup = {
        item["metric_name"]: item
        for item in fundamentals.get("metrics", [])
    }
    for metric_name in [
        "pe",
        "pb",
        "roe",
        "roa",
        "marketCap",
        "revenue_growth",
        "profit_growth",
    ]:
        item = fundamental_lookup.get(metric_name)
        if item is None:
            continue
        lines.append(
            f"- {item['metric_label']}: {format_metric(item['metric_value'], item['metric_unit'])}."
        )
    lines.extend(f"- {note}" for note in fundamentals.get("assessment", []))
    lines.extend(f"- Ghi chú dữ liệu: {note}" for note in fundamentals.get("notes", []))

    xgboost_metrics = metrics["xgboost"]
    logistic_metrics = metrics["logistic_baseline"]
    lines.extend(
        [
            "",
            "## Mô hình XGBoost",
            "",
            f"- Kiểm thử: {metrics['split']['test_start']} -> {metrics['split']['test_end']}.",
            f"- XGBoost: độ chính xác cân bằng {xgboost_metrics['balanced_accuracy']:.3f}; AUC {format_number(xgboost_metrics['roc_auc'], 3)}; log-loss {xgboost_metrics['log_loss']:.3f}.",
            f"- Mô hình Logistic đối chứng: độ chính xác cân bằng {logistic_metrics['balanced_accuracy']:.3f}; AUC {format_number(logistic_metrics['roc_auc'], 3)}.",
            f"- Mô hình đa số đối chứng: độ chính xác cân bằng {metrics['majority_baseline']['balanced_accuracy']:.3f}.",
            f"- Vòng boosting tốt nhất: {xgboost_metrics['best_iteration']}.",
        ]
    )
    validation = metrics.get("validation") or metrics.get("walk_forward", {})
    if validation:
        lines.append(
            f"- Thẩm định: {validation.get('scheme', validation.get('layout', 'walk-forward'))}; "
            f"{validation.get('fold_count', len(validation.get('folds', [])))} lần chia; "
            f"khoảng cách {validation.get('gap_rows', 0)} phiên."
        )
    strategy = metrics.get("backtest", {})
    if strategy:
        lines.append(
            f"- Kiểm thử chiến lược ngoài mẫu sau chi phí: tổng lợi nhuận {format_percent(safe_float(strategy.get('net_total_return', strategy.get('total_return'))))}; "
            f"Sharpe {format_number(safe_float(strategy.get('sharpe_ratio', strategy.get('sharpe'))), 2)}; "
            f"mức sụt giảm tối đa {format_percent(safe_float(strategy.get('max_drawdown')))}."
        )
    top_features = list(xgboost_metrics["feature_importance_gain"].items())[:6]
    if top_features:
        lines.append(
            "- Mức độ quan trọng của đặc trưng: "
            + "; ".join(f"{name}={value:.2f}" for name, value in top_features)
            + "."
        )

    lines.extend(
        [
            "",
            "## Quản trị rủi ro",
            "",
            f"- Vốn tham chiếu {risk_plan['capital_reference_vnd']:,.0f} VND; rủi ro mỗi lệnh {risk_plan['risk_per_trade_pct']:.1%}.",
            f"- Mức dừng lỗ {format_price(risk_plan['stop_loss'])}; mục tiêu 1 {format_price(risk_plan['target_1'])}; mục tiêu 2 {format_price(risk_plan['target_2'])}.",
            f"- Tỷ lệ lợi nhuận/rủi ro {format_number(risk_plan['reward_risk'])}; khối lượng vị thế {risk_plan['position_shares'] or 0:,} cổ phiếu.",
            "",
            f"## Dự báo {config['forecast_sessions']} phiên",
            "",
            f"- P50 cuối kỳ {forecast_end['p50']:.2f} ({forecast_end['p50'] / latest - 1:.2%}).",
            f"- P10/P90 cuối kỳ {forecast_end['p10']:.2f} / {forecast_end['p90']:.2f}.",
            "",
            "## Khung hành động tham khảo",
            "",
        ]
    )
    lines.extend(
        f"- {item}"
        for item in _scenario_text(
            levels,
            forecast,
            latest_probabilities,
            technical,
            risk_plan,
            decision,
        )
    )
    lines.extend(
        [
            "",
            "Lưu ý: báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.",
        ]
    )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _escape(value) -> str:
    return html.escape(str(value), quote=True)


def _metric_card(label: str, value: str, detail: str = "") -> str:
    return (
        '<div class="metric">'
        f'<div class="metric-label">{_escape(label)}</div>'
        f'<div class="metric-value">{_escape(value)}</div>'
        f'<div class="metric-detail">{_escape(detail)}</div>'
        "</div>"
    )


def _table(rows: list[tuple[str, str, str]]) -> str:
    body = "".join(
        f"<tr><td>{_escape(name)}</td><td>{_escape(value)}</td><td>{_escape(detail)}</td></tr>"
        for name, value, detail in rows
    )
    return f"<table><tbody>{body}</tbody></table>"


def write_dashboard(
    config: dict,
    frame: pd.DataFrame,
    forecast: pd.DataFrame,
    levels: dict,
    metrics: dict,
    latest_probabilities: dict,
    technical: dict,
    fundamentals: dict,
    risk_plan: dict,
    decision: dict,
    output_path: Path,
) -> None:
    latest = levels["latest_close"]
    forecast_end = forecast.iloc[-1]
    company = fundamentals.get("company", {})
    company_name = company.get("organ_short_name") or company.get("organ_name") or config["symbol"]
    result_cards = "".join(
        [
            _metric_card("Giá hiện tại", format_price(latest), f"{levels['latest_date']} - nghìn VND/cp"),
            _metric_card("Xu hướng kỹ thuật", technical["bias"], f"Điểm {technical['score']}"),
            _metric_card("Trạng thái tín hiệu", signal_status_label(decision["status"]), "; ".join(signal_check_label(name) for name in decision.get("failed_checks", [])) or "Đã vượt qua tất cả điều kiện phát hành"),
            _metric_card("Xác suất XGBoost", f"{latest_probabilities['xgboost']:.1%}", "Xác suất giá đóng cửa phiên tới cao hơn giá mở cửa"),
            _metric_card("Dự báo", format_price(safe_float(forecast_end["p50"])), f"P50 sau {config['forecast_sessions']} phiên - {format_percent(forecast_end['p50'] / latest - 1)}"),
            _metric_card("Quản trị rủi ro", f"Lợi nhuận/rủi ro {format_number(risk_plan['reward_risk'])}", f"Dừng lỗ {format_price(risk_plan['stop_loss'])} / Mục tiêu {format_price(risk_plan['target_1'])}"),
        ]
    )
    fundamental_lookup = {
        item["metric_name"]: item
        for item in fundamentals.get("metrics", [])
    }
    fundamental_specs = [
        ("pe", "P/E"),
        ("pb", "P/B"),
        ("roe", "ROE"),
        ("roa", "ROA"),
        ("marketCap", "Vốn hóa thị trường"),
        ("revenue_growth", "Tăng trưởng doanh thu"),
        ("profit_growth", "Tăng trưởng lợi nhuận"),
    ]
    fundamental_cards = "".join(
        _metric_card(
            label,
            format_metric(item["metric_value"], item["metric_unit"]) if item else "N/A",
            item.get("period", "") if item else "Không có dữ liệu",
        )
        for metric_name, label in fundamental_specs
        for item in [fundamental_lookup.get(metric_name)]
    )
    technical_table = _table(
        [(item["name"], item["status"], item["detail"]) for item in technical["signals"]]
    )
    model_table = _table(
        [
            ("XGBoost", format_number(metrics["xgboost"]["balanced_accuracy"], 3), f"AUC {format_number(metrics['xgboost']['roc_auc'], 3)}"),
            ("Logistic", format_number(metrics["logistic_baseline"]["balanced_accuracy"], 3), f"AUC {format_number(metrics['logistic_baseline']['roc_auc'], 3)}"),
            ("Đa số", format_number(metrics["majority_baseline"]["balanced_accuracy"], 3), "Mốc so sánh"),
        ]
    )
    strategy = metrics.get("backtest", {}) or {}
    backtest_table = _table(
        [
            (
                "Lợi nhuận ròng",
                format_percent(
                    safe_float(
                        strategy.get("net_total_return", strategy.get("total_return"))
                    )
                ),
                f"{strategy.get('observations', 0)} quan sát ngoài mẫu",
            ),
            (
                "Sharpe",
                format_number(
                    safe_float(strategy.get("sharpe_ratio", strategy.get("sharpe"))),
                    2,
                ),
                "Sau chi phí",
            ),
            (
                "Mức sụt giảm tối đa",
                format_percent(safe_float(strategy.get("max_drawdown"))),
                f"{strategy.get('completed_round_trips', 0)} vòng giao dịch",
            ),
            (
                "Chi phí giả định",
                f"{safe_float(strategy.get('round_trip_cost_bps'), 0):.1f} bps",
                "Một vòng mua và bán",
            ),
        ]
    )
    risk_table = _table(
        [
            ("Rủi ro/lệnh", f"{risk_plan['risk_per_trade_pct']:.1%}", f"{risk_plan['risk_budget_vnd']:,.0f} VND"),
            ("Mức dừng lỗ", format_price(risk_plan["stop_loss"]), f"Rủi ro mỗi cổ phiếu {format_price(risk_plan['risk_per_share'])}"),
            ("Mục tiêu 1", format_price(risk_plan["target_1"]), f"Lợi nhuận/rủi ro {format_number(risk_plan['reward_risk'])}"),
            ("Mục tiêu 2", format_price(risk_plan["target_2"]), "Dự báo/kháng cự"),
        ]
    )
    decision_table = _table(
        [
            (
                signal_check_label(name),
                "ĐẠT" if passed else "KHÔNG ĐẠT",
                "Điều kiện phát hành tín hiệu",
            )
            for name, passed in decision.get("checks", {}).items()
        ]
    )
    fundamental_rows = [
        (item["metric_label"], format_metric(item["metric_value"], item["metric_unit"]), item.get("period") or "")
        for item in fundamentals.get("metrics", [])
    ] or [("Dữ liệu", "N/A", "Chưa lấy được dữ liệu cơ bản")]
    fundamental_table = _table(fundamental_rows)
    forecast_table = _table(
        [
            (str(index.date()), format_price(safe_float(row["p50"])), f"P10 {format_price(safe_float(row['p10']))} / P90 {format_price(safe_float(row['p90']))}")
            for index, row in forecast.head(8).iterrows()
        ]
    )
    top_features = list(metrics["xgboost"]["feature_importance_gain"].items())[:8]
    feature_table = _table(
        [(name, format_number(value, 2), "Mức đóng góp") for name, value in top_features]
    )

    document = f"""<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Bảng điều khiển XGBoost - {_escape(config['symbol'])}</title>
  <style>
    :root {{ --bg:#f4f6f3; --ink:#1f2933; --muted:#687382; --line:#d6ddd5; --panel:#fff; --green:#0f7b68; --blue:#2563a8; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif; background:var(--bg); color:var(--ink); }}
    header {{ padding:28px clamp(18px,4vw,46px) 20px; background:#fff; border-bottom:1px solid var(--line); }}
    .eyebrow {{ color:var(--green); font-size:12px; font-weight:750; text-transform:uppercase; letter-spacing:.08em; }}
    h1 {{ margin:8px 0 6px; font-size:clamp(28px,4vw,46px); line-height:1.05; letter-spacing:0; }}
    .subtitle,.disclaimer {{ color:var(--muted); line-height:1.55; }}
    main {{ padding:22px clamp(18px,4vw,46px) 44px; display:grid; gap:22px; }}
    .metrics {{ display:grid; gap:12px; }}
    .result-metrics {{ grid-template-columns:repeat(5,minmax(150px,1fr)); }}
    .fundamental-metrics {{ grid-template-columns:repeat(7,minmax(130px,1fr)); }}
    .metric,section {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; }}
    .metric {{ padding:14px; min-height:104px; }}
    .metric-label {{ color:var(--muted); font-size:12px; font-weight:750; text-transform:uppercase; }}
    .metric-value {{ margin-top:10px; font-size:23px; font-weight:760; line-height:1.1; }}
    .metric-detail {{ color:var(--muted); margin-top:7px; font-size:13px; }}
    section {{ padding:18px; }}
    .grid {{ display:grid; grid-template-columns:minmax(0,1.15fr) minmax(320px,.85fr); gap:22px; align-items:start; }}
    .two {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:22px; }}
    h2 {{ margin:0 0 12px; font-size:18px; letter-spacing:0; }}
    table {{ width:100%; border-collapse:collapse; font-size:14px; }}
    td {{ padding:10px 8px; border-top:1px solid var(--line); vertical-align:top; }}
    td:first-child {{ font-weight:700; width:28%; }}
    td:nth-child(2) {{ color:var(--blue); font-weight:650; width:24%; }}
    img {{ width:100%; height:auto; display:block; border-radius:6px; border:1px solid var(--line); background:#fff; }}
    @media (max-width:1200px) {{ .result-metrics,.fundamental-metrics {{ grid-template-columns:repeat(3,minmax(0,1fr)); }} .grid,.two {{ grid-template-columns:1fr; }} }}
    @media (max-width:620px) {{ .result-metrics,.fundamental-metrics {{ grid-template-columns:1fr; }} td {{ display:block; width:100%!important; border:0; padding:6px 4px; }} tr {{ display:block; border-top:1px solid var(--line); padding:8px 0; }} }}
  </style>
</head>
<body>
  <header>
    <div class="eyebrow">Phân tích cổ phiếu Việt Nam bằng XGBoost</div>
    <h1>{_escape(config['symbol'])} - {_escape(company_name)}</h1>
    <p class="subtitle">Dữ liệu {frame.index.min().date()} → {frame.index.max().date()}. Nguồn vnstock/{_escape(config['source'])}. XGBoost là mô hình chính; Logistic và mô hình đa số được dùng làm đối chứng.</p>
  </header>
  <main>
    <h2>Kết quả chính</h2>
    <div class="metrics result-metrics">{result_cards}</div>
    <h2>Tổng quan cơ bản</h2>
    <div class="metrics fundamental-metrics">{fundamental_cards}</div>
    <div class="grid"><section><h2>Biểu đồ kỹ thuật</h2><img src="technical_chart.png" alt="Biểu đồ kỹ thuật"></section><section><h2>Tín hiệu kỹ thuật</h2>{technical_table}</section></div>
    <div class="two"><section><h2>So sánh mô hình</h2>{model_table}<h2>Kiểm thử chiến lược ngoài mẫu sau chi phí</h2>{backtest_table}<h2>Mức độ quan trọng của đặc trưng</h2>{feature_table}</section><section><h2>Điều kiện phát hành tín hiệu</h2>{decision_table}<h2>Quản trị rủi ro</h2>{risk_table}</section></div>
    <div class="two"><section><h2>Phân tích cơ bản</h2>{fundamental_table}</section><section><h2>Dự báo ngắn hạn</h2>{forecast_table}</section></div>
    <section><h2>Biểu đồ dự báo</h2><img src="forecast_chart.png" alt="Biểu đồ dự báo"></section>
    <section><h2>Lịch sử giá và mức sụt giảm</h2><img src="history_chart.png" alt="Biểu đồ lịch sử giá"></section>
    <p class="disclaimer">Báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.</p>
  </main>
</body>
</html>
"""
    output_path.write_text(document, encoding="utf-8")
