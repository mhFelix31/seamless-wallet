from typing import Protocol


class HealthCheck(Protocol):
    async def is_healthy(self) -> bool: ...