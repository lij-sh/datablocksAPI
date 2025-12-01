"""
datablockAPI - Core Database Module
Handles database connection, initialization, and base configuration.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

# SQLAlchemy Base for all models
Base = declarative_base()

# Global engine and session
_engine = None
_SessionLocal = None


def init(database: str, echo: bool = False, **kwargs):
    """
    Initialize the database connection and create all tables.

    Args:
        database: Database connection string (e.g., 'postgresql://user:pass@localhost/db')
        echo: Whether to log SQL statements (default: False)
        **kwargs: Additional arguments to pass to create_engine

    Examples:
        >>> import datablockAPI as api
        >>> api.init(database='sqlite:///datablock.db')
        >>> api.init(database='postgresql://user:pass@localhost:5432/datablock')
    """
    global _engine, _SessionLocal

    # Create engine
    _engine = create_engine(
        database,
        echo=echo,
        poolclass=NullPool if database.startswith("sqlite") else None,
        **kwargs,
    )

    # Create session factory
    _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

    # Import all models to register them with Base

    # Create all tables
    Base.metadata.create_all(bind=_engine)

    print(f"✓ Database initialized: {database}")
    print(f"✓ Created {len(Base.metadata.tables)} tables")


def get_engine():
    """Get the current database engine."""
    if _engine is None:
        raise RuntimeError("Database not initialized. Call init() first.")
    return _engine


def get_session():
    """Get a new database session."""
    if _SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init() first.")
    return _SessionLocal()


def close():
    """Close database connections."""
    global _engine, _SessionLocal
    if _engine:
        _engine.dispose()
        _engine = None
        _SessionLocal = None
        print("✓ Database connections closed")
