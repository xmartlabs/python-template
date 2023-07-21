from enum import Enum

from pydantic import BaseSettings, PostgresDsn


class LogLevel(str, Enum):
    critical = "CRITICAL"
    error = "ERROR"
    warning = "WARNING"
    info = "INFO"
    debug = "DEBUG"


class Settings(BaseSettings):
    database_url: PostgresDsn
    test_database_url: PostgresDsn | None
    log_level: LogLevel = LogLevel.debug
    server_url: str

    # Auth
    access_token_expire_minutes: float
    jwt_signing_key: str
    accept_cookie: bool = True
    accept_token: bool = True


settings = Settings()
