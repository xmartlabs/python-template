import logging
import sys
from enum import IntEnum, StrEnum
from typing import Any, Literal

from pydantic import PostgresDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Env(StrEnum):
    dev = "dev"


class LogLevel(IntEnum):
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG


class LogSettings(BaseSettings):
    # Makes the settings immutable and hashable (can be used as dicts key)
    model_config = SettingsConfigDict(frozen=True)

    log_level: LogLevel = LogLevel.INFO
    structured_log: bool | Literal["auto"] = "auto"
    cache_loggers: bool = True

    def __hash__(self) -> int:
        """Make LogSettings hashable so it can be used as a dict key"""
        return hash((self.log_level, self.structured_log, self.cache_loggers))

    @property
    def enable_structured_log(self) -> bool:
        return not sys.stdout.isatty() if self.structured_log == "auto" else self.structured_log

    @model_validator(mode="before")
    @classmethod
    def parse_log_level(cls, data: Any) -> Any:
        if isinstance(data.get("log_level"), str):
            data["log_level"] = LogLevel[data["log_level"]]

        return data


class Settings(BaseSettings):
    # Makes the settings immutable and hashable (can be used as dicts key)
    model_config = SettingsConfigDict(frozen=True, env_file=".env", env_file_encoding="utf-8")

    env: str = "dev"
    project_name: str

    # Database
    async_database_url: PostgresDsn
    database_pool_pre_ping: bool
    database_pool_size: int
    database_pool_recycle: int
    database_max_overflow: int

    # Logging
    server_url: str
    log_settings: LogSettings = LogSettings()

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


settings = Settings()  # type: ignore[reportCallIssue]
