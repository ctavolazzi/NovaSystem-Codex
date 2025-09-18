"""Database helper utilities for NovaSystem core services."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Iterable, Sequence

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from .models import ActivityLog, DocumentArtifact


@dataclass(frozen=True, slots=True)
class HistoryPoint:
    """Represents aggregated activity counts for a single day."""

    day: date
    count: int


def create_activity_log(
    session: Session,
    *,
    activity: str,
    details: str | None = None,
    tags: Sequence[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ActivityLog:
    """Persist a new activity log entry and return the saved model."""

    record = ActivityLog(
        activity=activity,
        details=details,
        tags=list(tags or []),
        metadata=dict(metadata or {}),
    )
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


def update_activity_log(
    session: Session,
    log: ActivityLog,
    *,
    activity: str | None = None,
    details: str | None = None,
    tags: Sequence[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ActivityLog:
    """Update an existing log entry in place."""

    if activity is not None:
        log.activity = activity
    if details is not None:
        log.details = details
    if tags is not None:
        log.tags = list(tags)
    if metadata is not None:
        log.metadata = dict(metadata)

    session.add(log)
    session.commit()
    session.refresh(log)
    return log


def delete_activity_log(session: Session, log: ActivityLog) -> None:
    """Remove a log entry and cascade delete related documents."""

    session.delete(log)
    session.commit()


def get_activity_log(
    session: Session,
    log_id: int,
    *,
    with_documents: bool = True,
) -> ActivityLog | None:
    """Return a single activity log by primary key."""

    if with_documents:
        stmt = (
            select(ActivityLog)
            .options(selectinload(ActivityLog.documents))
            .where(ActivityLog.id == log_id)
        )
        return session.scalars(stmt).first()
    return session.get(ActivityLog, log_id)


def list_activity_logs(
    session: Session,
    *,
    search: str | None = None,
    tag: str | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
    doc_type: str | None = None,
    has_documents: bool | None = None,
    limit: int | None = None,
) -> list[ActivityLog]:
    """Return activity logs filtered by the provided criteria."""

    stmt = (
        select(ActivityLog)
        .options(selectinload(ActivityLog.documents))
        .order_by(ActivityLog.created_at.desc())
    )
    stmt = _apply_log_filters(
        stmt,
        search=search,
        tag=tag,
        start=start,
        end=end,
        doc_type=doc_type,
        has_documents=has_documents,
    )
    if limit:
        stmt = stmt.limit(limit)
    return list(session.scalars(stmt).all())


def _apply_log_filters(
    stmt,
    *,
    search: str | None,
    tag: str | None,
    start: datetime | None,
    end: datetime | None,
    doc_type: str | None,
    has_documents: bool | None,
):
    """Apply shared filtering options for log queries."""

    if search:
        like_term = f"%{search}%"
        stmt = stmt.where(
            or_(
                ActivityLog.activity.ilike(like_term),
                ActivityLog.details.ilike(like_term),
            )
        )
    if tag:
        stmt = stmt.where(ActivityLog.tags.contains([tag]))
    if start:
        stmt = stmt.where(ActivityLog.created_at >= start)
    if end:
        stmt = stmt.where(ActivityLog.created_at <= end)
    if doc_type:
        stmt = stmt.where(ActivityLog.documents.any(DocumentArtifact.doc_type == doc_type))
    if has_documents is True:
        stmt = stmt.where(ActivityLog.documents.any())
    elif has_documents is False:
        stmt = stmt.where(~ActivityLog.documents.any())
    return stmt


def create_document_artifact(
    session: Session,
    *,
    log_id: int,
    doc_type: str,
    title: str,
    path: str,
    notes: str | None = None,
) -> DocumentArtifact:
    """Persist a generated document and link it to the originating log."""

    document = DocumentArtifact(
        log_id=log_id,
        doc_type=doc_type,
        title=title,
        path=path,
        notes=notes,
    )
    session.add(document)
    session.commit()
    session.refresh(document)
    return document


def list_documents(
    session: Session,
    *,
    log_ids: Iterable[int] | None = None,
    doc_type: str | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
    limit: int | None = None,
) -> list[DocumentArtifact]:
    """Fetch generated documents filtered by metadata and time bounds."""

    stmt = select(DocumentArtifact).order_by(DocumentArtifact.created_at.desc())
    if log_ids:
        stmt = stmt.where(DocumentArtifact.log_id.in_(list(log_ids)))
    if doc_type:
        stmt = stmt.where(DocumentArtifact.doc_type == doc_type)
    if start:
        stmt = stmt.where(DocumentArtifact.created_at >= start)
    if end:
        stmt = stmt.where(DocumentArtifact.created_at <= end)
    if limit:
        stmt = stmt.limit(limit)
    return list(session.scalars(stmt).all())


def get_activity_history(
    session: Session,
    *,
    search: str | None = None,
    tag: str | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
    doc_type: str | None = None,
    has_documents: bool | None = None,
) -> list[HistoryPoint]:
    """Aggregate activity counts grouped by day with shared filters."""

    day_column = func.date(ActivityLog.created_at)
    stmt = select(day_column, func.count(ActivityLog.id)).select_from(ActivityLog)
    stmt = _apply_log_filters(
        stmt,
        search=search,
        tag=tag,
        start=start,
        end=end,
        doc_type=doc_type,
        has_documents=has_documents,
    )
    stmt = stmt.group_by(day_column).order_by(day_column)

    history: list[HistoryPoint] = []
    for day_value, count in session.execute(stmt).all():
        if isinstance(day_value, datetime):
            day = day_value.date()
        elif isinstance(day_value, date):
            day = day_value
        else:
            day = date.fromisoformat(str(day_value))
        history.append(HistoryPoint(day=day, count=int(count)))
    return history


__all__ = [
    "HistoryPoint",
    "create_activity_log",
    "update_activity_log",
    "delete_activity_log",
    "get_activity_log",
    "list_activity_logs",
    "create_document_artifact",
    "list_documents",
    "get_activity_history",
]
