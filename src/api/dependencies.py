from typing import AsyncGenerator

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.auth.handler import LoginHandler
from src.application.ports.cache import Cache
from src.application.ports.password_hasher import PasswordHasher
from src.application.ports.token_service import TokenService
from src.domain.user.entities import User
from src.infrastructure.cache.redis import RedisCache
from src.infrastructure.db.unit_of_work import AsyncUnitOfWork
from src.infrastructure.factories.health import build_cache_health, build_db_health
from src.infrastructure.factories.repositories import (
    build_user_repository,
    build_wallet_repository,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/rest/v1/auth/login/")


async def get_session(request: Request) -> AsyncGenerator:
    session_factory = request.app.state.session_factory

    async with session_factory() as session:
        yield session


async def get_db_engine(request: Request):
    db_engine = request.app.state.db_engine
    return db_engine


async def get_db_type(request: Request):
    db_type = request.app.state.db_type
    return db_type


async def get_cache_client(request: Request):
    cache_client = request.app.state.cache_client
    return cache_client


async def get_cache_type(request: Request):
    cache_type = request.app.state.cache_type
    return cache_type


def get_a_uow(
    session: AsyncSession = Depends(get_session),
):
    return AsyncUnitOfWork(session)


def get_env(request: Request) -> str:
    env = request.app.state.env
    return env


def get_password_hasher(request: Request) -> PasswordHasher:
    password_hasher: PasswordHasher = request.app.state.password_hasher
    return password_hasher


def get_token_service(request: Request) -> TokenService:
    token_service: TokenService = request.app.state.token_service
    return token_service


def is_production(env=Depends(get_env)):
    _is_production = env in ["PROD", "PRODUCTION"]
    return _is_production


async def check_db(db_type, db_engine) -> str:
    health = build_db_health(db_type=db_type, db_engine=db_engine)
    return "ok" if await health.is_healthy() else "failed"


async def check_cache(cache_type, cache_client) -> str:
    health = build_cache_health(cache_type=cache_type, cache_client=cache_client)
    return "ok" if await health.is_healthy() else "failed"


# --- Repository ---
def get_wallet_repository(request: Request):
    repository = build_wallet_repository(app=request.app)
    return repository


def get_user_repository(request: Request):
    repository = build_user_repository(app=request.app)
    return repository


# --- End Repository ---


def get_login_handler(
    user_repository=Depends(get_user_repository),
    password_hasher=Depends(get_password_hasher),
    token_service=Depends(get_token_service),
):
    login_handler = LoginHandler(
        user_repository=user_repository,
        password_hasher=password_hasher,
        token_service=token_service,
    )
    return login_handler


# --- Cache ---
def get_cache(
    cache_type=Depends(get_cache_type), cache_client=Depends(get_cache_client)
) -> Cache:
    match cache_type:
        case "redis":
            return RedisCache(cache_client)
        case "memory":
            return cache_client
        case _:
            raise NotImplementedError


def get_current_user(
    token=Depends(oauth2_scheme),
    token_service: TokenService = Depends(get_token_service),
):
    payload = token_service.verify(token)
    user_uuid = payload["u"]
    return user_uuid


def get_user_role(
    user_uuid=Depends(get_current_user), user_repository=Depends(get_user_repository)
):
    user: User = user_repository.get(user_uuid)
    if not user:
        raise Exception("No user")  # TODO change to proper Exception

    role = user.role
    return role


def require_permissions(
    roles_with_permission: list[str],
):
    async def _require_permission(user_role=Depends(get_user_role)):
        # Permission check
        matching_permission = user_role in roles_with_permission

        if not matching_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )  # TODO change to proper Exception

    return _require_permission
