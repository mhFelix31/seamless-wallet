from fastapi import Request

from src.config import settings
from src.application.ports.cache import Cache

from src.infrastructure.cache.redis import RedisCache

from src.infrastructure.factories.health import build_cache_health, build_db_health
from src.infrastructure.factories.repositories import build_wallet_repository

async def check_db(request: Request) -> str:
    health = build_db_health(request.app)
    return "ok" if await health.is_healthy() else "failed"
        

async def check_cache(request: Request) -> str:
    health = build_cache_health(request.app)
    return "ok" if await health.is_healthy() else "failed"

# --- Repository ---
def get_wallet_repository(request: Request):
    build_wallet_repository(app=request.app)

# --- Cache ---
def get_cache(request: Request) -> Cache:
    match(settings.cache_type):
        case "redis":
            return RedisCache(request.app.state.cache_client)
        case "memory":
            return request.app.state.cache_client
        case _:
            raise NotImplementedError