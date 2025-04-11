import logging
import sys
from typing import Dict, Optional

# Default log levels
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_SRC_LOG_LEVELS = {
    "DB": "INFO",
    "MODELS": "INFO",
    "AUTH": "INFO",
    "CHAT": "INFO",
    "INFERENCE": "INFO",
    "RETRIEVAL": "INFO",
    "AGENT": "INFO",
}


def configure_logger(
    name: str, 
    level: str = DEFAULT_LOG_LEVEL,
    src_log_levels: Optional[Dict[str, str]] = None
) -> logging.Logger:
    """Configure a logger with the specified name and level"""
    logger = logging.getLogger(name)
    
    # Set the default level
    logger.setLevel(getattr(logging, level))
    
    # Configure handler if not already configured
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    # Set specific source log levels if provided
    if src_log_levels:
        for src, level in src_log_levels.items():
            src_logger = logging.getLogger(f"{name}.{src}")
            src_logger.setLevel(getattr(logging, level))
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name"""
    return logging.getLogger(name)
