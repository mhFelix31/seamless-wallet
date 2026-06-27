from pydantic import (
    AliasChoices,
    Field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.enums import CacheType, DBtype

# This file should be only imported on main.py
# Why?
# On main.py is where we inject the settings, anything that has to be loaded outside there should get through the app
# This decouples the Main settings from the app structure, making easier to test and guarantee behavior.


class Settings(BaseSettings):
    app_name: str = "Wallet"
    version: str = "0.1.0"
    environment: str = Field(
        default="DEV", validation_alias=AliasChoices("env", "environment")
    )
    debug: bool = False
    # DB
    db_type: str = DBtype.SQLITE  # Postgres | SQLite | MySQL | mock
    db_url: str = "sqlite:///app.db"

    # Cache
    cache_type: str = CacheType.IN_MEMORY  # Redis | Memory | None
    cache_url: str = ""

    secret_pepper: str = "secret_rhc_pepper"
    # In case there is need to rotate the pepper, we have to gradually rotate users password to new format
    # Rotating Pepper without gradually rotate passwords will block users accounts
    stale_peppers: list[str] = []

    secret_token: str = "super_secret_jwt_token_new_final"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
