"""Database configuration for the NovaSystem logging service."""
from __future__ import annotations

import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    """Base class for declarative SQLAlchemy models."""


DATA_DIR = Path(os.environ.get("NOVASYSTEM_DATA_DIR", Path(__file__).resolve().parent / "data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = Path(os.environ.get("NOVASYSTEM_DB_PATH", DATA_DIR / "activity.db"))
ENGINE = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=ENGINE, autoflush=False, autocommit=False)


def init_db() -> None:
    """Initialise the SQLite database and create all tables."""
    from . import models  # noqa: F401  # imported for side effects

    Base.metadata.create_all(bind=ENGINE)


__all__ = ["Base", "ENGINE", "SessionLocal", "init_db", "DATA_DIR", "DB_PATH"]
