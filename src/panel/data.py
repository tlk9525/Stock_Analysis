from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from datetime import date
from pathlib import Path

import pandas as pd

from src.data.transform import clean_history


PriceFetcher = Callable[[str, str, str, str], pd.DataFrame]


def normalize_price_frame(frame: pd.DataFrame, symbol: str) -> pd.DataFrame:
    """Return a clean OHLCV frame with a timezone-naive DatetimeIndex.

    Injected test frames commonly already use a DatetimeIndex, while vnstock
    returns a ``time`` column.  Converting both shapes through ``clean_history``
    keeps panel and single-symbol validation consistent.
    """

    raw = frame.copy()
    if "time" not in raw.columns:
        if not isinstance(raw.index, pd.DatetimeIndex):
            raise ValueError(
                f"Dữ liệu {symbol} phải có cột time hoặc DatetimeIndex."
            )
        index_name = raw.index.name or "index"
        raw = raw.reset_index().rename(columns={index_name: "time"})
    return clean_history(raw, symbol)


def _default_fetcher(
    symbol: str,
    start_date: str,
    end_date: str,
    source: str,
) -> pd.DataFrame:
    from vnstock import Quote

    quote = Quote(symbol=symbol, source=source)
    return quote.history(start=start_date, end=end_date, interval="d")


def fetch_price_frames(
    symbols: Sequence[str],
    benchmark_symbol: str = "VNINDEX",
    *,
    start_date: str = "2015-01-01",
    end_date: str | None = None,
    source: str = "VCI",
    frames: Mapping[str, pd.DataFrame] | None = None,
    fetcher: PriceFetcher | None = None,
    cache_dir: str | Path | None = None,
    continue_on_error: bool = False,
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    """Load multiple stocks and one benchmark.

    ``frames`` is the deterministic injection point for tests/offline jobs.  A
    custom ``fetcher`` can be supplied by a cache or another licensed provider;
    it receives ``(symbol, start_date, end_date, source)``.
    """

    normalized_symbols = list(
        dict.fromkeys(
            str(symbol).strip().upper()
            for symbol in symbols
            if str(symbol).strip()
        )
    )
    benchmark = benchmark_symbol.strip().upper()
    normalized_symbols = [symbol for symbol in normalized_symbols if symbol != benchmark]
    if not normalized_symbols:
        raise ValueError("Cần ít nhất một mã cổ phiếu khác benchmark.")

    end = end_date or str(date.today())
    loader = fetcher or _default_fetcher
    injected = {str(key).strip().upper(): value for key, value in (frames or {}).items()}

    cache_path = Path(cache_dir) if cache_dir else None
    if cache_path:
        cache_path.mkdir(parents=True, exist_ok=True)

    def load(symbol: str) -> pd.DataFrame:
        if symbol in injected:
            raw = injected[symbol]
        elif frames is not None:
            raise ValueError(f"Không có frame inject cho mã {symbol}.")
        else:
            symbol_cache = cache_path / f"{symbol}.csv" if cache_path else None
            if symbol_cache is not None and symbol_cache.exists():
                raw = pd.read_csv(symbol_cache)
            else:
                raw = loader(symbol, start_date, end, source)
                if symbol_cache is not None and raw is not None and not raw.empty:
                    raw.to_csv(symbol_cache, index=False)
        return normalize_price_frame(raw, symbol)

    stock_frames: dict[str, pd.DataFrame] = {}
    failures: dict[str, str] = {}
    for symbol in normalized_symbols:
        try:
            stock_frames[symbol] = load(symbol)
        except Exception as exc:
            if not continue_on_error:
                raise
            failures[symbol] = f"{type(exc).__name__}: {exc}"
    if not stock_frames:
        raise ValueError("Không tải được dữ liệu của mã cổ phiếu nào.")
    benchmark_frame = load(benchmark)
    for frame in stock_frames.values():
        frame.attrs["universe_fetch_failures"] = failures
    return stock_frames, benchmark_frame


def assemble_price_panel(
    stock_frames: Mapping[str, pd.DataFrame],
    benchmark_frame: pd.DataFrame,
    benchmark_symbol: str = "VNINDEX",
    universe_registry: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Assemble stock OHLCV and aligned benchmark OHLCV into a long panel.

    The returned index is ``(date, symbol)``.  Benchmark columns have a
    ``market_`` prefix and are joined only on dates for which benchmark data is
    available, preventing accidental forward/back filling.
    """

    if not stock_frames:
        raise ValueError("Không có dữ liệu cổ phiếu để tạo panel.")

    parts: list[pd.DataFrame] = []
    quality_by_symbol: dict[str, dict] = {}
    for raw_symbol, raw_frame in stock_frames.items():
        symbol = str(raw_symbol).strip().upper()
        original_report = raw_frame.attrs.get("data_quality_report")
        frame = normalize_price_frame(raw_frame, symbol)
        quality_by_symbol[symbol] = original_report or frame.attrs.get(
            "data_quality_report", {}
        )
        frame = frame.copy()
        frame["symbol"] = symbol
        frame.index.name = "date"
        parts.append(frame.reset_index())

    stocks = pd.concat(parts, ignore_index=True)
    stocks = stocks.sort_values(["date", "symbol"]).drop_duplicates(
        ["date", "symbol"], keep="last"
    )

    benchmark_name = benchmark_symbol.strip().upper()
    benchmark_report = benchmark_frame.attrs.get("data_quality_report")
    market = normalize_price_frame(benchmark_frame, benchmark_name).copy()
    benchmark_report = benchmark_report or market.attrs.get(
        "data_quality_report", {}
    )
    market.index.name = "date"
    market = market.rename(
        columns={
            "open": "market_open",
            "high": "market_high",
            "low": "market_low",
            "close": "market_close",
            "volume": "market_volume",
        }
    )
    market_columns = [
        "market_open",
        "market_high",
        "market_low",
        "market_close",
        "market_volume",
    ]
    panel = stocks.merge(
        market[market_columns].reset_index(),
        on="date",
        how="inner",
        validate="many_to_one",
    )
    if panel.empty:
        raise ValueError("Cổ phiếu và benchmark không có ngày giao dịch trùng nhau.")

    panel["benchmark_symbol"] = benchmark_name
    if universe_registry is not None and not universe_registry.empty:
        metadata = universe_registry.copy()
        metadata["symbol"] = metadata["symbol"].astype(str).str.upper().str.strip()
        keep = [
            column
            for column in (
                "symbol",
                "exchange",
                "sector",
                "listed_at",
                "delisted_at",
                "available_at",
            )
            if column in metadata
        ]
        panel = panel.merge(
            metadata[keep].drop_duplicates("symbol", keep="last"),
            on="symbol",
            how="left",
            validate="many_to_one",
        )
    result = panel.set_index(["date", "symbol"]).sort_index()
    reports = [*quality_by_symbol.values(), benchmark_report]
    result.attrs["data_quality_report"] = {
        "stocks": quality_by_symbol,
        "benchmark": benchmark_report,
        "source_rows": int(sum(item.get("source_rows", 0) for item in reports)),
        "cleaned_rows": int(sum(item.get("cleaned_rows", 0) for item in reports)),
        "quarantined_rows": int(
            sum(item.get("quarantined_rows", 0) for item in reports)
        ),
        "aligned_panel_rows": int(len(result)),
        "universe_fetch_failures": next(
            (
                frame.attrs.get("universe_fetch_failures", {})
                for frame in stock_frames.values()
                if frame.attrs.get("universe_fetch_failures")
            ),
            {},
        ),
    }
    return result


def load_price_panel(
    symbols: Sequence[str],
    benchmark_symbol: str = "VNINDEX",
    **kwargs,
) -> pd.DataFrame:
    """Fetch and assemble a panel in one call, convenient for ``panel_main``."""

    universe_registry = kwargs.pop("universe_registry", None)
    stock_frames, benchmark_frame = fetch_price_frames(
        symbols,
        benchmark_symbol,
        **kwargs,
    )
    return assemble_price_panel(
        stock_frames,
        benchmark_frame,
        benchmark_symbol,
        universe_registry=universe_registry,
    )
