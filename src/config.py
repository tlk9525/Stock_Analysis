from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config.json"


def load_config() -> dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def normalize_symbol(symbol: str | None) -> str:
    if symbol is None:
        return ""
    return symbol.strip().upper()


def resolve_config(config: dict, args: argparse.Namespace) -> dict:
    selected_symbol = normalize_symbol(args.symbol_option or args.symbol or config.get("symbol"))

    if not selected_symbol and sys.stdin.isatty():
        selected_symbol = normalize_symbol(input("Nhập mã cổ phiếu, ví dụ HCM/FPT/VCB: "))

    if not selected_symbol:
        raise ValueError(
            "Chưa có mã cổ phiếu. Hãy chạy: ./run_now.sh HCM hoặc "
            "python3 -m src.main --once --symbol HCM"
        )

    resolved = config.copy()
    resolved["symbol"] = selected_symbol

    if args.source:
        resolved["source"] = args.source.strip().upper()
    if args.forecast_sessions:
        resolved["forecast_sessions"] = args.forecast_sessions
    if args.run_time:
        resolved["daily_run_time"] = args.run_time
    if args.database_url:
        resolved["database_url"] = args.database_url
    if args.no_postgres:
        resolved["save_to_postgres"] = False

    return resolved
