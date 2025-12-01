"""
datablockAPI - Configuration Management
Centralized configuration with validation using Pydantic.
"""

import os


class DatabaseConfig:
    """Database configuration settings."""

    def __init__(self):
        self.url = os.getenv("DATABASE_URL", "sqlite:///datablock.db")
        self.echo = os.getenv("DATABASE_ECHO", "False").lower() == "true"


class APIConfig:
    """D&B API configuration settings."""

    def __init__(self):
        self.key = os.getenv("DNB_API_KEY")
        self.secret = os.getenv("DNB_API_SECRET")
        self.url = os.getenv("DNB_API_URL", "https://plus.dnb.com")
        self.timeout = int(os.getenv("DNB_API_TIMEOUT", "30"))
        self.max_retries = int(os.getenv("DNB_API_MAX_RETRIES", "3"))
        self.rate_limit_per_minute = int(os.getenv("DNB_RATE_LIMIT_PER_MINUTE", "60"))


class LoggingConfig:
    """Logging configuration settings."""

    def __init__(self):
        self.level = os.getenv("LOG_LEVEL", "INFO")
        self.format = os.getenv(
            "LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )


class Config:
    """Main configuration class."""

    def __init__(self):
        self.database = DatabaseConfig()
        self.api = APIConfig()
        self.logging = LoggingConfig()


# Global configuration instance
config = Config()
