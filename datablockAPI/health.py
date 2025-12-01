"""
datablockAPI - Health Check Module
Health checks for monitoring and diagnostics.
"""

import logging
from typing import Any, Dict

from .api.client import DNBAPIClient
from .core.database import get_session

logger = logging.getLogger("datablockAPI")


def health_check() -> Dict[str, Any]:
    """
    Perform health checks on the system components.

    Returns:
        Dictionary with health status of each component
    """
    results = {
        "database": _check_database(),
        "api_client": _check_api_client(),
        "overall": "healthy",
    }

    # Determine overall health
    if any(
        result.get("status") == "unhealthy"
        for result in results.values()
        if isinstance(result, dict)
    ):
        results["overall"] = "unhealthy"

    return results


def _check_database() -> Dict[str, Any]:
    """Check database connectivity."""
    try:
        session = get_session()
        session.execute("SELECT 1")
        return {"status": "healthy", "message": "Database connection successful"}
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {"status": "unhealthy", "message": str(e)}


def _check_api_client() -> Dict[str, Any]:
    """Check API client configuration."""
    try:
        # Try to create client (this will validate credentials are configured)
        client = DNBAPIClient()
        return {
            "status": "healthy",
            "message": "API client configured successfully",
            "has_credentials": bool(client.api_key and client.api_secret),
        }
    except Exception as e:
        logger.error(f"API client health check failed: {e}")
        return {"status": "unhealthy", "message": str(e)}
