"""
Session data models for NovaSystem.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

@dataclass
class Message:
    """Represents a single message in a session."""
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Create message from dictionary."""
        return cls(
            role=data["role"],
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata", {})
        )

@dataclass
class SessionMetadata:
    """Metadata for a session."""
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    model_used: Optional[str] = None
    total_tokens: int = 0
    total_messages: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    custom_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary."""
        return {
            "session_id": self.session_id,
            "title": self.title,
            "description": self.description,
            "tags": self.tags,
            "model_used": self.model_used,
            "total_tokens": self.total_tokens,
            "total_messages": self.total_messages,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "custom_metadata": self.custom_metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SessionMetadata':
        """Create metadata from dictionary."""
        return cls(
            session_id=data["session_id"],
            title=data.get("title"),
            description=data.get("description"),
            tags=data.get("tags", []),
            model_used=data.get("model_used"),
            total_tokens=data.get("total_tokens", 0),
            total_messages=data.get("total_messages", 0),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            custom_metadata=data.get("custom_metadata", {})
        )

@dataclass
class Session:
    """Represents a complete session."""
    metadata: SessionMetadata = field(default_factory=SessionMetadata)
    messages: List[Message] = field(default_factory=list)

    def add_message(self, role: str, content: str, **kwargs) -> Message:
        """Add a message to the session."""
        message = Message(role=role, content=content, **kwargs)
        self.messages.append(message)
        self.metadata.total_messages = len(self.messages)
        self.metadata.updated_at = datetime.now()
        return message

    def get_messages_for_llm(self) -> List[Dict[str, str]]:
        """Get messages in format expected by LLM service."""
        return [
            {"role": msg.role, "content": msg.content}
            for msg in self.messages
        ]

    def to_markdown(self) -> str:
        """Convert session to markdown format."""
        lines = []

        # Header
        lines.append(f"# Session: {self.metadata.title or 'Untitled'}")
        lines.append("")

        # Metadata
        if self.metadata.description:
            lines.append(f"**Description:** {self.metadata.description}")
            lines.append("")

        lines.append(f"**Session ID:** {self.metadata.session_id}")
        lines.append(f"**Created:** {self.metadata.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Updated:** {self.metadata.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Messages:** {self.metadata.total_messages}")
        lines.append(f"**Tokens:** {self.metadata.total_tokens}")

        if self.metadata.model_used:
            lines.append(f"**Model:** {self.metadata.model_used}")

        if self.metadata.tags:
            lines.append(f"**Tags:** {', '.join(self.metadata.tags)}")

        lines.append("")
        lines.append("---")
        lines.append("")

        # Messages
        for i, message in enumerate(self.messages, 1):
            lines.append(f"## Message {i} - {message.role.title()}")
            lines.append(f"*{message.timestamp.strftime('%Y-%m-%d %H:%M:%S')}*")
            lines.append("")
            lines.append(message.content)
            lines.append("")

            # Add metadata if present
            if message.metadata:
                lines.append("**Metadata:**")
                for key, value in message.metadata.items():
                    lines.append(f"- {key}: {value}")
                lines.append("")

        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary."""
        return {
            "metadata": self.metadata.to_dict(),
            "messages": [msg.to_dict() for msg in self.messages]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Session':
        """Create session from dictionary."""
        session = cls()
        session.metadata = SessionMetadata.from_dict(data["metadata"])
        session.messages = [Message.from_dict(msg) for msg in data["messages"]]
        return session
