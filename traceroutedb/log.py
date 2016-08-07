
import logging
from logging.config import dictConfig

logging_config = dict(
    version=1,
    disable_existing_loggers=True,
    formatters={
        "f": {"format":
              "%(name)s %(asctime)s %(levelname)s %(message)s"}
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
        # "requests.packages.urllib3.connectionpool": {
        #     "handlers": ["h"],
        #     "propagate": False,
        # },
    }

)

dictConfig(logging_config)

logger = logging.getLogger()
