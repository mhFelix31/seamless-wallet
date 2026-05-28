from pydantic import (
    AliasChoices,
    Field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

# This file should be only imported on main.py
# Why?
# On main.py is where we inject the settings, anything that has to be loaded outside there should get through the app
# This decouples the Main settings from the app structure, making easier to test and guarantee behavior.


class Settings(BaseSettings):
    app_name: str = "Wallet"
    version: str = "0.1.0"
    environment: str = Field("DEV", validation_alias=AliasChoices("env", "environment"))
    debug: bool = False
    # DB
    database_type: str = "postgres"  # Postgres | SQLite | MySQL | mock
    database_url: str = "postgresql+psycopg://other@localhost/otherdb"

    # Cache
    cache_type: str = "in_memory"  # Redis | Memory | None
    cache_url: str = ""

    secret_pepper: str = "secret_rhc_pepper"
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
