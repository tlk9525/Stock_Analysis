from __future__ import annotations

import pandas as pd
from pandas.tseries.offsets import CustomBusinessDay


# Lịch nghỉ giao dịch/thanh toán Việt Nam đã được công bố cho năm 2026.
# Lưu ý: ngày làm bù Thứ Bảy không được coi là phiên giao dịch chứng khoán cơ sở.
DEFAULT_VN_MARKET_HOLIDAYS = [
    "2026-01-01",
    "2026-01-02",
    "2026-02-16",
    "2026-02-17",
    "2026-02-18",
    "2026-02-19",
    "2026-02-20",
    "2026-04-27",
    "2026-04-30",
    "2026-05-01",
    "2026-08-31",
    "2026-09-01",
    "2026-09-02",
]

DEFAULT_MARKET_CALENDAR_NOTE = (
    "VN stock calendar: loại Thứ Bảy/Chủ Nhật và các ngày nghỉ 2026 đã công bố; "
    "ngày làm bù Thứ Bảy không được tính là phiên giao dịch chứng khoán."
)


def market_holidays(config: dict) -> list[str]:
    configured = [str(value) for value in config.get("market_holidays", []) or []]
    values = sorted({*DEFAULT_VN_MARKET_HOLIDAYS, *configured})
    return [str(pd.Timestamp(value).date()) for value in values]


def market_calendar_note(config: dict) -> str:
    return str(config.get("market_calendar_note") or DEFAULT_MARKET_CALENDAR_NOTE)


def build_market_calendar(config: dict) -> CustomBusinessDay:
    return CustomBusinessDay(
        weekmask=str(config.get("market_weekmask", "Mon Tue Wed Thu Fri")),
        holidays=pd.to_datetime(market_holidays(config)),
    )
