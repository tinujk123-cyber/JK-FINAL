"""
Logging configuration for JK TRINETRA FastAPI Backend.

Provides structured JSON logging for production environments.
"""

import logging
import sys
from typing import Optional

from pythonjsonlogger import jsonlogger

from .config import settings


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter with additional fields."""
    
    def add_fields(self, log_record: dict, record: logging.LogRecord, message_dict: dict) -> None:
        super().add_fields(log_record, record, message_dict)
        log_record["level"] = record.levelname
        log_record["logger"] = record.name
        log_record["environment"] = settings.environment


def setup_logging(
    level: Optional[str] = None,
    format_type: Optional[str] = None
) -> logging.Logger:
    """
    Configure application logging.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_type: Format type ('json' or 'text')
    
    Returns:
        Configured root logger
    """
    log_level = level or settings.log_level
    log_format = format_type or settings.log_format
    
    # Get root logger
    logger = logging.getLogger("jk_trinetra")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Create handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, log_level.upper()))
    
    if log_format == "json":
        formatter = CustomJsonFormatter(
            "%(timestamp)s %(level)s %(name)s %(message)s"
        )
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a named logger.
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Named logger instance
    """
    return logging.getLogger(f"jk_trinetra.{name}")
