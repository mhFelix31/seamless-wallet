
from domain.wallet.entities import WalletSnapshot
from domain.wallet.repository import WalletSnapshotRepository


class SQLAlchemyWalletSnapshotRepository(WalletSnapshotRepository):
    def __init__(self, session):
        self.session = session

    def get_by_wallet_id(self, wallet_id) -> list[WalletSnapshot]: ...
    def get_latest_by_wallet_id(self, wallet_id: str) -> WalletSnapshot: ...
