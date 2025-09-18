"""FastAPI application providing the NovaSystem logging API."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from .database import SessionLocal, init_db
from .logging_service import DOCUMENT_DIR, append_to_log_file, create_document_file
from .models import ActivityLog, DocumentArtifact
from .schemas import DocumentCreate, DocumentResponse, LogCreate, LogListResponse, LogResponse


def create_app() -> FastAPI:
    app = FastAPI(title="NovaSystem Logging Service", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def _startup() -> None:  # pragma: no cover - executed by runtime
        init_db()
        DOCUMENT_DIR.mkdir(parents=True, exist_ok=True)

    app.mount("/documents", StaticFiles(directory=DOCUMENT_DIR), name="documents")

    def get_session() -> Session:
        session = SessionLocal()
        try:
            yield session
        finally:
            session.close()

    def serialise_document(document: DocumentArtifact) -> DocumentResponse:
        file_path = Path(document.path) if document.path else None
        download_url = f"/documents/{file_path.name}" if file_path else ""
        return DocumentResponse(
            id=document.id,
            log_id=document.log_id,
            doc_type=document.doc_type,
            title=document.title,
            notes=document.notes,
            created_at=document.created_at,
            download_url=download_url,
        )

    def serialise_log(log: ActivityLog) -> LogResponse:
        documents = [serialise_document(document) for document in log.documents]
        return LogResponse(
            id=log.id,
            created_at=log.created_at,
            activity=log.activity,
            details=log.details,
            tags=log.tags or [],
            metadata=log.metadata or {},
            documents=documents,
        )

    @app.post("/api/logs", response_model=LogResponse, status_code=201)
    def create_log(payload: LogCreate, session: Session = Depends(get_session)) -> LogResponse:
        record = ActivityLog(
            activity=payload.activity,
            details=payload.details,
            tags=payload.tags,
            metadata=payload.metadata,
        )
        session.add(record)
        session.commit()
        session.refresh(record)

        append_to_log_file(
            {
                "id": record.id,
                "activity": record.activity,
                "details": record.details,
                "tags": record.tags,
                "metadata": record.metadata,
                "created_at": record.created_at.isoformat(),
            }
        )

        return serialise_log(record)

    @app.get("/api/logs", response_model=LogListResponse)
    def list_logs(
        session: Session = Depends(get_session),
        search: str | None = Query(None, description="Search across activity and details."),
        tag: str | None = Query(None, description="Filter logs by a tag value."),
        start: datetime | None = Query(None, description="Earliest creation timestamp."),
        end: datetime | None = Query(None, description="Latest creation timestamp."),
        limit: int = Query(100, ge=1, le=500, description="Maximum number of records to return."),
    ) -> LogListResponse:
        query = select(ActivityLog)

        if search:
            like_term = f"%{search.lower()}%"
            query = query.where(
                or_(
                    ActivityLog.activity.ilike(like_term),
                    ActivityLog.details.ilike(like_term),
                )
            )
        if tag:
            query = query.where(ActivityLog.tags.contains([tag]))
        if start:
            query = query.where(ActivityLog.created_at >= start)
        if end:
            query = query.where(ActivityLog.created_at <= end)

        query = query.order_by(ActivityLog.created_at.desc()).limit(limit)

        logs = session.scalars(query).all()
        for log in logs:
            _ = log.documents
        return LogListResponse(items=[serialise_log(log) for log in logs])

    @app.get("/api/logs/{log_id}", response_model=LogResponse)
    def get_log(log_id: int, session: Session = Depends(get_session)) -> LogResponse:
        log = session.get(ActivityLog, log_id)
        if not log:
            raise HTTPException(status_code=404, detail="Log entry not found")
        _ = log.documents
        return serialise_log(log)

    @app.post("/api/logs/{log_id}/documents", response_model=DocumentResponse, status_code=201)
    def create_document(log_id: int, payload: DocumentCreate, session: Session = Depends(get_session)) -> DocumentResponse:
        log = session.get(ActivityLog, log_id)
        if not log:
            raise HTTPException(status_code=404, detail="Log entry not found")

        log_data = {
            "id": log.id,
            "created_at": log.created_at.isoformat(),
            "activity": log.activity,
            "details": log.details,
            "tags": log.tags or [],
            "metadata": log.metadata or {},
        }
        document_path = create_document_file(payload.doc_type, log_data, payload.notes)
        document = DocumentArtifact(
            log_id=log.id,
            doc_type=payload.doc_type,
            title=f"{payload.doc_type.replace('_', ' ').title()} for log {log.id}",
            notes=payload.notes,
            path=str(document_path),
        )
        session.add(document)
        session.commit()
        session.refresh(document)

        return DocumentResponse(
            id=document.id,
            log_id=log.id,
            doc_type=document.doc_type,
            title=document.title,
            notes=document.notes,
            created_at=document.created_at,
            download_url=f"/documents/{document_path.name}",
        )

    @app.get("/api/documents", response_model=list[DocumentResponse])
    def list_documents(session: Session = Depends(get_session)) -> list[DocumentResponse]:
        documents = session.scalars(select(DocumentArtifact).order_by(DocumentArtifact.created_at.desc())).all()
        return [serialise_document(document) for document in documents]

    @app.get("/api/documents/{document_id}")
    def download_document(document_id: int, session: Session = Depends(get_session)) -> FileResponse:
        document = session.get(DocumentArtifact, document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        file_path = Path(document.path)
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Document file missing")
        return FileResponse(file_path, media_type="text/markdown", filename=file_path.name)

    return app


app = create_app()
