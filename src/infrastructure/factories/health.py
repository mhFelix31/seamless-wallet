

from src.application.ports.health import HealthCheck
from src.config import settings
from src.infrastructure.db.postgres.health import SQLAlchemyHealthCheck

from src.infrastructure.cache.redis import RedisHealthCheck
from src.infrastructure.cache.in_memory import InMemoryHealthCheck


def build_db_health(app) -> HealthCheck:
    engine = app.state.db_engine
    match settings.database_type:
        case "postgres":
            return SQLAlchemyHealthCheck(engine)
        case _:
            raise NotImplementedError

def build_cache_health(app) -> HealthCheck:
    cache_client = app.state.cache_client
    match settings.cache_type:
        case "redis":
            return RedisHealthCheck(cache_client)
        case "in_memory":
            return InMemoryHealthCheck()
        case _:
            raise NotImplementedError