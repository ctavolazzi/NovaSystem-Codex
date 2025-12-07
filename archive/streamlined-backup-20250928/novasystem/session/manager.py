"""
Session Manager for NovaSystem.

Handles session creation, storage, and retrieval.
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

from .models import Session, SessionMetadata, Message
from ..config import get_config

logger = logging.getLogger(__name__)

class SessionManager:
    """Manages NovaSystem sessions."""

    def __init__(self, session_dir: Optional[str] = None):
        """Initialize session manager."""
        self.config = get_config()
        self.session_dir = Path(session_dir) if session_dir else self.config.get_session_dir()
        self.session_dir.mkdir(parents=True, exist_ok=True)

        # Current active session
        self._current_session: Optional[Session] = None

        logger.info(f"SessionManager initialized with directory: {self.session_dir}")

    def create_session(self,
                      title: Optional[str] = None,
                      description: Optional[str] = None,
                      tags: Optional[List[str]] = None,
                      custom_metadata: Optional[Dict[str, Any]] = None) -> Session:
        """Create a new session."""
        metadata = SessionMetadata(
            title=title,
            description=description,
            tags=tags or [],
            custom_metadata=custom_metadata or {}
        )

        session = Session(metadata=metadata)
        self._current_session = session

        logger.info(f"Created new session: {metadata.session_id}")
        return session

    def get_current_session(self) -> Optional[Session]:
        """Get the current active session."""
        return self._current_session

    def set_current_session(self, session: Session):
        """Set the current active session."""
        self._current_session = session
        logger.info(f"Set current session: {session.metadata.session_id}")

    def add_message(self,
                   role: str,
                   content: str,
                   session: Optional[Session] = None,
                   **kwargs) -> Message:
        """Add a message to a session."""
        target_session = session or self._current_session

        if target_session is None:
            # Create a new session if none exists
            target_session = self.create_session()

        message = target_session.add_message(role, content, **kwargs)

        # Auto-save if enabled
        if self.config.session.auto_save_sessions:
            self.save_session(target_session)

        return message

    def save_session(self, session: Optional[Session] = None, custom_path: Optional[str] = None) -> Path:
        """Save a session to disk."""
        target_session = session or self._current_session

        if target_session is None:
            raise ValueError("No session to save")

        # Determine file path
        if custom_path:
            file_path = Path(custom_path)
        else:
            timestamp = target_session.metadata.created_at.strftime("%Y%m%d_%H%M%S")
            session_id = target_session.metadata.session_id[:8]  # Short ID
            filename = f"session_{timestamp}_{session_id}.md"
            file_path = self.session_dir / filename

        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Save as markdown
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(target_session.to_markdown())

            logger.info(f"Saved session to: {file_path}")
            return file_path

        except Exception as e:
            logger.error(f"Failed to save session: {e}")
            raise

    def save_session_json(self, session: Optional[Session] = None, custom_path: Optional[str] = None) -> Path:
        """Save a session as JSON."""
        target_session = session or self._current_session

        if target_session is None:
            raise ValueError("No session to save")

        # Determine file path
        if custom_path:
            file_path = Path(custom_path)
        else:
            timestamp = target_session.metadata.created_at.strftime("%Y%m%d_%H%M%S")
            session_id = target_session.metadata.session_id[:8]
            filename = f"session_{timestamp}_{session_id}.json"
            file_path = self.session_dir / filename

        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Save as JSON
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(target_session.to_dict(), f, indent=2, ensure_ascii=False)

            logger.info(f"Saved session JSON to: {file_path}")
            return file_path

        except Exception as e:
            logger.error(f"Failed to save session JSON: {e}")
            raise

    def load_session(self, file_path: str) -> Session:
        """Load a session from file."""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Session file not found: {file_path}")

        try:
            if path.suffix.lower() == '.json':
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                session = Session.from_dict(data)
            else:
                # Try to parse as markdown (basic implementation)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                session = self._parse_markdown_session(content)

            logger.info(f"Loaded session: {session.metadata.session_id}")
            return session

        except Exception as e:
            logger.error(f"Failed to load session: {e}")
            raise

    def list_sessions(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """List all available sessions."""
        sessions = []

        # Find all session files
        for file_path in self.session_dir.glob("session_*.md"):
            try:
                # Extract metadata from filename
                parts = file_path.stem.split('_')
                if len(parts) >= 3:
                    timestamp_str = f"{parts[1]}_{parts[2]}"
                    session_id = parts[3] if len(parts) > 3 else "unknown"

                    # Get file stats
                    stat = file_path.stat()

                    sessions.append({
                        "file_path": str(file_path),
                        "session_id": session_id,
                        "created_at": datetime.fromtimestamp(stat.st_ctime),
                        "modified_at": datetime.fromtimestamp(stat.st_mtime),
                        "size_bytes": stat.st_size,
                        "filename": file_path.name
                    })
            except Exception as e:
                logger.warning(f"Failed to process session file {file_path}: {e}")

        # Sort by creation time (newest first)
        sessions.sort(key=lambda x: x["created_at"], reverse=True)

        if limit:
            sessions = sessions[:limit]

        return sessions

    def get_session_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get a summary of a specific session."""
        sessions = self.list_sessions()

        for session_info in sessions:
            if session_info["session_id"] == session_id:
                try:
                    session = self.load_session(session_info["file_path"])
                    return {
                        "session_id": session.metadata.session_id,
                        "title": session.metadata.title,
                        "description": session.metadata.description,
                        "tags": session.metadata.tags,
                        "model_used": session.metadata.model_used,
                        "total_messages": session.metadata.total_messages,
                        "total_tokens": session.metadata.total_tokens,
                        "created_at": session.metadata.created_at,
                        "updated_at": session.metadata.updated_at,
                        "file_path": session_info["file_path"]
                    }
                except Exception as e:
                    logger.warning(f"Failed to load session {session_id}: {e}")
                    return None

        return None

    def _parse_markdown_session(self, content: str) -> Session:
        """Parse a markdown session file (basic implementation)."""
        # This is a basic implementation - could be enhanced
        lines = content.split('\n')

        # Extract metadata from header
        title = None
        session_id = None
        created_at = None

        for line in lines[:20]:  # Check first 20 lines for metadata
            if line.startswith("# Session:"):
                title = line.replace("# Session:", "").strip()
            elif line.startswith("**Session ID:**"):
                session_id = line.replace("**Session ID:**", "").strip()
            elif line.startswith("**Created:**"):
                created_str = line.replace("**Created:**", "").strip()
                try:
                    created_at = datetime.strptime(created_str, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    created_at = datetime.now()

        # Create session
        metadata = SessionMetadata(
            session_id=session_id or str(uuid.uuid4()),
            title=title,
            created_at=created_at or datetime.now()
        )

        session = Session(metadata=metadata)

        # Parse messages (basic implementation)
        current_message = None
        for line in lines:
            if line.startswith("## Message"):
                if current_message:
                    session.add_message(
                        current_message["role"],
                        current_message["content"]
                    )

                # Extract role from message header
                role = "user"  # default
                if "assistant" in line.lower():
                    role = "assistant"
                elif "system" in line.lower():
                    role = "system"

                current_message = {"role": role, "content": ""}
            elif current_message and not line.startswith("#") and not line.startswith("*"):
                if line.strip():
                    current_message["content"] += line + "\n"

        # Add last message
        if current_message:
            session.add_message(
                current_message["role"],
                current_message["content"].strip()
            )

        return session

    def cleanup_old_sessions(self, days: Optional[int] = None):
        """Clean up old sessions based on retention policy."""
        if days is None:
            days = self.config.session.session_retention_days

        if days <= 0:
            return  # Keep forever

        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        sessions = self.list_sessions()

        for session_info in sessions:
            if session_info["created_at"].timestamp() < cutoff_date:
                try:
                    Path(session_info["file_path"]).unlink()
                    logger.info(f"Deleted old session: {session_info['filename']}")
                except Exception as e:
                    logger.warning(f"Failed to delete old session {session_info['filename']}: {e}")

# Global session manager instance
_session_manager: Optional[SessionManager] = None

def get_session_manager(session_dir: Optional[str] = None) -> SessionManager:
    """Get the global session manager instance."""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager(session_dir)
    return _session_manager
