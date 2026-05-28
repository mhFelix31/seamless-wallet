from src.application.ports.cache import Cache
from src.application.ports.health import HealthCheck


class InMemoryCache(Cache):
    def __init__(self):
        self.store = {}

    async def get(self, key: str):
        return self.store.get(key)

    async def set(self, key: str, value: str, ttl=None):
        self.store[key] = value


class InMemoryHealthCheck(HealthCheck):
    async def is_healthy(self) -> bool:
        return True
