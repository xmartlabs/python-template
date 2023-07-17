from pydantic import BaseModel


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "src"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(name)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"
    LOG_FILE_NAME: str = "logs/warning-error.log"
    LOG_FILE_LEVEL: str = "WARNING"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "console": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "file": {
            "formatter": "default",
            "class": "logging.FileHandler",
            "filename": LOG_FILE_NAME,
            "level": LOG_FILE_LEVEL,
        },
    }
    loggers = {
        LOGGER_NAME: {"handlers": ["console", "file"], "level": LOG_LEVEL},
    }
