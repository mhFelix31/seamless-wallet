from uuid import UUID
from src.domain.wallet.repository import WalletRepository
from src.domain.wallet.entities import Wallet
from src.infrastructure.db.models.wallet_model import WalletModel

class SQLAlchemyWalletRepository(WalletRepository):
    def __init__(self, session):
        self.session = session

    def get(self, session, id: UUID) -> Wallet:
        model = session.query(WalletModel).get(id)
        return self._to_domain(model)

    def save(self, wallet: Wallet) -> bool:
        # FIXME mock save
        try:
            self._to_model(wallet)
        except Exception:
            return False

        return True
        # END FIXME

    def _to_model(self, wallet:Wallet) ->  WalletModel:
        return WalletModel(
            uuid=str(wallet.uuid)
        )

    def _to_domain(self, model:WalletModel) -> Wallet:
        return Wallet(
            uuid=UUID(model.uuid),
            name=""
        )