from fastapi import FastAPI
from src.api import create_api_router
from src.config import settings

from contextlib import asynccontextmanager
from src.lifespan_utils import cache_shutdown, cache_startup, db_shutdown, db_startup



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start up
    db_startup(
        app=app,
        db_type=settings.database_type,
        db_url=settings.database_url,
        )
    cache_startup(
        app=app,
        cache_type=settings.cache_type,
        cache_url=settings.cache_url,
        )
    
    yield

    # Shutdown
    await db_shutdown(app=app)
    await cache_shutdown(app=app)


def _add_middlewares(app):
    ...

def _add_routes(app):
    app.include_router(create_api_router())

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        lifespan=lifespan
    )
    _add_middlewares(app)
    _add_routes(app)
    
    return app

app = create_app()

