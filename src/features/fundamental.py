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

    if pe is not None:
        if pe <= 10:
            notes.append(f"P/E {pe:.2f}: dinh gia tuong doi thap neu loi nhuan ben vung.")
        elif pe >= 20:
            notes.append(f"P/E {pe:.2f}: dinh gia cao, can tang truong loi nhuan ho tro.")
        else:
            notes.append(f"P/E {pe:.2f}: can so sanh them voi doanh nghiep cung nganh.")
    if pb is not None:
        notes.append(f"P/B {pb:.2f}: nen doc cung ROE va dac thu nganh.")
    if roe is not None:
        if roe >= 0.15:
            notes.append(f"ROE {roe:.1%}: hieu qua von chu so huu tot.")
        elif roe <= 0.08:
            notes.append(f"ROE {roe:.1%}: hieu qua von con yeu.")
    if roa is not None and roa >= 0.02:
        notes.append(f"ROA {roa:.1%}: kha tot, dac biet voi nhom ngan hang.")
    if debt_to_equity is not None and debt_to_equity > 2:
        notes.append(f"Debt/Equity {debt_to_equity:.2f}: don bay cao, can doc theo nganh.")
    if current_ratio is not None and current_ratio > 0:
        status = "kha" if current_ratio >= 1 else "can theo doi"
        notes.append(f"Current ratio {current_ratio:.2f}: thanh khoan ngan han {status}.")
    if npl is not None and npl > 0:
        status = "dang o muc kiem soat" if npl <= 0.02 else "can theo doi"
        notes.append(f"NPL {npl:.1%}: {status}.")
    if revenue_growth is not None:
        notes.append(f"Revenue Growth {revenue_growth:.1%} YoY.")
    if profit_growth is not None:
        notes.append(f"Profit Growth {profit_growth:.1%} YoY.")
    if not notes and not fundamentals.get("available"):
        notes.append("Chua lay duoc du lieu co ban tu nguon du lieu.")
    return notes
