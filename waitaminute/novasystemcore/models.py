"""SQLAlchemy models for activity logging."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class ActivityLog(Base):
    """Represents a single activity that has been logged."""

    __tablename__ = "activity_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    activity: Mapped[str] = mapped_column(String(255), nullable=False)
    details: Mapped[str | None] = mapped_column(Text)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    metadata: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)

    documents: Mapped[list["DocumentArtifact"]] = relationship(
        "DocumentArtifact", back_populates="log", cascade="all, delete-orphan"
    )


class DocumentArtifact(Base):
    """Represents an auxiliary document generated for a log entry."""

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    log_id: Mapped[int] = mapped_column(ForeignKey("activity_logs.id", ondelete="CASCADE"), nullable=False, index=True)
    doc_type: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    path: Mapped[str] = mapped_column(String(500), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    log: Mapped[ActivityLog] = relationship("ActivityLog", back_populates="documents")


__all__ = ["ActivityLog", "DocumentArtifact"]
