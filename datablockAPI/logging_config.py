"""
datablockAPI - Logging Configuration
Structured logging setup for the package.
"""

import logging
import sys
from .config import config


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, config.logging.level.upper()),
        format=config.logging.format,
        stream=sys.stdout
    )

    # Create logger for the package
    logger = logging.getLogger('datablockAPI')
    logger.setLevel(getattr(logging, config.logging.level.upper()))

    return logger


# Global logger instance
logger = setup_logging()</content>
<parameter name="filePath">c:\Users\jun\dataground\datablockAPI\logging_config.py