"""
datablockAPI - Configuration Management
Centralized configuration with validation using Pydantic.
"""

from pydantic import BaseSettings, Field
from typing import Optional
import os


class DatabaseConfig(BaseSettings):
    """Database configuration settings."""
    url: str = Field(default="sqlite:///datablock.db", env="DATABASE_URL")
    echo: bool = Field(default=False, env="DATABASE_ECHO")


class APIConfig(BaseSettings):
    """D&B API configuration settings."""
    key: Optional[str] = Field(default=None, env="DNB_API_KEY")
    secret: Optional[str] = Field(default=None, env="DNB_API_SECRET")
    url: str = Field(default="https://plus.dnb.com", env="DNB_API_URL")
    timeout: int = Field(default=30, env="DNB_API_TIMEOUT")
    max_retries: int = Field(default=3, env="DNB_API_MAX_RETRIES")
    rate_limit_per_minute: int = Field(default=60, env="DNB_RATE_LIMIT_PER_MINUTE")


class LoggingConfig(BaseSettings):
    """Logging configuration settings."""
    level: str = Field(default="INFO", env="LOG_LEVEL")
    format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT")


class Config(BaseSettings):
    """Main configuration class."""
    database: DatabaseConfig = DatabaseConfig()
    api: APIConfig = APIConfig()
    logging: LoggingConfig = LoggingConfig()

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global configuration instance
config = Config()</content>
<parameter name="filePath">c:\Users\jun\dataground\datablockAPI\config.py