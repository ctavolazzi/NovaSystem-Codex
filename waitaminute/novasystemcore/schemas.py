"""Pydantic schemas for the logging service API."""
from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


class DocumentCreate(BaseModel):
    doc_type: str = Field(..., description="Type of document to generate, e.g. 'work_summary'.")
    notes: str | None = Field(None, description="Optional notes to embed in the generated document.")


class DocumentResponse(BaseModel):
    id: int
    log_id: int
    doc_type: str
    title: str
    notes: str | None
    created_at: datetime
    download_url: str


class DocumentJobStatus(BaseModel):
    job_id: str
    status: Literal["queued", "processing", "completed", "failed"]
    document: DocumentResponse | None = Field(
        None, description="Document metadata when the job has completed successfully."
    )
    error: str | None = Field(None, description="Error information if the job failed.")


class LogCreate(BaseModel):
    activity: str = Field(..., min_length=1, description="Short description of the activity performed.")
    details: str | None = Field(None, description="Extended narrative or supporting information.")
    tags: list[str] = Field(default_factory=list, description="Optional tags to classify the activity.")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional structured metadata.")

    @field_validator("tags", mode="before")
    def _normalise_tags(cls, value: Any) -> list[str]:
        if isinstance(value, str):
            return [t.strip() for t in value.split(",") if t.strip()]
        return list(value or [])


class LogResponse(BaseModel):
    id: int
    created_at: datetime
    activity: str
    details: str | None
    tags: list[str]
    metadata: dict[str, Any]
    documents: list[DocumentResponse] = Field(default_factory=list)


class LogListResponse(BaseModel):
    items: list[LogResponse]


class LogHistoryBucket(BaseModel):
    day: date = Field(..., description="UTC date for the aggregated bucket")
    count: int = Field(..., ge=0, description="Number of logs created on this day")


class LogHistoryResponse(BaseModel):
    buckets: list[LogHistoryBucket] = Field(
        default_factory=list, description="Time ordered collection of activity counts"
    )
    total: int = Field(..., ge=0, description="Total count of logs covered by the query")


__all__ = [
    "DocumentCreate",
    "DocumentResponse",
    "DocumentJobStatus",
    "LogCreate",
    "LogResponse",
    "LogListResponse",
    "LogHistoryBucket",
    "LogHistoryResponse",
]
