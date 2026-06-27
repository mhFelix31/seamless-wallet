import copy
import tempfile
from contextlib import contextmanager

import jwt
import pytest
from fastapi.testclient import TestClient
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from src.config import settings
from src.infrastructure.auth.password_hasher.argon2_password_hasher import (
    Argon2PasswordHasher,
)
from src.infrastructure.auth.token_service.jwt_token_service import JWTTokenService
from src.infrastructure.db.models.user_model import UserModel
from src.main import create_app


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

    match backend:
        case "sqlite":
            with tempfile.NamedTemporaryFile(suffix=".db") as f:
                yield f"sqlite+pysqlite:///{f.name}"

        case "postgres":
            with PostgresContainer("postgres:16") as pg:
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
    return _settings


@pytest.fixture
def default_client(client_factory, mock_setting, postgres_url):
    mock_setting.database_url = postgres_url
    mock_setting.database_type = "postgres"
    with client_factory(mock_setting) as client:
        yield client


@pytest.fixture
def db_session(default_client):
    session = default_client.app.state.session_factory()
    yield session
    session.close()


# Factories
@pytest.fixture
def user_factory(db_session, mock_setting):
    password_hasher = Argon2PasswordHasher(secret_pepper=mock_setting.secret_pepper)

    def _create_user(
        email="user@example.com",
        password="valid-password",
        name="Test User",
    ):
        user = UserModel(
            full_name=name,
            email=email,
            password_hash=password_hasher.hash_value(password),
        )

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        return user

    return _create_user


@pytest.fixture
def token_factory(user_factory, mock_setting):
    token_service = JWTTokenService(priv_token_key=mock_setting.secret_token, env_token_pub_list=[])

    def _create_token(user=user_factory()):
        token = token_service.create(user_uuid=user.uuid)
        return token
    return _create_token


@pytest.fixture
def custom_token_payload(mock_setting):
    def _custom_payload(payload, secret_token=mock_setting.secret_token):
        jwt_token = jwt.encode(payload, secret_token, algorithm="HS256")
        return jwt_token

    return _custom_payload


@pytest.fixture
def create_header(token_factory):
    def _header(jwt_token=token_factory()):
        header = {"Authorization": f"Bearer {jwt_token}"}
        return header

    return _header