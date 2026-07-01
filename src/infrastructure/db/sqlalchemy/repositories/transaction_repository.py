from datetime import datetime

from domain.transaction.entities import Transaction
from domain.transaction.repository import TransactionRepository
from domain.wallet.entities import Wallet, WalletSnapshot


class SQLAlchemyTransactionRepository(TransactionRepository):
    def __init__(self, session):
        self.session = session

    def save(self, txn: Transaction) -> Transaction: ...

    def get_by_wallet(
        self,
        wallet: Wallet,
        start_datetime: datetime | None,
        end_datetime: datetime | None,
    ) -> list[Transaction]: ...

    def get_all_after_snapshot(self, snapshot: WalletSnapshot) -> list[Transaction]: ...
