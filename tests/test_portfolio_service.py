from __future__ import annotations

from decimal import Decimal

import pytest

from src.portfolio.service import LedgerTransaction, replay_ledger


def test_replay_ledger_uses_moving_average_cost_and_fees() -> None:
    positions = replay_ledger(
        [
            LedgerTransaction("FPT", "VN", "VND", "BUY", Decimal("100"), Decimal("100"), Decimal("10")),
            LedgerTransaction("FPT", "VN", "VND", "BUY", Decimal("100"), Decimal("120"), Decimal("10")),
            LedgerTransaction("FPT", "VN", "VND", "SELL", Decimal("50"), Decimal("130"), Decimal("5")),
        ]
    )

    position = positions[("FPT", "VN", "VND")]
    assert position["quantity"] == Decimal("150")
    assert position["average_cost"] == Decimal("110.1")
    assert position["realized_pnl"] == Decimal("990.0")


def test_replay_ledger_rejects_sell_above_position() -> None:
    with pytest.raises(ValueError, match="Không thể bán"):
        replay_ledger(
            [LedgerTransaction("FPT", "VN", "VND", "SELL", Decimal("1"), Decimal("100"), Decimal("0"))]
        )
