from enum import StrEnum


class DBtype(StrEnum):
    POSTGRES = "postgres"
    SQLITE = "sqlite"


class CacheType(StrEnum):
    REDIS = "redis"
    IN_MEMORY = "in_memory"

