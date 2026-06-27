from src.infrastructure.db.postgres.repositories.user_repository import (
    SQLAlchemyUserRepository,
)
from src.infrastructure.db.postgres.repositories.wallet_repository import (
    SQLAlchemyWalletRepository,
)
from src.infrastructure.db.utils import SQL_ALCHEMY_DB_LIST


def build_wallet_repository(app):
    db_type = app.state.database_type
    match db_type:
        case _ if db_type in SQL_ALCHEMY_DB_LIST:
            session_factory = app.state.session_factory
            session = session_factory()
            return SQLAlchemyWalletRepository(session)
        case _:
            raise NotImplementedError(
                f"Unsupported Database Type: {app.state.database_type}"
            )


def build_user_repository(app):
    db_type = app.state.database_type
    match db_type:
        case _ if db_type in SQL_ALCHEMY_DB_LIST:
            session_factory = app.state.session_factory
            session = session_factory()
            return SQLAlchemyUserRepository(session)
        case _:
            raise NotImplementedError(
                f"Unsupported Database Type: {app.state.database_type}"
            )
