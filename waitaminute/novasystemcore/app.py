"""FastAPI application providing the NovaSystem logging API."""
from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Query,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError
from sqlalchemy.orm import Session

from . import crud
from .database import SessionLocal, init_db
from .logging_service import DOCUMENT_DIR, LoggingService
from .models import ActivityLog, DocumentArtifact
from .schemas import (
    DocumentCreate,
    DocumentJobStatus,
    DocumentResponse,
    LogCreate,
    LogHistoryBucket,
    LogHistoryResponse,
    LogListResponse,
    LogResponse,
)

logger = logging.getLogger(__name__)

logging_service = LoggingService(SessionLocal)


class WebSocketManager:
    """Tracks active WebSocket connections for broadcasting events."""

    def __init__(self) -> None:
        self._connections: set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self._connections.add(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self._lock:
            self._connections.discard(websocket)

    async def broadcast(
        self, message: dict[str, Any], *, exclude: WebSocket | None = None
    ) -> None:
        async with self._lock:
            connections = list(self._connections)
        stale: list[WebSocket] = []
        for connection in connections:
            if exclude is not None and connection is exclude:
                continue
            try:
                await connection.send_json(message)
            except RuntimeError:
                stale.append(connection)
        if stale:
            async with self._lock:
                for connection in stale:
                    self._connections.discard(connection)


def create_app() -> FastAPI:
    app = FastAPI(title="NovaSystem Logging Service", version="2.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    manager = WebSocketManager()

    @app.on_event("startup")
    async def _startup() -> None:  # pragma: no cover - executed by runtime
        init_db()
        DOCUMENT_DIR.mkdir(parents=True, exist_ok=True)

        loop = asyncio.get_running_loop()

        def _handle_job_event(job_snapshot: dict[str, Any]) -> None:
            job_status = _format_job_status(job_snapshot)
            message = {
                "event": "document.job.updated",
                "payload": jsonable_encoder(job_status),
            }
            asyncio.run_coroutine_threadsafe(
                manager.broadcast(message), loop
            )

        logging_service.set_job_event_handler(_handle_job_event)

    app.mount("/documents", StaticFiles(directory=DOCUMENT_DIR), name="documents")

    async def get_session() -> Session:
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

    def _format_job_status(job_snapshot: dict[str, Any]) -> DocumentJobStatus:
        document_payload = job_snapshot.get("document")
        document_response: DocumentResponse | None = None
        if document_payload:
            document_response = DocumentResponse(
                id=document_payload["id"],
                log_id=document_payload["log_id"],
                doc_type=document_payload["doc_type"],
                title=document_payload["title"],
                notes=document_payload.get("notes"),
                created_at=document_payload["created_at"],
                download_url=f"/documents/{Path(document_payload['path']).name}",
            )
        return DocumentJobStatus(
            job_id=job_snapshot["job_id"],
            status=job_snapshot["status"],
            document=document_response,
            error=job_snapshot.get("error"),
        )

    @app.post("/api/logs", response_model=LogResponse, status_code=201)
    async def create_log(payload: LogCreate, session: Session = Depends(get_session)) -> LogResponse:
        record = crud.create_activity_log(
            session,
            activity=payload.activity,
            details=payload.details,
            tags=payload.tags,
            metadata=payload.metadata,
        )

        log_data = {
            "id": record.id,
            "activity": record.activity,
            "details": record.details,
            "tags": record.tags,
            "metadata": record.metadata,
            "created_at": record.created_at.isoformat(),
            "source": "rest",
        }
        recorded_entry = logging_service.record_log_entry(log_data)
        await manager.broadcast({"event": "log.recorded", "payload": recorded_entry})

        response_payload = serialise_log(record)
        await manager.broadcast(
            {"event": "log.created", "payload": jsonable_encoder(response_payload)}
        )
        return response_payload

    @app.get("/api/logs", response_model=LogListResponse)
    async def list_logs(
        session: Session = Depends(get_session),
        search: str | None = Query(None, description="Search across activity and details."),
        tag: str | None = Query(None, description="Filter logs by a tag value."),
        start: datetime | None = Query(None, description="Earliest creation timestamp."),
        end: datetime | None = Query(None, description="Latest creation timestamp."),
        doc_type: str | None = Query(
            None,
            description="Require that logs have documents of the specified type.",
        ),
        has_documents: bool | None = Query(
            None,
            description="Filter logs based on whether related documents exist.",
        ),
        limit: int = Query(100, ge=1, le=500, description="Maximum number of records to return."),
    ) -> LogListResponse:
        logs = crud.list_activity_logs(
            session,
            search=search,
            tag=tag,
            start=start,
            end=end,
            doc_type=doc_type,
            has_documents=has_documents,
            limit=limit,
        )
        return LogListResponse(items=[serialise_log(log) for log in logs])

    @app.get("/api/logs/{log_id}", response_model=LogResponse)
    async def get_log(log_id: int, session: Session = Depends(get_session)) -> LogResponse:
        log = crud.get_activity_log(session, log_id)
        if not log:
            raise HTTPException(status_code=404, detail="Log entry not found")
        return serialise_log(log)

    @app.post(
        "/api/logs/{log_id}/documents",
        response_model=DocumentJobStatus,
        status_code=202,
    )
    async def queue_document(
        log_id: int,
        payload: DocumentCreate,
        session: Session = Depends(get_session),
    ) -> DocumentJobStatus:
        log = crud.get_activity_log(session, log_id, with_documents=False)
        if not log:
            raise HTTPException(status_code=404, detail="Log entry not found")

        log_data = {
            "id": log.id,
            "created_at": log.created_at.isoformat(),
            "activity": log.activity,
            "details": log.details,
            "tags": log.tags or [],
            "metadata": log.metadata or {},
            "source": "rest",
        }
        job_snapshot = logging_service.enqueue_document_generation(
            log_data, payload.doc_type, payload.notes
        )
        job_status = _format_job_status(job_snapshot)
        await manager.broadcast(
            {"event": "document.job.queued", "payload": jsonable_encoder(job_status)}
        )
        return job_status

    @app.get("/api/documents", response_model=list[DocumentResponse])
    async def list_documents(
        session: Session = Depends(get_session),
        log_id: int | None = Query(
            None,
            ge=1,
            description="Limit results to documents associated with a specific log entry.",
        ),
        doc_type: str | None = Query(None, description="Filter by the stored document type."),
        start: datetime | None = Query(None, description="Earliest creation timestamp."),
        end: datetime | None = Query(None, description="Latest creation timestamp."),
        limit: int = Query(100, ge=1, le=500, description="Maximum number of records to return."),
    ) -> list[DocumentResponse]:
        documents = crud.list_documents(
            session,
            log_ids=[log_id] if log_id is not None else None,
            doc_type=doc_type,
            start=start,
            end=end,
            limit=limit,
        )
        return [serialise_document(document) for document in documents]

    @app.get("/api/logs/history", response_model=LogHistoryResponse)
    async def logs_history(
        session: Session = Depends(get_session),
        search: str | None = Query(None, description="Search across activity and details."),
        tag: str | None = Query(None, description="Filter logs by a tag value."),
        start: datetime | None = Query(None, description="Earliest creation timestamp."),
        end: datetime | None = Query(None, description="Latest creation timestamp."),
        doc_type: str | None = Query(
            None,
            description="Restrict to logs that have documents of the given type.",
        ),
        has_documents: bool | None = Query(
            None,
            description="Filter logs based on whether related documents exist.",
        ),
    ) -> LogHistoryResponse:
        history = crud.get_activity_history(
            session,
            search=search,
            tag=tag,
            start=start,
            end=end,
            doc_type=doc_type,
            has_documents=has_documents,
        )
        buckets = [
            LogHistoryBucket(day=entry.day, count=entry.count) for entry in history
        ]
        total = sum(bucket.count for bucket in buckets)
        return LogHistoryResponse(buckets=buckets, total=total)

    @app.get("/api/documents/{document_id}")
    async def download_document(document_id: int, session: Session = Depends(get_session)) -> FileResponse:
        document = session.get(DocumentArtifact, document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        file_path = Path(document.path)
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Document file missing")
        return FileResponse(file_path, media_type="text/markdown", filename=file_path.name)

    @app.get(
        "/api/documents/jobs/{job_id}",
        response_model=DocumentJobStatus,
    )
    async def get_document_job(job_id: str) -> DocumentJobStatus:
        job_snapshot = logging_service.get_job_status(job_id)
        if not job_snapshot:
            raise HTTPException(status_code=404, detail="Job not found")
        return _format_job_status(job_snapshot)

    @app.websocket("/ws/logs")
    async def websocket_logs(websocket: WebSocket) -> None:
        await manager.connect(websocket)
        try:
            while True:
                message = await websocket.receive_text()
                try:
                    payload = json.loads(message)
                except json.JSONDecodeError:
                    await websocket.send_json(
                        {"event": "error", "detail": "Invalid JSON payload"}
                    )
                    continue

                try:
                    log_payload = LogCreate.model_validate(payload)
                except ValidationError as exc:
                    await websocket.send_json(
                        {"event": "error", "detail": exc.errors()}
                    )
                    continue

                session = SessionLocal()
                try:
                    record = ActivityLog(
                        activity=log_payload.activity,
                        details=log_payload.details,
                        tags=log_payload.tags,
                        metadata=log_payload.metadata,
                    )
                    session.add(record)
                    session.commit()
                    session.refresh(record)
                except Exception as exc:  # pragma: no cover - runtime safety net
                    session.rollback()
                    logger.exception("Failed to persist log entry via WebSocket", exc_info=exc)
                    await websocket.send_json(
                        {"event": "error", "detail": "Failed to persist log entry"}
                    )
                    continue
                finally:
                    session.close()

                log_data = {
                    "id": record.id,
                    "activity": record.activity,
                    "details": record.details,
                    "tags": record.tags,
                    "metadata": record.metadata,
                    "created_at": record.created_at.isoformat(),
                    "source": "websocket",
                }
                recorded_entry = logging_service.record_log_entry(log_data)
                await websocket.send_json({"event": "log.recorded", "payload": recorded_entry})
                await manager.broadcast(
                    {"event": "log.recorded", "payload": recorded_entry},
                    exclude=websocket,
                )

                response_payload = serialise_log(record)
                await websocket.send_json(
                    {"event": "log.created", "payload": jsonable_encoder(response_payload)}
                )
                await manager.broadcast(
                    {"event": "log.created", "payload": jsonable_encoder(response_payload)},
                    exclude=websocket,
                )
        except WebSocketDisconnect:
            pass
        finally:
            await manager.disconnect(websocket)

    return app


app = create_app()
