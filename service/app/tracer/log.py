import logging
import os
import sys
from pprint import pformat

from loguru import logger
from loguru._defaults import LOGURU_FORMAT


# from: https://github.com/Delgan/loguru/issues/78#issuecomment-552111329
class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__ and frame.f_back:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def format_record(record: dict) -> str:
    format_string = LOGURU_FORMAT
    if record["extra"].get("payload") is not None:
        record["extra"]["payload"] = pformat(record["extra"]["payload"], indent=4, compact=True, width=88)
        format_string += "\n<level>{extra[payload]}</level>"
    format_string += "{exception}\n"
    return format_string


def setup_logging():
    level = os.environ.get("LOG_LEVEL", None)
    log_level = getattr(logging, level) if level else logging.INFO
    seen = set()
    for name in [
        *logging.root.manager.loggerDict.keys(),  # type: ignore
        "gunicorn",
        "gunicorn.access",
        "gunicorn.error",
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
        "celery",
    ]:
        if name not in seen:
            seen.add(name.split(".")[0])
            logging.getLogger(name).handlers = [InterceptHandler()]
    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "level": log_level,
                "serialize": True,
                "format": format_record,
            }
        ]
    )
