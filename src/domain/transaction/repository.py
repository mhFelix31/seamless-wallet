from datetime import datetime
from typing import Protocol

from src.domain.wallet.entities import Wallet, WalletTransactionSnapshot

from .entities import Transaction


class TransactionRepository(Protocol):
    def save(self, txn: Transaction) -> Transaction: ...

    def get_by_wallet(
            self,
            wallet: Wallet,
            start_datetime:datetime|None,
            end_datetime:datetime|None
        ) -> list[Transaction]: ...
    
    def get_all_after_snapshot(self, snapshot:WalletTransactionSnapshot) -> list[Transaction]: ...
