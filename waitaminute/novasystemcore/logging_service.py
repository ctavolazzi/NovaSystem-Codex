"""Core logging and document creation helpers."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .database import DATA_DIR

LOG_FILE = DATA_DIR / "activity.log.jsonl"
DOCUMENT_DIR = DATA_DIR / "documents"
DOCUMENT_DIR.mkdir(parents=True, exist_ok=True)


def append_to_log_file(entry: dict[str, Any]) -> None:
    """Append the provided entry to the JSONL log file."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    serialisable = {
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        **entry,
    }
    with LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(serialisable, ensure_ascii=False) + "\n")


def build_document_content(doc_type: str, log_entry: dict[str, Any], notes: str | None) -> str:
    """Create human-readable content for generated documents."""
    created_at = log_entry.get("created_at")
    created_str = created_at if isinstance(created_at, str) else str(created_at)
    header = f"# {doc_type.replace('_', ' ').title()}\n\n"
    summary = f"- **Log ID:** {log_entry['id']}\n- **Created:** {created_str}\n- **Activity:** {log_entry['activity']}\n"
    details = log_entry.get("details")
    if details:
        summary += f"- **Details:** {details}\n"
    tags = log_entry.get("tags") or []
    if tags:
        summary += f"- **Tags:** {', '.join(tags)}\n"
    metadata = log_entry.get("metadata") or {}
    if metadata:
        metadata_lines = "\n".join(f"    - {key}: {value}" for key, value in metadata.items())
        summary += f"- **Metadata:**\n{metadata_lines}\n"

    sections = [header, summary, "\n## Notes\n", (notes or "No additional notes supplied.") + "\n"]
    sections.append("\n## Next Steps\n- [ ] Define follow-up tasks\n- [ ] Capture dependencies\n- [ ] Update the main activity log if plans change\n")
    return "".join(sections)


def create_document_file(doc_type: str, log_entry: dict[str, Any], notes: str | None) -> Path:
    """Generate a markdown document for the log entry and return the file path."""
    DOCUMENT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    file_name = f"log-{log_entry['id']}-{doc_type}-{timestamp}.md"
    file_path = DOCUMENT_DIR / file_name
    content = build_document_content(doc_type, log_entry, notes)
    file_path.write_text(content, encoding="utf-8")
    return file_path


__all__ = ["append_to_log_file", "create_document_file", "LOG_FILE", "DOCUMENT_DIR"]
