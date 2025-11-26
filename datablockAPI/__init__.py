"""
datablockAPI - Main Package
Entry point for the API with init() and load() functions.
"""

from .core.database import init, close, get_session
from .core.loader import load

__version__ = "0.2.0"
__all__ = ["init", "load", "close", "get_session"]
