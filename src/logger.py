import logging
import os
from logging.handlers import RotatingFileHandler

# Define the log directory at the root of the project
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(name="quant_pipeline"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Institutional Log Format
    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(module)s:%(lineno)d | %(message)s')

    # 1. Console Handler (Outputs to terminal)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # 2. Rotating File Handler (Max 5MB per file, keeps 3 backups. Prevents disk bloat)
    log_file = os.path.join(LOG_DIR, "system.log")
    file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Prevent duplicate handlers if instantiated multiple times
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

# Singleton instance for system-wide use
logger = setup_logger()