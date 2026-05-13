"""Logging configuration."""
import logging
import sys
from decouple import config

# Logging level
LOG_LEVEL = config("LOG_LEVEL", default="INFO")

def setup_logger():
    """Setup application logger."""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Create logger
    logger = logging.getLogger("age_calculator")
    return logger

# Global logger instance
logger = setup_logger()
