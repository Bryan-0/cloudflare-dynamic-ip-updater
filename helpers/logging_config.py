import logging.config
import os
from pythonjsonlogger import jsonlogger
from datetime import datetime, timezone

today = datetime.now(timezone.utc)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": "%(asctime)s %(levelname)s %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "json",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": f"{os.environ.get("LOGS_DIR", ".")}/cloudflare_dynamic_ip_updater-{today.strftime("%d_%m_%Y")}.log",
            "formatter": "json",
            "mode": "a",
            "maxBytes": 5242880,
            "backupCount": 7,
        },
    },
    "loggers": {"": {"handlers": ["stdout", "file"], "level": "INFO"}},
}


logging.config.dictConfig(LOGGING)
