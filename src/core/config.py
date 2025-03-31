from enum import Enum

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class LogLevel(str, Enum):
    critical = "CRITICAL"
    error = "ERROR"
    warning = "WARNING"
    info = "INFO"
    debug = "DEBUG"


class Settings(BaseSettings):
    # Database
    database_url: PostgresDsn
    async_database_url: PostgresDsn | None = None
    database_pool_pre_ping: bool | None = None
    database_pool_size: int | None = None
    database_pool_recycle: int | None = None
    database_max_overflow: int | None = None

    # Logging
    log_level: LogLevel = LogLevel.debug
    server_url: str | None = None

    # Auth
    access_token_expire_minutes: float | None = None
    jwt_signing_key: str | None = None
    accept_cookie: bool = True
    accept_token: bool = True


settings = Settings()
