


from src.config import settings
from src.infrastructure.db.postgres.repositories.wallet_repository import SQLAlchemyWalletRepository


def build_wallet_repository(app):
    match settings.database_type:
        case "postgres":
            session_factory = app.state.session_factory
            session = session_factory()
            return SQLAlchemyWalletRepository(session)
        case _:
            raise NotImplementedError(f"Unsupported Database Type: {settings.database_type}")