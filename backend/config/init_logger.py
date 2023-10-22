"""Module to initialise and setup logging."""
# See https://www.pylenin.com/blogs/python-logging-guide/#logging-from-multiple-modules
import logging
import os
import sys


def init_logger():
    """Initialise logger."""
    # Define module logger
    logger = logging.getLogger(__name__)
    # Initially set to log all - change this in production
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    # best for development or debugging
    consoleHandler = logging.StreamHandler(stream=sys.stderr)
    # create formatter - can also use %(lineno)d -
    # see https://stackoverflow.com/questions/533048/how-to-log-source-file-name-and-line-number-in-python/44401529
    formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s | %(filename)s > %(module)s > %(funcName)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # add formatter to ch and jh
    consoleHandler.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(consoleHandler)
    # Get logging level from environment variable - tweak to convert to boolean
    DEBUG_MODE = (os.environ.get('DEBUG_MODE', 'False') == 'True')
    if DEBUG_MODE:
        logger.setLevel(logging.DEBUG)
        # Set SQLAlchemy logger to DEBUG level in DEBUG_MODE
        logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        # Silence the SQLAlchemy logger when not in DEBUG_MODE
        logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
    return logger, consoleHandler


logger, consoleHandler = init_logger()
