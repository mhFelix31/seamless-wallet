import tempfile
import pytest
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# --------------------
# PostgreSQL container
# --------------------
@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def postgres_url(postgres_container):
    return postgres_container.get_connection_url(driver="psycopg")

@pytest.fixture(scope="function")
def db_url(request):
    backend = request.param

    match(backend):
        case "sqlite":
            with tempfile.NamedTemporaryFile(suffix=".db") as f:
                yield f"sqlite+pysqlite:///{f.name}"

        case "postgres":
            with PostgresContainer("postgres:16") as pg:
                yield pg.get_connection_url(driver="psycopg")

        case _:
            raise ValueError(f"Unsupported backend: {backend}")

# --------------------
# SQLAlchemy engine
# --------------------
@pytest.fixture(scope="session")
def engine(postgres_url):
    engine = create_engine(postgres_url)
    yield engine
    engine.dispose()


# --------------------
# Apply migrations (Alembic)
# --------------------
@pytest.fixture(scope="session", autouse=True)
def apply_migrations(postgres_url):
    from alembic.config import Config
    from alembic import command

    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", postgres_url)

    command.upgrade(alembic_cfg, "head")
    yield
    command.downgrade(alembic_cfg, "base")


# --------------------
# DB Session per test
# --------------------
@pytest.fixture(scope="function")
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()

    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


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