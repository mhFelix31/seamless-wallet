

from typing import Protocol
from uuid import UUID

from .entities import Transaction


class TransactionRepository(Protocol):
    def save(self, txn: Transaction) -> bool: ...

    def get_by_wallet(self, wallet_id: UUID) -> list[Transaction]: ...