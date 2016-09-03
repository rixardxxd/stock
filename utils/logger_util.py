"""
This module provides logger related methods.
"""
import logging


def get_logger(filename, name=None, level=logging.DEBUG):
    """
    This method gets a logger based on given parameters.
    Parameters
    ----------
    filename: logger filename
    name: logger name
    level: logger level

    Returns
    -------
    logger
    """
    logger = logging.getLogger(name)
    logging.basicConfig(filename=filename, format="%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s",
                        level=level)
    return logger
