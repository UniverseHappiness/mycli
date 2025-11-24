"""Logging utilities for mycli."""

import sys
from pathlib import Path
from typing import Optional
from loguru import logger

from mycli.config import get_config


def setup_logging(log_level: Optional[str] = None, log_file: Optional[Path] = None) -> None:
    """Setup logging configuration.
    
    Args:
        log_level: Log level (DEBUG, INFO, WARN, ERROR). If None, use config.
        log_file: Log file path. If None, use default location.
    """
    config = get_config()
    
    # Remove default handler
    logger.remove()
    
    # Determine log level
    level = log_level or config.general.log_level
    
    # Add console handler with color
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=level,
        colorize=True,
    )
    
    # Add file handler
    if log_file is None:
        log_dir = config.get_data_dir() / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "mycli.log"
    
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=level,
        rotation="10 MB",
        retention="1 week",
        compression="zip",
    )
    
    logger.info(f"Logging initialized at level {level}")


def get_logger(name: str):
    """Get a logger instance.
    
    Args:
        name: Logger name.
    
    Returns:
        Logger instance.
    """
    return logger.bind(name=name)
