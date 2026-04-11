
from sqlalchemy.ext.asyncio import (create_async_engine, async_sessionmaker, AsyncSession)
def create_engine_and_session(db_url: str):
    engine = create_async_engine(
        db_url,
        pool_pre_ping=True,
    )
    session_factory = async_sessionmaker[AsyncSession](
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
    )
    return engine, session_factory