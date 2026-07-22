from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

import numpy as np
import pandas as pd


def safe_float(value, default: float | None = None) -> float | None:
    if value is None:
        return default
    try:
        if pd.isna(value):
            return default
    except TypeError:
        pass
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def resolve_price_multiplier(config: dict, default: float = 1000.0) -> float:
    backtest = config.get("backtest", {}) or {}
    raw_value = backtest.get("price_multiplier", config.get("price_multiplier", default))
    multiplier = float(raw_value)
    if multiplier <= 0:
        raise ValueError("price_multiplier phải lớn hơn 0.")
    return multiplier


def clean_json_value(value):
    if isinstance(value, dict):
        return {str(key): clean_json_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [clean_json_value(item) for item in value]
    if isinstance(value, tuple):
        return [clean_json_value(item) for item in value]
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        value = float(value)
    try:
        if pd.isna(value):
            return None
    except TypeError:
        pass
    return value


def write_json(path: Path, data: dict | list) -> None:
    path.write_text(
        json.dumps(clean_json_value(data), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
