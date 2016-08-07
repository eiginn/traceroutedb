
import logging
from logging.config import dictConfig

logging_config = dict(
    version=1,
    disable_existing_loggers=True,
    formatters={
        "f": {"format":
              "TracerouteDB %(asctime)s %(levelname)s %(message)s",
              "datefmt": "%Y-%m-%d %H:%M:%S",
              },
    },
    handlers={
        "h": {
            "class": "logging.StreamHandler",
            "formatter": "f",
        },
        "null": {
            "class": "logging.NullHandler",
        },
    },
    root={
        "handlers": ["h"],
    },
    loggers={
        "requests": {
            "handlers": ["null"],
            "propagate": False,
        },
        "traceroutedb": {
            "handlers": ["h"],
        },
    }

)

dictConfig(logging_config)

logger = logging.getLogger()
