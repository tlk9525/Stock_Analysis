from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import pandas as pd


UNIVERSE_COLUMNS = [
    "symbol",
    "organ_name",
    "exchange",
    "sector",
    "listed_at",
    "delisted_at",
    "available_at",
    "source",
    "status",
]


def normalize_universe_registry(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize a point-in-time universe registry without inventing history."""

    if frame is None or frame.empty or "symbol" not in frame:
        raise ValueError("Universe registry phải có ít nhất một cột symbol.")
    out = frame.copy()
    out["symbol"] = out["symbol"].astype(str).str.strip().str.upper()
    out = out[out["symbol"].str.fullmatch(r"[A-Z0-9]{2,10}", na=False)]
    for column in UNIVERSE_COLUMNS:
        if column not in out:
            out[column] = pd.NA
    for column in ("listed_at", "delisted_at", "available_at"):
        out[column] = pd.to_datetime(out[column], errors="coerce", utc=True)
    out["exchange"] = out["exchange"].astype("string").str.upper()
    out["sector"] = out["sector"].astype("string")
    out["status"] = out["status"].fillna("active").astype(str).str.lower()
    out["source"] = out["source"].fillna("unknown").astype(str).str.upper()
    return (
        out[UNIVERSE_COLUMNS]
        .drop_duplicates("symbol", keep="last")
        .sort_values("symbol")
        .reset_index(drop=True)
    )


def load_universe_registry(path: str | Path) -> pd.DataFrame:
    return normalize_universe_registry(pd.read_csv(path))


def point_in_time_symbols(
    registry: pd.DataFrame,
    as_of: str | pd.Timestamp,
    *,
    exchanges: Iterable[str] | None = None,
) -> list[str]:
    """Return only symbols known and listed at ``as_of``.

    Missing ``listed_at`` is allowed for a current snapshot, but missing
    ``available_at`` is not: it would make the point-in-time claim unauditable.
    """

    frame = normalize_universe_registry(registry)
    timestamp = pd.Timestamp(as_of)
    if timestamp.tzinfo is None:
        timestamp = timestamp.tz_localize("UTC")
    else:
        timestamp = timestamp.tz_convert("UTC")
    eligible = frame[frame["available_at"].notna() & (frame["available_at"] <= timestamp)]
    eligible = eligible[
        (eligible["listed_at"].isna() | (eligible["listed_at"] <= timestamp))
        & (eligible["delisted_at"].isna() | (eligible["delisted_at"] > timestamp))
    ]
    if exchanges:
        allowed = {str(value).strip().upper() for value in exchanges}
        eligible = eligible[eligible["exchange"].isin(allowed)]
    return eligible["symbol"].tolist()


def apply_point_in_time_eligibility(
    panel: pd.DataFrame,
    registry: pd.DataFrame,
    *,
    timezone_name: str = "Asia/Ho_Chi_Minh",
    close_hour: int = 15,
) -> pd.DataFrame:
    """Remove rows where the symbol was not yet known/listed on that date."""

    if not isinstance(panel.index, pd.MultiIndex) or not {"date", "symbol"}.issubset(
        panel.index.names
    ):
        raise ValueError("panel phải có MultiIndex (date, symbol).")
    frame = panel.reset_index()
    meta = normalize_universe_registry(registry)[
        ["symbol", "listed_at", "delisted_at", "available_at"]
    ]
    frame = frame.merge(meta, on="symbol", how="left", suffixes=("", "_registry"))
    signal_cutoff = (
        pd.to_datetime(frame["date"]).dt.tz_localize(timezone_name)
        + pd.Timedelta(hours=close_hour)
    ).dt.tz_convert("UTC")
    listed = frame["listed_at_registry"] if "listed_at_registry" in frame else frame["listed_at"]
    delisted = frame["delisted_at_registry"] if "delisted_at_registry" in frame else frame["delisted_at"]
    available = frame["available_at_registry"] if "available_at_registry" in frame else frame["available_at"]
    mask = (
        available.notna()
        & (available <= signal_cutoff)
        & (listed.isna() | (listed <= signal_cutoff))
        & (delisted.isna() | (delisted > signal_cutoff))
    )
    out = frame.loc[mask].drop(
        columns=[column for column in frame if column.endswith("_registry")],
        errors="ignore",
    )
    result = out.set_index(["date", "symbol"]).sort_index()
    result.attrs = panel.attrs.copy()
    result.attrs["point_in_time_rows_removed"] = int(len(frame) - len(result))
    return result


def discover_current_universe(
    *,
    source: str = "VCI",
    exchanges: Iterable[str] = ("HOSE", "HNX", "UPCOM"),
    observed_at: datetime | None = None,
) -> tuple[pd.DataFrame, dict]:
    """Discover the provider's current equity snapshot.

    This does not pretend to reconstruct delisted constituents. The returned
    metadata explicitly marks survivorship completeness as false.
    """

    from vnstock import Listing

    listing = Listing(source=source, show_log=False)
    snapshot = listing.symbols_by_exchange(show_log=False)
    if not isinstance(snapshot, pd.DataFrame) or snapshot.empty:
        raise RuntimeError("Provider không trả về danh sách mã hiện tại.")
    now = observed_at or datetime.now(timezone.utc)
    snapshot = snapshot.copy()
    if "type" in snapshot:
        snapshot = snapshot[snapshot["type"].astype(str).str.upper().eq("STOCK")]
    snapshot["exchange"] = snapshot.get("exchange", pd.Series(index=snapshot.index, dtype="object")).replace(
        {"HSX": "HOSE"}
    )
    if "icb_code2" in snapshot:
        snapshot["sector"] = snapshot["icb_code2"].astype("string")
    snapshot["available_at"] = pd.Timestamp(now)
    snapshot["source"] = source
    snapshot["status"] = "active"

    registry = normalize_universe_registry(snapshot)
    allowed = {str(value).upper() for value in exchanges}
    if registry["exchange"].notna().any():
        registry = registry[registry["exchange"].isin(allowed)].reset_index(drop=True)
    metadata = {
        "mode": "current_snapshot",
        "source": source.upper(),
        "observed_at": pd.Timestamp(now).isoformat(),
        "symbols": int(len(registry)),
        "survivorship_complete": False,
        "point_in_time_complete": False,
        "warning": "Current listing snapshot excludes unknown delisted history; not production PIT universe.",
    }
    return registry, metadata
