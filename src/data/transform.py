from __future__ import annotations

import math
from collections.abc import Mapping

import numpy as np
import pandas as pd


REQUIRED_PRICE_COLUMNS = ["open", "high", "low", "close", "volume"]
PRICE_COLUMNS = ["open", "high", "low", "close"]
ZERO_VOLUME_POLICY = "quarantine"


def _report_value(value: object) -> object:
    """Convert a pandas/numpy scalar to a JSON-friendly audit value."""
    if value is None or pd.isna(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, np.generic):
        value = value.item()
    if isinstance(value, float) and not math.isfinite(value):
        return str(value)
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _quarantine_record(
    row: Mapping,
    reasons: list[str],
    *,
    time_value: object | None = None,
) -> dict:
    if time_value is None:
        time_value = row.get("time")
    return {
        "time": _report_value(time_value),
        "reasons": reasons,
        "values": {
            column: _report_value(row.get(column))
            for column in REQUIRED_PRICE_COLUMNS
        },
    }


def clean_history(raw: pd.DataFrame, symbol: str) -> pd.DataFrame:
    if raw.empty:
        raise ValueError(f"Không lấy được dữ liệu cho mã {symbol}.")

    frame = raw.copy()
    frame = frame.rename(
        columns={column: str(column).lower() for column in frame.columns}
    )
    if "time" not in frame.columns:
        raise ValueError(f"Dữ liệu {symbol} thiếu cột: time")

    missing = [column for column in REQUIRED_PRICE_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Dữ liệu {symbol} thiếu cột: {', '.join(missing)}")

    source_rows = len(frame)
    quarantine: list[dict] = []

    raw_time = frame["time"].copy()
    frame["time"] = pd.to_datetime(
        frame["time"],
        errors="coerce",
        format="mixed",
    ).dt.tz_localize(None)
    invalid_time = frame["time"].isna()
    for row_position in np.flatnonzero(invalid_time.to_numpy()):
        quarantine.append(
            _quarantine_record(
                frame.iloc[row_position],
                ["invalid_time"],
                time_value=raw_time.iloc[row_position],
            )
        )
    frame = frame.loc[~invalid_time].copy()

    duplicate_time = frame.duplicated("time", keep="last")
    for _, row in frame.loc[duplicate_time].iterrows():
        quarantine.append(_quarantine_record(row, ["duplicate_time"]))
    frame = frame.loc[~duplicate_time].sort_values("time").set_index("time")

    for column in REQUIRED_PRICE_COLUMNS:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")

    finite_values = pd.DataFrame(
        np.isfinite(frame[REQUIRED_PRICE_COLUMNS].to_numpy(dtype=float)),
        index=frame.index,
        columns=REQUIRED_PRICE_COLUMNS,
    )
    reason_masks = {
        "missing_or_non_finite_ohlcv": ~finite_values.all(axis=1),
        "non_positive_price": (frame[PRICE_COLUMNS] <= 0).any(axis=1),
        "negative_volume": frame["volume"] < 0,
        "zero_volume": frame["volume"] == 0,
        "high_below_low": frame["high"] < frame["low"],
        "high_below_open_or_close": frame["high"]
        < frame[["open", "close"]].max(axis=1),
        "low_above_open_or_close": frame["low"]
        > frame[["open", "close"]].min(axis=1),
    }
    invalid_ohlcv = pd.Series(False, index=frame.index)
    for mask in reason_masks.values():
        invalid_ohlcv |= mask.fillna(False)

    for timestamp, row in frame.loc[invalid_ohlcv].iterrows():
        reasons = [
            reason
            for reason, mask in reason_masks.items()
            if bool(mask.loc[timestamp])
        ]
        quarantine.append(_quarantine_record(row, reasons, time_value=timestamp))

    cleaned = frame.loc[~invalid_ohlcv].copy()
    if cleaned.empty:
        raise ValueError(f"Không có dòng giá hợp lệ cho mã {symbol}.")

    reason_counts = {
        "invalid_time": int(invalid_time.sum()),
        "duplicate_time": int(duplicate_time.sum()),
        **{
            reason: int(mask.fillna(False).sum())
            for reason, mask in reason_masks.items()
        },
    }
    cleaned.attrs["data_quality_report"] = {
        "symbol": str(symbol).upper(),
        "source_rows": int(source_rows),
        "cleaned_rows": int(len(cleaned)),
        "quarantined_rows": int(len(quarantine)),
        "zero_volume_policy": ZERO_VOLUME_POLICY,
        "reason_counts": reason_counts,
        "quarantine": quarantine,
    }
    return cleaned
