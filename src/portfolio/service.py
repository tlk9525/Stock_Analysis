from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Iterable


PORTFOLIO_SCHEMA = """
CREATE TABLE IF NOT EXISTS portfolios (
    portfolio_id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    base_currency TEXT NOT NULL DEFAULT 'VND',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS portfolio_transactions (
    transaction_id BIGSERIAL PRIMARY KEY,
    portfolio_id BIGINT NOT NULL REFERENCES portfolios(portfolio_id) ON DELETE CASCADE,
    symbol TEXT NOT NULL,
    market TEXT NOT NULL DEFAULT 'VN',
    side TEXT NOT NULL CHECK (side IN ('BUY', 'SELL')),
    quantity NUMERIC(20, 6) NOT NULL CHECK (quantity > 0),
    price NUMERIC(20, 6) NOT NULL CHECK (price > 0),
    fee NUMERIC(20, 6) NOT NULL DEFAULT 0 CHECK (fee >= 0),
    currency TEXT NOT NULL DEFAULT 'VND',
    executed_at TIMESTAMPTZ NOT NULL,
    realized_pnl NUMERIC(20, 6),
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_portfolio_transactions_portfolio_time
    ON portfolio_transactions (portfolio_id, executed_at, transaction_id);
"""


@dataclass(frozen=True)
class LedgerTransaction:
    symbol: str
    market: str
    currency: str
    side: str
    quantity: Decimal
    price: Decimal
    fee: Decimal


def _decimal(value: object, field: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{field} phải là số hợp lệ.") from exc
    if not result.is_finite():
        raise ValueError(f"{field} phải là số hữu hạn.")
    return result


def _normalise_symbol(value: str) -> str:
    symbol = value.strip().upper()
    if not symbol:
        raise ValueError("Symbol không được để trống.")
    return symbol


def _normalise_code(value: str, field: str) -> str:
    result = value.strip().upper()
    if not result:
        raise ValueError(f"{field} không được để trống.")
    return result


def replay_ledger(transactions: Iterable[LedgerTransaction]) -> dict[tuple[str, str, str], dict]:
    """Calculate positions and realised P/L using a moving-average cost basis."""

    positions: dict[tuple[str, str, str], dict] = {}
    for transaction in transactions:
        key = (transaction.symbol, transaction.market, transaction.currency)
        position = positions.setdefault(
            key,
            {
                "symbol": transaction.symbol,
                "market": transaction.market,
                "currency": transaction.currency,
                "quantity": Decimal("0"),
                "cost_basis": Decimal("0"),
                "realized_pnl": Decimal("0"),
            },
        )
        if transaction.side == "BUY":
            position["quantity"] += transaction.quantity
            position["cost_basis"] += transaction.quantity * transaction.price + transaction.fee
            continue

        if transaction.side != "SELL":
            raise ValueError(f"Side không hợp lệ: {transaction.side}")
        if transaction.quantity > position["quantity"]:
            raise ValueError(
                f"Không thể bán {transaction.quantity} {transaction.symbol}; "
                f"chỉ đang có {position['quantity']}."
            )
        average_cost = position["cost_basis"] / position["quantity"]
        position["realized_pnl"] += (
            transaction.quantity * transaction.price
            - transaction.fee
            - transaction.quantity * average_cost
        )
        position["quantity"] -= transaction.quantity
        position["cost_basis"] -= transaction.quantity * average_cost
        if position["quantity"] == 0:
            position["cost_basis"] = Decimal("0")

    for position in positions.values():
        position["average_cost"] = (
            position["cost_basis"] / position["quantity"]
            if position["quantity"] > 0
            else Decimal("0")
        )
    return positions


def _database_url(database_url: str | None) -> str:
    return database_url or os.environ.get("DATABASE_URL") or "postgresql:///stock_db"


def _connect(database_url: str | None):
    try:
        import psycopg
    except ImportError as exc:
        raise RuntimeError("Thiếu psycopg. Hãy cài dependencies của project.") from exc
    return psycopg.connect(_database_url(database_url))


def _ensure_schema(connection) -> None:
    with connection.cursor() as cursor:
        cursor.execute(PORTFOLIO_SCHEMA)


def create_portfolio(name: str, base_currency: str = "VND", database_url: str | None = None) -> dict:
    clean_name = name.strip()
    if not clean_name:
        raise ValueError("Tên portfolio không được để trống.")
    currency = _normalise_code(base_currency, "base_currency")
    with _connect(database_url) as connection:
        _ensure_schema(connection)
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO portfolios (name, base_currency)
                VALUES (%s, %s)
                ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
                RETURNING portfolio_id, name, base_currency, created_at
                """,
                (clean_name, currency),
            )
            row = cursor.fetchone()
    return {"portfolio_id": row[0], "name": row[1], "base_currency": row[2], "created_at": row[3]}


def _portfolio_id(cursor, name: str) -> int:
    cursor.execute("SELECT portfolio_id FROM portfolios WHERE name = %s", (name,))
    row = cursor.fetchone()
    if row is None:
        raise ValueError(f"Không tìm thấy portfolio '{name}'. Hãy tạo trước.")
    return int(row[0])


def _load_transactions(cursor, portfolio_id: int) -> list[LedgerTransaction]:
    cursor.execute(
        """
        SELECT symbol, market, currency, side, quantity, price, fee
        FROM portfolio_transactions
        WHERE portfolio_id = %s
        ORDER BY executed_at, transaction_id
        """,
        (portfolio_id,),
    )
    return [LedgerTransaction(*row) for row in cursor.fetchall()]


def record_transaction(
    portfolio_name: str,
    *,
    side: str,
    symbol: str,
    quantity: object,
    price: object,
    fee: object = 0,
    market: str = "VN",
    currency: str = "VND",
    executed_at: datetime | None = None,
    notes: str | None = None,
    database_url: str | None = None,
) -> dict:
    trade_side = _normalise_code(side, "side")
    if trade_side not in {"BUY", "SELL"}:
        raise ValueError("side chỉ có thể là BUY hoặc SELL.")
    trade = LedgerTransaction(
        symbol=_normalise_symbol(symbol),
        market=_normalise_code(market, "market"),
        currency=_normalise_code(currency, "currency"),
        side=trade_side,
        quantity=_decimal(quantity, "quantity"),
        price=_decimal(price, "price"),
        fee=_decimal(fee, "fee"),
    )
    if trade.quantity <= 0 or trade.price <= 0 or trade.fee < 0:
        raise ValueError("quantity và price phải > 0; fee phải >= 0.")
    timestamp = executed_at or datetime.now().astimezone()

    with _connect(database_url) as connection:
        _ensure_schema(connection)
        with connection.cursor() as cursor:
            portfolio_id = _portfolio_id(cursor, portfolio_name)
            prior = _load_transactions(cursor, portfolio_id)
            replay_ledger([*prior, trade])
            prior_positions = replay_ledger(prior)
            key = (trade.symbol, trade.market, trade.currency)
            realized_pnl = None
            if trade.side == "SELL":
                position = prior_positions.get(key)
                if position is None or position["quantity"] < trade.quantity:
                    available = Decimal("0") if position is None else position["quantity"]
                    raise ValueError(
                        f"Không thể bán {trade.quantity} {trade.symbol}; chỉ đang có {available}."
                    )
                realized_pnl = (
                    trade.quantity * trade.price
                    - trade.fee
                    - trade.quantity * position["average_cost"]
                )
            cursor.execute(
                """
                INSERT INTO portfolio_transactions (
                    portfolio_id, symbol, market, side, quantity, price, fee,
                    currency, executed_at, realized_pnl, notes
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING transaction_id, realized_pnl
                """,
                (
                    portfolio_id, trade.symbol, trade.market, trade.side, trade.quantity,
                    trade.price, trade.fee, trade.currency, timestamp, realized_pnl, notes,
                ),
            )
            row = cursor.fetchone()
    return {"transaction_id": row[0], "realized_pnl": row[1], "side": trade.side, "symbol": trade.symbol}


def portfolio_summary(name: str, database_url: str | None = None) -> dict:
    with _connect(database_url) as connection:
        _ensure_schema(connection)
        with connection.cursor() as cursor:
            portfolio_id = _portfolio_id(cursor, name)
            transactions = _load_transactions(cursor, portfolio_id)
    positions = replay_ledger(transactions)
    active = [position for position in positions.values() if position["quantity"] > 0]
    realized = sum((position["realized_pnl"] for position in positions.values()), Decimal("0"))
    return {
        "name": name,
        "transaction_count": len(transactions),
        "realized_pnl": realized,
        "positions": sorted(active, key=lambda item: (item["market"], item["symbol"])),
    }
