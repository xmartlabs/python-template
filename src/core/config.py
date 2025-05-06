from enum import StrEnum

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class LogLevel(StrEnum):
    critical = "CRITICAL"
    error = "ERROR"
    warning = "WARNING"
    info = "INFO"
    debug = "DEBUG"


class Env(StrEnum):
    dev = "dev"


class Settings(BaseSettings):
    env: str = "dev"
    project_name: str

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

    # Celery
    celery_broker_url: str
    celery_result_backend: str

    # OpenTelemetry
    otel_exporter_otlp_endpoint: str


settings = Settings()
