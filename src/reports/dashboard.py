from __future__ import annotations

import html
import json
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

from src.market_calendar import market_calendar_note, market_holidays
from src.plotting_backend import configure_publication_style, save_figure
from src.utils import safe_float

configure_publication_style()


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
    "swing_frozen_holdout": "Swing qua frozen holdout và stress phí",
    "swing_latest_edge": "Expected excess return swing vượt chi phí + margin",
    "swing_available": "Có artifact swing fixed-horizon",
    "swing_margin_selected": "Margin được chọn hợp lệ trong validation",
    "swing_development_sample": "Development OOS đủ số trade",
    "swing_development_ranking": "Ranking edge dương trên development OOS",
    "swing_frozen_ranking": "Ranking edge dương trên frozen holdout",
    "swing_net_edge": "Frozen holdout có lợi thế ròng sau phí",
    "swing_cost_stress": "Frozen holdout chịu được stress phí 1.5x",
    "swing_uncertainty_calibrated": "Dải bất định đã được conformal calibration",
    "swing_beats_naive_baseline": "Swing vượt baseline excess return bằng 0",
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


def format_signed_percent(value: float | None, decimals: int = 1) -> str:
    return "N/A" if value is None else f"{value:+.{decimals}%}"


def format_metric(value: float | None, unit: str = "number") -> str:
    if value is None:
        return "N/A"
    if unit == "percent":
        return format_percent(value)
    if unit == "money":
        return f"{value / 1_000_000_000:,.1f} tỷ"
    return format_number(value)


def format_money_vnd(value: float | None) -> str:
    return "N/A" if value is None else f"{value:,.0f} VND"


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
    save_figure(figure, output_path)
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
    save_figure(figure, output_path)
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
    save_figure(figure, output_path)
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
    forecast_method = str(forecast.attrs.get("method") or "")
    if forecast_method == "xgboost_direct_quantile_conformal":
        forecast_probability_text = (
            "Quantile forecast ước tính xác suất return cuối kỳ dương từ residual "
            f"frozen holdout: {forecast_end['prob_end_above_latest']:.1%}."
        )
    else:
        forecast_probability_text = (
            "Monte Carlo ước tính xác suất kết thúc trên giá hiện tại: "
            f"{forecast_end['prob_end_above_latest']:.1%}."
        )
    return [
        f"Trạng thái tín hiệu: {signal_status_label(decision['status'])}.",
        *[f"Điều kiện phát hành tín hiệu: {reason}." for reason in decision.get("reasons", [])],
        trend,
        f"Xu hướng kỹ thuật nghiêng về: {technical['bias']}.",
        f"XGBoost ước tính xác suất giá đóng cửa phiên tới cao hơn giá mở cửa: {latest_probabilities['xgboost']:.1%}.",
        f"Mô hình Logistic đối chứng: {latest_probabilities['logistic_regression']:.1%}.",
        forecast_probability_text,
        f"Mức dừng lỗ tham chiếu {format_price(risk_plan['stop_loss'])}, mục tiêu 1 {format_price(risk_plan['target_1'])}, tỷ lệ lợi nhuận/rủi ro {format_number(risk_plan['reward_risk'])}.",
    ]


def _cost_breakdown_rows(strategy: dict, decision: dict | None = None) -> list[tuple[str, str, str]]:
    gross = safe_float(strategy.get("gross_total_return"))
    net = safe_float(strategy.get("net_total_return", strategy.get("total_return")))
    cost_sum = safe_float(strategy.get("transaction_cost_sum"))
    cost_value = safe_float(strategy.get("transaction_cost_value_sum"))
    gross_pnl = safe_float(strategy.get("gross_pnl_sum"))
    net_pnl = safe_float(strategy.get("net_pnl_sum"))
    initial_capital = safe_float(strategy.get("initial_capital"))
    active_sessions = int(strategy.get("active_sessions") or 0)
    completed_round_trips = int(strategy.get("completed_round_trips") or 0)
    entry_cost = safe_float(strategy.get("entry_cost_bps"))
    exit_cost = safe_float(strategy.get("exit_cost_bps"))
    round_trip_cost = safe_float(strategy.get("round_trip_cost_bps"))
    gross_after_cost_gap = None if gross is None or net is None else gross - net
    breakeven_cost_bps = (
        None
        if gross is None
        or cost_sum is None
        or cost_sum <= 0
        or round_trip_cost is None
        else round_trip_cost * gross / cost_sum
    )
    if gross_pnl is None and gross is not None and initial_capital is not None:
        gross_pnl = initial_capital * gross
    if net_pnl is None and net is not None and initial_capital is not None:
        net_pnl = initial_capital * net

    if gross is not None and net is not None and gross > 0 and net < 0:
        action = "Không mở vị thế mới; nếu đang giữ thì xem khung HOLD/REDUCE/SELL riêng theo model health, kỹ thuật, tin và stop-loss."
    elif net is not None and net > 0:
        action = "Sau phí vẫn dương; có thể xem tiếp các gate còn lại trước khi cân nhắc hành động."
    else:
        action = "Không đủ lợi thế sau phí; giữ NO_EDGE."
    if decision and decision.get("status") == "ACTIONABLE" and net is not None and net > 0:
        action = "Sau phí dương và signal đạt; có thể xem xét theo risk plan."

    return [
        (
            "Kịch bản trước chi phí",
            format_signed_percent(gross),
            f"Gross PnL {format_money_vnd(gross_pnl)}; chưa trừ commission/slippage/tax.",
        ),
        (
            "Chi phí giao dịch",
            f"-{format_percent(cost_sum)}" if cost_sum is not None else "N/A",
            (
                f"{completed_round_trips} vòng; entry {format_number(entry_cost, 1)} bps + "
                f"exit {format_number(exit_cost, 1)} bps = {format_number(round_trip_cost, 1)} bps/vòng; "
                f"tổng phí {format_money_vnd(cost_value)}."
            ),
        ),
        (
            "Kịch bản sau chi phí",
            format_signed_percent(net),
            f"Net PnL {format_money_vnd(net_pnl)}; gross - cost gap khoảng {format_signed_percent(gross_after_cost_gap)}.",
        ),
        (
            "Ngưỡng phí hòa vốn",
            f"{format_number(breakeven_cost_bps, 1)} bps/vòng",
            (
                f"Phí hiện tại {format_number(round_trip_cost, 1)} bps/vòng; "
                "cao hơn ngưỡng này thì gross dương vẫn có thể thành net âm."
            ),
        ),
        (
            "Kết luận hành động",
            signal_status_label((decision or {}).get("status", "NO_EDGE")),
            action,
        ),
        (
            "Cách cải thiện cần test",
            "Giảm turnover",
            (
                f"Hiện có {active_sessions} phiên active/{completed_round_trips} vòng; "
                "nên test threshold 0.58/0.60/0.62 hoặc giữ nhiều phiên hơn."
            ),
        ),
    ]


def _capital_scenario_box(strategy: dict, risk_plan: dict) -> str:
    """Render an adjustable capital illustration without changing report evidence.

    A static dashboard cannot recalculate discrete lots, liquidity limits, or a
    full backtest. The control therefore only scales VND illustrations from the
    original return rates; all saved metrics and signal decisions stay intact.
    """

    reference_capital = safe_float(risk_plan.get("capital_reference_vnd"))
    if reference_capital is None:
        reference_capital = safe_float(strategy.get("initial_capital"))
    if reference_capital is None or reference_capital <= 0:
        return ""

    gross_return = safe_float(strategy.get("gross_total_return"))
    net_return = safe_float(strategy.get("net_total_return", strategy.get("total_return")))
    cost_return = safe_float(strategy.get("transaction_cost_sum"))
    risk_pct = safe_float(risk_plan.get("risk_per_trade_pct"))

    def scaled_metric(label: str, rate: float | None) -> str:
        if rate is None:
            return ""
        return (
            '<div class="capital-scenario-metric">'
            f'<span class="capital-scenario-label">{_escape(label)}</span>'
            f'<strong>{_escape(format_signed_percent(rate))}</strong>'
            f'<small data-capital-rate="{rate:.12g}">Đang tính...</small>'
            "</div>"
        )

    risk_metric = ""
    if risk_pct is not None:
        risk_metric = (
            '<div class="capital-scenario-metric">'
            '<span class="capital-scenario-label">Rủi ro/lệnh</span>'
            f'<strong>{_escape(format_percent(risk_pct))}</strong>'
            f'<small data-capital-risk-pct="{risk_pct:.12g}">Đang tính...</small>'
            "</div>"
        )

    metrics = "".join(
        [
            scaled_metric("Gross backtest", gross_return),
            scaled_metric("Phí backtest", -cost_return if cost_return is not None else None),
            scaled_metric("Net backtest", net_return),
            risk_metric,
        ]
    )
    return f"""
      <aside class="capital-scenario" data-reference-capital="{reference_capital:.12g}">
        <label for="assumed-capital-input">Vốn giả định</label>
        <div class="capital-input-row">
          <input id="assumed-capital-input" type="number" min="100000" step="100000" inputmode="numeric" value="{reference_capital:.0f}" aria-describedby="assumed-capital-note">
          <span>VND</span>
        </div>
        <p id="assumed-capital-note">Quy đổi từ tỷ suất của backtest gốc dùng {format_money_vnd(reference_capital)}.</p>
        <div class="capital-scenario-metrics">{metrics}</div>
        <p class="capital-scenario-note">Chỉ quy đổi tiền minh họa. Muốn tính lại số cổ phiếu theo lô, thanh khoản và phí chính xác, cần chạy lại report với vốn đó.</p>
      </aside>
    """


def _turnover_sensitivity_rows(strategy: dict) -> list[dict[str, str]]:
    """Build one consolidated view for base, threshold and trade-count scenarios."""

    rows: list[dict[str, str]] = []

    def add_row(
        scenario: str,
        selection_rule: str,
        item: dict,
        probability_note: str = "",
    ) -> None:
        active_sessions = int(item.get("active_sessions") or 0)
        round_trips = int(item.get("completed_round_trips") or 0)
        gross = safe_float(item.get("gross_total_return"))
        net = safe_float(item.get("net_total_return", item.get("total_return")))
        cost_sum = safe_float(item.get("transaction_cost_sum"))
        sharpe = safe_float(item.get("sharpe_ratio", item.get("sharpe")))
        rows.append(
            {
                "scenario": scenario,
                "selection_rule": selection_rule,
                "round_trips": str(round_trips),
                "active_sessions": str(active_sessions),
                "gross": format_signed_percent(gross),
                "cost": format_percent(cost_sum),
                "net": format_signed_percent(net),
                "sharpe": format_number(sharpe, 2),
                "probability_note": probability_note,
            }
        )

    base_threshold = safe_float(strategy.get("signal_threshold"))
    if strategy:
        base_rule = (
            f"Ngưỡng gốc ≥ {format_number(base_threshold, 2)}"
            if base_threshold is not None
            else "Chiến lược gốc"
        )
        add_row(
            "Gốc",
            base_rule,
            strategy,
            "Baseline lịch sử để đo turnover/phí; không phải số lệnh khuyến nghị.",
        )

    for item in strategy.get("threshold_sensitivity") or []:
        threshold = safe_float(item.get("signal_threshold"))
        if base_threshold is not None and threshold is not None and abs(threshold - base_threshold) < 1e-9:
            continue
        label = f"Ngưỡng {format_number(threshold, 2)}"
        add_row(
            label,
            f"Chỉ vào lệnh khi xác suất ≥ {format_number(threshold, 2)}",
            item,
            "Kịch bản nghiên cứu; cần xác nhận trên holdout/future trước khi dùng làm rule.",
        )

    for item in strategy.get("top_n_trade_sensitivity") or []:
        top_n = int(item.get("top_n") or 0)
        min_probability = safe_float(item.get("min_probability_included"))
        add_row(
            f"Giới hạn {top_n} vòng",
            f"Tối đa {top_n} vòng, ưu tiên xác suất cao hơn",
            item,
            (
                f"Ngưỡng trong nhóm: {format_percent(min_probability)}. "
                "Không dùng làm rule vì chọn số vòng sau khi đã thấy OOS."
            ),
        )

    unique_rows = []
    seen = set()
    for row in rows:
        key = (row["scenario"], row["round_trips"], row["gross"], row["net"])
        if key in seen:
            continue
        seen.add(key)
        unique_rows.append(row)
    return unique_rows


def _turnover_sensitivity_markdown_rows(strategy: dict) -> list[str]:
    rows = _turnover_sensitivity_rows(strategy)
    if not rows:
        return ["| Chưa có dữ liệu | N/A | N/A | N/A | N/A | N/A | N/A | N/A |"]
    return [
        "| {scenario} | {selection_rule} | {round_trips} | {gross} | {cost} | {net} | {sharpe} | {probability_note} |".format(
            **row
        )
        for row in rows
    ]


def _best_after_cost_threshold(strategy: dict) -> dict | None:
    """Return a threshold-sensitivity candidate for monitoring, not a live rule."""

    scenarios = []
    base_threshold = safe_float(strategy.get("signal_threshold"))
    if strategy:
        scenarios.append(
            {
                "label": "Baseline cấu hình",
                "threshold": base_threshold,
                "item": strategy,
            }
        )
    for item in strategy.get("threshold_sensitivity") or []:
        threshold = safe_float(item.get("signal_threshold"))
        if threshold is None:
            continue
        scenarios.append(
            {
                "label": f"Ngưỡng {format_number(threshold, 2)}",
                "threshold": threshold,
                "item": item,
            }
        )

    viable = []
    for scenario in scenarios:
        item = scenario["item"]
        net = safe_float(item.get("net_total_return", item.get("total_return")))
        sharpe = safe_float(item.get("sharpe_ratio", item.get("sharpe")))
        round_trips = int(item.get("completed_round_trips") or 0)
        if (
            net is not None
            and net > 0
            and sharpe is not None
            and sharpe > 0
            and round_trips > 0
        ):
            viable.append(
                {
                    **scenario,
                    "net_total_return": net,
                    "gross_total_return": safe_float(item.get("gross_total_return")),
                    "transaction_cost_sum": safe_float(item.get("transaction_cost_sum")),
                    "sharpe_ratio": sharpe,
                    "completed_round_trips": round_trips,
                }
            )
    if not viable:
        return None
    return sorted(
        viable,
        key=lambda item: (
            item["net_total_return"],
            item["sharpe_ratio"],
            -float(item["threshold"] or 0),
        ),
        reverse=True,
    )[0]


def build_investment_recommendation(
    metrics: dict,
    latest_probabilities: dict,
    decision: dict,
    risk_plan: dict,
    technical: dict | None = None,
    news: dict | None = None,
) -> dict:
    """Translate model/backtest artifacts into a cautious after-cost action."""

    technical = technical or {}
    news = news or {}
    swing = metrics.get("swing_strategy", {}) or {}
    strategy = metrics.get("backtest", {}) or {}
    probability = safe_float(latest_probabilities.get("xgboost"))
    selected = _best_after_cost_threshold(strategy)
    base_net = safe_float(strategy.get("net_total_return", strategy.get("total_return")))
    base_rounds = int(strategy.get("completed_round_trips") or 0)
    selected_threshold = safe_float(selected.get("threshold")) if selected else None
    selected_net = safe_float(selected.get("net_total_return")) if selected else None
    selected_rounds = int(selected.get("completed_round_trips") or 0) if selected else 0
    reward_risk = safe_float(risk_plan.get("reward_risk"))
    status = str((decision or {}).get("status") or "NO_EDGE")
    failed_checks = set((decision or {}).get("failed_checks") or [])
    structural_failures = failed_checks - {"backtest_net_edge", "probability_edge"}
    model_checks = {
        "model_auc",
        "model_balanced_accuracy",
        "model_beats_logistic",
        "backtest_available",
        "backtest_sample",
        "backtest_net_edge",
    }
    failed_model_checks = failed_checks & model_checks
    technical_score = int(technical.get("score", 0) or 0)
    technical_bias = str(technical.get("bias") or "N/A")
    latest_news_features = news.get("latest_asof_features", {}) or {}
    news_negative_count = safe_float(latest_news_features.get("news_negative_count_lookback"), 0.0)
    news_sentiment = safe_float(latest_news_features.get("news_sentiment_mean_lookback"))
    has_news_warning = bool(
        news_negative_count and news_negative_count > 0
    ) or (news_sentiment is not None and news_sentiment < -0.15)

    if swing.get("available"):
        frozen = (swing.get("frozen_holdout", {}) or {}).get("backtest", {}) or {}
        gate = swing.get("publish_gate", {}) or {}
        expected = safe_float(swing.get("latest_expected_excess_return"))
        margin = safe_float(swing.get("selected_entry_margin"), 0.0) or 0.0
        required_return = safe_float(frozen.get("round_trip_cost_bps"), 0.0) / 10_000.0 + margin
        frozen_trades = int(frozen.get("completed_round_trips") or 0)
        minimum_trades = int(swing.get("min_completed_round_trips") or 10)
        evidence_missing = any(
            not gate.get(name, False)
            for name in (
                "margin_selected_in_validation",
                "development_sufficient_trades",
                "sufficient_trades",
                "development_ranking_edge",
                "frozen_ranking_edge",
            )
        )
        model_health = "INSUFFICIENT_EDGE" if evidence_missing else ("OK" if gate.get("passed") else "WEAK")
        model_health_reason = (
            f"Swing fixed-horizon 5D chưa đủ bằng chứng: frozen holdout {frozen_trades}/{minimum_trades} trade; "
            "không dùng classifier 1D hay sensitivity legacy để quyết định."
            if evidence_missing
            else "Swing fixed-horizon đã có đủ sample/ranking; vẫn chờ toàn bộ publish gate."
        )
        if model_health == "INSUFFICIENT_EDGE":
            action, title, reason = "INSUFFICIENT_EDGE", "Chưa có edge 5D đủ để giao dịch", model_health_reason
        elif expected is None or expected <= required_return:
            action, title = "WAIT", "Expected return 5D chưa vượt chi phí"
            reason = f"Expected excess return {format_signed_percent(expected)} chưa vượt chi phí + margin {format_percent(required_return)}."
        elif status == "ACTIONABLE":
            action, title, reason = "BUY_CANDIDATE", "Có thể xem xét mua theo swing 5D", "Frozen holdout, stress phí và expected excess return đều đã qua guard."
        else:
            action, title, reason = "WAIT", "Theo dõi swing 5D, chưa mở vị thế", "Publish guard 5D chưa hoàn tất dù expected return hiện tại đã đạt ngưỡng."
        holding_action = "HOLD_DISCIPLINED" if technical_score >= 2 else "REDUCE"
        holding_reason = (
            "Nếu đã nắm giữ: giữ theo stop-loss, không mua thêm khi swing 5D chưa đủ edge."
            if holding_action == "HOLD_DISCIPLINED"
            else "Kỹ thuật chưa hỗ trợ và swing 5D chưa có edge; ưu tiên giảm rủi ro."
        )
        return {
            "action": action, "title": title, "reason": reason,
            "entry_action": action, "entry_reason": reason,
            "recommended_new_entries": 1 if action == "BUY_CANDIDATE" else 0,
            "holding_action": holding_action, "holding_reason": holding_reason,
            "model_health": model_health, "model_health_reason": model_health_reason,
            "technical_score": technical_score, "technical_bias": technical_bias,
            "news_warning": has_news_warning, "news_negative_count": news_negative_count,
            "news_sentiment": news_sentiment, "current_probability": expected,
            "required_expected_return": required_return, "frozen_holdout_trades": frozen_trades,
            "minimum_swing_trades": minimum_trades, "reward_risk": reward_risk,
            "decision_status": status, "execution_contract": "fixed_horizon_swing_5d",
            "base_net_total_return": base_net, "base_round_trips": base_rounds,
        }

    if not failed_model_checks and selected is not None:
        model_health = "OK"
        model_health_reason = "Model và kiểm thử sau phí đạt các guard chính."
    elif selected is not None:
        model_health = "WEAK"
        model_health_reason = (
            "Có ngưỡng dương trong sensitivity (chưa phải rule live), nhưng model health chưa sạch: "
            + ", ".join(signal_check_label(name) for name in sorted(failed_model_checks))
            + "."
        )
    else:
        model_health = "BAD"
        model_health_reason = (
            "Chưa tìm được ngưỡng nào có net dương và Sharpe dương sau phí trong OOS."
        )

    if selected is None:
        action = "NO_EDGE"
        title = "Chưa có ngưỡng sau phí đủ tốt"
        reason = (
            "Không có threshold nào trong kiểm thử OOS vừa net dương vừa Sharpe dương; "
            "không nên cố mở vị thế."
        )
    elif probability is None:
        action = "NO_EDGE"
        title = "Thiếu xác suất hiện tại"
        reason = "Không có xác suất XGBoost mới nhất để so với ngưỡng sau phí."
    elif probability < selected_threshold:
        action = "WAIT"
        title = "Không có lệnh mua mới hôm nay"
        reason = (
            f"0 lệnh mới: xác suất hiện tại {format_percent(probability)} chưa đạt "
            f"ngưỡng theo dõi {format_number(selected_threshold, 2)}."
        )
    elif structural_failures:
        action = "WATCH"
        title = "Có xác suất nhưng guard mô hình chưa sạch"
        reason = (
            "Xác suất đã vượt ngưỡng sau phí, nhưng vẫn còn guard khác chưa đạt: "
            + ", ".join(signal_check_label(name) for name in sorted(structural_failures))
            + "."
        )
    elif status == "ACTIONABLE":
        action = "BUY_CANDIDATE"
        title = "Có thể xem xét mua theo risk plan"
        reason = (
            f"Xác suất hiện tại {format_percent(probability)} vượt ngưỡng sau phí "
            f"{format_number(selected_threshold, 2)} và publish guard đạt."
        )
    else:
        action = "WATCH"
        title = "Theo dõi, chưa mở vị thế"
        reason = (
            f"Xác suất hiện tại {format_percent(probability)} vượt ngưỡng sau phí "
            f"{format_number(selected_threshold, 2)}, nhưng decision chính vẫn là {signal_status_label(status)}."
        )

    entry_action = action
    recommended_new_entries = 1 if action == "BUY_CANDIDATE" else 0
    entry_reason = reason
    if model_health == "BAD":
        holding_action = "REDUCE_OR_EXIT"
        holding_reason = "Model health xấu và chưa có edge sau phí; nếu đang giữ thì ưu tiên giảm tỷ trọng hoặc thoát theo kỷ luật."
    elif probability is not None and selected_threshold is not None and probability < selected_threshold and has_news_warning:
        holding_action = "REDUCE"
        holding_reason = "Xác suất chưa đạt ngưỡng sau phí và có cảnh báo tin/sentiment; nên giảm rủi ro nếu đang giữ."
    elif probability is not None and selected_threshold is not None and probability < selected_threshold and technical_score >= 2:
        holding_action = "HOLD_DISCIPLINED"
        holding_reason = "Chưa đủ điều kiện mua mới, nhưng kỹ thuật chưa xấu; nếu đang giữ thì có thể giữ có stop-loss, không mua thêm."
    elif probability is not None and selected_threshold is not None and probability >= selected_threshold and model_health == "OK":
        holding_action = "HOLD_OR_ADD_BY_RISK"
        holding_reason = "Xác suất vượt ngưỡng sau phí và model health đạt; có thể giữ hoặc tăng vị thế nhỏ theo risk plan."
    elif technical_score < 0:
        holding_action = "REDUCE"
        holding_reason = "Kỹ thuật yếu và model chưa đủ sạch; ưu tiên giảm tỷ trọng."
    else:
        holding_action = "HOLD_WATCH"
        holding_reason = "Chưa đủ điều kiện mua thêm; nếu đang giữ thì theo dõi sát xác suất, kỹ thuật và stop-loss."

    return {
        "action": action,
        "title": title,
        "reason": reason,
        "entry_action": entry_action,
        "entry_reason": entry_reason,
        "recommended_new_entries": recommended_new_entries,
        "holding_action": holding_action,
        "holding_reason": holding_reason,
        "model_health": model_health,
        "model_health_reason": model_health_reason,
        "technical_score": technical_score,
        "technical_bias": technical_bias,
        "news_warning": has_news_warning,
        "news_negative_count": news_negative_count,
        "news_sentiment": news_sentiment,
        "current_probability": probability,
        "selected_threshold": selected_threshold,
        "selected_threshold_label": selected.get("label") if selected else None,
        "selected_net_total_return": selected_net,
        "selected_round_trips": selected_rounds,
        "base_net_total_return": base_net,
        "base_round_trips": base_rounds,
        "reward_risk": reward_risk,
        "decision_status": status,
    }


def _investment_recommendation_rows(recommendation: dict) -> list[tuple[str, str, str]]:
    if recommendation.get("execution_contract") == "fixed_horizon_swing_5d":
        return [
            ("Lệnh mới hôm nay", f"{int(recommendation.get('recommended_new_entries') or 0)} lệnh", "Không DCA hoặc chia nhỏ lệnh khi fixed-horizon swing chưa qua publish gate."),
            ("Trạng thái edge 5D", str(recommendation.get("model_health") or "UNKNOWN"), str(recommendation.get("model_health_reason") or "")),
            ("Nếu chưa có cổ phiếu", str(recommendation.get("entry_action") or "INSUFFICIENT_EDGE"), str(recommendation.get("entry_reason") or "")),
            ("Nếu đang nắm giữ", str(recommendation.get("holding_action") or "HOLD_WATCH"), str(recommendation.get("holding_reason") or "")),
            ("Expected excess return 5D", format_signed_percent(safe_float(recommendation.get("current_probability"))), f"Cần vượt chi phí + margin {format_percent(safe_float(recommendation.get('required_expected_return')))}."),
            ("Mẫu frozen holdout", f"{int(recommendation.get('frozen_holdout_trades') or 0)}/{int(recommendation.get('minimum_swing_trades') or 0)} trade", "Chưa đủ số trade thì không có kết luận lợi nhuận/Sharpe và không được trade live."),
            ("Kỹ thuật / tin", f"{recommendation.get('technical_score')} điểm", f"{recommendation.get('technical_bias')}; news warning: {'có' if recommendation.get('news_warning') else 'không'}."),
        ]
    threshold = safe_float(recommendation.get("selected_threshold"))
    return [
        (
            "Lệnh mới hôm nay",
            f"{int(recommendation.get('recommended_new_entries') or 0)} lệnh",
            "0 lệnh khi chưa ACTIONABLE. Không chia nhỏ/DCA để che một backtest có turnover cao.",
        ),
        (
            "Model health",
            str(recommendation.get("model_health") or "UNKNOWN"),
            str(recommendation.get("model_health_reason") or ""),
        ),
        (
            "Nếu chưa có cổ phiếu",
            str(recommendation.get("entry_action") or recommendation.get("action") or "NO_EDGE"),
            str(recommendation.get("title") or ""),
        ),
        (
            "Lý do cho mua mới",
            "",
            str(recommendation.get("entry_reason") or recommendation.get("reason") or ""),
        ),
        (
            "Nếu đang nắm giữ",
            str(recommendation.get("holding_action") or "HOLD_WATCH"),
            str(recommendation.get("holding_reason") or ""),
        ),
        (
            "Xác suất hiện tại",
            format_percent(safe_float(recommendation.get("current_probability"))),
            "So với ngưỡng sau phí được chọn từ OOS.",
        ),
        (
            "Ngưỡng theo dõi từ sensitivity",
            format_number(threshold, 2) if threshold is not None else "N/A",
            (
                f"{recommendation.get('selected_threshold_label')}; "
                f"net {format_signed_percent(safe_float(recommendation.get('selected_net_total_return')))}; "
                f"{int(recommendation.get('selected_round_trips') or 0)} vòng; chưa phải rule live."
                if threshold is not None
                else "Chưa có threshold nào đạt net dương + Sharpe dương."
            ),
        ),
        (
            "Baseline cấu hình",
            f"{int(recommendation.get('base_round_trips') or 0)} vòng",
            f"Net sau phí {format_signed_percent(safe_float(recommendation.get('base_net_total_return')))}.",
        ),
        (
            "Reward/Risk",
            format_number(safe_float(recommendation.get("reward_risk")), 2),
            "Chỉ dùng nếu decision cuối cùng cho phép mở vị thế.",
        ),
        (
            "Kỹ thuật / tin",
            f"{recommendation.get('technical_score')} điểm",
            (
                f"{recommendation.get('technical_bias')}; "
                f"news warning: {'có' if recommendation.get('news_warning') else 'không'}; "
                f"sentiment {format_number(safe_float(recommendation.get('news_sentiment')), 2)}."
            ),
        ),
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
    news: dict,
    risk_plan: dict,
    decision: dict,
    output_path: Path,
) -> None:
    latest = levels["latest_close"]
    forecast_end = forecast.iloc[-1]
    calendar_note = market_calendar_note(config)
    calendar_holidays = market_holidays(config)
    investment_recommendation = build_investment_recommendation(
        metrics,
        latest_probabilities,
        decision,
        risk_plan,
        technical,
        news,
    )
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
        f"- Model health: {investment_recommendation['model_health']} - {investment_recommendation['model_health_reason']}",
        f"- Nếu chưa có cổ phiếu: {investment_recommendation['entry_action']} - {investment_recommendation['entry_reason']}",
        f"- Nếu đang nắm giữ: {investment_recommendation['holding_action']} - {investment_recommendation['holding_reason']}",
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

    lines.extend(["", "## Tin tức doanh nghiệp (research only)", ""])
    if news.get("available"):
        lines.extend(
            [
                f"- Nguồn: {news.get('provider')}; số bài lấy được: {news.get('article_count', 0)}.",
                f"- Bài có timestamp đủ điều kiện point-in-time: {news.get('eligible_article_count', 0)}.",
                f"- Sentiment trung bình: {format_number(safe_float(news.get('mean_sentiment')), 2)} ({news.get('analysis_method')}).",
                f"- Bài mới nhất: {news.get('latest_published_at') or 'N/A'}.",
            ]
        )
    else:
        lines.append("- Chưa lấy được dữ liệu tin tức.")
    lines.extend(f"- Ghi chú dữ liệu: {note}" for note in news.get("notes", []))

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
    swing = metrics.get("swing_strategy", {}) or {}
    if strategy and (not swing.get("available") or bool(strategy.get("available"))):
        lines.append(
            f"- {'Diagnostic classifier 1D legacy' if swing.get('available') else 'Kiểm thử chiến lược ngoài mẫu sau chi phí'}: tổng lợi nhuận {format_percent(safe_float(strategy.get('net_total_return', strategy.get('total_return'))))}; "
            f"Sharpe {format_number(safe_float(strategy.get('sharpe_ratio', strategy.get('sharpe'))), 2)}; "
            f"mức sụt giảm tối đa {format_percent(safe_float(strategy.get('max_drawdown')))}."
        )
        if not swing.get("available"):
            lines.extend(["", "### Khuyến nghị hành động sau phí", ""])
            lines.extend(["| Mục | Kết quả | Diễn giải |", "|---|---:|---|"])
            lines.extend(
                f"| {name} | {value} | {detail} |"
                for name, value, detail in _investment_recommendation_rows(investment_recommendation)
            )
        lines.extend(
            [
                "",
                "### Breakdown legacy 1D trước phí / sau phí"
                if swing.get("available")
                else "### Breakdown trước phí / sau phí",
                "",
            ]
        )
        lines.extend(["| Kịch bản | Kết quả | Diễn giải |", "|---|---:|---|"])
        lines.extend(
            f"| {name} | {value} | {detail} |"
            for name, value, detail in _cost_breakdown_rows(strategy, decision)
        )
        lines.extend(
            [
                "",
                "### Phụ lục legacy 1D — Kiểm thử kịch bản lịch sử (không phải khuyến nghị giao dịch)"
                if swing.get("available")
                else "### Kiểm thử kịch bản lịch sử (không phải khuyến nghị giao dịch)",
                "",
            ]
        )
        lines.extend(
            [
                "| Kịch bản | Cách chọn | Vòng | Gross trước phí | Phí | Net sau phí | Sharpe | Ghi chú |",
                "|---|---|---:|---:|---:|---:|---:|---|",
            ]
        )
        lines.extend(_turnover_sensitivity_markdown_rows(strategy))
        lines.append(
            "Ghi chú: baseline chỉ để đo turnover/phí. Không dùng bảng để chọn 1 lệnh hoặc DCA; các dòng threshold cần holdout/future đã khóa, còn 10/5/1 có selection bias vì số vòng được chọn sau khi đã thấy OOS. Khi signal chưa ACTIONABLE, lệnh mới hôm nay là 0."
        )
    if swing.get("available"):
        frozen = swing.get("frozen_holdout", {}) or {}
        frozen_backtest = frozen.get("backtest", {}) or {}
        gate = swing.get("publish_gate", {}) or {}
        lines.extend(
            [
                "",
                "## Chiến lược swing 5 phiên: contract phát hành tín hiệu",
                "",
                "### Khuyến nghị hành động sau phí",
                "",
                "| Mục | Kết quả | Diễn giải |",
                "|---|---:|---|",
                *(
                    f"| {name} | {value} | {detail} |"
                    for name, value, detail in _investment_recommendation_rows(investment_recommendation)
                ),
                "",
                f"- Target: {swing.get('target_definition') or swing.get('target')}",
                f"- Expected excess return mới nhất: {format_signed_percent(safe_float(swing.get('latest_expected_excess_return')))}; safety margin đã chọn {format_percent(safe_float(swing.get('selected_entry_margin')))}.",
                f"- Frozen holdout: {int(frozen_backtest.get('completed_round_trips') or 0)}/{int(swing.get('min_completed_round_trips') or 0)} trade; net/Sharpe chỉ được kết luận khi đủ mẫu.",
                f"- Publish gate swing: {'ĐẠT' if gate.get('passed') else 'CHƯA ĐẠT'}. Gate yêu cầu sample/ranking dương ở development+frozen, net/Sharpe dương và stress phí 1.5×; chưa đạt thì giữ NO_EDGE.",
                "- Các file audit: swing_development_oos.csv, swing_frozen_holdout.csv, swing_development_backtest.csv, swing_frozen_backtest.csv và file trades tương ứng.",
            ]
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
            (
                "- Phương pháp: XGBoost direct quantile 5/10/20D + conformal calibration; "
                f"toàn bộ horizon qua gate: {'có' if (metrics.get('forecast_model', {}) or {}).get('all_horizons_publish_ready') else 'chưa'}."
                if (metrics.get("forecast_model", {}) or {}).get("method")
                == "xgboost_direct_quantile_conformal"
                else "- Phương pháp: Monte Carlo fallback."
            ),
            f"- P50 cuối kỳ {forecast_end['p50']:.2f} ({forecast_end['p50'] / latest - 1:.2%}).",
            f"- P10/P90 cuối kỳ {forecast_end['p10']:.2f} / {forecast_end['p90']:.2f}.",
            f"- Lịch giao dịch: {calendar_note}",
            f"- Ngày nghỉ đã loại khỏi forecast: {', '.join(calendar_holidays) or 'chưa cấu hình'}.",
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


def _pulse_card(
    label: str,
    value: str,
    detail: str = "",
    tone: str = "neutral",
    status: str = "",
) -> str:
    """Render a compact, stateful market KPI for the dashboard hero."""

    status_markup = (
        f'<div class="pulse-status">{_escape(status)}</div>' if status else ""
    )
    return (
        f'<article class="pulse-card {_escape(tone)}">'
        '<div class="pulse-head">'
        f'<div class="pulse-label"><span class="pulse-mark" aria-hidden="true"></span>{_escape(label)}</div>'
        '<span class="pulse-help" aria-hidden="true">?</span>'
        "</div>"
        f'<div class="pulse-value">{_escape(value)}</div>'
        f'<div class="pulse-detail">{_escape(detail)}</div>'
        f"{status_markup}"
        "</article>"
    )


def _status_tone(value: object) -> str:
    """Classify human-readable dashboard states without changing their meaning."""

    normalized = str(value or "").strip().casefold()
    if not normalized:
        return "neutral"
    if any(token in normalized for token in ("không đạt", "chưa đạt", "fail", "insufficient", "reduce")):
        return "negative"
    if normalized in {"đạt", "ok", "có dữ liệu", "actionable", "buy_candidate", "tích cực", "ổn định"}:
        return "positive"
    if any(token in normalized for token in ("watch", "wait", "no_edge", "research_only", "n/a", "chưa có", "cẩn thận", "yếu")):
        return "warning"
    return "neutral"


def _status_chip(value: object) -> str:
    return f'<span class="status-chip {_status_tone(value)}">{_escape(value)}</span>'


def _table(
    rows: list[tuple[str, str, str]],
    *,
    headers: tuple[str, str, str] = ("Hạng mục", "Kết quả", "Cách đọc"),
    status_column: bool = False,
) -> str:
    """Render a compact, readable dashboard table with optional status badges."""

    body = "".join(
        "<tr>"
        f"<td>{_escape(name)}</td>"
        f"<td class=\"table-value\">{_status_chip(value) if status_column else _escape(value)}</td>"
        f"<td class=\"table-detail\">{_escape(detail)}</td>"
        "</tr>"
        for name, value, detail in rows
    )
    head = "".join(f"<th>{_escape(header)}</th>" for header in headers)
    return f'<div class="table-wrap report-table-wrap"><table class="report-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def _html_table(headers: list[str], rows: list[list[str]], *, status_column: int | None = None) -> str:
    """Render a responsive HTML table from already-escaped cells."""

    head = "".join(f"<th>{_escape(header)}</th>" for header in headers)

    def render_row(row: list[str]) -> str:
        cells = []
        for index, cell in enumerate(row):
            class_attr = ' class="table-value"' if index == status_column else ""
            value = _status_chip(cell) if index == status_column else cell
            cells.append(f"<td{class_attr}>{value}</td>")
        return "<tr>" + "".join(cells) + "</tr>"

    body = "".join(render_row(row) for row in rows)
    return f'<div class="table-wrap report-table-wrap"><table class="report-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def _gate_overview(checks: dict[str, object], detail_table: str) -> str:
    """Keep the release gate legible while retaining every audit condition on demand."""

    total = len(checks)
    passed = [signal_check_label(name) for name, value in checks.items() if value]
    failed = [signal_check_label(name) for name, value in checks.items() if not value]
    failed_markup = (
        "".join(f'<li><span class="status-dot negative"></span>{_escape(label)}</li>' for label in failed)
        if failed
        else '<li><span class="status-dot positive"></span>Không có điều kiện nào chưa đạt.</li>'
    )
    return f"""
    <div class="gate-overview">
      <div class="gate-score"><strong>{len(passed)}/{total}</strong><span>điều kiện đã đạt</span></div>
      <div class="gate-next"><span class="eyebrow">Cần cải thiện</span><ul>{failed_markup}</ul></div>
    </div>
    <details class="detail-section gate-detail"><summary>Xem toàn bộ {total} điều kiện kiểm định</summary>{detail_table}</details>
    """


def _accordion(title: str, body: str, *, open_by_default: bool = False, note: str = "") -> str:
    open_attr = " open" if open_by_default else ""
    note_html = f'<span class="accordion-note">{_escape(note)}</span>' if note else ""
    return (
        f'<details class="accordion"{open_attr}>'
        f'<summary><span>{_escape(title)}</span>{note_html}</summary>'
        f'<div class="accordion-body">{body}</div>'
        "</details>"
    )


def _read_dashboard_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _external_link(url: object, label: str = "Mở nguồn") -> str:
    value = str(url or "")
    if not value.startswith(("https://", "http://")):
        return "N/A"
    return f'<a href="{_escape(value)}" target="_blank" rel="noopener noreferrer">{_escape(label)}</a>'


def _list_items(items: list[object]) -> str:
    if not items:
        return "<p class=\"muted\">Chưa có dữ liệu.</p>"
    return "<ul>" + "".join(f"<li>{_escape(item)}</li>" for item in items) + "</ul>"


def _news_impact_section(report_directory: Path) -> str:
    impact = _read_dashboard_json(report_directory / "news_impact_summary.json")
    if not impact:
        return ""

    delta = impact.get("probability_delta")
    delta_text = "N/A" if delta is None else f"{float(delta):+.1%}"
    importance = impact.get("news_feature_importance_gain") or {}
    importance_rows = [
        [_escape(name), format_number(safe_float(value), 3)]
        for name, value in importance.items()
        if str(name).startswith("news_")
    ] or [["N/A", "N/A"]]
    gates = impact.get("gates") or {}
    gate_rows = [
        [_escape(name), "Đạt" if passed else "Chưa đạt"]
        for name, passed in gates.items()
    ] or [["N/A", "N/A"]]
    failed = impact.get("failed_gates") or []
    failed_text = ", ".join(str(item) for item in failed) if failed else "Không"
    return f"""
    <section>
      <h2>Tác động của tin lên model</h2>
      <div class="grid">
        {_metric_card("Base XGBoost", format_percent(safe_float(impact.get("base_xgboost_probability"))), "Model chính hiện dùng cho signal")}
        {_metric_card("News-adjusted XGBoost", format_percent(safe_float(impact.get("news_adjusted_xgboost_probability"))), "Model phụ có thêm feature tin")}
        {_metric_card("Chênh lệch xác suất", delta_text, "News-adjusted trừ Base")}
        {_metric_card("Số bài tin", str(impact.get("symbol_article_count") or 0), "Tin trong CSV của mã này")}
      </div>
      <p><strong>Trạng thái:</strong> {_escape(impact.get("status") or "research_only")} · <strong>Áp vào signal chính:</strong> {_escape(impact.get("effect_on_primary_signal") or "not_applied")}</p>
      <p><strong>Khuyến nghị hệ thống:</strong> {_escape(impact.get("recommendation") or "")}</p>
      <p><strong>Gate chưa đạt:</strong> {_escape(failed_text)}</p>
      <h3>News feature importance</h3>
      {_html_table(["Feature tin", "Gain"], importance_rows)}
      <h3>Điều kiện bật news vào signal chính</h3>
      {_html_table(["Gate", "Kết quả"], gate_rows, status_column=1)}
      <p class="muted">{_escape(impact.get("limitation") or "News model đang là lớp research/shadow.")}</p>
    </section>
    """


def _statement_detail(report_directory: Path, filename: str, label: str) -> str:
    path = report_directory / filename
    if not path.exists():
        return ""
    try:
        frame = pd.read_csv(path)
    except (OSError, pd.errors.ParserError, UnicodeDecodeError):
        return ""
    if frame.empty or "item" not in frame.columns:
        return ""
    periods = sorted(
        (column for column in frame.columns if len(column) == 7 and column[4:6] == "-Q"),
        reverse=True,
    )[:4]
    if not periods:
        return ""
    rows = []
    for _, row in frame.head(35).iterrows():
        values = [_escape(row.get("item", "N/A"))]
        for period in periods:
            value = safe_float(row.get(period))
            values.append("N/A" if value is None else f"{value / 1_000_000_000:,.1f} tỷ")
        rows.append(values)
    table = _html_table(["Khoản mục", *periods], rows)
    return (
        "<details class=\"detail-section\">"
        f"<summary>{_escape(label)} — 4 kỳ gần nhất</summary>"
        f"<p class=\"muted\">Hiển thị 35 dòng đầu; <a href=\"{_escape(filename)}\" target=\"_blank\">mở CSV đầy đủ</a>.</p>"
        f"{table}</details>"
    )


def enhance_dashboard_with_research(report_directory: Path, ai_result: dict | None = None) -> None:
    """Append auditable AI, web-research and statement details to one report dashboard.

    The base dashboard is created by the ML run. This function is deliberately
    idempotent because research and AI may be run later as separate CLI commands.
    """

    dashboard_path = report_directory / "dashboard.html"
    if not dashboard_path.exists():
        return
    document = dashboard_path.read_text(encoding="utf-8")
    live_research = _read_dashboard_json(report_directory / "live_research.json")
    news_reader = _read_dashboard_json(report_directory / "news_reader.json")
    analysis = ai_result or _read_dashboard_json(report_directory / "ai_analysis.json")
    news_impact = _news_impact_section(report_directory)

    live_rows = [
        [
            _escape(article.get("publisher") or "N/A"),
            _escape(article.get("title") or "N/A"),
            _escape(article.get("published_at") or "N/A"),
            _external_link(article.get("url")),
        ]
        for article in live_research.get("articles", []) or []
        if isinstance(article, dict)
    ]
    live_table = _html_table(
        ["Nguồn", "Tiêu đề", "Thời điểm", "Link"],
        live_rows,
    ) if live_rows else "<p class=\"muted\">Chưa có snapshot live research cho report này.</p>"

    reader_rows = []
    for article in news_reader.get("articles", []) or []:
        if not isinstance(article, dict):
            continue
        excerpt = str(article.get("content_excerpt") or article.get("description") or "Không trích được nội dung.")
        reader_rows.append(
            [
                _escape(article.get("publisher") or "N/A"),
                _escape(article.get("title") or "N/A"),
                _escape(", ".join(article.get("topics") or []) or "khác"),
                _escape(article.get("published_at") or "N/A"),
                "<details><summary>Xem trích đoạn</summary>"
                f"<p>{_escape(excerpt)}</p></details>",
                _external_link(article.get("final_url") or article.get("publisher_url") or article.get("url")),
            ]
        )
    reader_table = _html_table(
        ["Nguồn", "Tiêu đề", "Nhóm", "Thời điểm", "Trích đoạn đã đọc", "Link"],
        reader_rows,
    ) if reader_rows else "<p class=\"muted\">News Reader chưa đọc được bài gốc nào.</p>"

    ai_snapshot = ""
    ai_section = ""
    if analysis:
        decision = _escape(analysis.get("decision_status") or "UNKNOWN")
        ai_snapshot = f"""
        <article class="ai-summary">
          <div>
            <div class="eyebrow">AI research · có kiểm chứng</div>
            <h3>AI tóm tắt từ artifact, headline và trích đoạn đã lưu</h3>
            <p>{_escape(analysis.get("summary") or "AI chưa trả về phần tóm tắt cho report này.")}</p>
          </div>
          <div class="ai-summary-meta">
            <span>Trạng thái signal gốc</span>
            <strong>{decision}</strong>
            <span>AI không có quyền ghi đè publish guard hoặc tạo lệnh mua/bán.</span>
          </div>
        </article>
        """
        ai_section = _accordion(
            "Phân tích AI có kiểm chứng",
            f"""
          <p><strong>Trạng thái quyết định:</strong> {decision}</p>
          <p><strong>Tóm tắt:</strong> {_escape(analysis.get("summary") or "N/A")}</p>
          <p><strong>Kỹ thuật:</strong> {_escape(analysis.get("technical_view") or "N/A")}</p>
          <p><strong>Cơ bản:</strong> {_escape(analysis.get("fundamental_view") or "N/A")}</p>
          <p><strong>Tin tức:</strong> {_escape(analysis.get("news_view") or "N/A")}</p>
          <p><strong>Live research:</strong> {_escape(analysis.get("live_research_view") or "N/A")}</p>
          <h3>Rủi ro cần kiểm chứng</h3>{_list_items(analysis.get("risks") or [])}
          <h3>Bằng chứng</h3>{_list_items(analysis.get("evidence") or [])}
          <p class="muted">{_escape(analysis.get("disclaimer") or "Không phải khuyến nghị mua/bán.")}</p>
            """,
            open_by_default=False,
            note="bấm mở",
        )

    statements = "".join(
        _statement_detail(report_directory, filename, label)
        for filename, label in (
            ("income_statement.csv", "Kết quả kinh doanh"),
            ("balance_sheet.csv", "Bảng cân đối kế toán"),
            ("cash_flow.csv", "Lưu chuyển tiền tệ"),
        )
    )
    statement_section = (
        _accordion("Chi tiết báo cáo tài chính", statements, note="bảng dài")
        if statements
        else ""
    )
    enrichment = f"""
    <!-- FinAI dynamic enrichment start -->
    <section class="research-workspace" aria-labelledby="research-heading">
      <div class="section-title"><div><div class="eyebrow">Evidence-first research</div><h2 id="research-heading">AI phân tích & tin tức có nguồn</h2></div><span class="section-kicker">AI chỉ tóm tắt dữ liệu đã lưu, không tự tạo tín hiệu</span></div>
      {ai_snapshot}
      <div class="two">
        <div class="stack">{ai_section}{_accordion("Tin web đã lấy", live_table, note="headline + nguồn")}</div>
        <div class="stack">{_accordion("News Reader: bài đã đọc và trích đoạn", reader_table, note="bấm mở trích đoạn")}{news_impact}</div>
      </div>
      {statement_section}
    </section>
    <!-- FinAI dynamic enrichment end -->
    """
    start = "<!-- FinAI dynamic enrichment start -->"
    end = "<!-- FinAI dynamic enrichment end -->"
    if start in document and end in document:
        before, _, remainder = document.partition(start)
        _, _, after = remainder.partition(end)
        document = before + enrichment + after
    else:
        document = document.replace("</main>", enrichment + "\n  </main>", 1)
    dashboard_path.write_text(document, encoding="utf-8")


def _chart_number(value: object) -> float | None:
    number = safe_float(value)
    if number is None or not np.isfinite(number):
        return None
    return round(float(number), 6)


def _interactive_chart_payload(frame: pd.DataFrame, symbol: str) -> str:
    """Serialize a bounded OHLCV window for the self-contained browser chart."""

    chart_frame = frame.tail(1600).copy()
    close = pd.to_numeric(chart_frame.get("close"), errors="coerce")
    chart_drawdown = close.div(close.cummax()).sub(1)

    def series(name: str, fallback: pd.Series | None = None) -> pd.Series:
        if name in chart_frame:
            return pd.to_numeric(chart_frame[name], errors="coerce")
        if fallback is not None:
            return fallback
        return pd.Series(np.nan, index=chart_frame.index, dtype=float)

    open_price = series("open", close)
    high = series("high", pd.concat([open_price, close], axis=1).max(axis=1))
    low = series("low", pd.concat([open_price, close], axis=1).min(axis=1))
    rows = []
    for index, values in pd.DataFrame(
        {
            "open": open_price,
            "high": high,
            "low": low,
            "close": close,
            "volume": series("volume"),
            "sma20": series("sma_20"),
            "sma60": series("sma_60"),
            "bbUpper": series("bb_upper_20"),
            "bbLower": series("bb_lower_20"),
            "rsi": series("rsi_14"),
            "macd": series("macd"),
            "macdSignal": series("macd_signal"),
            "macdHist": series("macd_hist"),
            "drawdown": chart_drawdown,
        }
    ).iterrows():
        if pd.isna(values["close"]):
            continue
        rows.append(
            {
                "date": pd.Timestamp(index).strftime("%Y-%m-%d"),
                **{name: _chart_number(value) for name, value in values.items()},
            }
        )
    payload = json.dumps(
        {"symbol": symbol, "rows": rows},
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return payload.replace("</", "<\\/")


INTERACTIVE_CHART_CSS = r"""
    html[data-theme="dark"] {
      --bg:#080d17; --ink:#e8edf7; --muted:#8f9bad; --line:#263143;
      --panel:#111827; --navy:#e8edf7; --blue:#60a5fa; --cyan:#2dd4bf;
      --red:#f87171; --amber:#fbbf24; --soft-blue:#172554;
      --soft-amber:#292113; --soft-slate:#151e2d;
      --shadow:0 18px 42px rgba(0,0,0,.28);
    }
    body, header, .quick-nav, .metric, section, .accordion,
    .accordion > summary, th, td, .capital-scenario, input {
      transition:background-color .22s ease,color .22s ease,border-color .22s ease;
    }
    html[data-theme="dark"] header {
      background:radial-gradient(circle at 84% -15%,#173a64 0%,transparent 32%),
                 linear-gradient(125deg,#060a12 0%,#0b1320 52%,#102137 100%);
    }
    html[data-theme="dark"] .quick-nav { background:rgba(8,13,23,.9); }
    html[data-theme="dark"] .quick-nav a,
    html[data-theme="dark"] .accordion > summary,
    html[data-theme="dark"] .capital-scenario { background:var(--panel); color:var(--ink); }
    html[data-theme="dark"] .decision-summary {
      background:linear-gradient(110deg,#111827 0%,#0f1b2d 100%);
      border-color:var(--line);
    }
    html[data-theme="dark"] .decision-summary p { color:var(--muted); }
    html[data-theme="dark"] td:nth-child(2) { color:#7db7ff; }
    html[data-theme="dark"] img { background:#e9eef5; }
    .nav-spacer { flex:1; }
    .ui-button {
      appearance:none; border:1px solid var(--line); background:var(--panel); color:var(--ink);
      border-radius:8px; padding:7px 10px; font:inherit; font-size:12px; font-weight:750;
      cursor:pointer; white-space:nowrap;
    }
    .ui-button:hover { border-color:var(--blue); color:var(--blue); }
    .ui-button.active { color:#fff; background:#2563eb; border-color:#2563eb; }
    #theme-toggle { display:inline-flex; align-items:center; gap:7px; }
    .market-terminal {
      padding:0; overflow:hidden; border-radius:15px; background:#0b111c;
      border:1px solid #273247; box-shadow:0 24px 55px rgba(7,15,29,.24);
    }
    .terminal-head {
      display:flex; align-items:flex-start; justify-content:space-between; gap:18px; flex-wrap:wrap;
      padding:19px 20px; color:#e8edf7; background:linear-gradient(100deg,#111827,#132238);
      border-bottom:1px solid #273247;
    }
    .chart-title-block { min-width:0; }
    .chart-title-row { display:flex; align-items:center; gap:12px; flex-wrap:wrap; }
    .chart-title-row h2 { margin:0; font-size:20px; color:#f8fafc; letter-spacing:-.02em; }
    .chart-chip { padding:5px 9px; border-radius:7px; background:#1e2b40; color:#aab7cb; font:700 12px ui-monospace,SFMono-Regular,monospace; }
    .chart-snapshot { display:flex; align-items:center; gap:10px 15px; flex-wrap:wrap; margin-top:10px; color:#aab7c6; font:600 12px ui-monospace,SFMono-Regular,monospace; }
    .chart-snapshot strong { color:#f8fafc; font-size:13px; }
    .chart-snapshot .up,.chart-snapshot .positive { color:#2dd4bf; }.chart-snapshot .down,.chart-snapshot .negative { color:#fb7185; }
    .chart-snapshot .sma20 { color:#60a5fa; }.chart-snapshot .sma60 { color:#fbbf24; }
    .terminal-actions { display:flex; align-items:center; gap:10px; flex-wrap:wrap; }
    .data-table-trigger { color:#bcd4ff!important; border-color:#315784!important; background:#111e31!important; }
    .live-label { display:flex; align-items:center; gap:7px; color:#9eabbf; font-size:12px; }
    .live-dot { width:8px; height:8px; border-radius:50%; background:#22c55e; box-shadow:0 0 0 5px rgba(34,197,94,.12); }
    .chart-toolbar {
      display:flex; align-items:center; gap:8px; flex-wrap:wrap; padding:9px 12px;
      background:#0f1724; border-bottom:1px solid #273247;
    }
    .chart-toolbar .ui-button { color:#b9c3d4; background:#151f2f; border-color:#2b374b; padding:6px 9px; }
    .chart-toolbar .ui-button:hover { color:#fff; border-color:#5b7295; }
    .chart-toolbar .ui-button.active { color:#fff; background:#2563eb; border-color:#3b82f6; }
    .chart-toolbar .mdd-toggle { color:#fda4af; border-color:#7f1d2d; background:#27141b; }
    .chart-toolbar .mdd-toggle.active { color:#fecdd3; border-color:#e11d48; background:#4c1723; }
    .tool-separator { width:1px; height:24px; background:#2b374b; margin:0 2px; }
    .chart-stage { position:relative; height:640px; min-height:440px; background:#0b111c; touch-action:none; }
    #market-canvas { display:block; width:100%; height:100%; cursor:crosshair; }
    .chart-tooltip {
      position:absolute; z-index:4; pointer-events:none; min-width:192px; padding:9px 10px;
      border:1px solid rgba(148,163,184,.28); border-radius:8px; color:#dbe5f3;
      background:rgba(10,17,28,.92); box-shadow:0 10px 28px rgba(0,0,0,.3);
      font-size:12px; line-height:1.55; opacity:0; transform:translate(12px,12px);
    }
    .chart-tooltip.visible { opacity:1; }
    .chart-tooltip b { color:#fff; }
    .chart-legend {
      display:flex; gap:18px; flex-wrap:wrap; padding:10px 16px; color:#9eabbf;
      background:#0f1724; border-top:1px solid #273247; font-size:11px;
    }
    .legend-item::before { content:""; display:inline-block; width:18px; height:3px; margin-right:6px; vertical-align:middle; border-radius:5px; background:var(--legend); }
    .chart-help { margin-left:auto; }
    .static-fallback img { margin-top:12px; }
    .market-data-modal { width:min(1120px,calc(100vw - 32px)); max-height:min(82vh,800px); margin:auto; padding:0; color:#e7edf7; background:#0d131d; border:1px solid #2b3a50; border-radius:14px; box-shadow:0 28px 90px rgba(0,0,0,.62); }
    .market-data-modal::backdrop { background:rgba(0,0,0,.7); backdrop-filter:blur(4px); }
    .market-data-shell { display:flex; flex-direction:column; max-height:min(82vh,800px); }
    .market-data-head { display:flex; align-items:center; justify-content:space-between; gap:16px; padding:16px 18px; border-bottom:1px solid #263449; background:linear-gradient(100deg,#101925,#121d2d); }
    .market-data-head h2 { margin:0; color:#f8fafc; font-size:17px; }.market-data-head p { margin:4px 0 0; color:#8f9bad; font-size:12px; }
    .market-data-actions { display:flex; align-items:center; gap:8px; }.market-data-close { min-width:32px; padding:6px 9px; color:#aebbd0!important; background:transparent!important; }
    .market-data-toolbar { display:flex; align-items:center; justify-content:space-between; gap:12px; flex-wrap:wrap; padding:12px 18px; border-bottom:1px solid #1d2a3d; background:#0b111b; }
    .market-data-search { min-width:min(280px,100%); padding:8px 10px; color:#dbe5f3; border:1px solid #2b3b52; border-radius:8px; background:#111b2a; font:12px ui-monospace,SFMono-Regular,monospace; }.market-data-search:focus { outline:2px solid rgba(96,165,250,.42); border-color:#60a5fa; }
    .market-data-scroll { min-height:0; overflow:auto; }.market-data-table { min-width:980px; width:100%; border-collapse:collapse; font:12px ui-monospace,SFMono-Regular,monospace; }
    .market-data-table th { position:sticky; top:0; z-index:1; padding:10px 9px; color:#8f9bad; border-bottom:1px solid #2b3a50; background:#121b28; font-size:10px; text-transform:none; letter-spacing:0; white-space:nowrap; }
    .market-data-table td { padding:9px; color:#b7c5d8; border-top:1px solid #1d2a3a; white-space:nowrap; }.market-data-table tbody tr:hover { background:#142238; }.market-data-table td.up { color:#2dd4bf; font-weight:750; }.market-data-table td.down { color:#fb7185; font-weight:750; }.market-data-table td.sma20 { color:#7db7ff; font-weight:750; }.market-data-table td.sma60 { color:#fbbf24; font-weight:750; }.market-data-table td.rsi { color:#34d399; font-weight:750; }.market-data-table td.mdd { color:#fda4af; font-weight:750; }
    .market-data-footer { display:flex; align-items:center; justify-content:space-between; gap:12px; padding:12px 18px; color:#8f9bad; border-top:1px solid #263449; background:#0b111b; font-size:12px; }.market-data-pagination { display:flex; gap:7px; }.market-data-pagination .ui-button { padding:5px 9px; }.market-data-empty { padding:22px 18px; color:#8f9bad; text-align:center; }
    @media (max-width:760px) {
      .chart-stage { height:520px; }
      .chart-help { width:100%; margin-left:0; }
      .tool-separator { display:none; }
      .terminal-head { align-items:flex-start; }
      .chart-title-row h2 { font-size:17px; }
      .market-data-modal { width:calc(100vw - 18px); max-height:88vh; }.market-data-shell { max-height:88vh; }.market-data-head,.market-data-toolbar,.market-data-footer { padding-left:12px; padding-right:12px; }.market-data-search { width:100%; min-width:0; }
    }
"""


INTERACTIVE_CHART_JS = r"""
(() => {
  const root = document.documentElement;
  const themeButton = document.getElementById('theme-toggle');
  const preferredTheme = () => {
    try { return localStorage.getItem('vn-stock-dashboard-theme'); } catch (_) { return null; }
  };
  const setTheme = (theme) => {
    root.dataset.theme = theme;
    if (themeButton) themeButton.querySelector('span').textContent = theme === 'dark' ? 'Giao diện sáng' : 'Giao diện tối';
    try { localStorage.setItem('vn-stock-dashboard-theme', theme); } catch (_) {}
    window.dispatchEvent(new Event('dashboard-theme-change'));
  };
  // Financial workspace starts in dark mode like the charting surface; users can
  // still persist a light preference with the toggle.
  setTheme(preferredTheme() || 'dark');
  themeButton?.addEventListener('click', () => setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark'));

  const source = document.getElementById('market-chart-data');
  const canvas = document.getElementById('market-canvas');
  const stage = document.querySelector('.chart-stage');
  if (!source || !canvas || !stage) return;
  const payload = JSON.parse(source.textContent);
  const rows = payload.rows || [];
  if (!rows.length) return;
  const dataModal = document.getElementById('market-data-modal');
  const dataBody = document.getElementById('market-data-body');
  const dataEmpty = document.getElementById('market-data-empty');
  const dataPage = document.getElementById('market-data-page');
  const dataSearch = document.getElementById('market-data-search');
  const dataSort = document.getElementById('market-data-sort');
  const dataPrev = document.getElementById('market-data-prev');
  const dataNext = document.getElementById('market-data-next');
  const tableState = { query:'', newestFirst:true, page:0, pageSize:20 };
  const escapeHtml = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[char]));
  const tableNumber = (value, digits = 2) => finite(value) ? Number(value).toLocaleString('vi-VN', { minimumFractionDigits:digits, maximumFractionDigits:digits }) : '—';
  const tableVolume = (value) => finite(value) ? Math.round(Number(value)).toLocaleString('vi-VN') : '—';
  const tableRows = () => rows.filter((row) => row.date.includes(tableState.query)).sort((left, right) => tableState.newestFirst ? right.date.localeCompare(left.date) : left.date.localeCompare(right.date));
  const renderDataTable = () => {
    if (!dataBody || !dataPage || !dataEmpty) return;
    const filtered = tableRows();
    const totalPages = Math.max(1, Math.ceil(filtered.length / tableState.pageSize));
    tableState.page = Math.min(tableState.page, totalPages - 1);
    const start = tableState.page * tableState.pageSize;
    const pageRows = filtered.slice(start, start + tableState.pageSize);
    dataBody.innerHTML = pageRows.map((row) => {
      const closeClass = Number(row.close) >= Number(row.open) ? 'up' : 'down';
      const drawdown = finite(row.drawdown) ? `${(Number(row.drawdown) * 100).toFixed(2)}%` : '—';
      return `<tr><td>${escapeHtml(row.date)}</td><td>${tableNumber(row.open)}</td><td class="up">${tableNumber(row.high)}</td><td class="down">${tableNumber(row.low)}</td><td class="${closeClass}">${tableNumber(row.close)}</td><td>${tableVolume(row.volume)}</td><td class="sma20">${tableNumber(row.sma20)}</td><td class="sma60">${tableNumber(row.sma60)}</td><td class="rsi">${tableNumber(row.rsi, 1)}</td><td class="sma20">${tableNumber(row.macd, 3)}</td><td class="mdd">${drawdown}</td></tr>`;
    }).join('');
    dataEmpty.hidden = pageRows.length > 0;
    dataPage.textContent = filtered.length ? `Trang ${tableState.page + 1}/${totalPages} · Hiển thị ${pageRows.length}/${filtered.length} phiên` : 'Không có dữ liệu';
    if (dataPrev) dataPrev.disabled = tableState.page === 0;
    if (dataNext) dataNext.disabled = tableState.page >= totalPages - 1;
    if (dataSort) dataSort.textContent = `Thứ tự ngày: ${tableState.newestFirst ? 'Mới nhất trước' : 'Cũ nhất trước'}`;
  };
  document.querySelectorAll('[data-open-data-table]').forEach((button) => button.addEventListener('click', () => {
    renderDataTable();
    if (!dataModal) return;
    if (typeof dataModal.showModal === 'function') dataModal.showModal(); else dataModal.setAttribute('open', '');
  }));
  document.getElementById('market-data-close')?.addEventListener('click', () => dataModal?.close?.());
  dataSearch?.addEventListener('input', () => { tableState.query = dataSearch.value.trim(); tableState.page = 0; renderDataTable(); });
  dataSort?.addEventListener('click', () => { tableState.newestFirst = !tableState.newestFirst; tableState.page = 0; renderDataTable(); });
  dataPrev?.addEventListener('click', () => { tableState.page = Math.max(0, tableState.page - 1); renderDataTable(); });
  dataNext?.addEventListener('click', () => { tableState.page += 1; renderDataTable(); });
  document.getElementById('market-data-export')?.addEventListener('click', () => {
    const columns = [['Ngày','Mở','Cao','Thấp','Đóng','Khối lượng','SMA20','SMA60','RSI14','MACD','Drawdown']];
    tableRows().forEach((row) => columns.push([row.date,row.open,row.high,row.low,row.close,row.volume,row.sma20,row.sma60,row.rsi,row.macd,row.drawdown]));
    const csv = `\ufeff${columns.map((row) => row.map((value) => `"${String(value ?? '').replaceAll('"', '""')}"`).join(',')).join('\n')}`;
    const link = document.createElement('a'); link.href = URL.createObjectURL(new Blob([csv], { type:'text/csv;charset=utf-8' })); link.download = `${payload.symbol}_technical_data.csv`; link.click(); setTimeout(() => URL.revokeObjectURL(link.href), 0);
  });
  const ctx = canvas.getContext('2d');
  const tooltip = document.getElementById('chart-tooltip');
  const state = {
    count: Math.min(260, rows.length), end: rows.length, mode: 'candle', indicator: 'rsi',
    overlays: { sma20: true, sma60: true, bollinger: false, mdd: true }, tool: 'cursor',
    drawings: [], draft: null, hover: null, dragging: null,
  };
  let cssWidth = 0;
  let cssHeight = 0;
  let plot = null;

  const finite = (value) => value !== null && value !== '' && Number.isFinite(Number(value));
  const fmt = (value, digits = 2) => finite(value) ? Number(value).toLocaleString('vi-VN', { minimumFractionDigits: digits, maximumFractionDigits: digits }) : 'N/A';
  const compact = (value) => finite(value) ? Intl.NumberFormat('vi-VN', { notation: 'compact', maximumFractionDigits: 1 }).format(value) : 'N/A';
  const colors = () => ({
    bg:'#0b111c', panel:'#0d1522', grid:'#243044', text:'#91a0b5', up:'#19b394', down:'#ef5350',
    sma20:'#f59e0b', sma60:'#60a5fa', band:'#818cf8', cross:'#8b9bb3', volume:'#42617e', white:'#e7edf7', fib:'#c084fc'
  });
  const visible = () => rows.slice(Math.max(0, state.end - state.count), state.end);
  const resize = () => {
    const rect = stage.getBoundingClientRect();
    cssWidth = Math.max(320, Math.floor(rect.width));
    cssHeight = Math.max(420, Math.floor(rect.height));
    const ratio = Math.min(2, window.devicePixelRatio || 1);
    canvas.width = Math.floor(cssWidth * ratio);
    canvas.height = Math.floor(cssHeight * ratio);
    canvas.style.width = `${cssWidth}px`;
    canvas.style.height = `${cssHeight}px`;
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    draw();
  };
  const range = (values, fallback = [0, 1]) => {
    const valid = values.filter(finite).map(Number);
    if (!valid.length) return fallback;
    let min = Math.min(...valid), max = Math.max(...valid);
    if (min === max) { min -= 1; max += 1; }
    return [min, max];
  };
  const path = (data, getter, mapX, mapY, color, width = 1.35) => {
    ctx.beginPath(); let started = false;
    data.forEach((row, index) => {
      const value = getter(row);
      if (!finite(value)) { started = false; return; }
      const x = mapX(index), y = mapY(Number(value));
      if (!started) { ctx.moveTo(x, y); started = true; } else ctx.lineTo(x, y);
    });
    ctx.strokeStyle = color; ctx.lineWidth = width; ctx.stroke();
  };
  const roundedRect = (x, y, width, height, radius = 4) => {
    ctx.beginPath(); ctx.roundRect(x, y, width, height, radius); ctx.fill();
  };
  const draw = () => {
    if (!cssWidth || !cssHeight) return;
    const c = colors(), data = visible();
    const startIndex = Math.max(0, state.end - state.count);
    const left = 14, right = 70, top = 18, bottom = 28;
    const usable = cssHeight - top - bottom;
    const priceHeight = usable * .66, volumeHeight = usable * .15, indicatorHeight = usable * .19;
    const volumeTop = top + priceHeight, indicatorTop = volumeTop + volumeHeight;
    const width = cssWidth - left - right;
    const xStep = width / Math.max(1, data.length);
    const highs = data.map(row => row.high), lows = data.map(row => row.low);
    const [rawMin, rawMax] = range([...highs, ...lows]);
    const pad = (rawMax - rawMin) * .08;
    const minPrice = rawMin - pad, maxPrice = rawMax + pad;
    const maxVolume = Math.max(1, ...data.map(row => Number(row.volume) || 0));
    const x = (index) => left + xStep * (index + .5);
    const y = (price) => top + (maxPrice - price) / (maxPrice - minPrice) * priceHeight;
    const priceAt = (pointY) => maxPrice - ((pointY - top) / priceHeight) * (maxPrice - minPrice);
    const indexAt = (pointX) => Math.max(0, Math.min(data.length - 1, Math.floor((pointX - left) / xStep)));
    plot = { data, startIndex, left, right, top, width, priceHeight, volumeTop, volumeHeight, indicatorTop, indicatorHeight, xStep, x, y, priceAt, indexAt };

    ctx.clearRect(0, 0, cssWidth, cssHeight);
    ctx.fillStyle = c.bg; ctx.fillRect(0, 0, cssWidth, cssHeight);
    ctx.strokeStyle = c.grid; ctx.lineWidth = 1; ctx.setLineDash([3, 5]);
    ctx.font = '11px ui-sans-serif,system-ui'; ctx.fillStyle = c.text;
    for (let line = 0; line <= 5; line += 1) {
      const lineY = top + priceHeight * line / 5;
      ctx.beginPath(); ctx.moveTo(left, lineY); ctx.lineTo(cssWidth - right, lineY); ctx.stroke();
      const label = maxPrice - (maxPrice - minPrice) * line / 5;
      ctx.fillText(fmt(label), cssWidth - right + 8, lineY + 4);
    }
    for (let line = 0; line <= 5; line += 1) {
      const lineX = left + width * line / 5;
      ctx.beginPath(); ctx.moveTo(lineX, top); ctx.lineTo(lineX, cssHeight - bottom); ctx.stroke();
      const row = data[Math.min(data.length - 1, Math.floor((data.length - 1) * line / 5))];
      if (row) ctx.fillText(row.date.slice(5), Math.max(left, lineX - 20), cssHeight - 8);
    }
    ctx.setLineDash([]);

    if (state.overlays.mdd) {
      const troughIndex = data.reduce((selected, row, index) => (
        finite(row.drawdown) && Number(row.drawdown) < Number(data[selected]?.drawdown ?? 0)
          ? index : selected
      ), 0);
      const drawdown = Number(data[troughIndex]?.drawdown);
      if (Number.isFinite(drawdown) && drawdown < -0.0005) {
        let peakIndex = 0;
        let peakClose = -Infinity;
        for (let index = 0; index <= troughIndex; index += 1) {
          const close = Number(data[index]?.close);
          if (Number.isFinite(close) && close >= peakClose) { peakClose = close; peakIndex = index; }
        }
        const zoneLeft = x(peakIndex) - xStep / 2;
        const zoneRight = x(troughIndex) + xStep / 2;
        ctx.save();
        ctx.fillStyle = 'rgba(251,113,133,.11)';
        ctx.fillRect(zoneLeft, top, Math.max(xStep, zoneRight - zoneLeft), priceHeight);
        ctx.setLineDash([6, 5]); ctx.strokeStyle = 'rgba(251,113,133,.62)'; ctx.lineWidth = 1;
        ctx.strokeRect(zoneLeft, top, Math.max(xStep, zoneRight - zoneLeft), priceHeight);
        ctx.setLineDash([]); ctx.fillStyle = '#fda4af';
        ctx.fillText(`MDD vùng xem: ${(drawdown * 100).toFixed(2)}%`, zoneLeft + 7, top + 17);
        ctx.restore();
      }
    }

    if (state.overlays.bollinger) {
      ctx.beginPath(); let started = false;
      data.forEach((row, index) => { if (!finite(row.bbUpper)) return; const px = x(index), py = y(row.bbUpper); if (!started) { ctx.moveTo(px, py); started = true; } else ctx.lineTo(px, py); });
      [...data].reverse().forEach((row, reverseIndex) => { if (!finite(row.bbLower)) return; ctx.lineTo(x(data.length - 1 - reverseIndex), y(row.bbLower)); });
      ctx.closePath(); ctx.fillStyle = 'rgba(129,140,248,.10)'; ctx.fill();
      path(data, row => row.bbUpper, x, y, c.band, 1); path(data, row => row.bbLower, x, y, c.band, 1);
    }
    if (state.mode === 'line') {
      path(data, row => row.close, x, y, '#3b82f6', 2);
    } else {
      const bodyWidth = Math.max(1.2, Math.min(12, xStep * .66));
      data.forEach((row, index) => {
        if (![row.open, row.high, row.low, row.close].every(finite)) return;
        const up = row.close >= row.open, color = up ? c.up : c.down, px = x(index);
        ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(px, y(row.high)); ctx.lineTo(px, y(row.low)); ctx.stroke();
        const bodyTop = y(Math.max(row.open, row.close));
        const bodyBottom = y(Math.min(row.open, row.close));
        ctx.fillRect(px - bodyWidth / 2, bodyTop, bodyWidth, Math.max(1.2, bodyBottom - bodyTop));
      });
    }
    if (state.overlays.sma20) path(data, row => row.sma20, x, y, c.sma20, 1.35);
    if (state.overlays.sma60) path(data, row => row.sma60, x, y, c.sma60, 1.35);

    data.forEach((row, index) => {
      const height = (Number(row.volume) || 0) / maxVolume * (volumeHeight - 8);
      ctx.fillStyle = row.close >= row.open ? 'rgba(25,179,148,.45)' : 'rgba(239,83,80,.45)';
      ctx.fillRect(x(index) - Math.max(1, xStep * .28), volumeTop + volumeHeight - height, Math.max(1, xStep * .56), height);
    });
    ctx.fillStyle = c.text; ctx.fillText('VOL', left + 4, volumeTop + 14);

    ctx.strokeStyle = c.grid; ctx.beginPath(); ctx.moveTo(left, indicatorTop); ctx.lineTo(cssWidth - right, indicatorTop); ctx.stroke();
    if (state.indicator === 'rsi') {
      const indicatorY = (value) => indicatorTop + (100 - value) / 100 * indicatorHeight;
      [30, 50, 70].forEach(value => { ctx.setLineDash([3, 4]); ctx.strokeStyle = c.grid; ctx.beginPath(); ctx.moveTo(left, indicatorY(value)); ctx.lineTo(cssWidth - right, indicatorY(value)); ctx.stroke(); ctx.setLineDash([]); ctx.fillStyle = c.text; ctx.fillText(String(value), cssWidth - right + 8, indicatorY(value) + 4); });
      path(data, row => row.rsi, x, indicatorY, '#c084fc', 1.4);
      ctx.fillStyle = c.text; ctx.fillText('RSI 14', left + 4, indicatorTop + 14);
    } else {
      const values = data.flatMap(row => [row.macd, row.macdSignal, row.macdHist]).filter(finite).map(Number);
      let [min, max] = range(values, [-1, 1]); const extra = (max - min) * .12; min -= extra; max += extra;
      const indicatorY = (value) => indicatorTop + (max - value) / (max - min) * indicatorHeight;
      const zeroY = indicatorY(0); ctx.strokeStyle = c.grid; ctx.beginPath(); ctx.moveTo(left, zeroY); ctx.lineTo(cssWidth - right, zeroY); ctx.stroke();
      data.forEach((row, index) => { if (!finite(row.macdHist)) return; const barY = indicatorY(row.macdHist); ctx.fillStyle = row.macdHist >= 0 ? 'rgba(25,179,148,.5)' : 'rgba(239,83,80,.5)'; ctx.fillRect(x(index) - Math.max(1, xStep * .25), Math.min(zeroY, barY), Math.max(1, xStep * .5), Math.abs(zeroY - barY)); });
      path(data, row => row.macd, x, indicatorY, '#60a5fa', 1.35); path(data, row => row.macdSignal, x, indicatorY, '#f59e0b', 1.2);
      ctx.fillStyle = c.text; ctx.fillText('MACD 12·26·9', left + 4, indicatorTop + 14);
    }
    drawAnnotations(c);
    if (state.hover && state.tool === 'cursor') drawCrosshair(c);
  };

  const annotationPoint = (point) => ({ x: plot.x(point.index - plot.startIndex), y: plot.y(point.price) });
  const drawAnnotations = (c) => {
    [...state.drawings, ...(state.draft ? [state.draft] : [])].forEach(item => {
      const a = annotationPoint(item.a), b = item.b ? annotationPoint(item.b) : a;
      ctx.strokeStyle = item.type === 'fib' ? c.fib : '#fbbf24'; ctx.fillStyle = ctx.strokeStyle; ctx.lineWidth = 1.4;
      if (item.type === 'horizontal') { ctx.setLineDash([7, 4]); ctx.beginPath(); ctx.moveTo(plot.left, a.y); ctx.lineTo(cssWidth - plot.right, a.y); ctx.stroke(); ctx.setLineDash([]); ctx.fillText(fmt(item.a.price), cssWidth - plot.right + 8, a.y - 5); }
      if (item.type === 'trend') { ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); }
      if (item.type === 'fib') {
        [0, .236, .382, .5, .618, .786, 1].forEach(level => { const price = item.a.price + (item.b.price - item.a.price) * level; const lineY = plot.y(price); ctx.globalAlpha = .78; ctx.beginPath(); ctx.moveTo(Math.min(a.x, b.x), lineY); ctx.lineTo(Math.max(a.x, b.x), lineY); ctx.stroke(); ctx.fillText(`${Math.round(level * 100)}%`, Math.max(a.x, b.x) + 5, lineY + 4); }); ctx.globalAlpha = 1;
      }
    });
  };
  const drawCrosshair = (c) => {
    const index = plot.indexAt(state.hover.x), row = plot.data[index]; if (!row) return;
    const px = plot.x(index), py = Math.max(plot.top, Math.min(plot.top + plot.priceHeight, state.hover.y));
    ctx.strokeStyle = c.cross; ctx.lineWidth = 1; ctx.setLineDash([4, 4]);
    ctx.beginPath(); ctx.moveTo(px, plot.top); ctx.lineTo(px, cssHeight - 28); ctx.moveTo(plot.left, py); ctx.lineTo(cssWidth - plot.right, py); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle = '#27364c'; roundedRect(cssWidth - plot.right + 3, py - 10, 63, 20, 4); ctx.fillStyle = c.white; ctx.fillText(fmt(plot.priceAt(py)), cssWidth - plot.right + 8, py + 4);
  };
  const pointFromEvent = (event) => { const rect = canvas.getBoundingClientRect(); return { x: event.clientX - rect.left, y: event.clientY - rect.top }; };
  const chartPoint = (point) => ({ index: plot.startIndex + plot.indexAt(point.x), price: plot.priceAt(Math.max(plot.top, Math.min(plot.top + plot.priceHeight, point.y))) });
  const showTooltip = (point) => {
    const index = plot.indexAt(point.x), row = plot.data[index]; if (!row || !tooltip) return;
    const delta = finite(row.open) ? Number(row.close) / Number(row.open) - 1 : null;
    tooltip.innerHTML = `<b>${row.date} · ${payload.symbol}</b><br>O ${fmt(row.open)} &nbsp; H ${fmt(row.high)}<br>L ${fmt(row.low)} &nbsp; C ${fmt(row.close)}<br>Thay đổi ${finite(delta) ? `${delta >= 0 ? '+' : ''}${fmt(delta * 100)}%` : 'N/A'} · KL ${compact(row.volume)}`;
    tooltip.style.left = `${Math.min(cssWidth - 215, Math.max(5, point.x))}px`; tooltip.style.top = `${Math.min(cssHeight - 120, Math.max(5, point.y))}px`; tooltip.classList.add('visible');
  };
  canvas.addEventListener('pointermove', (event) => {
    const point = pointFromEvent(event); state.hover = point;
    if (state.dragging?.type === 'pan') { const bars = Math.round((state.dragging.x - point.x) / plot.xStep); state.end = Math.max(state.count, Math.min(rows.length, state.dragging.end + bars)); }
    if (state.dragging?.type === 'draw') { state.draft.b = chartPoint(point); }
    showTooltip(point); draw();
  });
  canvas.addEventListener('pointerleave', () => { state.hover = null; tooltip?.classList.remove('visible'); draw(); });
  canvas.addEventListener('pointerdown', (event) => {
    const point = pointFromEvent(event); canvas.setPointerCapture(event.pointerId);
    if (state.tool === 'cursor') { state.dragging = { type:'pan', x:point.x, end:state.end }; return; }
    const anchor = chartPoint(point);
    if (state.tool === 'horizontal') { state.drawings.push({ type:'horizontal', a:anchor }); draw(); return; }
    state.draft = { type:state.tool, a:anchor, b:anchor }; state.dragging = { type:'draw' };
  });
  canvas.addEventListener('pointerup', () => { if (state.dragging?.type === 'draw' && state.draft) state.drawings.push(state.draft); state.draft = null; state.dragging = null; draw(); });
  canvas.addEventListener('wheel', (event) => { event.preventDefault(); const direction = event.deltaY > 0 ? 1.18 : .84; state.count = Math.max(25, Math.min(rows.length, Math.round(state.count * direction))); state.end = Math.max(state.count, Math.min(rows.length, state.end)); draw(); }, { passive:false });

  document.querySelectorAll('[data-range]').forEach(button => button.addEventListener('click', () => { const requested = button.dataset.range === 'all' ? rows.length : Number(button.dataset.range); state.count = Math.min(rows.length, requested); state.end = rows.length; document.querySelectorAll('[data-range]').forEach(item => item.classList.toggle('active', item === button)); draw(); }));
  document.querySelectorAll('[data-mode]').forEach(button => button.addEventListener('click', () => { state.mode = button.dataset.mode; document.querySelectorAll('[data-mode]').forEach(item => item.classList.toggle('active', item === button)); draw(); }));
  document.querySelectorAll('[data-overlay]').forEach(button => button.addEventListener('click', () => { const name = button.dataset.overlay; state.overlays[name] = !state.overlays[name]; button.classList.toggle('active', state.overlays[name]); draw(); }));
  document.querySelectorAll('[data-indicator]').forEach(button => button.addEventListener('click', () => { state.indicator = button.dataset.indicator; document.querySelectorAll('[data-indicator]').forEach(item => item.classList.toggle('active', item === button)); draw(); }));
  document.querySelectorAll('[data-tool]').forEach(button => button.addEventListener('click', () => { const tool = button.dataset.tool; if (tool === 'clear') { state.drawings = []; state.draft = null; draw(); return; } state.tool = tool; document.querySelectorAll('[data-tool]:not([data-tool="clear"])').forEach(item => item.classList.toggle('active', item === button)); canvas.style.cursor = tool === 'cursor' ? 'crosshair' : 'cell'; }));
  window.addEventListener('dashboard-theme-change', draw);
  new ResizeObserver(resize).observe(stage);
  resize();
})();
"""


def _interactive_chart_markup(
    frame: pd.DataFrame,
    symbol: str,
) -> tuple[str, str]:
    close = pd.to_numeric(frame.get("close"), errors="coerce").dropna()
    latest = float(close.iloc[-1]) if not close.empty else 0.0
    previous = float(close.iloc[-2]) if len(close) > 1 else latest
    change = 0.0 if previous == 0 else latest / previous - 1
    tone = "positive" if change >= 0 else "negative"
    latest_row = frame.iloc[-1] if not frame.empty else pd.Series(dtype=float)
    latest_date = pd.Timestamp(frame.index[-1]).strftime("%Y-%m-%d") if not frame.empty else "N/A"
    open_price = safe_float(latest_row.get("open")) or latest
    high_price = safe_float(latest_row.get("high")) or latest
    low_price = safe_float(latest_row.get("low")) or latest
    sma20 = safe_float(latest_row.get("sma_20"))
    sma60 = safe_float(latest_row.get("sma_60"))
    markup = f"""
    <section class="market-terminal" aria-labelledby="market-chart-heading">
      <div class="terminal-head">
        <div class="chart-title-block">
          <div class="chart-title-row"><h2 id="market-chart-heading">Biểu đồ giá &amp; SMA (20, 60)</h2><span class="chart-chip">{_escape(symbol)} · 1N mặc định</span></div>
          <div class="chart-snapshot"><span>{latest_date}</span><span>O: <strong>{format_price(open_price)}</strong></span><span>H: <strong class="up">{format_price(high_price)}</strong></span><span>L: <strong class="down">{format_price(low_price)}</strong></span><span>C: <strong class="{tone}">{format_price(latest)}</strong></span><span class="sma20">SMA20: <strong>{format_price(sma20)}</strong></span><span class="sma60">SMA60: <strong>{format_price(sma60)}</strong></span></div>
        </div>
        <div class="terminal-actions"><button class="ui-button data-table-trigger" type="button" data-open-data-table>Bảng dữ liệu</button><span class="live-label"><span class="live-dot"></span>Dữ liệu EOD · chart tương tác</span></div>
      </div>
      <div class="chart-toolbar" role="toolbar" aria-label="Công cụ biểu đồ">
        <button class="ui-button active" type="button" data-mode="candle">Nến</button>
        <button class="ui-button" type="button" data-mode="line">Đường</button>
        <span class="tool-separator"></span>
        <button class="ui-button active" type="button" data-overlay="sma20">SMA20</button>
        <button class="ui-button active" type="button" data-overlay="sma60">SMA60</button>
        <button class="ui-button mdd-toggle active" type="button" data-overlay="mdd" title="MDD của vùng giá đang hiển thị">Vùng MDD</button>
        <span class="tool-separator"></span>
        <button class="ui-button" type="button" data-range="65">3T</button>
        <button class="ui-button" type="button" data-range="130">6T</button>
        <button class="ui-button active" type="button" data-range="260">1N</button>
        <button class="ui-button" type="button" data-range="780">3N</button>
        <button class="ui-button" type="button" data-range="all">Tất cả</button>
        <span class="tool-separator"></span>
        <button class="ui-button" type="button" data-overlay="bollinger">Bollinger</button>
        <button class="ui-button active" type="button" data-indicator="rsi">RSI</button>
        <button class="ui-button" type="button" data-indicator="macd">MACD</button>
        <span class="tool-separator"></span>
        <button class="ui-button active" type="button" data-tool="cursor">Crosshair</button>
        <button class="ui-button" type="button" data-tool="trend">Trendline</button>
        <button class="ui-button" type="button" data-tool="horizontal">Đường ngang</button>
        <button class="ui-button" type="button" data-tool="fib">Fibonacci</button>
        <button class="ui-button" type="button" data-tool="clear">Xóa nét vẽ</button>
      </div>
      <div class="chart-stage">
        <canvas id="market-canvas" aria-label="Biểu đồ nến tương tác của {_escape(symbol)}"></canvas>
        <div class="chart-tooltip" id="chart-tooltip"></div>
      </div>
      <div class="chart-legend">
        <span class="legend-item" style="--legend:#19b394">Tăng</span>
        <span class="legend-item" style="--legend:#ef5350">Giảm</span>
        <span class="legend-item" style="--legend:#f59e0b">SMA20</span>
        <span class="legend-item" style="--legend:#60a5fa">SMA60</span>
        <span class="legend-item" style="--legend:#fb7185">MDD vùng xem</span>
        <span class="chart-help">Cuộn để zoom · kéo để pan · chọn công cụ rồi vẽ trực tiếp trên vùng giá</span>
      </div>
    </section>
    <dialog class="market-data-modal" id="market-data-modal" aria-labelledby="market-data-heading">
      <div class="market-data-shell">
        <header class="market-data-head"><div><h2 id="market-data-heading">Bảng dữ liệu chi tiết &amp; chỉ báo kỹ thuật</h2><p>{_escape(symbol)} · dữ liệu EOD trong report hiện tại</p></div><div class="market-data-actions"><button class="ui-button" type="button" id="market-data-export">Xuất CSV</button><button class="ui-button market-data-close" type="button" id="market-data-close" aria-label="Đóng bảng dữ liệu">×</button></div></header>
        <div class="market-data-toolbar"><input class="market-data-search" id="market-data-search" type="search" placeholder="Tìm theo ngày (YYYY-MM-DD)" aria-label="Tìm theo ngày"><button class="ui-button" type="button" id="market-data-sort">Thứ tự ngày: Mới nhất trước</button></div>
        <div class="market-data-scroll"><table class="market-data-table"><thead><tr><th>Ngày</th><th>Mở</th><th>Cao</th><th>Thấp</th><th>Đóng</th><th>Khối lượng</th><th>SMA20</th><th>SMA60</th><th>RSI14</th><th>MACD</th><th>Drawdown</th></tr></thead><tbody id="market-data-body"></tbody></table><p class="market-data-empty" id="market-data-empty" hidden>Không có dòng khớp ngày tìm kiếm.</p></div>
        <footer class="market-data-footer"><span id="market-data-page">—</span><div class="market-data-pagination"><button class="ui-button" type="button" id="market-data-prev" aria-label="Trang trước">‹</button><button class="ui-button" type="button" id="market-data-next" aria-label="Trang sau">›</button></div></footer>
      </div>
    </dialog>
    """
    payload = _interactive_chart_payload(frame, symbol)
    scripts = (
        '<script type="application/json" id="market-chart-data">'
        f"{payload}</script><script>{INTERACTIVE_CHART_JS}</script>"
    )
    return markup, scripts


FORECAST_CHART_CSS = r"""
    .forecast-workspace { background:var(--panel); border:1px solid var(--line); border-radius:14px; overflow:hidden; box-shadow:var(--shadow); }
    .forecast-head { display:flex; align-items:center; justify-content:space-between; gap:16px; padding:16px 18px 12px; border-bottom:1px solid var(--line); }
    .forecast-head h3 { margin:0 0 4px; font-size:17px; }
    .forecast-head p { margin:0; color:var(--muted); font-size:12px; }
    .forecast-badge { display:inline-flex; align-items:center; gap:7px; padding:7px 10px; border-radius:999px; color:#0f766e; background:#e8f8f5; border:1px solid #bce9df; font-size:11px; font-weight:800; white-space:nowrap; }
    .forecast-badge.warning { color:#8a4b00; background:var(--soft-amber); border-color:#f4d89a; }
    .forecast-toolbar { display:flex; flex-wrap:wrap; gap:7px; padding:10px 14px; border-bottom:1px solid var(--line); background:var(--soft-slate); }
    .forecast-toolbar button { appearance:none; border:1px solid var(--line); border-radius:7px; padding:7px 10px; color:var(--ink); background:var(--panel); font:inherit; font-size:12px; font-weight:750; cursor:pointer; }
    .forecast-toolbar button.active { color:#fff; background:var(--blue); border-color:var(--blue); }
    .forecast-stage { position:relative; min-height:390px; padding:8px 10px 6px; }
    #future-forecast-canvas { width:100%; height:390px; display:block; touch-action:none; }
    .forecast-tooltip { position:absolute; z-index:4; min-width:190px; padding:10px 11px; border-radius:9px; color:var(--ink); background:color-mix(in srgb,var(--panel) 94%,transparent); border:1px solid var(--line); box-shadow:0 12px 28px rgba(15,23,42,.18); font-size:12px; line-height:1.55; pointer-events:none; transform:translate(12px,-50%); display:none; }
    .forecast-legend { display:flex; flex-wrap:wrap; gap:14px; padding:0 18px 14px; color:var(--muted); font-size:11px; }
    .forecast-legend span::before { content:""; display:inline-block; width:16px; height:3px; margin-right:6px; border-radius:3px; vertical-align:middle; background:var(--legend-color); }
    [data-theme="dark"] .forecast-badge { color:#78e0ce; background:#123a38; border-color:#245c57; }
"""


FORECAST_CHART_JS = r"""
(() => {
  const canvas = document.getElementById('future-forecast-canvas');
  const source = document.getElementById('future-forecast-data');
  const root = document.getElementById('future-forecast-workspace');
  if (!canvas || !source || !root) return;
  const payload = JSON.parse(source.textContent || '{}');
  const allRows = payload.rows || [];
  const tooltip = root.querySelector('.forecast-tooltip');
  let horizon = Math.min(20, allRows.length);
  let showBand = true;
  let hoverIndex = null;
  const fmt = new Intl.NumberFormat('vi-VN', {maximumFractionDigits: 2});
  const css = (name, fallback) => getComputedStyle(document.body).getPropertyValue(name).trim() || fallback;

  function rows() { return allRows.slice(0, horizon); }
  function setup() {
    const dpr = Math.max(1, Math.min(window.devicePixelRatio || 1, 2));
    const rect = canvas.getBoundingClientRect();
    canvas.width = Math.max(320, Math.round(rect.width * dpr));
    canvas.height = Math.round(390 * dpr);
    const ctx = canvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return {ctx, width:rect.width, height:390};
  }
  function line(ctx, points, color, width=2) {
    ctx.beginPath(); points.forEach((p,i) => i ? ctx.lineTo(p.x,p.y) : ctx.moveTo(p.x,p.y));
    ctx.strokeStyle=color; ctx.lineWidth=width; ctx.stroke();
  }
  function draw() {
    const visible = rows(); if (!visible.length) return;
    const {ctx,width,height} = setup();
    const pad={l:58,r:20,t:22,b:38}, w=width-pad.l-pad.r, h=height-pad.t-pad.b;
    const values=visible.flatMap(r => [r.p10,r.p50,r.p90]).filter(Number.isFinite);
    let min=Math.min(...values), max=Math.max(...values); const extra=Math.max((max-min)*.12, max*.005);
    min-=extra; max+=extra;
    const x=i => pad.l + (visible.length===1 ? w/2 : i*w/(visible.length-1));
    const y=v => pad.t + (max-v)*h/(max-min || 1);
    ctx.clearRect(0,0,width,height);
    ctx.font='11px Inter,system-ui,sans-serif'; ctx.fillStyle=css('--muted','#68758a');
    ctx.strokeStyle=css('--line','#e3e9f2'); ctx.lineWidth=1;
    for(let i=0;i<=4;i++){ const yy=pad.t+i*h/4, value=max-i*(max-min)/4; ctx.beginPath();ctx.moveTo(pad.l,yy);ctx.lineTo(width-pad.r,yy);ctx.stroke();ctx.fillText(fmt.format(value),6,yy+4); }
    const tickStep=Math.max(1,Math.ceil(visible.length/5));
    visible.forEach((r,i)=>{ if(i%tickStep===0 || i===visible.length-1) ctx.fillText(r.date.slice(5),Math.max(pad.l,x(i)-24),height-13); });
    const lower=visible.map((r,i)=>({x:x(i),y:y(r.p10)}));
    const median=visible.map((r,i)=>({x:x(i),y:y(r.p50)}));
    const upper=visible.map((r,i)=>({x:x(i),y:y(r.p90)}));
    if(showBand){ ctx.beginPath(); lower.forEach((p,i)=>i?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y)); [...upper].reverse().forEach(p=>ctx.lineTo(p.x,p.y)); ctx.closePath(); ctx.fillStyle='rgba(37,99,235,.14)'; ctx.fill(); }
    line(ctx,lower,'#38bdf8',1.2); line(ctx,upper,'#38bdf8',1.2); line(ctx,median,css('--blue','#2563eb'),2.6);
    visible.forEach((r,i)=>{ if(r.anchor){ctx.beginPath();ctx.arc(x(i),y(r.p50),4,0,Math.PI*2);ctx.fillStyle='#f59e0b';ctx.fill();} });
    if(hoverIndex!==null && hoverIndex<visible.length){ const i=hoverIndex;ctx.beginPath();ctx.moveTo(x(i),pad.t);ctx.lineTo(x(i),pad.t+h);ctx.strokeStyle=css('--muted','#68758a');ctx.setLineDash([4,4]);ctx.stroke();ctx.setLineDash([]);ctx.beginPath();ctx.arc(x(i),y(visible[i].p50),4.5,0,Math.PI*2);ctx.fillStyle=css('--blue','#2563eb');ctx.fill(); }
  }
  function updateTooltip(event) {
    const visible=rows(), rect=canvas.getBoundingClientRect(), padL=58, padR=20;
    const ratio=Math.max(0,Math.min(1,(event.clientX-rect.left-padL)/(rect.width-padL-padR)));
    hoverIndex=Math.round(ratio*Math.max(visible.length-1,0)); const row=visible[hoverIndex];
    if(!row)return; tooltip.style.display='block'; tooltip.style.left=`${Math.min(rect.width-215,Math.max(6,event.clientX-rect.left))}px`; tooltip.style.top=`${Math.max(55,event.clientY-rect.top)}px`;
    tooltip.innerHTML=`<strong>${row.date}${row.anchor?' · mốc model':''}</strong><br>P50: ${fmt.format(row.p50)}<br>P10–P90: ${fmt.format(row.p10)} – ${fmt.format(row.p90)}<br>Xác suất dương: ${fmt.format(row.probability*100)}%`; draw();
  }
  root.querySelectorAll('[data-forecast-range]').forEach(button=>button.addEventListener('click',()=>{ horizon=Math.min(Number(button.dataset.forecastRange),allRows.length); root.querySelectorAll('[data-forecast-range]').forEach(b=>b.classList.toggle('active',b===button)); hoverIndex=null; tooltip.style.display='none'; draw(); }));
  const bandButton=root.querySelector('[data-forecast-band]'); if(bandButton)bandButton.addEventListener('click',()=>{showBand=!showBand;bandButton.classList.toggle('active',showBand);draw();});
  canvas.addEventListener('mousemove',updateTooltip); canvas.addEventListener('mouseleave',()=>{hoverIndex=null;tooltip.style.display='none';draw();});
  window.addEventListener('resize',draw); window.addEventListener('dashboard-theme-change',draw); draw();
})();
"""


def _interactive_forecast_markup(
    forecast: pd.DataFrame,
    symbol: str,
) -> tuple[str, str]:
    rows = []
    for index, row in forecast.iterrows():
        rows.append(
            {
                "date": str(pd.Timestamp(index).date()),
                "p10": _chart_number(row.get("p10")),
                "p50": _chart_number(row.get("p50")),
                "p90": _chart_number(row.get("p90")),
                "probability": _chart_number(row.get("prob_end_above_latest")),
                "anchor": bool(row.get("is_model_anchor", False)),
            }
        )
    method = str(forecast.attrs.get("method") or "scenario_forecast")
    model_metrics = forecast.attrs.get("forecast_model_metrics", {}) or {}
    publish_ready = bool(model_metrics.get("all_horizons_publish_ready", False))
    method_label = (
        "XGBoost quantile + conformal"
        if method == "xgboost_direct_quantile_conformal"
        else "Monte Carlo fallback"
    )
    if method == "xgboost_direct_quantile_conformal" and not publish_ready:
        method_label += " · research-only"
    payload = json.dumps(
        {"symbol": symbol, "method": method, "rows": rows},
        ensure_ascii=False,
        separators=(",", ":"),
    ).replace("</", "<\\/")
    markup = f"""
    <section class="forecast-workspace" id="future-forecast-workspace">
      <div class="forecast-head">
        <div><h3>Dự báo tương lai ngắn hạn · {_escape(symbol)}</h3><p>P10/P50/P90 cho các phiên tới; mốc cam là dự báo trực tiếp 5/10/20D. Giá được neo tại close hiện tại, còn target model dùng open[t+1] → close[t+h], nên vùng giá chỉ là kịch bản quy đổi.</p></div>
        <span class="forecast-badge{' warning' if not publish_ready else ''}">● {_escape(method_label)}</span>
      </div>
      <div class="forecast-toolbar" role="toolbar" aria-label="Công cụ biểu đồ dự báo">
        <button type="button" data-forecast-range="5">5 phiên</button>
        <button type="button" data-forecast-range="10">10 phiên</button>
        <button type="button" class="active" data-forecast-range="20">20 phiên</button>
        <button type="button" class="active" data-forecast-band>Dải P10–P90</button>
      </div>
      <div class="forecast-stage">
        <canvas id="future-forecast-canvas" role="img" aria-label="Biểu đồ dự báo tương lai tương tác của {_escape(symbol)}"></canvas>
        <div class="forecast-tooltip"></div>
      </div>
      <div class="forecast-legend">
        <span style="--legend-color:#2563eb">P50</span><span style="--legend-color:#38bdf8">P10/P90</span><span style="--legend-color:#f59e0b">Mốc model trực tiếp</span>
      </div>
    </section>
    """
    scripts = (
        '<script type="application/json" id="future-forecast-data">'
        f"{payload}</script><script>{FORECAST_CHART_JS}</script>"
    )
    return markup, scripts


# The dashboard remains a standalone HTML artifact. The widget only calls the
# local workspace API when the report is opened through ``src.web_server``.
CHAT_WIDGET_CSS = r"""
    .report-chat-launcher { position:fixed; right:24px; bottom:24px; z-index:40; display:inline-flex; align-items:center; gap:9px; border:1px solid #77aaff; border-radius:999px; padding:13px 17px; background:linear-gradient(135deg,#165dca,#2563eb); color:#fff; box-shadow:0 16px 38px rgba(20,77,175,.38); font:800 14px Inter,ui-sans-serif,system-ui,sans-serif; cursor:pointer; }
    .report-chat-launcher:hover { filter:brightness(1.08); transform:translateY(-1px); }
    .report-chat-launcher .chat-spark { display:grid; width:20px; height:20px; place-items:center; border-radius:50%; background:rgba(255,255,255,.2); font-size:14px; }
    .report-chat-panel { position:fixed; right:24px; bottom:84px; z-index:41; width:min(390px,calc(100vw - 32px)); overflow:hidden; border:1px solid #315d99; border-radius:18px; background:#091323; color:#eaf2ff; box-shadow:0 24px 64px rgba(0,0,0,.42); }
    .report-chat-panel[hidden] { display:none; }
    .report-chat-head { display:flex; align-items:flex-start; justify-content:space-between; gap:12px; padding:15px 16px 13px; background:linear-gradient(110deg,#133c72,#172554); border-bottom:1px solid #315d99; }
    .report-chat-head strong { display:block; font-size:14px; }
    .report-chat-head small { display:block; margin-top:3px; color:#b7cbe7; font-size:11px; line-height:1.35; }
    .report-chat-close { border:0; border-radius:8px; padding:3px 8px; background:rgba(255,255,255,.1); color:#fff; font-size:19px; line-height:1; cursor:pointer; }
    .report-chat-messages { display:grid; gap:10px; max-height:min(48vh,430px); overflow:auto; padding:14px; background:#091323; }
    .report-chat-message { max-width:92%; padding:10px 12px; border:1px solid #223b5d; border-radius:12px; background:#101e31; color:#e2edf9; font-size:13px; line-height:1.5; white-space:pre-wrap; }
    .report-chat-message.user { justify-self:end; border-color:#3475dc; background:#1d4ed8; color:#fff; }
    .report-chat-message.system { border-color:#29445f; background:#0c192a; color:#bfcee1; font-size:12px; }
    .report-chat-message .chat-note { display:block; margin-top:6px; color:#f6c55c; font-size:11px; font-weight:700; }
    .report-chat-form { display:flex; gap:8px; padding:12px; border-top:1px solid #223b5d; background:#0d1828; }
    .report-chat-input { min-width:0; flex:1; resize:none; border:1px solid #355678; border-radius:10px; padding:10px; background:#08111d; color:#fff; font:13px/1.4 Inter,ui-sans-serif,system-ui,sans-serif; }
    .report-chat-input:focus { outline:2px solid rgba(77,150,255,.35); border-color:#67a2ff; }
    .report-chat-send { align-self:flex-end; border:0; border-radius:10px; padding:10px 12px; background:#2563eb; color:#fff; font-weight:800; cursor:pointer; }
    .report-chat-send:disabled { opacity:.55; cursor:wait; }
    @media (max-width:620px) { .report-chat-launcher { right:16px; bottom:16px; padding:12px 14px; } .report-chat-panel { right:16px; bottom:74px; } }
"""


CHAT_WIDGET_MARKUP = """
  <button id="report-chat-launcher" class="report-chat-launcher" type="button" aria-expanded="false" aria-controls="report-chat-panel"><span class="chat-spark">✦</span>Hỏi AI</button>
  <aside id="report-chat-panel" class="report-chat-panel" hidden aria-label="Trợ lý AI cho report">
    <div class="report-chat-head"><div><strong>StockLens AI</strong><small>Chỉ dùng dữ liệu của report đang mở · không phải khuyến nghị đầu tư.</small></div><button id="report-chat-close" class="report-chat-close" type="button" aria-label="Đóng trợ lý">×</button></div>
    <div id="report-chat-messages" class="report-chat-messages" aria-live="polite"></div>
    <form id="report-chat-form" class="report-chat-form"><textarea id="report-chat-input" class="report-chat-input" rows="2" maxlength="2000" placeholder="Hỏi về chỉ số, model hoặc dữ liệu của report này…" aria-label="Câu hỏi cho trợ lý AI"></textarea><button id="report-chat-send" class="report-chat-send" type="submit">Gửi</button></form>
  </aside>
"""


CHAT_WIDGET_SCRIPT = r"""
  <script>
    (() => {
      const launcher = document.getElementById('report-chat-launcher');
      const panel = document.getElementById('report-chat-panel');
      const close = document.getElementById('report-chat-close');
      const messages = document.getElementById('report-chat-messages');
      const form = document.getElementById('report-chat-form');
      const input = document.getElementById('report-chat-input');
      const send = document.getElementById('report-chat-send');
      if (!launcher || !panel || !messages || !form || !input || !send) return;
      const report = decodeURIComponent(window.location.pathname.replace(/^\/reports\//, ''));
      const localWorkspace = window.location.pathname.startsWith('/reports/');
      const history = [];
      const append = (role, content, fallback) => {
        const element = document.createElement('div');
        element.className = 'report-chat-message ' + role;
        element.textContent = content;
        if (fallback) { const note = document.createElement('span'); note.className = 'chat-note'; note.textContent = 'Đang dùng trả lời dự phòng từ artifact.'; element.appendChild(note); }
        messages.appendChild(element); messages.scrollTop = messages.scrollHeight;
      };
      const setOpen = (open) => { panel.hidden = !open; launcher.setAttribute('aria-expanded', String(open)); if (open) input.focus(); };
      append('system', localWorkspace ? 'Mình có ngữ cảnh riêng của report này. Bạn có thể hỏi cách đọc chỉ số, chất lượng model, rủi ro và nguồn dữ liệu.' : 'Để dùng AI, hãy mở report từ Local Workspace (python -m src.web_server). Chat không gửi dữ liệu ra ngoài report local.', false);
      launcher.addEventListener('click', () => setOpen(panel.hidden));
      close.addEventListener('click', () => setOpen(false));
      form.addEventListener('submit', async (event) => {
        event.preventDefault(); const message = input.value.trim(); if (!message || send.disabled) return;
        append('user', message, false); history.push({ role: 'user', content: message }); input.value = ''; send.disabled = true;
        const pending = document.createElement('div'); pending.className = 'report-chat-message system'; pending.textContent = 'Đang đối chiếu artifact của report…'; messages.appendChild(pending); messages.scrollTop = messages.scrollHeight;
        try {
          if (!localWorkspace) throw new Error('Report chưa được mở qua Local Workspace.');
          const response = await fetch('/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ report, message, history: history.slice(-8) }) });
          const payload = await response.json(); if (!response.ok) throw new Error(payload.error || 'Không thể trả lời câu hỏi lúc này.');
          pending.remove(); append('assistant', payload.answer || 'Chưa có câu trả lời.', Boolean(payload.fallback)); history.push({ role: 'assistant', content: payload.answer || '' }); while (history.length > 8) history.shift();
        } catch (error) { pending.remove(); append('system', error.message || 'Không thể kết nối trợ lý AI.', false); }
        finally { send.disabled = false; input.focus(); }
      });
      input.addEventListener('keydown', (event) => { if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); form.requestSubmit(); } });
    })();
  </script>
"""


def write_dashboard(
    config: dict,
    frame: pd.DataFrame,
    forecast: pd.DataFrame,
    levels: dict,
    metrics: dict,
    latest_probabilities: dict,
    technical: dict,
    fundamentals: dict,
    news: dict,
    risk_plan: dict,
    decision: dict,
    output_path: Path,
) -> None:
    latest = levels["latest_close"]
    forecast_end = forecast.iloc[-1]
    calendar_note = market_calendar_note(config)
    calendar_holidays = market_holidays(config)
    company = fundamentals.get("company", {})
    company_name = company.get("organ_short_name") or company.get("organ_name") or config["symbol"]
    investment_recommendation = build_investment_recommendation(
        metrics,
        latest_probabilities,
        decision,
        risk_plan,
        technical,
        news,
    )
    strategy = metrics.get("backtest", {}) or {}
    swing = metrics.get("swing_strategy", {}) or {}
    swing_frozen = (swing.get("frozen_holdout", {}) or {}).get("backtest", {}) or {}
    swing_gate = swing.get("publish_gate", {}) or {}
    decision_status = str(decision.get("status") or "NO_EDGE")
    decision_tone = {
        "ACTIONABLE": "positive",
        "WATCH": "warning",
        "NO_EDGE": "neutral",
    }.get(decision_status, "neutral")
    failed_checks = list(decision.get("failed_checks", []) or [])
    capital_scenario_box = _capital_scenario_box(strategy, risk_plan)
    interactive_chart, interactive_chart_scripts = _interactive_chart_markup(
        frame,
        str(config["symbol"]),
    )
    interactive_forecast, interactive_forecast_scripts = _interactive_forecast_markup(
        forecast,
        str(config["symbol"]),
    )
    closes = pd.to_numeric(frame.get("close"), errors="coerce").dropna()
    previous_close = safe_float(closes.iloc[-2]) if len(closes) > 1 else latest
    daily_change = None if not previous_close else latest / previous_close - 1
    sma20 = safe_float(levels.get("sma20"))
    sma60 = safe_float(levels.get("sma60"))
    rsi14 = safe_float(levels.get("rsi14"))
    macd = safe_float(levels.get("macd"))
    macd_signal = safe_float(levels.get("macd_signal"))
    macd_hist = safe_float(levels.get("macd_hist"))
    annualized_volatility = safe_float(levels.get("vol20"))
    annualized_volatility = (
        annualized_volatility * np.sqrt(252)
        if annualized_volatility is not None
        else None
    )
    max_drawdown = safe_float(levels.get("max_drawdown"))
    sma_tone = "positive" if sma20 is not None and sma60 is not None and sma20 >= sma60 else "negative"
    rsi_tone = "positive" if rsi14 is not None and 30 <= rsi14 <= 70 else "warning"
    macd_tone = "positive" if macd_hist is not None and macd_hist >= 0 else "negative"
    market_pulse_cards = "".join(
        [
            _pulse_card(
                "Giá đóng cửa",
                format_price(latest),
                f"{format_signed_percent(daily_change, 2)} so với phiên trước · {levels['latest_date']}",
                "positive" if daily_change is not None and daily_change >= 0 else "negative",
                "Biến động phiên gần nhất",
            ),
            _pulse_card(
                "Xu hướng SMA",
                "SMA20 ≥ SMA60" if sma_tone == "positive" else "SMA20 < SMA60",
                f"SMA20 {format_price(sma20)} · SMA60 {format_price(sma60)}",
                sma_tone,
                "Xu hướng giá ngắn và trung hạn",
            ),
            _pulse_card(
                "RSI (14)",
                format_number(rsi14, 1),
                "Trung tính (30–70)" if rsi_tone == "positive" else "Ngoài vùng trung tính",
                rsi_tone,
                "Động lượng 14 phiên",
            ),
            _pulse_card(
                "MACD (12,26,9)",
                format_number(macd, 3),
                f"Signal {format_number(macd_signal, 3)} · Hist {format_number(macd_hist, 3)}",
                macd_tone,
                "Xung lực giá hiện tại",
            ),
            _pulse_card(
                "Biến động năm",
                format_percent(annualized_volatility, 1),
                "Quy đổi từ biến động 20 phiên gần nhất",
                "warning",
                "Vol 20D × √252",
            ),
            _pulse_card(
                "Sụt giảm tối đa",
                format_percent(max_drawdown, 1),
                f"Đỉnh {levels.get('drawdown_peak') or 'N/A'} → đáy {levels.get('drawdown_trough') or 'N/A'}",
                "negative",
                "MDD lịch sử · chỉ báo rủi ro",
            ),
        ]
    )
    result_cards = "".join(
        [
            _metric_card("Xu hướng kỹ thuật", technical["bias"], f"Điểm {technical['score']}"),
            _metric_card("Trạng thái tín hiệu", signal_status_label(decision["status"]), "; ".join(signal_check_label(name) for name in decision.get("failed_checks", [])) or "Đã vượt qua tất cả điều kiện phát hành"),
            _metric_card("Mua mới", str(investment_recommendation["entry_action"]), str(investment_recommendation["title"])),
            _metric_card("Đang giữ", str(investment_recommendation["holding_action"]), str(investment_recommendation["holding_reason"])),
            _metric_card("Dự báo", format_price(safe_float(forecast_end["p50"])), f"P50 sau {config['forecast_sessions']} phiên - {format_percent(forecast_end['p50'] / latest - 1)}"),
            _metric_card("Quản trị rủi ro", f"Lợi nhuận/rủi ro {format_number(risk_plan['reward_risk'])}", f"Dừng lỗ {format_price(risk_plan['stop_loss'])} / Mục tiêu {format_price(risk_plan['target_1'])}"),
        ]
    )
    if swing.get("available"):
        result_cards += "".join(
            [
                _metric_card(
                    "Expected excess return 5D",
                    format_signed_percent(safe_float(swing.get("latest_expected_excess_return"))),
                    (
                        "Cận dưới đã hiệu chỉnh: "
                        + format_signed_percent(
                            safe_float(
                                swing.get("latest_expected_excess_return_lower_bound")
                            )
                        )
                    ),
                ),
                _metric_card(
                    "Frozen holdout",
                    f"{int(swing_frozen.get('completed_round_trips') or 0)}/{int(swing.get('min_completed_round_trips') or 0)} trade",
                    "Chưa đủ mẫu = INSUFFICIENT_EDGE, không được suy luận 0% là ổn định.",
                ),
            ]
        )
    else:
        result_cards += _metric_card("Xác suất XGBoost", f"{latest_probabilities['xgboost']:.1%}", "Xác suất giá đóng cửa phiên tới cao hơn giá mở cửa")
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
        [(item["name"], item["status"], item["detail"]) for item in technical["signals"]],
        headers=("Chỉ báo", "Trạng thái", "Cách đọc"),
        status_column=True,
    )
    model_table = _table(
        [
            ("XGBoost", format_number(metrics["xgboost"]["balanced_accuracy"], 3), f"AUC {format_number(metrics['xgboost']['roc_auc'], 3)}"),
            ("Logistic", format_number(metrics["logistic_baseline"]["balanced_accuracy"], 3), f"AUC {format_number(metrics['logistic_baseline']['roc_auc'], 3)}"),
            ("Đa số", format_number(metrics["majority_baseline"]["balanced_accuracy"], 3), "Mốc so sánh"),
        ],
        headers=("Mô hình", "Balanced accuracy", "Đối chiếu"),
    )
    investment_recommendation_table = _table(
        _investment_recommendation_rows(investment_recommendation),
        headers=("Tình huống", "Kết luận", "Cách đọc"),
        status_column=True,
    )
    swing_table = _table(
        [
            (
                "Target / execution",
                f"{swing.get('horizon_sessions', 'N/A')} phiên",
                str(swing.get("target_definition") or "Chưa chạy swing strategy."),
            ),
            (
                "Frozen holdout sample",
                f"{int(swing_frozen.get('completed_round_trips') or 0)}/{int(swing.get('min_completed_round_trips') or 0)} trade",
                "Nếu chưa đủ trade, net/Sharpe là inconclusive chứ không phải return bằng 0.",
            ),
            (
                "Nắm giữ / T+2",
                f"{format_number(safe_float(swing_frozen.get('average_holding_sessions')), 1)} phiên",
                f"Tối thiểu {swing_frozen.get('minimum_holding_sessions', 'N/A')} phiên trước khi bán.",
            ),
            (
                "Ranking edge frozen",
                "Đạt" if swing_gate.get("frozen_ranking_edge") else "Không đạt",
                "Correlation dự báo-excess return phải dương trên frozen holdout.",
            ),
            (
                "Cận dưới excess return 5D",
                format_signed_percent(
                    safe_float(swing.get("latest_expected_excess_return_lower_bound"))
                ),
                "Phải vượt chi phí + margin; không dùng riêng dự báo điểm để mở lệnh.",
            ),
            (
                "Baseline MAE",
                "Đạt" if swing_gate.get("beats_zero_baseline_mae") else "Không đạt",
                "XGBoost phải tốt hơn dự báo excess return bằng 0 trên frozen holdout.",
            ),
            (
                "Stress phí 1.5x",
                "Đạt" if swing_gate.get("cost_stress_1_5x") else "Không đạt",
                "Điều kiện bắt buộc trước khi chiến lược được publish-ready.",
            ),
            (
                "Publish gate",
                "ĐẠT" if swing_gate.get("passed") else "CHƯA ĐẠT",
                "Frozen holdout không được dùng để chọn margin/boosting rounds.",
            ),
        ]
        if swing.get("available")
        else [("Trạng thái", "Chưa chạy", "Bật swing_strategy.enabled để chạy chiến lược 5D.")],
        headers=("Tiêu chí", "Kết quả", "Cách đọc"),
        status_column=True,
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
        ],
        headers=("Điều kiện", "Kết quả", "Ý nghĩa"),
        status_column=True,
    )
    fundamental_rows = [
        (item["metric_label"], format_metric(item["metric_value"], item["metric_unit"]), item.get("period") or "")
        for item in fundamentals.get("metrics", [])
    ] or [("Dữ liệu", "N/A", "Chưa lấy được dữ liệu cơ bản")]
    fundamental_table = _table(fundamental_rows)
    latest_news = news.get("latest_asof_features", {}) or {}
    news_rows = [
        ("Trạng thái", "Có dữ liệu" if news.get("available") else "Chưa có dữ liệu", news.get("mode", "research_only")),
        ("Nguồn / số bài", str(news.get("provider") or "N/A"), str(news.get("article_count", 0))),
        (
            "Bài đủ timestamp",
            str(news.get("eligible_article_count", 0)),
            "Chỉ các bài này mới được phép dùng point-in-time",
        ),
        (
            "Sentiment 5 ngày",
            format_number(safe_float(latest_news.get("news_sentiment_mean_lookback")), 2),
            f"{latest_news.get('news_count_lookback', 0)} bài trước cutoff",
        ),
        (
            "Phương pháp",
            str(news.get("analysis_method") or "N/A"),
            "Research only; chưa dùng làm tín hiệu mua/bán",
        ),
    ]
    news_table = _table(news_rows)
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
    model_quality_panel = _accordion(
        "So sánh mô hình",
        model_table,
        open_by_default=False,
        note="XGBoost vs Logistic",
    )
    recommendation_panel = _accordion(
        "Khuyến nghị theo fixed-horizon swing 5D" if swing.get("available") else "Khuyến nghị hành động sau phí",
        investment_recommendation_table
        + '<p class="muted">Classifier next-day và bảng sensitivity legacy không tham gia quyết định này. Mua mới chỉ được xét khi swing 5D có sample đủ lớn, ranking edge dương, frozen holdout/stress phí đạt và expected excess return vượt chi phí + margin.</p>',
        open_by_default=True,
        note=str(investment_recommendation["entry_action"]),
    )
    swing_panel = _accordion(
        "Chiến lược swing 5 phiên: frozen holdout & T+2",
        swing_table
        + '<p class="muted">Chiến lược này không dùng top-N hay threshold tối ưu trên OOS. Margin được chọn trong validation của từng fold; frozen holdout chỉ dùng một lần để kiểm định. Stop-loss không được giả định vượt qua ràng buộc chứng khoán chưa về.</p>',
        open_by_default=False,
        note="stateful cash → long → cash",
    )
    technical_panel = _accordion("Tín hiệu kỹ thuật", technical_table, open_by_default=False, note="chi tiết")
    decision_panel = _accordion(
        "Điều kiện phát hành tín hiệu",
        _gate_overview(decision.get("checks", {}), decision_table),
        open_by_default=True,
        note=signal_status_label(decision["status"]),
    )
    risk_panel = _accordion("Quản trị rủi ro", risk_table, open_by_default=False, note="stop / target")
    feature_panel = _accordion("Mức độ quan trọng của đặc trưng", feature_table, open_by_default=False, note="top feature")
    fundamental_panel = _accordion("Phân tích cơ bản", fundamental_table, open_by_default=False, note="BCTC/tỷ số")
    news_panel = _accordion("Tin tức doanh nghiệp", news_table, open_by_default=False, note="research only")
    forecast_panel = _accordion("Dự báo ngắn hạn", forecast_table, open_by_default=False, note=f"{config['forecast_sessions']} phiên")
    calendar_panel = _accordion(
        "Lịch giao dịch Việt Nam dùng cho forecast",
        (
            f"<p>{_escape(calendar_note)}</p>"
            f"<p><strong>Ngày nghỉ đã loại:</strong> {_escape(', '.join(calendar_holidays) or 'chưa cấu hình')}</p>"
            "<p class=\"muted\">Nếu HOSE/HNX/UPCoM công bố nghỉ đột xuất, cần thêm ngày đó vào config `market_holidays` rồi chạy lại report.</p>"
        ),
        open_by_default=False,
        note="không tính T7/CN/lễ",
    )

    document = f"""<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Bảng điều khiển XGBoost - {_escape(config['symbol'])}</title>
  <style>
    :root {{ --bg:#f4f7fb; --ink:#162033; --muted:#68758a; --line:#e3e9f2; --panel:#fff; --navy:#102a43; --blue:#2563eb; --cyan:#0f766e; --red:#b42318; --amber:#a15c07; --soft-blue:#eff6ff; --soft-amber:#fff7e6; --soft-slate:#f6f8fb; --shadow:0 14px 34px rgba(25,42,70,.08); }}
    * {{ box-sizing:border-box; }}
    html {{ scroll-behavior:smooth; }}
    body {{ margin:0; font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif; background:var(--bg); color:var(--ink); }}
    header {{ padding:38px clamp(18px,4vw,56px) 30px; background:radial-gradient(circle at 84% -15%,#315f9d 0%,transparent 30%),linear-gradient(125deg,#0b1f33 0%,#102a43 52%,#163e63 100%); color:#fff; border-bottom:1px solid rgba(255,255,255,.12); }}
    .header-layout {{ max-width:1360px; margin:0 auto; display:grid; grid-template-columns:minmax(0,1fr) minmax(300px,370px); gap:34px; align-items:start; }}
    .eyebrow {{ color:var(--cyan); font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:.11em; }}
    header .eyebrow {{ color:#8dd9d0; }}
    h1 {{ margin:10px 0 8px; font-size:clamp(30px,4vw,48px); line-height:1.04; letter-spacing:-.035em; }}
    .subtitle,.disclaimer {{ color:var(--muted); line-height:1.6; }}
    header .subtitle {{ color:#dce9f6; max-width:850px; margin:0; }}
    .capital-scenario {{ background:rgba(255,255,255,.98); color:var(--ink); border:1px solid rgba(255,255,255,.45); border-radius:14px; padding:16px; box-shadow:0 18px 40px rgba(1,14,29,.28); }}
    .capital-scenario label {{ display:block; color:var(--navy); font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:.08em; }}
    .capital-input-row {{ display:flex; align-items:center; gap:8px; margin-top:8px; }}
    .capital-input-row input {{ width:100%; min-width:0; padding:10px 11px; border:1px solid #60a5fa; border-radius:8px; background:#eaf4ff; color:#0b2b55; caret-color:#1d4ed8; box-shadow:inset 0 1px 0 rgba(255,255,255,.85); font:inherit; font-size:17px; font-weight:800; font-variant-numeric:tabular-nums; letter-spacing:.015em; }}
    .capital-input-row input::selection {{ background:#1d4ed8; color:#fff; }}
    .capital-input-row input:focus {{ outline:3px solid rgba(96,165,250,.42); border-color:#2563eb; background:#f8fbff; }}
    .capital-input-row span {{ color:var(--muted); font-size:13px; font-weight:750; }}
    .capital-scenario p {{ margin:8px 0 0; color:var(--muted); font-size:12px; line-height:1.45; }}
    .capital-scenario-metrics {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; margin-top:12px; }}
    .capital-scenario-metric {{ padding:9px; border-radius:8px; background:var(--soft-blue); border:1px solid #dbeafe; }}
    .capital-scenario-label,.capital-scenario-metric small {{ display:block; font-size:11px; color:var(--muted); }}
    .capital-scenario-metric strong {{ display:block; margin:3px 0; color:var(--navy); font-size:14px; }}
    .capital-scenario-note {{ border-top:1px solid var(--line); padding-top:8px; }}
    main {{ padding:28px clamp(18px,4vw,56px) 52px; display:grid; gap:24px; max-width:1440px; margin:0 auto; }}
    .quick-nav {{ position:sticky; top:0; z-index:10; display:flex; gap:8px; flex-wrap:wrap; padding:11px clamp(18px,4vw,56px); background:rgba(244,247,251,.9); backdrop-filter:blur(14px); border-bottom:1px solid var(--line); }}
    .quick-nav a {{ text-decoration:none; color:#38506b; background:#fff; border:1px solid var(--line); border-radius:7px; padding:8px 11px; font-weight:750; font-size:12px; }}
    .quick-nav a:hover {{ color:var(--blue); border-color:#b9d2ff; background:var(--soft-blue); }}
    .metrics {{ display:grid; gap:12px; }}
    .market-pulse {{ grid-template-columns:repeat(6,minmax(190px,1fr)); gap:16px; }}
    .pulse-card {{ display:flex; flex-direction:column; min-height:174px; padding:18px; border:1px solid var(--line); border-radius:17px; background:linear-gradient(145deg,var(--panel),color-mix(in srgb,var(--panel) 92%,#1e3a5f)); box-shadow:var(--shadow); position:relative; overflow:hidden; }}
    .pulse-card::before {{ content:""; position:absolute; inset:0 0 auto; height:3px; background:#64748b; }}
    .pulse-card.positive::before {{ background:#10b981; }}
    .pulse-card.negative::before {{ background:#f87171; }}
    .pulse-card.warning::before {{ background:#fbbf24; }}
    .pulse-head {{ display:flex; align-items:center; justify-content:space-between; gap:10px; }}
    .pulse-label {{ display:flex; align-items:center; gap:8px; color:var(--muted); font-size:11px; font-weight:850; letter-spacing:.065em; text-transform:uppercase; }}
    .pulse-mark {{ width:9px; height:9px; border:2px solid currentColor; border-radius:50%; opacity:.9; }}
    .pulse-help {{ display:grid; place-items:center; width:20px; height:20px; border:1px solid currentColor; border-radius:50%; color:var(--muted); font-size:12px; font-weight:850; opacity:.8; }}
    .pulse-value {{ margin-top:22px; color:var(--ink); font-size:31px; font-weight:850; line-height:1.04; letter-spacing:-.045em; font-variant-numeric:tabular-nums; }}
    .pulse-card.positive .pulse-value,.pulse-card.positive .pulse-mark {{ color:#10d993; }}
    .pulse-card.negative .pulse-value,.pulse-card.negative .pulse-mark {{ color:#fb7185; }}
    .pulse-card.warning .pulse-value,.pulse-card.warning .pulse-mark {{ color:#fbbf24; }}
    .pulse-detail {{ margin-top:10px; color:var(--muted); font-size:12px; line-height:1.42; }}
    .pulse-status {{ margin-top:auto; padding:7px 9px; border:1px solid var(--line); border-radius:8px; color:var(--muted); background:color-mix(in srgb,var(--panel) 82%,var(--soft-slate)); font-size:11px; font-weight:750; line-height:1.25; }}
    .pulse-card.positive .pulse-status {{ color:#20c997; border-color:rgba(16,185,129,.38); background:rgba(16,185,129,.09); }}
    .pulse-card.negative .pulse-status {{ color:#fb7185; border-color:rgba(248,113,113,.42); background:rgba(248,113,113,.09); }}
    .pulse-card.warning .pulse-status {{ color:#fbbf24; border-color:rgba(251,191,36,.4); background:rgba(251,191,36,.08); }}
    .result-metrics {{ grid-template-columns:repeat(4,minmax(165px,1fr)); }}
    .strategy-metrics {{ grid-template-columns:repeat(4,minmax(160px,1fr)); }}
    .fundamental-metrics {{ grid-template-columns:repeat(7,minmax(130px,1fr)); }}
    .metric,section {{ background:var(--panel); border:1px solid var(--line); border-radius:12px; }}
    .metric,section,.accordion {{ box-shadow:var(--shadow); }}
    .metric {{ padding:16px; min-height:112px; border-radius:12px; position:relative; overflow:hidden; }}
    .metric::before {{ content:""; position:absolute; inset:0 auto 0 0; width:3px; background:#dbe5f1; }}
    .metric-label {{ color:var(--muted); font-size:12px; font-weight:750; text-transform:uppercase; }}
    .metric-value {{ margin-top:10px; font-size:23px; font-weight:780; line-height:1.1; letter-spacing:-.025em; }}
    .metric-detail {{ color:var(--muted); margin-top:7px; font-size:13px; }}
    section {{ padding:20px; border-radius:14px; }}
    .section-title {{ display:flex; align-items:end; justify-content:space-between; gap:12px; margin:10px 0 0; }}
    .section-title h2 {{ margin:0; }}
    .section-kicker {{ color:var(--muted); font-size:12px; font-weight:650; }}
    .decision-summary {{ display:grid; grid-template-columns:minmax(0,1.25fr) minmax(280px,.75fr); gap:22px; padding:22px 24px; border-radius:14px; border:1px solid #d7e2ef; background:linear-gradient(110deg,#fff 0%,#f7fbff 100%); box-shadow:var(--shadow); }}
    .decision-summary h2 {{ margin:8px 0; font-size:22px; }}
    .decision-summary p {{ margin:0; color:#526175; line-height:1.58; }}
    .decision-summary .status-badge {{ margin-top:10px; }}
    .status-badge {{ display:inline-flex; align-items:center; width:max-content; padding:6px 10px; border-radius:999px; font-size:11px; font-weight:850; letter-spacing:.06em; }}
    .status-badge.neutral {{ color:#475569; background:#eef2f7; border:1px solid #d9e1ec; }}
    .status-badge.warning {{ color:#8a4b00; background:var(--soft-amber); border:1px solid #f4d89a; }}
    .status-badge.positive {{ color:#086455; background:#e6f8f4; border:1px solid #aee8db; }}
    .gate-summary {{ display:grid; align-content:center; gap:8px; padding-left:22px; border-left:1px solid #dbe5f0; }}
    .gate-summary strong {{ font-size:28px; letter-spacing:-.04em; color:var(--navy); }}
    .gate-summary span {{ color:var(--muted); font-size:13px; line-height:1.45; }}
    .grid {{ display:grid; grid-template-columns:minmax(0,1.15fr) minmax(320px,.85fr); gap:22px; align-items:start; }}
    .two {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:22px; }}
    .dashboard-grid {{ display:grid; grid-template-columns:minmax(0,1.32fr) minmax(340px,.68fr); gap:22px; align-items:start; }}
    .stack {{ display:grid; gap:14px; }}
    .research-workspace {{ padding:24px; border:1px solid #31516f; border-radius:15px; background:linear-gradient(115deg,#0b1422 0%,#101e31 52%,#0e1726 100%); color:#e9eff9; box-shadow:0 22px 50px rgba(7,15,29,.18); }}
    .research-workspace h2,.research-workspace h3 {{ color:#f7fbff; }}
    .research-workspace .eyebrow {{ color:#5da6ff; }}
    .research-workspace .muted {{ color:#aebbd0; }}
    .research-workspace .section-title {{ align-items:flex-start; gap:16px; margin:0 0 18px; }}
    .research-workspace .section-title > div {{ min-width:0; }}
    .research-workspace .section-title h2 {{ margin:3px 0 0; line-height:1.25; }}
    .research-workspace .section-kicker {{ display:block; max-width:340px; padding:8px 10px; border:1px solid rgba(93,166,255,.24); border-radius:8px; background:rgba(7,18,33,.38); color:#b8c8dd; font-size:11px; line-height:1.45; }}
    .research-workspace .two {{ width:100%; min-width:0; }}
    .research-workspace .stack {{ min-width:0; grid-template-columns:minmax(0,1fr); }}
    .research-workspace .grid {{ grid-template-columns:repeat(2,minmax(0,1fr)); gap:12px; }}
    .research-workspace .accordion {{ min-width:0; max-width:100%; box-shadow:none; background:#111d2e; border-color:#2a405c; }}
    .research-workspace section {{ background:#0d1726; border-color:#2a405c; box-shadow:none; }}
    .research-workspace .accordion > summary {{ min-width:0; background:#111d2e; color:#e8effa; border-color:#2a405c; }}
    .research-workspace .accordion-body {{ background:#0d1726; }}
    .research-workspace .accordion-note {{ color:#93a7c0; }}
    .research-workspace td:nth-child(2) {{ color:#86b8ff; }}
    .research-workspace th {{ background:#17263a; color:#aebbd0; border-color:#2a405c; }}
    .research-workspace td {{ border-color:#263b55; }}
    .ai-summary {{ display:grid; grid-template-columns:minmax(0,1.25fr) minmax(260px,.75fr); gap:22px; padding:20px; margin:0 0 18px; border:1px solid #245a8f; border-radius:12px; background:linear-gradient(105deg,rgba(37,99,235,.19),rgba(14,116,144,.14)); }}
    .ai-summary h3 {{ margin:4px 0 10px; font-size:17px; line-height:1.35; }}
    .ai-summary p {{ margin:0; color:#d5dfed; line-height:1.55; }}
    .ai-summary-meta {{ display:grid; align-content:center; gap:8px; padding-left:18px; border-left:1px solid #325979; }}
    .ai-summary-meta strong {{ color:#6bdcc8; font-size:19px; }}
    h2 {{ margin:0 0 12px; font-size:18px; letter-spacing:0; }}
    table {{ width:100%; border-collapse:collapse; font-size:14px; }}
    th {{ padding:10px 8px; border-bottom:2px solid var(--line); text-align:left; background:var(--soft-slate); font-size:11px; color:var(--muted); text-transform:uppercase; letter-spacing:.04em; }}
    td {{ padding:10px 8px; border-top:1px solid var(--line); vertical-align:top; }}
    td:first-child {{ font-weight:700; width:28%; }}
    td:nth-child(2) {{ color:#1d4f91; font-weight:700; width:24%; }}
    img {{ width:100%; height:auto; display:block; border-radius:9px; border:1px solid var(--line); background:#fff; }}
    .table-wrap {{ overflow-x:auto; }}
    .table-wrap table {{ min-width:680px; }}
    .table-wrap td {{ white-space:normal; }}
    .report-table-wrap {{ border:1px solid var(--line); border-radius:10px; background:var(--panel); }}
    .report-table {{ min-width:620px; font-size:13px; }}
    .report-table th {{ position:sticky; top:0; z-index:1; padding:11px 12px; background:var(--soft-slate); }}
    .report-table td {{ padding:12px; line-height:1.42; }}
    .report-table tbody tr:nth-child(even) {{ background:color-mix(in srgb,var(--soft-slate) 48%,transparent); }}
    .report-table tbody tr:hover {{ background:color-mix(in srgb,var(--blue) 7%,var(--panel)); }}
    .report-table td:first-child {{ width:31%; color:var(--ink); }}
    .report-table .table-value {{ width:22%; color:var(--ink); font-variant-numeric:tabular-nums; }}
    .report-table .table-detail {{ width:47%; color:var(--muted); font-weight:500; }}
    .status-chip {{ display:inline-flex; align-items:center; width:max-content; max-width:100%; padding:5px 8px; border:1px solid currentColor; border-radius:999px; font-size:11px; font-weight:850; line-height:1.2; letter-spacing:.025em; }}
    .status-chip.positive {{ color:#087d59; background:#e8f8f1; border-color:#9ee1c8; }}
    .status-chip.negative {{ color:#b4233c; background:#fff0f2; border-color:#fec3cc; }}
    .status-chip.warning {{ color:#9a5b00; background:#fff7e8; border-color:#f6d391; }}
    .status-chip.neutral {{ color:#526175; background:#eef2f7; border-color:#d7e0ea; }}
    .gate-overview {{ display:grid; grid-template-columns:minmax(150px,.36fr) minmax(0,1fr); gap:16px; align-items:stretch; margin-bottom:12px; }}
    .gate-score {{ display:grid; align-content:center; gap:4px; min-height:104px; padding:16px; border-radius:10px; background:linear-gradient(145deg,#ecf8f4,#f7fcfa); border:1px solid #b8e5d4; }}
    .gate-score strong {{ color:#087d59; font-size:30px; line-height:1; letter-spacing:-.05em; }}
    .gate-score span {{ color:#467565; font-size:12px; font-weight:700; }}
    .gate-next {{ padding:14px 16px; border:1px solid #f3d0d6; border-radius:10px; background:#fff9fa; }}
    .gate-next .eyebrow {{ color:#b4233c; font-size:10px; }}
    .gate-next ul {{ display:grid; gap:6px; padding:0; margin:8px 0 0; list-style:none; }}
    .gate-next li {{ display:flex; align-items:flex-start; gap:8px; color:#5c3540; font-size:12px; line-height:1.35; }}
    .status-dot {{ width:7px; height:7px; flex:0 0 auto; margin-top:5px; border-radius:999px; }}
    .status-dot.positive {{ background:#10b981; }}
    .status-dot.negative {{ background:#ef476f; }}
    .gate-detail {{ margin:0; padding:0; border:0; }}
    .gate-detail > summary {{ color:var(--blue); font-size:12px; }}
    .muted {{ color:var(--muted); line-height:1.55; }}
    details {{ border:1px solid var(--line); border-radius:10px; padding:9px 11px; margin:8px 0; }}
    .accordion {{ background:var(--panel); border:1px solid var(--line); border-radius:12px; padding:0; overflow:hidden; }}
    .accordion > summary {{ list-style:none; display:flex; align-items:center; justify-content:space-between; gap:14px; padding:15px 17px; background:#fff; border-bottom:1px solid transparent; }}
    .accordion > summary::-webkit-details-marker {{ display:none; }}
    .accordion > summary::after {{ content:"▾"; color:var(--muted); transform:rotate(-90deg); transition:transform .18s ease; }}
    .accordion[open] > summary {{ border-bottom-color:var(--line); }}
    .accordion[open] > summary::after {{ transform:rotate(0deg); }}
    .accordion-body {{ padding:15px 17px 17px; }}
    .accordion-note {{ color:var(--muted); font-size:12px; font-weight:650; margin-left:auto; }}
    summary {{ cursor:pointer; font-weight:700; }}
    details p {{ white-space:pre-wrap; line-height:1.55; }}
    a {{ color:var(--blue); }}
    @media (max-width:1200px) {{ .market-pulse,.result-metrics,.fundamental-metrics,.strategy-metrics {{ grid-template-columns:repeat(3,minmax(0,1fr)); }} .grid,.two,.dashboard-grid,.header-layout,.decision-summary,.ai-summary {{ grid-template-columns:1fr; }} .capital-scenario {{ max-width:460px; }} .gate-summary,.ai-summary-meta {{ border-left:0; border-top:1px solid #dbe5f0; padding:18px 0 0; }} .ai-summary-meta {{ border-color:#325979; }} }}
    @media (max-width:900px) {{ .research-workspace .section-title {{ flex-direction:column; gap:10px; }} .research-workspace .section-kicker {{ max-width:none; width:100%; }} }}
    @media (max-width:620px) {{ .market-pulse,.result-metrics,.fundamental-metrics,.strategy-metrics {{ grid-template-columns:1fr; }} .gate-overview {{ grid-template-columns:1fr; }} td {{ display:block; width:100%!important; border:0; padding:6px 4px; }} tr {{ display:block; border-top:1px solid var(--line); padding:8px 0; }} .report-table {{ min-width:0; }} .report-table thead {{ display:none; }} .report-table tr {{ padding:10px 12px; }} .report-table td:first-child {{ padding-top:0; }} .report-table .table-detail {{ padding-bottom:0; }} .quick-nav {{ position:static; }} }}
    {INTERACTIVE_CHART_CSS}
    {FORECAST_CHART_CSS}
    {CHAT_WIDGET_CSS}
  </style>
</head>
<body>
  <header>
    <div class="header-layout">
      <div>
        <div class="eyebrow">Phân tích cổ phiếu Việt Nam bằng XGBoost</div>
        <h1>{_escape(config['symbol'])} - {_escape(company_name)}</h1>
        <p class="subtitle">Dữ liệu {frame.index.min().date()} → {frame.index.max().date()}. Nguồn vnstock/{_escape(config['source'])}. XGBoost là mô hình chính; Logistic và mô hình đa số được dùng làm đối chứng.</p>
      </div>
      {capital_scenario_box}
    </div>
  </header>
  <nav class="quick-nav">
    <a href="#research">AI & tin có nguồn</a>
    <a href="#technical">Kỹ thuật</a>
    <a href="#overview">Tổng quan</a>
    <a href="#fundamental">Cơ bản & tin</a>
    <a href="#forecast">Dự báo</a>
    <span class="nav-spacer"></span>
    <button class="ui-button" id="theme-toggle" type="button" aria-label="Đổi giao diện sáng tối">◐ <span>Giao diện tối</span></button>
  </nav>
  <main>
    <section class="decision-summary" aria-labelledby="decision-heading">
      <div>
        <div class="eyebrow">Quyết định đã qua guard sau phí</div>
        <div class="status-badge {decision_tone}">{_escape(signal_status_label(decision_status))}</div>
        <h2 id="decision-heading">{_escape(investment_recommendation['title'])}</h2>
        <p>{_escape(investment_recommendation['reason'])}</p>
      </div>
      <div class="gate-summary">
        <span>Điều kiện chưa đạt</span>
        <strong>{len(failed_checks)}</strong>
        <span>{_escape(', '.join(signal_check_label(name) for name in failed_checks) if failed_checks else 'Tất cả điều kiện phát hành hiện có đều đạt.')}</span>
      </div>
    </section>
    <div class="metrics market-pulse" aria-label="Chỉ số thị trường đọc nhanh">{market_pulse_cards}</div>
    <div id="technical" class="section-title"><h2>Trading workspace</h2><span class="section-kicker">Nến động, chỉ báo và công cụ vẽ · dữ liệu cuối ngày</span></div>
    {interactive_chart}
    <div class="two">
      <div class="stack">{technical_panel}</div>
      <details class="accordion static-fallback"><summary><strong>Biểu đồ kỹ thuật tĩnh</strong><span class="accordion-note">ảnh dự phòng / in báo cáo</span></summary><div class="accordion-body"><img src="technical_chart.png" alt="Biểu đồ kỹ thuật tĩnh"></div></details>
    </div>
    <div id="research">
      <!-- FinAI dynamic enrichment start -->
      <!-- FinAI dynamic enrichment end -->
    </div>
    <div id="overview" class="section-title"><h2>Kết quả chính</h2><span class="section-kicker">KPI đọc nhanh trước, chi tiết bấm mở bên dưới</span></div>
    <div class="metrics result-metrics">{result_cards}</div>
    <div class="dashboard-grid">
      <div class="stack">{recommendation_panel}{swing_panel}{model_quality_panel}{feature_panel}</div>
      <div class="stack">{decision_panel}{risk_panel}</div>
    </div>
    <div id="fundamental" class="section-title"><h2>Cơ bản & tin tức</h2><span class="section-kicker">Các bảng dài để trong nút bung</span></div>
    <div class="metrics fundamental-metrics">{fundamental_cards}</div>
    <div class="two"><div class="stack">{fundamental_panel}</div><div class="stack">{news_panel}</div></div>
    <div id="forecast" class="section-title"><h2>Dự báo</h2><span class="section-kicker">Kịch bản giá và lịch sử drawdown</span></div>
    {interactive_forecast}
    <div class="two"><div class="stack">{forecast_panel}{calendar_panel}</div><details class="accordion static-fallback"><summary><strong>Biểu đồ dự báo tĩnh</strong><span class="accordion-note">ảnh dự phòng / in báo cáo</span></summary><div class="accordion-body"><img src="forecast_chart.png" alt="Biểu đồ dự báo tĩnh"></div></details></div>
    <section><h2>Lịch sử giá và mức sụt giảm</h2><img src="history_chart.png" alt="Biểu đồ lịch sử giá"></section>
    <p class="disclaimer">Báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.</p>
  </main>
  {CHAT_WIDGET_MARKUP}
  <script>
    (() => {{
      const box = document.querySelector('.capital-scenario');
      const input = document.getElementById('assumed-capital-input');
      if (!box || !input) return;

      const storageKey = 'vn-stock-analysis-assumed-capital-vnd';
      const formatVnd = (value) => `${{new Intl.NumberFormat('vi-VN', {{ maximumFractionDigits: 0 }}).format(Math.round(value))}} VND`;
      const parseCapital = (value) => Number(String(value).replace(/[^0-9.-]/g, ''));
      const render = () => {{
        const capital = parseCapital(input.value);
        const valid = Number.isFinite(capital) && capital >= 100000;
        document.querySelectorAll('[data-capital-rate]').forEach((element) => {{
          const rate = Number(element.dataset.capitalRate);
          element.textContent = valid && Number.isFinite(rate) ? formatVnd(capital * rate) : 'Nhập vốn ≥ 100.000 VND';
        }});
        document.querySelectorAll('[data-capital-risk-pct]').forEach((element) => {{
          const rate = Number(element.dataset.capitalRiskPct);
          element.textContent = valid && Number.isFinite(rate) ? formatVnd(capital * rate) : 'Nhập vốn ≥ 100.000 VND';
        }});
        if (valid) {{
          try {{ localStorage.setItem(storageKey, String(capital)); }} catch (_) {{ /* Browser storage is optional. */ }}
        }}
      }};
      try {{
        const saved = parseCapital(localStorage.getItem(storageKey));
        if (Number.isFinite(saved) && saved >= 100000) input.value = String(saved);
      }} catch (_) {{ /* Safari private mode or file restrictions: use report default. */ }}
      input.addEventListener('input', render);
      input.addEventListener('change', render);
      render();
    }})();
  </script>
  {interactive_chart_scripts}
  {interactive_forecast_scripts}
  {CHAT_WIDGET_SCRIPT}
</body>
</html>
"""
    output_path.write_text(document, encoding="utf-8")
