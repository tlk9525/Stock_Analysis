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


def _threshold_sensitivity_rows(strategy: dict) -> list[tuple[str, str, str]]:
    scenarios = strategy.get("threshold_sensitivity") or []
    rows = []
    for item in scenarios:
        threshold = safe_float(item.get("signal_threshold"))
        net = safe_float(item.get("net_total_return"))
        cost_sum = safe_float(item.get("transaction_cost_sum"))
        active_sessions = int(item.get("active_sessions") or 0)
        round_trips = int(item.get("completed_round_trips") or 0)
        rows.append(
            (
                f"Ngưỡng {format_number(threshold, 2)}",
                format_signed_percent(net),
                (
                    f"{active_sessions} phiên active/{round_trips} vòng; "
                    f"phí cộng dồn {format_percent(cost_sum)}; "
                    f"Sharpe {format_number(safe_float(item.get('sharpe_ratio')), 2)}."
                ),
            )
        )
    return rows or [("Chưa có sensitivity", "N/A", "Cần chạy lại model để sinh threshold_sensitivity.")]


def _top_n_sensitivity_rows(strategy: dict) -> list[tuple[str, str, str]]:
    scenarios = strategy.get("top_n_trade_sensitivity") or []
    rows = []
    for item in scenarios:
        top_n = int(item.get("top_n") or 0)
        net = safe_float(item.get("net_total_return"))
        gross = safe_float(item.get("gross_total_return"))
        cost_sum = safe_float(item.get("transaction_cost_sum"))
        min_probability = safe_float(item.get("min_probability_included"))
        round_trips = int(item.get("completed_round_trips") or 0)
        rows.append(
            (
                f"Giới hạn tối đa {top_n} vòng",
                format_signed_percent(net),
                (
                    f"Gross {format_signed_percent(gross)}; phí {format_percent(cost_sum)}; "
                    f"thực chạy {round_trips} vòng; ngưỡng xác suất trong nhóm {format_percent(min_probability)}; "
                    f"Sharpe {format_number(safe_float(item.get('sharpe_ratio')), 2)}."
                ),
            )
        )
    return rows or [("Chưa có top-N", "N/A", "Cần chạy lại model để sinh top_n_trade_sensitivity.")]


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


def _turnover_sensitivity_table(strategy: dict) -> str:
    rows = _turnover_sensitivity_rows(strategy)
    if not rows:
        return _table(
            [
                (
                    "Chưa có dữ liệu",
                    "N/A",
                    "Cần chạy lại model để sinh threshold_sensitivity/top_n_trade_sensitivity.",
                )
            ]
        )
    return _html_table(
        [
            "Kịch bản",
            "Cách chọn",
            "Vòng",
            "Gross trước phí",
            "Phí",
            "Net sau phí",
            "Sharpe",
            "Ghi chú",
        ],
        [
            [
                _escape(row["scenario"]),
                _escape(row["selection_rule"]),
                _escape(row["round_trips"]),
                _escape(row["gross"]),
                _escape(row["cost"]),
                _escape(row["net"]),
                _escape(row["sharpe"]),
                _escape(row["probability_note"]),
            ]
            for row in rows
        ],
    )


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


def _table(rows: list[tuple[str, str, str]]) -> str:
    body = "".join(
        f"<tr><td>{_escape(name)}</td><td>{_escape(value)}</td><td>{_escape(detail)}</td></tr>"
        for name, value, detail in rows
    )
    return f"<table><tbody>{body}</tbody></table>"


def _html_table(headers: list[str], rows: list[list[str]]) -> str:
    """Render a responsive HTML table from already-escaped cells."""

    head = "".join(f"<th>{_escape(header)}</th>" for header in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
        for row in rows
    )
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


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
      {_html_table(["Gate", "Kết quả"], gate_rows)}
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

    ai_section = ""
    if analysis:
        decision = _escape(analysis.get("decision_status") or "UNKNOWN")
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
    {ai_section}
    {news_impact}
    {_accordion("Tin web đã lấy", live_table, note="headline + nguồn")}
    {_accordion("News Reader: bài đã đọc và trích đoạn", reader_table, note="bấm mở trích đoạn")}
    {statement_section}
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
    legacy_execution_visible = not swing.get("available") or bool(strategy.get("available"))
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
    result_cards = "".join(
        [
            _metric_card("Giá hiện tại", format_price(latest), f"{levels['latest_date']} - nghìn VND/cp"),
            _metric_card("Xu hướng kỹ thuật", technical["bias"], f"Điểm {technical['score']}"),
            _metric_card("Trạng thái tín hiệu", signal_status_label(decision["status"]), "; ".join(signal_check_label(name) for name in decision.get("failed_checks", [])) or "Đã vượt qua tất cả điều kiện phát hành"),
            _metric_card("Mua mới", str(investment_recommendation["entry_action"]), str(investment_recommendation["title"])),
            _metric_card(
                "Lệnh mới hôm nay",
                f"{int(investment_recommendation.get('recommended_new_entries') or 0)} lệnh",
                "Chỉ là 1 khi signal ACTIONABLE; không lấy số vòng lịch sử làm khuyến nghị.",
            ),
            _metric_card("Đang giữ", str(investment_recommendation["holding_action"]), str(investment_recommendation["holding_reason"])),
            _metric_card("Model health", str(investment_recommendation["model_health"]), str(investment_recommendation["model_health_reason"])),
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
                    "Dự báo return vượt VNINDEX; không phải xác suất phiên kế tiếp.",
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
        [(item["name"], item["status"], item["detail"]) for item in technical["signals"]]
    )
    model_table = _table(
        [
            ("XGBoost", format_number(metrics["xgboost"]["balanced_accuracy"], 3), f"AUC {format_number(metrics['xgboost']['roc_auc'], 3)}"),
            ("Logistic", format_number(metrics["logistic_baseline"]["balanced_accuracy"], 3), f"AUC {format_number(metrics['logistic_baseline']['roc_auc'], 3)}"),
            ("Đa số", format_number(metrics["majority_baseline"]["balanced_accuracy"], 3), "Mốc so sánh"),
        ]
    )
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
    cost_breakdown_table = _table(_cost_breakdown_rows(strategy, decision))
    investment_recommendation_table = _table(
        _investment_recommendation_rows(investment_recommendation)
    )
    turnover_sensitivity_table = _turnover_sensitivity_table(strategy)
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
        else [("Trạng thái", "Chưa chạy", "Bật swing_strategy.enabled để chạy chiến lược 5D.")]
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
    gross_return = safe_float(strategy.get("gross_total_return"))
    net_return = safe_float(strategy.get("net_total_return", strategy.get("total_return")))
    round_trips = int(strategy.get("completed_round_trips") or 0)
    cost_sum = safe_float(strategy.get("transaction_cost_sum"))
    round_trip_cost = safe_float(strategy.get("round_trip_cost_bps"))
    breakeven_cost_bps = (
        None
        if gross_return is None
        or cost_sum is None
        or cost_sum <= 0
        or round_trip_cost is None
        else round_trip_cost * gross_return / cost_sum
    )
    strategy_cards = "".join(
        [
            _metric_card("Gross legacy trước phí" if swing.get("available") else "Gross trước phí", format_signed_percent(gross_return), "Lợi nhuận classifier 1D trước phí/thuế" if swing.get("available") else "Lợi nhuận chiến lược trước phí/thuế"),
            _metric_card("Net legacy sau phí" if swing.get("available") else "Net sau phí", format_signed_percent(net_return), "Diagnostic 1D, không dùng cho publish guard 5D" if swing.get("available") else "Kết quả dùng cho publish guard"),
            _metric_card("Vòng baseline legacy" if swing.get("available") else "Vòng baseline lịch sử", str(round_trips), "Dùng đo turnover/phí, không phải số lệnh nên thực hiện"),
            _metric_card("Phí cộng dồn", format_percent(cost_sum), f"Ngưỡng hòa vốn {format_number(breakeven_cost_bps, 1)} bps/vòng"),
        ]
    )
    model_quality_panel = _accordion(
        "So sánh mô hình",
        model_table,
        open_by_default=True,
        note="XGBoost vs Logistic",
    )
    backtest_panel = _accordion(
        "Diagnostic legacy 1D: kiểm thử ngoài mẫu sau chi phí" if swing.get("available") else "Kiểm thử chiến lược ngoài mẫu sau chi phí",
        backtest_table,
        open_by_default=True,
        note=f"{round_trips} vòng",
    )
    cost_panel = _accordion(
        "Breakdown legacy 1D trước phí / sau phí" if swing.get("available") else "Breakdown trước phí / sau phí",
        cost_breakdown_table,
        open_by_default=True,
        note="vì sao gross dương nhưng net âm",
    )
    recommendation_panel = _accordion(
        "Khuyến nghị theo fixed-horizon swing 5D" if swing.get("available") else "Khuyến nghị hành động sau phí",
        investment_recommendation_table
        + '<p class="muted">Classifier next-day và bảng sensitivity legacy không tham gia quyết định này. Mua mới chỉ được xét khi swing 5D có sample đủ lớn, ranking edge dương, frozen holdout/stress phí đạt và expected excess return vượt chi phí + margin.</p>',
        open_by_default=True,
        note=str(investment_recommendation["entry_action"]),
    )
    turnover_panel = _accordion(
        "Phụ lục legacy 1D — Kiểm thử kịch bản lịch sử (không phải khuyến nghị giao dịch)",
        turnover_sensitivity_table
        + f'<p class="muted"><strong>Không dùng bảng này để chọn “1 lệnh” hay DCA.</strong> Baseline {round_trips} vòng chỉ để đo turnover/phí. Các dòng threshold là ứng viên nghiên cứu cần holdout/future đã khóa; các dòng 10/5/1 có selection bias vì số vòng được chọn sau khi đã thấy OOS. Khi signal chưa ACTIONABLE, lệnh mới hôm nay luôn là 0.</p>',
        open_by_default=False,
        note="nghiên cứu OOS · research-only",
    )
    legacy_panels = (
        f"{turnover_panel}{cost_panel}{backtest_panel}"
        if legacy_execution_visible
        else ""
    )
    legacy_strategy_section = (
        f'''<div id="strategy" class="section-title"><h2>Chi phí & vòng lệnh</h2><span class="section-kicker">Trọng tâm: tránh giao dịch nhiều làm phí ăn hết lợi thế</span></div>
    <div class="metrics strategy-metrics">{strategy_cards}</div>'''
        if legacy_execution_visible
        else ""
    )
    swing_panel = _accordion(
        "Chiến lược swing 5 phiên: frozen holdout & T+2",
        swing_table
        + '<p class="muted">Chiến lược này không dùng top-N hay threshold tối ưu trên OOS. Margin được chọn trong validation của từng fold; frozen holdout chỉ dùng một lần để kiểm định. Stop-loss không được giả định vượt qua ràng buộc chứng khoán chưa về.</p>',
        open_by_default=True,
        note="stateful cash → long → cash",
    )
    technical_panel = _accordion("Tín hiệu kỹ thuật", technical_table, open_by_default=False, note="chi tiết")
    decision_panel = _accordion("Điều kiện phát hành tín hiệu", decision_table, open_by_default=True, note=signal_status_label(decision["status"]))
    risk_panel = _accordion("Quản trị rủi ro", risk_table, open_by_default=True, note="stop / target")
    feature_panel = _accordion("Mức độ quan trọng của đặc trưng", feature_table, open_by_default=False, note="top feature")
    fundamental_panel = _accordion("Phân tích cơ bản", fundamental_table, open_by_default=False, note="BCTC/tỷ số")
    news_panel = _accordion("Tin tức doanh nghiệp", news_table, open_by_default=False, note="research only")
    forecast_panel = _accordion("Dự báo ngắn hạn", forecast_table, open_by_default=True, note=f"{config['forecast_sessions']} phiên")
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
    .capital-input-row input {{ width:100%; min-width:0; padding:10px 11px; border:1px solid #b9c8d9; border-radius:8px; color:var(--ink); font:inherit; font-size:17px; font-weight:750; }}
    .capital-input-row input:focus {{ outline:3px solid rgba(37,99,235,.2); border-color:var(--blue); }}
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
    @media (max-width:1200px) {{ .result-metrics,.fundamental-metrics,.strategy-metrics {{ grid-template-columns:repeat(3,minmax(0,1fr)); }} .grid,.two,.dashboard-grid,.header-layout,.decision-summary {{ grid-template-columns:1fr; }} .capital-scenario {{ max-width:460px; }} .gate-summary {{ border-left:0; border-top:1px solid #dbe5f0; padding:18px 0 0; }} }}
    @media (max-width:620px) {{ .result-metrics,.fundamental-metrics,.strategy-metrics {{ grid-template-columns:1fr; }} td {{ display:block; width:100%!important; border:0; padding:6px 4px; }} tr {{ display:block; border-top:1px solid var(--line); padding:8px 0; }} .quick-nav {{ position:static; }} }}
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
    <a href="#overview">Tổng quan</a>
    <a href="#strategy">Chi phí & vòng lệnh</a>
    <a href="#technical">Kỹ thuật</a>
    <a href="#fundamental">Cơ bản & tin</a>
    <a href="#forecast">Dự báo</a>
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
    <div id="overview" class="section-title"><h2>Kết quả chính</h2><span class="section-kicker">KPI đọc nhanh trước, chi tiết bấm mở bên dưới</span></div>
    <div class="metrics result-metrics">{result_cards}</div>
    {legacy_strategy_section}
    <div class="dashboard-grid">
      <div class="stack">{recommendation_panel}{swing_panel}{legacy_panels}{model_quality_panel}{feature_panel}</div>
      <div class="stack">{decision_panel}{risk_panel}</div>
    </div>
    <div id="technical" class="section-title"><h2>Kỹ thuật</h2><span class="section-kicker">Biểu đồ mở sẵn, bảng tín hiệu thu gọn</span></div>
    <div class="grid"><section><h2>Biểu đồ kỹ thuật</h2><img src="technical_chart.png" alt="Biểu đồ kỹ thuật"></section><div class="stack">{technical_panel}</div></div>
    <div id="fundamental" class="section-title"><h2>Cơ bản & tin tức</h2><span class="section-kicker">Các bảng dài để trong nút bung</span></div>
    <div class="metrics fundamental-metrics">{fundamental_cards}</div>
    <div class="two"><div class="stack">{fundamental_panel}</div><div class="stack">{news_panel}</div></div>
    <div id="forecast" class="section-title"><h2>Dự báo</h2><span class="section-kicker">Kịch bản giá và lịch sử drawdown</span></div>
    <div class="two"><div class="stack">{forecast_panel}{calendar_panel}</div><section><h2>Biểu đồ dự báo</h2><img src="forecast_chart.png" alt="Biểu đồ dự báo"></section></div>
    <section><h2>Lịch sử giá và mức sụt giảm</h2><img src="history_chart.png" alt="Biểu đồ lịch sử giá"></section>
    <p class="disclaimer">Báo cáo dùng để học tập và lập kịch bản, không phải khuyến nghị mua/bán.</p>
  </main>
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
</body>
</html>
"""
    output_path.write_text(document, encoding="utf-8")
