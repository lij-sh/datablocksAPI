"""
datablockAPI - Test Configuration
Test-specific configuration and fixtures.
"""

import pytest
import os
from datablockAPI.config import Config


@pytest.fixture
def test_config():
    """Test configuration with test-specific settings."""
    return Config(
        database__url="sqlite:///:memory:",
        api__timeout=5,
        api__max_retries=1
    )


@pytest.fixture(autouse=True)
def mock_env_vars():
    """Mock environment variables for testing."""
    original_env = os.environ.copy()

    # Set test environment variables
    os.environ.update({
        "DNB_API_KEY": "test_key",
        "DNB_API_SECRET": "test_secret",
        "DATABASE_URL": "sqlite:///:memory:",
        "LOG_LEVEL": "DEBUG"
    })

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)</content>
<parameter name="filePath">c:\Users\jun\dataground\tests\conftest.py