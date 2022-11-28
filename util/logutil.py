import os, sys
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_PATH = os.path.join(os.path.dirname(BASE_DIR), 'log')
LOG_NAME = 'trends.log'

if not os.path.exists(LOG_PATH):
    try:
        os.mkdir(LOG_PATH)
    except PermissionError as e:
        pass

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S',
                    filename=os.path.join(LOG_PATH, LOG_NAME),
                    filemode='w')
logger = logging.getLogger('trends')
logger.addHandler(logging.StreamHandler(sys.stdout))

CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s [%(module)s:%(funcName)s] %(process)d %(thread)d %(filename)s:%(lineno)d %(message)s"
        },
        "simple": {
            "format": "%(levelname)s %(asctime)s - %(filename)s:%(lineno)d - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple"
        },
        "server_file": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "verbose",
            "filename": os.path.join(LOG_PATH, "trends_server.log"),
            "when": "D",
            "interval": 1,
            "backupCount": 30,
            "encoding": "utf-8"
        },
        "task_file": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "verbose",
            "filename": os.path.join(LOG_PATH, "trends_task.log"),
            "when": "D",
            "interval": 1,
            "backupCount": 30,
            "encoding": "utf-8"
        },
    },
    "loggers": {
        "server": {
            "handlers": ["server_file", "console"],
            "level": "DEBUG"
        },
        "task": {
            "handlers": ["task_file", "console"],
            "level": "DEBUG"
        }
    }
}
