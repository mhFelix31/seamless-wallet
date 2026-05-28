from typing import Protocol

from redis.asyncio.client import Redis

from src.application.ports.cache import Cache
from src.application.ports.health import HealthCheck


class RedisCache(Cache):
    def __init__(self, client: Redis):
        self.client = client

    async def get(self, key: str):
        return await self.client.get(key)

    async def set(self, key: str, value: str, ttl=None):
        await self.client.set(key, value, ex=ttl)


class AsyncCacheClient(Protocol):
    async def ping(self): ...


class RedisHealthCheck(HealthCheck):
    def __init__(self, client: AsyncCacheClient):
        self.client = client

    async def is_healthy(self) -> bool:
        try:
            return await self.client.ping()
        except Exception as ex:
            print(ex)
            return False
