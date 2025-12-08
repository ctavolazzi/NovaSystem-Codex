"""
Domain Models for NovaSystem.

These are typed value objects that replace ad-hoc dictionaries,
providing type safety and reducing coupling to the database layer.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class RunStatus(str, Enum):
    """Run status states."""
    PENDING = "pending"
    ANALYZING = "analyzing"
    GATED = "gated"  # Awaiting user decision on policy violation
    RUNNING = "running"
    PAUSED = "paused"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ARCHIVED = "archived"
    ERROR = "error"

    @property
    def is_terminal(self) -> bool:
        """Check if this is a terminal state."""
        return self in {
            RunStatus.SUCCESS,
            RunStatus.FAILED,
            RunStatus.CANCELLED,
            RunStatus.ARCHIVED,
            RunStatus.ERROR,
        }

    @property
    def is_active(self) -> bool:
        """Check if this is an active state."""
        return self in {
            RunStatus.PENDING,
            RunStatus.ANALYZING,
            RunStatus.RUNNING,
        }


class CommandStatus(str, Enum):
    """Command execution status."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    BLOCKED = "blocked"  # Blocked by policy


@dataclass
class Run:
    """
    Domain model for a repository processing run.

    This replaces ad-hoc dictionaries from DatabaseManager.get_run().
    """
    id: int
    repo_url: str
    status: RunStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    success: Optional[bool] = None
    summary: Optional[str] = None
    repository_type: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Run":
        """Create Run from database row dictionary."""
        return cls(
            id=data["id"],
            repo_url=data["repo_url"],
            status=RunStatus(data.get("status", "pending")),
            start_time=datetime.fromisoformat(data["start_time"]) if isinstance(data["start_time"], str) else data["start_time"],
            end_time=datetime.fromisoformat(data["end_time"]) if data.get("end_time") and isinstance(data["end_time"], str) else data.get("end_time"),
            success=data.get("success"),
            summary=data.get("summary"),
            repository_type=data.get("repository_type"),
            metadata=data.get("metadata", {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage."""
        return {
            "id": self.id,
            "repo_url": self.repo_url,
            "status": self.status.value,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "success": self.success,
            "summary": self.summary,
            "repository_type": self.repository_type,
            "metadata": self.metadata,
        }

    @property
    def duration(self) -> Optional[float]:
        """Calculate run duration in seconds."""
        if self.end_time and self.start_time:
            return (self.end_time - self.start_time).total_seconds()
        return None


@dataclass
class CommandLog:
    """
    Domain model for a command execution log.

    This replaces ad-hoc dictionaries from DatabaseManager.get_commands().
    """
    id: int
    run_id: int
    command: str
    status: CommandStatus
    timestamp: datetime
    exit_code: Optional[int] = None
    output: Optional[str] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None
    command_type: Optional[str] = None
    priority: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CommandLog":
        """Create CommandLog from database row dictionary."""
        status_str = data.get("status", "pending")
        # Map old status values to new enum
        status_map = {
            "completed": CommandStatus.SUCCESS,
            "success": CommandStatus.SUCCESS,
            "failed": CommandStatus.FAILED,
            "error": CommandStatus.FAILED,
            "pending": CommandStatus.PENDING,
            "running": CommandStatus.RUNNING,
            "skipped": CommandStatus.SKIPPED,
            "blocked": CommandStatus.BLOCKED,
        }
        status = status_map.get(status_str, CommandStatus.PENDING)

        return cls(
            id=data["id"],
            run_id=data["run_id"],
            command=data["command"],
            status=status,
            timestamp=datetime.fromisoformat(data["timestamp"]) if isinstance(data["timestamp"], str) else data["timestamp"],
            exit_code=data.get("exit_code"),
            output=data.get("output"),
            error=data.get("error"),
            execution_time=data.get("execution_time"),
            command_type=data.get("command_type"),
            priority=data.get("priority"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage."""
        return {
            "id": self.id,
            "run_id": self.run_id,
            "command": self.command,
            "status": self.status.value,
            "timestamp": self.timestamp.isoformat(),
            "exit_code": self.exit_code,
            "output": self.output,
            "error": self.error,
            "execution_time": self.execution_time,
            "command_type": self.command_type,
            "priority": self.priority,
        }

    @property
    def successful(self) -> bool:
        """Check if command was successful."""
        return self.status == CommandStatus.SUCCESS and self.exit_code == 0


@dataclass
class Documentation:
    """
    Domain model for documentation file content.

    This replaces ad-hoc dictionaries from DatabaseManager.get_documentation().
    """
    id: int
    run_id: int
    file_path: str
    content: str
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Documentation":
        """Create Documentation from database row dictionary."""
        return cls(
            id=data["id"],
            run_id=data["run_id"],
            file_path=data["file_path"],
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]) if isinstance(data["timestamp"], str) else data["timestamp"],
            metadata=data.get("metadata", {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage."""
        return {
            "id": self.id,
            "run_id": self.run_id,
            "file_path": self.file_path,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class PipelineContext:
    """
    Context passed through pipeline steps.

    Contains all the state needed by pipeline steps and gets
    enriched as the pipeline progresses.
    """
    run_id: int
    repo_url: str
    repo_path: Optional[str] = None
    repository_type: Optional[str] = None
    strategy_name: Optional[str] = None
    doc_files: List[str] = field(default_factory=list)
    commands: List["ParsedCommand"] = field(default_factory=list)
    results: List[CommandLog] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Flags for pipeline control
    should_stop: bool = False
    stop_reason: Optional[str] = None
    awaiting_user_input: bool = False

    def add_metadata(self, key: str, value: Any) -> None:
        """Add or update metadata."""
        self.metadata[key] = value

    def stop(self, reason: str) -> None:
        """Signal the pipeline to stop."""
        self.should_stop = True
        self.stop_reason = reason


@dataclass
class ParsedCommand:
    """
    A command parsed from documentation.

    Simplified version of the parser.Command class for pipeline use.
    """
    text: str
    source: str  # "code_block", "inline_code", "llm_extracted"
    command_type: str = "shell"
    context: str = ""
    line_number: Optional[int] = None
    file_path: Optional[str] = None
    priority: int = 50

    # Policy validation results
    policy_violations: List[str] = field(default_factory=list)
    allowed: bool = True
