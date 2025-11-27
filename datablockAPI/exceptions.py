"""
datablockAPI - Custom Exceptions
Custom exception classes for the datablockAPI package.
"""


class APIError(Exception):
    """Base exception for API-related errors."""
    pass


class AuthenticationError(APIError):
    """Raised when authentication fails."""
    pass


class RateLimitError(APIError):
    """Raised when rate limit is exceeded."""
    pass