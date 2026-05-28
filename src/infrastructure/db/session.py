from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


def create_engine_and_session(db_url: str):
    engine = create_engine(db_url=db_url)
    session_factory = create_session_factory(engine)
    return engine, session_factory


def create_engine(db_url: str):
    engine = create_async_engine(
        db_url,
        pool_pre_ping=True,
    )
    return engine


def create_session_factory(engine):
    session_factory = async_sessionmaker[AsyncSession](
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
    )
    return session_factory
