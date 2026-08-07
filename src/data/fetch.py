from __future__ import annotations

from datetime import date

import pandas as pd

from src.data.transform import clean_history
from src.features.fundamental import (
    dataframe_first_record,
    fundamental_assessment,
    summarize_financial_statements,
    summarize_income_growth,
    summarize_ratios,
)


def fetch_history(config: dict) -> pd.DataFrame:
    from vnstock import Quote

    quote = Quote(symbol=config["symbol"], source=config["source"])
    raw = quote.history(
        start=config["start_date"],
        end=str(date.today()),
        interval="d",
    )
    return clean_history(raw, config["symbol"])


def fetch_fundamentals(config: dict) -> tuple[dict, dict[str, pd.DataFrame]]:
    symbol = config["symbol"]
    source = config.get("source", "VCI")
    result = {
        "available": False,
        "source": source,
        "symbol": symbol,
        "company": {},
        "metrics": [],
        "latest_period": None,
        "growth_period": None,
        "statement_quality": {},
        "notes": [],
    }
    frames: dict[str, pd.DataFrame] = {}

    try:
        from vnstock import Company

        overview = Company(source=source, symbol=symbol, show_log=False).overview()
        if not overview.empty:
            frames["company_overview"] = overview
            result["company"] = dataframe_first_record(overview)
            result["available"] = True
    except Exception as exc:
        result["notes"].append(f"Không lấy được overview: {exc}")

    finance = None
    try:
        from vnstock import Finance

        finance = Finance(
            source=source,
            symbol=symbol,
            period="quarter",
            get_all=True,
            show_log=False,
        )
    except Exception as exc:
        result["notes"].append(f"Không khởi tạo được Finance API: {exc}")

    if finance is not None:
        try:
            ratios = pd.DataFrame()
            provider = getattr(finance, "provider", None)
            if source.lower() == "vci" and provider is not None and hasattr(provider, "_get_report"):
                ratios = provider._get_report(
                    report_type="ratio",
                    mode="raw",
                    period="quarter",
                    limit=120,
                )
            if ratios.empty:
                ratios = finance.ratio(period="quarter", lang="en", dropna=True)
            if not ratios.empty:
                frames["financial_ratios"] = ratios
                result["metrics"], result["latest_period"] = summarize_ratios(ratios)
                result["available"] = True
        except Exception as exc:
            result["notes"].append(f"Không lấy được financial ratios: {exc}")

        try:
            income_statement = pd.DataFrame()
            provider = getattr(finance, "provider", None)
            if source.lower() == "vci" and provider is not None and hasattr(provider, "_get_report"):
                income_statement = provider._get_report(
                    report_type="income_statement",
                    mode="final",
                    lang="en",
                    get_all=True,
                    period="quarter",
                    limit=120,
                )
            if income_statement.empty:
                income_statement = finance.income_statement(
                    period="quarter",
                    lang="en",
                    dropna=True,
                )
            if not income_statement.empty:
                frames["income_statement"] = income_statement
                growth_metrics, growth_period = summarize_income_growth(income_statement)
                result["metrics"].extend(growth_metrics)
                result["growth_period"] = growth_period
                result["available"] = True
        except Exception as exc:
            result["notes"].append(f"Không lấy được income statement: {exc}")

        # Dùng public API thay vì provider private để balance sheet/cash flow
        # vẫn có fallback tương thích giữa các nguồn vnstock.
        for frame_name, method_name, label in [
            ("balance_sheet", "balance_sheet", "balance sheet"),
            ("cash_flow", "cash_flow", "cash flow"),
        ]:
            try:
                statement = getattr(finance, method_name)(
                    period="quarter",
                    lang="en",
                    dropna=True,
                )
                if not statement.empty:
                    frames[frame_name] = statement
                    result["available"] = True
            except Exception as exc:
                result["notes"].append(f"Không lấy được {label}: {exc}")

    statement_metrics, statement_quality = summarize_financial_statements(frames)
    result["metrics"].extend(statement_metrics)
    result["statement_quality"] = statement_quality
    if statement_quality:
        result["notes"].append(statement_quality["note"])

    result["assessment"] = fundamental_assessment(result)
    return result, frames
