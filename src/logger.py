import logging
from typing import Optional
from logging import Logger

from src.constants import LOG_LEVEL


# The logger setup in this file allows the program to have this set up modularized away from the main (app.py) file, to keep things easy to read.

def setup_logging(log_level: str = LOG_LEVEL):
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format='%(asctime)s [%(levelname)s] [%(name)s] (%(filename)s:%(funcName)s:%(lineno)d): %(message)s',
    )


def get_logger(name: Optional[str]=None) -> Logger:
    return logging.getLogger(name)
