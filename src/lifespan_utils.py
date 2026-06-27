from contextlib import asynccontextmanager

import redis.asyncio as redis
from fastapi import FastAPI

from src.enums import CacheType
from src.infrastructure.auth.password_hasher.argon2_password_hasher import (
    Argon2PasswordHasher,
)
from src.infrastructure.auth.token_service.jwt_token_service import JWTTokenService
from src.infrastructure.cache.in_memory import InMemoryCache
from src.infrastructure.db.session import create_engine_and_session
from src.infrastructure.db.utils import SQL_ALCHEMY_DB_LIST


def db_startup(app: FastAPI, db_type: str, db_url: str):
    app.state.db_type = db_type

    match db_type:
        case _ if db_type in SQL_ALCHEMY_DB_LIST:
            engine, session_factory = create_engine_and_session(db_url)
            app.state.db_engine = engine
            app.state.session_factory = session_factory
        case _:
            raise NotImplementedError("DB type not supported yet.")


def cache_startup(app: FastAPI, cache_type: str, cache_url: str):
    app.state.cache_type = cache_type

    match cache_type:
        case CacheType.REDIS:
            redis_client = redis.from_url(cache_url)
            app.state.cache_client = redis_client
        case CacheType.IN_MEMORY:
            app.state.cache_client = InMemoryCache()
        case _:
            raise NotImplementedError("Cache type not supported yet.")


async def db_shutdown(app: FastAPI):
    if hasattr(app.state, "db_engine"):
        await app.state.db_engine.dispose()


async def cache_shutdown(app: FastAPI):
    if hasattr(app.state, "cache_client") and app.state.cache_client:
        if hasattr(app.state.cache_client, "close"):
            await app.state.cache_client.close()


def extra_configs_startup(app: FastAPI, settings) -> FastAPI:
    password_hasher = Argon2PasswordHasher(secret_pepper=settings.secret_pepper)
    token_service = JWTTokenService(
        priv_token_key=settings.secret_token, env_token_pub_list=[]
    )

    app.state.password_hasher = password_hasher
    app.state.token_service = token_service
    return app


def lifespan_factory(settings):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.env = settings.environment
        # Start up

        db_startup(
            app=app,
            db_type=settings.database_type,
            db_url=settings.database_url,
        )
        cache_startup(
            app=app,
            cache_type=settings.cache_type,
            cache_url=settings.cache_url,
        )
        app = extra_configs_startup(app=app, settings=settings)

        yield

        # Shutdown
        await db_shutdown(app=app)
        await cache_shutdown(app=app)

    return lifespan
