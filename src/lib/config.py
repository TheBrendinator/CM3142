import logging


def logConfig():
    loggingConfig = {
        "version": 1,
        "formatters": {
            "simple": {
                "format": "%(asctime)s | %(levelname)-8s | process: %(processName)-12s | thread: %(threadName)-12s | %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": logging.StreamHandler,
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            }
        },
        "loggers": {
            "": {
                "level": logging.DEBUG,
                "handlers": ["console"],
                "propagate": False,
            }
        },
    }
    return loggingConfig
