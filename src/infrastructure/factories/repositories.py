from src.infrastructure.db.postgres.repositories.wallet_repository import (
    SQLAlchemyWalletRepository,
)
from src.infrastructure.db.postgres.repositories.user_repository import (
    SQLAlchemyUserRepository,
)


def build_wallet_repository(app):
    match app.state.database_type:
        case "postgres":
            session_factory = app.state.session_factory
            session = session_factory()
            return SQLAlchemyWalletRepository(session)
        case _:
            raise NotImplementedError(
                f"Unsupported Database Type: {app.state.database_type}"
            )


def build_user_repository(app):
    match app.state.database_type:
        case "postgres":
            session_factory = app.state.session_factory
            session = session_factory()
            return SQLAlchemyUserRepository(session)
        case _:
            raise NotImplementedError(
                f"Unsupported Database Type: {app.state.database_type}"
            )
