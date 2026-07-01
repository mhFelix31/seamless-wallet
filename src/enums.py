from enum import StrEnum


class DBtype(StrEnum):
    POSTGRES = "sqlalchemy"
    SQLITE = "sqlite"


class CacheType(StrEnum):
    REDIS = "redis"
    IN_MEMORY = "in_memory"
