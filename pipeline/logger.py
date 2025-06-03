import logging
import os

def setup_logger(log_file='logs/enrollment_log.txt'):
    """Set up logger to write to both console and file."""
    logger = logging.getLogger("enrollment_logger")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # Ensure log directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # File handler
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
