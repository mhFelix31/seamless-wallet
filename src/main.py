from fastapi import FastAPI
from src.api import create_api_router
from src.config import settings
from src.lifespan_utils import lifespan_factory



def _add_middlewares(app):
    ...

def _add_routes(app):
    app.include_router(create_api_router())

def create_app(app_settings) -> FastAPI:
    app = FastAPI(
        title=app_settings.app_name,
        version=app_settings.version,
        lifespan=lifespan_factory(app_settings)
    )
    _add_middlewares(app)
    _add_routes(app)
    
    return app

app = create_app(settings)

