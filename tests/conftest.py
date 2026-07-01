import copy
import tempfile
from contextlib import contextmanager

import pytest
from fastapi.testclient import TestClient
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from src.config import settings
from src.main import create_app


# --------------------
# PostgreSQL container
# --------------------
@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("sqlalchemy:16") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def postgres_url(postgres_container):
    return postgres_container.get_connection_url(driver="psycopg")


@pytest.fixture(scope="function")
def db_url(request):
    backend = request.param

    match backend:
        case "sqlite":
            with tempfile.NamedTemporaryFile(suffix=".db") as f:
                yield f"sqlite+pysqlite:///{f.name}"

        case "sqlalchemy":
            with PostgresContainer("sqlalchemy:16") as pg:
                yield pg.get_connection_url(driver="psycopg")

        case _:
            raise ValueError(f"Unsupported backend: {backend}")


# --------------------
# Apply migrations (Alembic)
# --------------------
@pytest.fixture(scope="session", autouse=True)
def apply_migrations(postgres_url):
    from alembic import command
    from alembic.config import Config

    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", postgres_url)

    command.upgrade(alembic_cfg, "head")
    yield
    command.downgrade(alembic_cfg, "base")


# --------------------
# Redis container
# --------------------
@pytest.fixture(scope="session")
def redis_container():
    with RedisContainer("redis:latest") as redis:
        yield redis


@pytest.fixture(scope="session")
def redis_url(redis_container):
    return f"redis://{redis_container.get_container_host_ip()}:{redis_container.get_exposed_port(redis_container.port)}"


# TestClient
@pytest.fixture
def client_factory():
    @contextmanager
    def _client(custom_settings):
        app = create_app(custom_settings)
        with TestClient(app=app, base_url="http://test") as client:
            yield client

    return _client


@pytest.fixture(scope="session")
def mock_setting():
    _settings = copy.deepcopy(settings)
    _settings.environment = "TEST"
    return _settings


@pytest.fixture
def default_client(client_factory, mock_setting, postgres_url, redis_url):
    mock_setting.database_url = postgres_url
    mock_setting.database_type = "sqlalchemy"
    mock_setting.cache_url = redis_url
    mock_setting.cache_type = "redis"
    with client_factory(mock_setting) as client:
        yield client
