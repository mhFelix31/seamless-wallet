from fastapi import FastAPI
import redis.asyncio as redis

from src.infrastructure.cache.in_memory import InMemoryCache
from src.infrastructure.db.session import create_engine_and_session

# TODO maybe split in two files? shutdown.py and start_up.py ???

def db_startup(app: FastAPI, db_type: str, db_url: str):
    match(db_type):
        case "postgres":
            engine, session_factory = create_engine_and_session(db_url)
            app.state.db_engine = engine
            app.state.session_factory = session_factory
        case _:
            raise NotImplementedError("DB type not supported yet.")


def cache_startup(app: FastAPI, cache_type: str, cache_url: str):
    match(cache_type):
        case "redis":
            redis_client = redis.from_url(cache_url)
            app.state.cache_client = redis_client
        case "memory":
            app.state.cache_client = InMemoryCache()
        case _:
            raise NotImplementedError("Cache type not supported yet.")



async def db_shutdown(app: FastAPI):
    if hasattr(app.state, "db_engine"):
        await app.state.db_engine.dispose()

async def cache_shutdown(app: FastAPI):
    if hasattr(app.state, "cache_client") and app.state.cache_client:
        await app.state.cache_client.close()