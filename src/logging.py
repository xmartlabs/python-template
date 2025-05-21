import logging.config
import os
import sys
import time
import typing
from functools import cache
from typing import TYPE_CHECKING, Any

import structlog
from structlog import PrintLogger

from src.core.config import LogLevel

if typing.TYPE_CHECKING:
    from src.core.config import LogSettings

if TYPE_CHECKING:
    from structlog.types import EventDict
    from structlog.typing import Processor


class Logger:
    name: str

    _stderr_logger: PrintLogger
    _stdout_logger: PrintLogger

    def __init__(self, name: str):
        self.name = name

        self._stderr_logger = PrintLogger(sys.stderr)
        self._stdout_logger = PrintLogger(sys.stdout)

    def _print_to_stderr(self, message: str) -> None:
        self._stderr_logger.msg(message)

    def _print_to_stdout(self, message: str) -> None:
        self._stdout_logger.msg(message)

    debug = _print_to_stdout
    info = _print_to_stdout
    msg = _print_to_stdout
    warning = _print_to_stdout
    error = _print_to_stderr
    exception = _print_to_stderr
    critical = _print_to_stderr


def logger_factory(name: str | None, *args: Any) -> Logger:
    """Create a logger instance."""
    return Logger(name=name or "default")


class StreamHandler(logging.Handler):
    _loggers: dict[str, Logger]

    def __init__(self) -> None:
        self._loggers = {}
        super().__init__(logging.DEBUG)

    def _logging_method(self, level: int) -> str | None:
        if level >= logging.CRITICAL:
            return "critical"
        if level >= logging.ERROR:
            return "error"
        if level >= logging.WARNING:
            return "warning"
        if level >= logging.INFO:
            return "info"
        if level >= logging.DEBUG:
            return "debug"

        return None

    def _logger(self, name: str) -> Logger:
        if not self._loggers.get(name, None):
            self._loggers[name] = structlog.get_logger(name)

        return self._loggers[name]

    def emit(self, record: logging.LogRecord) -> None:
        logging_func = self._logging_method(record.levelno)
        if not logging_func:
            return

        logger = self._logger(record.name)
        getattr(logger, logging_func)(record.getMessage())


def default_logging_config(log_level: LogLevel = LogLevel.INFO) -> dict:
    """Python logging configuration."""

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {},
        "handlers": {
            "stream": {
                "level": log_level.value,
                "class": "src.logging.StreamHandler",
            },
        },
        "loggers": {
            "": {"handlers": ["stream"], "level": log_level.value, "propagate": True},
        },
    }


def _timestamp_processor(logger: Logger, msg: str, event_dict: "EventDict") -> "EventDict":
    """Add timestamp to the event dictionary."""
    event_dict["timestamp"] = time.time_ns()
    return event_dict


def _pid_processor(logger: Logger, msg: str, event_dict: "EventDict") -> "EventDict":
    """Add process ID to the event dictionary."""
    event_dict["pid"] = os.getpid()
    return event_dict


@cache
def configure_logging(config: "LogSettings") -> None:
    """Configure logging for the application."""
    logging.config.dictConfig(default_logging_config(config.log_level))

    processors: list["Processor"] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
    ]

    if config.enable_structured_log:
        processors.extend(
            [
                _timestamp_processor,
                _pid_processor,
                structlog.processors.dict_tracebacks,
                structlog.processors.ExceptionRenderer(),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.JSONRenderer(),
            ]
        )
    else:
        processors.extend(
            [
                structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M.%S"),
                structlog.dev.ConsoleRenderer(),
            ]
        )

    structlog.configure(
        processors=processors,
        logger_factory=logger_factory,
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=config.cache_loggers,
    )
