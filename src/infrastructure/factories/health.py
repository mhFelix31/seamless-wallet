from src.application.ports.health import HealthCheck
from src.infrastructure.cache.in_memory import InMemoryHealthCheck
from src.infrastructure.cache.redis import RedisHealthCheck
from src.infrastructure.db.sqlalchemy.health import SQLAlchemyHealthCheck


def build_db_health(db_type, db_engine) -> HealthCheck:

    match db_type:
        case "sqlalchemy":
            return SQLAlchemyHealthCheck(db_engine)
        case _:
            raise NotImplementedError


def build_cache_health(cache_type, cache_client) -> HealthCheck:
    match cache_type:
        case "redis":
            return RedisHealthCheck(cache_client)
        case "in_memory":
            return InMemoryHealthCheck()
        case _:
            raise NotImplementedError
