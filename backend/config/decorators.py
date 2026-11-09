from functools import wraps
import logging

logger = logging.getLogger(__name__)


def log_execute(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        logging.info("Starting %s", func.__name__)
        try:
            func(*args, **kwargs)
        except Exception:
            logging.exception(
                "Error executing %s",
                func.__name__
            )
            raise

        logging.info("Finished %s", func.__name__)
    return wrapper
