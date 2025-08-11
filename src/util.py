import logging
import time
from typing import Callable, Type

def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

def retry(fn: Callable, exceptions: tuple[Type[Exception], ...], tries=3, base=0.5):
    def wrapper(*args, **kwargs):
        for attempt in range(1, tries + 1):
            try:
                return fn(*args, **kwargs)
            except exceptions as e:
                if attempt == tries:
                    raise
                sleep = base * (2 ** (attempt - 1))
                logging.getLogger("retry").warning(f"{e} (attempt {attempt}/{tries}) -> sleeping {sleep:.1f}s")
                time.sleep(sleep)
    return wrapper
