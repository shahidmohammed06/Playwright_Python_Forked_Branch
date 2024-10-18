import logging
from logging.handlers import RotatingFileHandler
import os


def __log_configure():

    # Ensure the 'logs' directory exists
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Configure RotatingFileHandler
    handler = RotatingFileHandler(os.path.join(log_dir, "test_run.log"), maxBytes=5000000, backupCount=3)
    handler.setLevel(logging.INFO)

    # Set logging format
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    # Get or create a logger
    _logger = logging.getLogger(__name__)

    # Avoid adding multiple handlers if the logger is already configured
    if not _logger.hasHandlers():
        _logger.addHandler(handler)
        _logger.setLevel(logging.INFO)

    return _logger


# Initialize the logger
logger = __log_configure()
