from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


FLOW_MODEL_FEATURES = [
    "foreign_net_value_1d",
    "foreign_net_value_ratio_20d",
    "foreign_net_value_z20",
]


def load_foreign_flow(path: str | Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    required = {"symbol", "date", "available_at", "foreign_buy_value", "foreign_sell_value"}
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"Foreign-flow CSV thiếu cột: {', '.join(missing)}")
    out = frame.copy()
    out["symbol"] = out["symbol"].astype(str).str.upper().str.strip()
    out["date"] = pd.to_datetime(out["date"], errors="coerce").dt.tz_localize(None)
    out["available_at"] = pd.to_datetime(out["available_at"], errors="coerce", utc=True)
    for column in ("foreign_buy_value", "foreign_sell_value"):
        out[column] = pd.to_numeric(out[column], errors="coerce")
    return out.dropna(subset=list(required)).sort_values(["symbol", "date", "available_at"])


def add_foreign_flow_features(
    featured_panel: pd.DataFrame,
    flows: pd.DataFrame,
    *,
    timezone: str = "Asia/Ho_Chi_Minh",
    close_hour: int = 15,
) -> pd.DataFrame:
    """Join daily foreign flow only when it was available by signal close."""

    if not isinstance(featured_panel.index, pd.MultiIndex):
        raise ValueError("featured_panel phải có MultiIndex (date, symbol).")
    out = featured_panel.reset_index().copy()
    flow = flows.copy()
    required = {"symbol", "date", "available_at", "foreign_buy_value", "foreign_sell_value"}
    missing = sorted(required - set(flow.columns))
    if missing:
        raise ValueError(f"Foreign-flow thiếu cột: {', '.join(missing)}")
    flow["symbol"] = flow["symbol"].astype(str).str.upper().str.strip()
    flow["date"] = pd.to_datetime(flow["date"], errors="coerce").dt.tz_localize(None)
    flow["available_at"] = pd.to_datetime(flow["available_at"], errors="coerce", utc=True)
    signal_cutoff = (
        pd.to_datetime(flow["date"]).dt.tz_localize(timezone)
        + pd.Timedelta(hours=close_hour)
    ).dt.tz_convert("UTC")
    flow = flow[flow["available_at"].notna() & (flow["available_at"] <= signal_cutoff)]
    flow = flow.sort_values("available_at").drop_duplicates(["date", "symbol"], keep="last")
    flow["foreign_net_value_1d"] = (
        pd.to_numeric(flow["foreign_buy_value"], errors="coerce")
        - pd.to_numeric(flow["foreign_sell_value"], errors="coerce")
    )
    out = out.merge(
        flow[["date", "symbol", "foreign_net_value_1d"]],
        on=["date", "symbol"],
        how="left",
        validate="one_to_one",
    )
    # Missing means unavailable, not neutral. These rows are excluded if flow
    # features are enabled in the model.
    grouped = out.sort_values(["symbol", "date"]).groupby("symbol", sort=False)
    median = grouped["foreign_net_value_1d"].transform(lambda value: value.rolling(20).median())
    std = grouped["foreign_net_value_1d"].transform(lambda value: value.rolling(20).std())
    out["foreign_net_value_ratio_20d"] = out["foreign_net_value_1d"] / median.abs().replace(0, np.nan)
    out["foreign_net_value_z20"] = (out["foreign_net_value_1d"] - median) / std.replace(0, np.nan)
    return out.set_index(["date", "symbol"]).sort_index()
