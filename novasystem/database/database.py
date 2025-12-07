"""
Database Connection and Management

This module provides database connection, initialization, and management
functionality for the NovaSystem performance tracking database.
"""

import os
import logging
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
from typing import Generator, Optional
from pathlib import Path

from .models import Base

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database connections and operations."""

    def __init__(self, database_url: Optional[str] = None):
        """
        Initialize database manager.

        Args:
            database_url: Database connection URL. If None, uses default SQLite.
        """
        self.database_url = database_url or self._get_default_database_url()
        self.engine = None
        self.SessionLocal = None
        self._initialize_engine()

    def _get_default_database_url(self) -> str:
        """Get default database URL based on environment."""
        # Check for environment variable
        db_url = os.getenv("NOVASYSTEM_DATABASE_URL")
        if db_url:
            return db_url

        # Default to SQLite in project data directory
        data_dir = Path(__file__).parent.parent.parent / "data"
        data_dir.mkdir(exist_ok=True)

        db_path = data_dir / "novasystem_performance.db"
        return f"sqlite:///{db_path}"

    def _initialize_engine(self):
        """Initialize SQLAlchemy engine with appropriate settings."""
        try:
            # Configure engine based on database type
            if self.database_url.startswith("sqlite"):
                # SQLite configuration
                self.engine = create_engine(
                    self.database_url,
                    poolclass=StaticPool,
                    connect_args={
                        "check_same_thread": False,
                        "timeout": 30
                    },
                    echo=False  # Set to True for SQL debugging
                )

                # Enable foreign key constraints for SQLite
                @event.listens_for(self.engine, "connect")
                def set_sqlite_pragma(dbapi_connection, connection_record):
                    cursor = dbapi_connection.cursor()
                    cursor.execute("PRAGMA foreign_keys=ON")
                    cursor.close()

            else:
                # PostgreSQL/MySQL configuration
                self.engine = create_engine(
                    self.database_url,
                    pool_size=10,
                    max_overflow=20,
                    pool_pre_ping=True,
                    echo=False
                )

            # Create session factory
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )

            logger.info(f"Database engine initialized: {self.database_url}")

        except Exception as e:
            logger.error(f"Failed to initialize database engine: {e}")
            raise

    def create_tables(self):
        """Create all database tables."""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise

    def drop_tables(self):
        """Drop all database tables."""
        try:
            Base.metadata.drop_all(bind=self.engine)
            logger.info("Database tables dropped successfully")
        except Exception as e:
            logger.error(f"Failed to drop database tables: {e}")
            raise

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Get database session with automatic cleanup."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()

    def get_session_sync(self) -> Session:
        """Get database session (caller responsible for cleanup)."""
        return self.SessionLocal()

    def health_check(self) -> bool:
        """Check database connectivity."""
        try:
            with self.get_session() as session:
                from sqlalchemy import text
                session.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False

# Global database manager instance
_database_manager: Optional[DatabaseManager] = None

def get_database_manager() -> DatabaseManager:
    """Get the global database manager instance."""
    global _database_manager
    if _database_manager is None:
        _database_manager = DatabaseManager()
    return _database_manager

def get_database() -> DatabaseManager:
    """Get the global database manager instance (alias)."""
    return get_database_manager()

def init_database(database_url: Optional[str] = None, create_tables: bool = True) -> DatabaseManager:
    """
    Initialize the database system.

    Args:
        database_url: Database connection URL
        create_tables: Whether to create tables if they don't exist

    Returns:
        DatabaseManager instance
    """
    global _database_manager

    # Initialize database manager
    _database_manager = DatabaseManager(database_url)

    # Create tables if requested
    if create_tables:
        _database_manager.create_tables()

    # Perform health check
    if not _database_manager.health_check():
        raise RuntimeError("Database initialization failed health check")

    logger.info("Database system initialized successfully")
    return _database_manager

def get_session() -> Generator[Session, None, None]:
    """Get database session (convenience function)."""
    return get_database_manager().get_session()

# Database configuration
DATABASE_CONFIG = {
    "default_url": "sqlite:///data/novasystem_performance.db",
    "backup_interval_hours": 24,
    "retention_days": 90,
    "max_connections": 20,
    "connection_timeout": 30
}
