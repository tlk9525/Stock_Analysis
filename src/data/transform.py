from __future__ import annotations

import pandas as pd


REQUIRED_PRICE_COLUMNS = ["open", "high", "low", "close", "volume"]


def clean_history(raw: pd.DataFrame, symbol: str) -> pd.DataFrame:
    if raw.empty or "time" not in raw.columns:
        raise ValueError(f"Khong lay duoc du lieu cho ma {symbol}.")

    frame = raw.copy()
    frame["time"] = pd.to_datetime(frame["time"]).dt.tz_localize(None)
    frame = frame.sort_values("time").drop_duplicates("time").set_index("time")
    frame = frame.rename(columns={column: column.lower() for column in frame.columns})

    missing = [column for column in REQUIRED_PRICE_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Du lieu {symbol} thieu cot: {', '.join(missing)}")

    for column in REQUIRED_PRICE_COLUMNS:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")

    cleaned = frame.dropna(subset=REQUIRED_PRICE_COLUMNS)
    if cleaned.empty:
        raise ValueError(f"Khong co dong gia hop le cho ma {symbol}.")
    return cleaned

