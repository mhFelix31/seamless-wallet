from src.config import settings
from src.infrastructure.db.sqlalchemy.repositories.currency_repository import (
    SQLAlchemyCurrencyRepository,
)
from src.infrastructure.db.sqlalchemy.repositories.transaction_repository import (
    SQLAlchemyTransactionRepository,
)
from src.infrastructure.db.sqlalchemy.repositories.wallet_repository import (
    SQLAlchemyWalletRepository,
)
from src.infrastructure.db.sqlalchemy.repositories.wallet_snapshot_repository import (
    SQLAlchemyWalletSnapshotRepository,
)
from src.infrastructure.db.utils import SQL_ALCHEMY_DB_LIST


def build_wallet_repository(app):
    db_type = app.state.db_type
    match db_type:
        case _ if db_type in SQL_ALCHEMY_DB_LIST:
            session_factory = app.state.session_factory
            session = session_factory()
            return SQLAlchemyWalletRepository(session)
        case _:
            raise NotImplementedError(
                f"Unsupported Database Type: {settings.database_type}"
            )


def build_currency_repository(app):
    db_type = app.state.db_type
    match db_type:
        case _ if db_type in SQL_ALCHEMY_DB_LIST:
            session_factory = app.state.session_factory
            session = session_factory()
            return SQLAlchemyCurrencyRepository(session)
        case _:
            raise NotImplementedError(
                f"Unsupported Database Type: {settings.database_type}"
            )


def build_transaction_repository(app):
    db_type = app.state.db_type
    match db_type:
        case _ if db_type in SQL_ALCHEMY_DB_LIST:
            session_factory = app.state.session_factory
            session = session_factory()
            return SQLAlchemyTransactionRepository(session)
        case _:
            raise NotImplementedError(
                f"Unsupported Database Type: {settings.database_type}"
            )


def build_wallet_snapshot_repository(app):
    db_type = app.state.db_type
    match db_type:
        case _ if db_type in SQL_ALCHEMY_DB_LIST:
            session_factory = app.state.session_factory
            session = session_factory()
            return SQLAlchemyWalletSnapshotRepository(session)
        case _:
            raise NotImplementedError(
                f"Unsupported Database Type: {settings.database_type}"
            )
