from __future__ import annotations

import re

import pandas as pd

from src.utils import clean_json_value, safe_float


FUNDAMENTAL_RATIO_COLUMNS = [
    ("pe", "P/E", "number"),
    ("pb", "P/B", "number"),
    ("ps", "P/S", "number"),
    ("roe", "ROE", "percent"),
    ("roa", "ROA", "percent"),
    ("grossMargin", "Gross margin", "percent"),
    ("afterTaxProfitMargin", "Net margin", "percent"),
    ("debtToEquity", "Debt/Equity", "number"),
    ("currentRatio", "Current ratio", "number"),
    ("npl", "NPL", "percent"),
    ("casaRatio", "CASA", "percent"),
    ("dividendYield", "Dividend yield", "percent"),
    ("marketCap", "Market cap", "money"),
]

TRANSPOSED_RATIO_IDS = {
    "pe": ["pe", "pe_ratio"],
    "pb": ["pb", "pb_ratio"],
    "ps": ["ps", "ps_ratio"],
    "roe": ["roe"],
    "roa": ["roa"],
    "grossMargin": ["gross_margin", "grossmargin"],
    "afterTaxProfitMargin": ["after_tax_profit_margin", "net_margin"],
    "debtToEquity": ["debt_to_equity", "debt_per_equity"],
    "currentRatio": ["current_ratio"],
    "npl": ["npl"],
    "casaRatio": ["casa_ratio"],
    "dividendYield": ["dividend_yield"],
    "marketCap": ["market_cap"],
}

INCOME_GROWTH_ROWS = [
    (
        "revenue_growth",
        "Revenue Growth",
        ["net_sales", "sales", "total_operating_income", "net_interest_income"],
    ),
    (
        "profit_growth",
        "Profit Growth",
        ["attributable_to_parent_company", "net_profit_loss_after_tax"],
    ),
]


# Các chỉ số dưới đây được tính từ ba báo cáo tài chính, không phải từ giá thị
# trường. Chúng chỉ dùng cho dashboard/research cho tới khi có ``available_at``
# lịch sử đáng tin cậy để backtest point-in-time.
STATEMENT_ITEM_ALIASES = {
    "operating_cash_flow": (
        "cash_flow",
        ["net_cash_inflows_outflows_from_operating_activities"],
        "Dòng tiền từ HĐKD",
        "money",
    ),
    "capital_expenditure": (
        "cash_flow",
        ["purchases_of_fixed_assets_and_other_long_term_assets"],
        "CAPEX",
        "money",
    ),
    "net_profit_after_tax": (
        "income_statement",
        ["net_profit_loss_after_tax", "attributable_to_parent_company"],
        "Lợi nhuận sau thuế",
        "money",
    ),
    "operating_profit": (
        "income_statement",
        ["operating_profit_loss"],
        "Lợi nhuận hoạt động",
        "money",
    ),
    "interest_expense": (
        "income_statement",
        ["interest_expenses"],
        "Chi phí lãi vay",
        "money",
    ),
    "cash_and_equivalents": (
        "balance_sheet",
        ["cash_and_cash_equivalents"],
        "Tiền và tương đương tiền",
        "money",
    ),
    "short_term_debt": (
        "balance_sheet",
        ["short_term_borrowings"],
        "Vay ngắn hạn",
        "money",
    ),
    "long_term_debt": (
        "balance_sheet",
        ["long_term_borrowings"],
        "Vay dài hạn",
        "money",
    ),
    "total_assets": (
        "balance_sheet",
        ["total_assets"],
        "Tổng tài sản",
        "money",
    ),
    "total_liabilities": (
        "balance_sheet",
        ["liabilities"],
        "Tổng nợ phải trả",
        "money",
    ),
    "owners_equity": (
        "balance_sheet",
        ["owners_equity"],
        "Vốn chủ sở hữu",
        "money",
    ),
    "accounts_receivable": (
        "balance_sheet",
        ["accounts_receivable", "trade_accounts_receivable"],
        "Khoản phải thu",
        "money",
    ),
    "inventories": (
        "balance_sheet",
        ["inventories_net", "inventories"],
        "Hàng tồn kho",
        "money",
    ),
}


def dataframe_first_record(frame: pd.DataFrame) -> dict:
    if frame.empty:
        return {}
    return {
        str(key): clean_json_value(value)
        for key, value in frame.iloc[0].to_dict().items()
    }


def _period_label(row: pd.Series) -> str | None:
    year = safe_float(row.get("year"))
    quarter = safe_float(row.get("quarter"))
    if year is None:
        return None
    if quarter is None or quarter >= 5:
        return str(int(year))
    return f"{int(year)}-Q{int(quarter)}"


def _summarize_transposed(frame: pd.DataFrame) -> tuple[list[dict], str | None]:
    metadata_columns = {"item", "item_en", "item_id"}
    period_columns = [column for column in frame.columns if column not in metadata_columns]
    if not period_columns:
        return [], None

    latest_period = str(period_columns[-1])
    item_ids = frame["item_id"].astype(str).str.strip()
    metrics = []
    for metric_name, label, unit in FUNDAMENTAL_RATIO_COLUMNS:
        aliases = TRANSPOSED_RATIO_IDS.get(metric_name, [metric_name])
        row = frame[item_ids.isin(aliases)]
        if row.empty:
            continue
        value = safe_float(row.iloc[0][period_columns[-1]])
        if value is not None:
            metrics.append(_metric(metric_name, label, value, unit, latest_period))
    return metrics, latest_period


def _metric(name: str, label: str, value: float, unit: str, period: str | None) -> dict:
    return {
        "metric_name": name,
        "metric_label": label,
        "metric_value": value,
        "metric_unit": unit,
        "period": period,
    }


def summarize_ratios(frame: pd.DataFrame) -> tuple[list[dict], str | None]:
    if frame.empty:
        return [], None
    if "item_id" in frame.columns and "pe" not in frame.columns:
        return _summarize_transposed(frame)

    out = frame.copy()
    for column in ["year", "quarter"]:
        if column in out.columns:
            out[column] = pd.to_numeric(out[column], errors="coerce")
    sort_columns = [column for column in ["year", "quarter"] if column in out.columns]
    if sort_columns:
        out = out.sort_values(sort_columns)
    latest = out.iloc[-1]
    period = _period_label(latest)

    metrics = []
    for column, label, unit in FUNDAMENTAL_RATIO_COLUMNS:
        if column not in latest.index:
            continue
        value = safe_float(latest.get(column))
        if value is not None:
            metrics.append(_metric(column, label, value, unit, period))
    return metrics, period


def summarize_income_growth(frame: pd.DataFrame) -> tuple[list[dict], str | None]:
    if frame.empty or "item_id" not in frame.columns:
        return [], None

    quarter_pattern = re.compile(r"^(\d{4})-Q([1-4])$")
    period_columns = [
        str(column)
        for column in frame.columns
        if quarter_pattern.fullmatch(str(column))
    ]
    if not period_columns:
        return [], None
    period_columns.sort(
        key=lambda period: tuple(int(value) for value in period.replace("-Q", "-").split("-"))
    )
    latest_period = period_columns[-1]
    match = quarter_pattern.fullmatch(latest_period)
    if match is None:
        return [], None
    previous_period = f"{int(match.group(1)) - 1}-Q{match.group(2)}"
    if previous_period not in frame.columns:
        return [], latest_period

    item_ids = frame["item_id"].fillna("").astype(str).str.strip()
    metrics = []
    for metric_name, label, aliases in INCOME_GROWTH_ROWS:
        selected = pd.DataFrame()
        for alias in aliases:
            selected = frame[item_ids == alias]
            if not selected.empty:
                break
        if selected.empty:
            continue
        current_value = safe_float(selected.iloc[0][latest_period])
        previous_value = safe_float(selected.iloc[0][previous_period])
        if current_value is None or previous_value is None or previous_value <= 0:
            continue
        growth = current_value / previous_value - 1
        metrics.append(
            _metric(
                metric_name,
                label,
                growth,
                "percent",
                f"{latest_period} YoY",
            )
        )
    return metrics, latest_period


def _statement_period_columns(frame: pd.DataFrame) -> list[str]:
    """Return quarter columns in chronological order for vnstock statements."""

    pattern = re.compile(r"^\d{4}-Q[1-4]$")
    columns = [str(column) for column in frame.columns if pattern.fullmatch(str(column))]
    return sorted(columns, key=lambda value: (int(value[:4]), int(value[-1])))


def _statement_value(
    frame: pd.DataFrame,
    aliases: list[str],
    period: str | None,
) -> float | None:
    if frame.empty or not period or "item_id" not in frame.columns or period not in frame:
        return None
    item_ids = frame["item_id"].fillna("").astype(str).str.strip()
    for alias in aliases:
        selected = frame[item_ids == alias]
        if not selected.empty:
            value = safe_float(selected.iloc[0][period])
            if value is not None:
                return value
    return None


def summarize_financial_statements(
    frames: dict[str, pd.DataFrame],
) -> tuple[list[dict], dict]:
    """Create auditable latest-quarter cash-flow and balance-sheet metrics.

    ``vnstock`` returns statement rows transposed by reporting period. The
    function deliberately does not infer a publication date: these metrics are
    a current snapshot until an official ``available_at`` history is supplied.
    """

    statement_periods = {
        name: _statement_period_columns(frame)
        for name, frame in frames.items()
        if name in {"income_statement", "balance_sheet", "cash_flow"}
    }
    latest_periods = {
        name: periods[-1]
        for name, periods in statement_periods.items()
        if periods
    }
    values: dict[str, float] = {}
    metrics: list[dict] = []
    for metric_name, (statement_name, aliases, label, unit) in STATEMENT_ITEM_ALIASES.items():
        period = latest_periods.get(statement_name)
        value = _statement_value(frames.get(statement_name, pd.DataFrame()), aliases, period)
        if value is None:
            continue
        values[metric_name] = value
        metrics.append(_metric(metric_name, label, value, unit, period))

    cash_flow = values.get("operating_cash_flow")
    capex = values.get("capital_expenditure")
    profit = values.get("net_profit_after_tax")
    operating_profit = values.get("operating_profit")
    interest_expense = values.get("interest_expense")
    cash = values.get("cash_and_equivalents")
    short_debt = values.get("short_term_debt")
    long_debt = values.get("long_term_debt")
    equity = values.get("owners_equity")
    assets = values.get("total_assets")
    receivables = values.get("accounts_receivable")

    cash_period = latest_periods.get("cash_flow")
    balance_period = latest_periods.get("balance_sheet")
    income_period = latest_periods.get("income_statement")
    if cash_flow is not None and capex is not None:
        metrics.append(
            _metric(
                "free_cash_flow",
                "Dòng tiền tự do (CFO - CAPEX)",
                cash_flow - abs(capex),
                "money",
                cash_period,
            )
        )
    if cash_flow is not None and profit not in (None, 0):
        metrics.append(
            _metric(
                "cash_conversion",
                "CFO / Lợi nhuận sau thuế",
                cash_flow / profit,
                "number",
                cash_period or income_period,
            )
        )
    if cash is not None and short_debt is not None and long_debt is not None:
        metrics.append(
            _metric(
                "net_debt",
                "Nợ vay ròng",
                short_debt + long_debt - cash,
                "money",
                balance_period,
            )
        )
    if equity not in (None, 0) and short_debt is not None and long_debt is not None:
        metrics.append(
            _metric(
                "debt_to_equity_statement",
                "Nợ vay / Vốn chủ sở hữu",
                (short_debt + long_debt) / equity,
                "number",
                balance_period,
            )
        )
    if assets not in (None, 0) and receivables is not None:
        metrics.append(
            _metric(
                "receivables_to_assets",
                "Phải thu / Tổng tài sản",
                receivables / assets,
                "percent",
                balance_period,
            )
        )
    if operating_profit is not None and interest_expense not in (None, 0):
        metrics.append(
            _metric(
                "interest_coverage",
                "Khả năng trả lãi (EBIT / lãi vay)",
                operating_profit / abs(interest_expense),
                "number",
                income_period,
            )
        )

    balance_check = None
    liabilities = values.get("total_liabilities")
    if assets not in (None, 0) and liabilities is not None and equity is not None:
        balance_check = abs(assets - liabilities - equity) / abs(assets)
    quality = {
        "statement_periods": statement_periods,
        "latest_periods": latest_periods,
        "balance_check_relative_error": balance_check,
        "available_at_status": "unverified_publication_time",
        "note": (
            "Dữ liệu BCTC hiện được lưu theo thời điểm lấy; chưa có lịch sử "
            "thời điểm công bố chính thức nên chưa được đưa vào model/backtest."
        ),
    }
    return metrics, quality


def fundamental_assessment(fundamentals: dict) -> list[str]:
    metrics = {
        item["metric_name"]: item["metric_value"]
        for item in fundamentals.get("metrics", [])
    }
    notes: list[str] = []
    pe = metrics.get("pe")
    pb = metrics.get("pb")
    roe = metrics.get("roe")
    roa = metrics.get("roa")
    debt_to_equity = metrics.get("debtToEquity")
    current_ratio = metrics.get("currentRatio")
    npl = metrics.get("npl")
    revenue_growth = metrics.get("revenue_growth")
    profit_growth = metrics.get("profit_growth")
    cash_conversion = metrics.get("cash_conversion")
    free_cash_flow = metrics.get("free_cash_flow")
    net_debt = metrics.get("net_debt")
    interest_coverage = metrics.get("interest_coverage")

    if pe is not None:
        if pe <= 10:
            notes.append(f"P/E {pe:.2f}: định giá tương đối thấp nếu lợi nhuận bền vững.")
        elif pe >= 20:
            notes.append(f"P/E {pe:.2f}: định giá cao, cần tăng trưởng lợi nhuận hỗ trợ.")
        else:
            notes.append(f"P/E {pe:.2f}: cần so sánh thêm với doanh nghiệp cùng ngành.")
    if pb is not None:
        notes.append(f"P/B {pb:.2f}: nên đọc cùng ROE và đặc thù ngành.")
    if roe is not None:
        if roe >= 0.15:
            notes.append(f"ROE {roe:.1%}: hiệu quả vốn chủ sở hữu tốt.")
        elif roe <= 0.08:
            notes.append(f"ROE {roe:.1%}: hiệu quả vốn còn yếu.")
    if roa is not None and roa >= 0.02:
        notes.append(f"ROA {roa:.1%}: khá tốt, đặc biệt với nhóm ngân hàng.")
    if debt_to_equity is not None and debt_to_equity > 2:
        notes.append(f"Debt/Equity {debt_to_equity:.2f}: đòn bẩy cao, cần đọc theo ngành.")
    if current_ratio is not None and current_ratio > 0:
        status = "khá" if current_ratio >= 1 else "cần theo dõi"
        notes.append(f"Current ratio {current_ratio:.2f}: thanh khoản ngắn hạn {status}.")
    if npl is not None and npl > 0:
        status = "đang ở mức kiểm soát" if npl <= 0.02 else "cần theo dõi"
        notes.append(f"NPL {npl:.1%}: {status}.")
    if revenue_growth is not None:
        notes.append(f"Revenue Growth {revenue_growth:.1%} YoY.")
    if profit_growth is not None:
        notes.append(f"Profit Growth {profit_growth:.1%} YoY.")
    if cash_conversion is not None:
        if cash_conversion < 0.8:
            notes.append(
                f"CFO/LNST {cash_conversion:.2f}: dòng tiền chưa theo kịp lợi nhuận, cần đọc thêm biến động vốn lưu động."
            )
        else:
            notes.append(f"CFO/LNST {cash_conversion:.2f}: chất lượng chuyển đổi lợi nhuận sang tiền mặt khá tốt.")
    if free_cash_flow is not None:
        status = "dương" if free_cash_flow >= 0 else "âm"
        notes.append(f"Dòng tiền tự do quý gần nhất {status}; cần xem xu hướng nhiều quý và đặc thù ngành.")
    if net_debt is not None:
        status = "nợ vay ròng" if net_debt > 0 else "tiền mặt ròng"
        notes.append(f"Cấu trúc vốn hiện là {status}; không dùng một mình để kết luận rủi ro.")
    if interest_coverage is not None and interest_coverage < 2:
        notes.append(f"Khả năng trả lãi {interest_coverage:.2f} lần: cần theo dõi áp lực lãi vay.")
    if not notes and not fundamentals.get("available"):
        notes.append("Chưa lấy được dữ liệu cơ bản từ nguồn dữ liệu.")
    return notes
