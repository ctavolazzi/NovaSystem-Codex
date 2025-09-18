"""Logging service utilities for activity tracking and document generation."""
from __future__ import annotations

import copy
import json
import os
import threading
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from queue import Queue
from tempfile import NamedTemporaryFile
from typing import Any, Callable, Dict

from . import crud
from .database import DATA_DIR

LOG_FILE_PATH = Path(
    os.environ.get("NOVASYSTEM_LOG_FILE", DATA_DIR / "activity.log.jsonl")
).resolve()
DOCUMENT_DIR = Path(
    os.environ.get("NOVASYSTEM_DOCUMENT_DIR", DATA_DIR / "documents")
).resolve()
DOCUMENT_DIR.mkdir(parents=True, exist_ok=True)


@dataclass(slots=True)
class DocumentJob:
    """In-memory representation of a queued document generation request."""

    job_id: str
    log_data: dict[str, Any]
    doc_type: str
    notes: str | None


class LoggingService:
    """High level orchestration for log persistence and document generation."""

    def __init__(
        self,
        session_factory: Callable[[], Any],
        *,
        log_file: Path | None = None,
        document_dir: Path | None = None,
    ) -> None:
        self.log_file = (log_file or LOG_FILE_PATH).resolve()
        self.document_dir = (document_dir or DOCUMENT_DIR).resolve()
        self.document_dir.mkdir(parents=True, exist_ok=True)

        self._session_factory = session_factory
        self._job_queue: Queue[DocumentJob] = Queue()
        self._jobs: dict[str, Dict[str, Any]] = {}
        self._jobs_lock = threading.Lock()
        self._job_event_handler: Callable[[dict[str, Any]], None] | None = None

        self._worker_thread = threading.Thread(
            target=self._process_document_jobs,
            name="nova-document-worker",
            daemon=True,
        )
        self._worker_thread.start()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def record_log_entry(self, log_entry: dict[str, Any]) -> dict[str, Any]:
        """Append an activity entry to the JSONL log file atomically.

        The provided ``log_entry`` is expected to contain serialisable data.
        The method enriches it with a ``recorded_at`` timestamp and writes the
        entry to disk using an atomic append strategy.
        """

        enriched = {
            "recorded_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            **log_entry,
        }
        serialised = json.dumps(enriched, ensure_ascii=False)
        self._atomic_append(serialised + "\n")
        return enriched

    def enqueue_document_generation(
        self, log_data: dict[str, Any], doc_type: str, notes: str | None
    ) -> dict[str, Any]:
        """Queue a new document generation job and return its initial status."""

        job_id = uuid.uuid4().hex
        job = DocumentJob(job_id=job_id, log_data=log_data, doc_type=doc_type, notes=notes)

        initial_state = {
            "job_id": job_id,
            "status": "queued",
            "log_id": log_data.get("id"),
            "doc_type": doc_type,
            "notes": notes,
            "document": None,
            "error": None,
        }
        with self._jobs_lock:
            self._jobs[job_id] = initial_state
        self._notify_job_update(job_id)
        self._job_queue.put(job)
        return copy.deepcopy(initial_state)

    def get_job_status(self, job_id: str) -> dict[str, Any] | None:
        """Return the most recent snapshot of a queued job."""

        with self._jobs_lock:
            job = self._jobs.get(job_id)
            return copy.deepcopy(job) if job else None

    def set_job_event_handler(self, handler: Callable[[dict[str, Any]], None] | None) -> None:
        """Register a callback to be notified whenever job status changes."""

        self._job_event_handler = handler

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _atomic_append(self, payload: str) -> None:
        """Append ``payload`` to the log file using ``O_APPEND`` semantics."""

        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(
            self.log_file,
            os.O_CREAT | os.O_WRONLY | os.O_APPEND,
            0o644,
        )
        try:
            with os.fdopen(fd, "ab", closefd=True) as handle:
                handle.write(payload.encode("utf-8"))
        finally:
            # ``os.fdopen`` closes ``fd`` when exiting the context manager.
            pass

    def _process_document_jobs(self) -> None:
        """Background worker that processes document generation requests."""

        while True:
            job = self._job_queue.get()
            if job is None:  # pragma: no cover - defensive; not used currently.
                continue

            self._update_job_state(job.job_id, status="processing", error=None)

            try:
                document_path = create_document_file(
                    job.doc_type,
                    job.log_data,
                    job.notes,
                    base_dir=self.document_dir,
                )
                document_info = self._persist_document_metadata(job, document_path)
                self._update_job_state(
                    job.job_id,
                    status="completed",
                    document=document_info,
                    error=None,
                )
            except Exception as exc:  # pragma: no cover - logged via handler/traceback
                self._update_job_state(
                    job.job_id,
                    status="failed",
                    error=str(exc),
                )

            self._job_queue.task_done()

    def _persist_document_metadata(
        self, job: DocumentJob, file_path: Path
    ) -> dict[str, Any]:
        """Persist generated document metadata to the database."""

        session = self._session_factory()
        try:
            log_id = job.log_data.get("id")
            log = crud.get_activity_log(session, log_id, with_documents=False)
            if log is None:
                raise RuntimeError(f"Log entry {log_id} no longer exists")

            document = crud.create_document_artifact(
                session,
                log_id=log.id,
                doc_type=job.doc_type,
                title=self._format_document_title(job),
                notes=job.notes,
                path=str(file_path),
            )

            return {
                "id": document.id,
                "log_id": document.log_id,
                "doc_type": document.doc_type,
                "title": document.title,
                "notes": document.notes,
                "path": document.path,
                "created_at": document.created_at,
            }
        finally:
            session.close()

    def _format_document_title(self, job: DocumentJob) -> str:
        activity = job.log_data.get("activity")
        doc_label = job.doc_type.replace("_", " ").title()
        if activity:
            return f"{doc_label}: {activity[:60]}"
        return f"{doc_label} for log {job.log_data.get('id')}"

    def _update_job_state(
        self,
        job_id: str,
        *,
        status: str,
        document: dict[str, Any] | None = None,
        error: str | None,
    ) -> None:
        with self._jobs_lock:
            state = self._jobs.setdefault(job_id, {
                "job_id": job_id,
                "status": status,
                "document": None,
                "error": error,
            })
            state["status"] = status
            if document is not None:
                state["document"] = document
            if error is not None:
                state["error"] = error
        self._notify_job_update(job_id)

    def _notify_job_update(self, job_id: str) -> None:
        if not self._job_event_handler:
            return
        snapshot = self.get_job_status(job_id)
        if snapshot is not None:
            try:
                self._job_event_handler(snapshot)
            except Exception:
                # Best-effort notification; errors are intentionally suppressed to
                # avoid terminating the worker thread.
                pass


def build_document_content(
    doc_type: str, log_entry: dict[str, Any], notes: str | None
) -> str:
    """Create human-readable content for generated documents."""

    created_at = log_entry.get("created_at")
    created_str = created_at if isinstance(created_at, str) else str(created_at)
    header = f"# {doc_type.replace('_', ' ').title()}\n\n"
    summary = (
        f"- **Log ID:** {log_entry.get('id')}\n"
        f"- **Created:** {created_str}\n"
        f"- **Activity:** {log_entry.get('activity')}\n"
    )
    details = log_entry.get("details")
    if details:
        summary += f"- **Details:** {details}\n"
    tags = log_entry.get("tags") or []
    if tags:
        summary += f"- **Tags:** {', '.join(tags)}\n"
    metadata = log_entry.get("metadata") or {}
    if metadata:
        metadata_lines = "\n".join(
            f"    - {key}: {value}" for key, value in metadata.items()
        )
        summary += f"- **Metadata:**\n{metadata_lines}\n"

    sections = [
        header,
        summary,
        "\n## Notes\n",
        (notes or "No additional notes supplied.") + "\n",
    ]
    sections.append(
        "\n## Next Steps\n- [ ] Define follow-up tasks\n- [ ] Capture dependencies\n- [ ] Update the main activity log if plans change\n",
    )
    return "".join(sections)


def create_document_file(
    doc_type: str,
    log_entry: dict[str, Any],
    notes: str | None,
    *,
    base_dir: Path | None = None,
) -> Path:
    """Generate a markdown document for the log entry and return the file path."""

    target_dir = (base_dir or DOCUMENT_DIR).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    file_name = f"log-{log_entry.get('id')}-{doc_type}-{timestamp}.md"
    destination = target_dir / file_name
    content = build_document_content(doc_type, log_entry, notes)

    with NamedTemporaryFile("w", encoding="utf-8", dir=target_dir, delete=False) as tmp_file:
        tmp_file.write(content)
        tmp_path = Path(tmp_file.name)
    tmp_path.replace(destination)
    return destination


__all__ = [
    "LoggingService",
    "LOG_FILE_PATH",
    "DOCUMENT_DIR",
    "build_document_content",
    "create_document_file",
]
