"""Logging configuration for the application."""
import os
import logging
import logging.config
from datetime import datetime
from typing import Dict, Any

# Log level from environment
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = os.getenv("LOG_FORMAT", "json")  # json or text
LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")

def get_logging_config() -> Dict[str, Any]:
    """Get logging configuration."""

    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "json": {
                "format": '{"timestamp": "%(asctime)s", "logger": "%(name)s", "level": "%(levelname)s", "message": "%(message)s", "module": "%(module)s", "function": "%(funcName)s", "line": %(lineno)d}',
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": LOG_LEVEL,
                "formatter": "json" if LOG_FORMAT == "json" else "standard",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.FileHandler",
                "level": LOG_LEVEL,
                "formatter": "json" if LOG_FORMAT == "json" else "standard",
                "filename": LOG_FILE,
                "mode": "a"
            }
        },
        "loggers": {
            "": {  # Root logger
                "handlers": ["console", "file"],
                "level": LOG_LEVEL,
                "propagate": False
            },
            "uvicorn": {
                "handlers": ["console", "file"],
                "level": LOG_LEVEL,
                "propagate": False
            },
            "sqlalchemy": {
                "handlers": ["console", "file"],
                "level": "WARNING",  # Reduce SQL noise
                "propagate": False
            }
        }
    }

    return config

def setup_logging():
    """Setup application logging."""
    config = get_logging_config()
    logging.config.dictConfig(config)

    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized - Level: {LOG_LEVEL}, Format: {LOG_FORMAT}")

def get_logger(name: str) -> logging.Logger:
    """Get logger instance."""
    return logging.getLogger(name)

# Custom log functions for different contexts
def log_admin_action(user_id: str, action: str, details: Dict[str, Any]):
    """Log admin actions for audit trail."""
    logger = get_logger("admin_audit")
    logger.info(f"Admin action - User: {user_id}, Action: {action}, Details: {details}")

def log_api_request(api_key_id: str, endpoint: str, status: int, response_time: float):
    """Log API requests for monitoring."""
    logger = get_logger("api_monitoring")
    logger.info(f"API request - Key: {api_key_id}, Endpoint: {endpoint}, Status: {status}, Time: {response_time}ms")

def log_security_event(event_type: str, details: Dict[str, Any], severity: str = "INFO"):
    """Log security events."""
    logger = get_logger("security")
    log_method = getattr(logger, severity.lower(), logger.info)
    log_method(f"Security event - Type: {event_type}, Details: {details}")
