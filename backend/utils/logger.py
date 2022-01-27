import logging
import sys


class HealthFilter(logging.Filter):
    # Disable logging HealthCheck
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("/health") == -1


# Filter out /endpoint
logging.getLogger("uvicorn.access").addFilter(HealthFilter())


def init_logger() -> logging.Logger:
    logger = logging.getLogger("main")
    sh = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s %(message)s")
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    logger.setLevel(logging.DEBUG)
    return logger


def get_logger() -> logging.Logger:
    return logging.getLogger("main")
