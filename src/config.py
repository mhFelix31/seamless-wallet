from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
  Field,
  AliasChoices,
)


class Settings(BaseSettings):
    app_name: str = "Wallet"
    version: str = "0.1.0"
    environment: str = Field(
      "DEV",
      validation_alias=AliasChoices('env','environment')
    )
    debug: bool = False
    # DB
    database_type: str = "postgres" # Postgres | SQLite | MySQL | mock
    database_url: str = "postgresql://other@localhost/otherdb"

    # Cache
    cache_type: str = "in_memory" # Redis | Memory | None
    cache_url: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def is_production(self) -> bool:
        return self.environment == "PROD"


settings = Settings()