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
    async_database_url: PostgresDsn
    database_pool_pre_ping: bool
    database_pool_size: int
    database_pool_recycle: int
    database_max_overflow: int

    # Logging
    log_level: LogLevel = LogLevel.debug
    server_url: str

    # Auth
    access_token_expire_minutes: float
    jwt_signing_key: str
    accept_cookie: bool = True
    accept_token: bool = True


settings = Settings()
