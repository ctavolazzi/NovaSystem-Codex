"""
Event Bus and Event Types for NovaSystem.

This module implements the Observer pattern, allowing components to subscribe
to and emit events without direct coupling. The Event Bus is the central
nervous system that connects:
- CLI (display progress)
- Database (persist state)
- Web Dashboard (real-time updates)
- Future: WebSocket reporters, metrics collectors

Events are immutable dataclasses that capture what happened in the system.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Type, Union
from collections import defaultdict
import threading

logger = logging.getLogger(__name__)


# =============================================================================
# BASE EVENT
# =============================================================================

@dataclass(frozen=True)
class Event:
    """
    Base class for all events.

    All events are immutable (frozen=True) and include a timestamp.
    Subclasses should define additional fields relevant to the event.
    """
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def event_type(self) -> str:
        """Return the event type name."""
        return self.__class__.__name__


# =============================================================================
# RUN LIFECYCLE EVENTS
# =============================================================================

@dataclass(frozen=True)
class RunCreated(Event):
    """Emitted when a new run is created."""
    run_id: int = 0
    repo_url: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RunStatusChanged(Event):
    """Emitted when a run's status changes."""
    run_id: int = 0
    old_status: str = ""
    new_status: str = ""
    reason: str = ""


@dataclass(frozen=True)
class RunCompleted(Event):
    """Emitted when a run finishes (success or failure)."""
    run_id: int = 0
    success: bool = False
    summary: str = ""
    execution_time: float = 0.0


# =============================================================================
# PIPELINE EVENTS
# =============================================================================

class PipelineStep(str, Enum):
    """Pipeline step identifiers."""
    CLONE = "clone"
    DETECT_STRATEGY = "detect_strategy"
    DISCOVER_DOCS = "discover_docs"
    PARSE_COMMANDS = "parse_commands"
    VALIDATE_COMMANDS = "validate_commands"
    EXECUTE = "execute"
    SUMMARIZE = "summarize"


@dataclass(frozen=True)
class StepStarted(Event):
    """Emitted when a pipeline step begins."""
    run_id: int = 0
    step_name: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class StepCompleted(Event):
    """Emitted when a pipeline step completes successfully."""
    run_id: int = 0
    step_name: str = ""
    result: Any = None
    duration: float = 0.0


@dataclass(frozen=True)
class StepFailed(Event):
    """Emitted when a pipeline step fails."""
    run_id: int = 0
    step_name: str = ""
    error: str = ""
    recoverable: bool = True


# =============================================================================
# COMMAND EVENTS
# =============================================================================

@dataclass(frozen=True)
class CommandQueued(Event):
    """Emitted when a command is added to the execution queue."""
    run_id: int = 0
    command: str = ""
    priority: int = 50
    command_type: str = "shell"


@dataclass(frozen=True)
class CommandStarted(Event):
    """Emitted when command execution begins."""
    run_id: int = 0
    command: str = ""
    container_id: Optional[str] = None


class OutputType(str, Enum):
    """Output stream type."""
    STDOUT = "stdout"
    STDERR = "stderr"


@dataclass(frozen=True)
class CommandOutput(Event):
    """Emitted for command output chunks (enables streaming)."""
    run_id: int = 0
    command: str = ""
    output_type: OutputType = OutputType.STDOUT
    chunk: str = ""


@dataclass(frozen=True)
class CommandCompleted(Event):
    """Emitted when command execution finishes."""
    run_id: int = 0
    command: str = ""
    exit_code: int = 0
    output: str = ""
    error: str = ""
    execution_time: float = 0.0


# =============================================================================
# POLICY EVENTS
# =============================================================================

@dataclass(frozen=True)
class PolicyViolation(Event):
    """Emitted when a command violates a security policy."""
    run_id: int = 0
    command: str = ""
    policy_name: str = ""
    reason: str = ""
    severity: str = "warning"  # "warning", "error", "critical"


@dataclass(frozen=True)
class PolicyOverride(Event):
    """Emitted when a user overrides a policy violation."""
    run_id: int = 0
    command: str = ""
    policy_name: str = ""
    user: str = ""
    justification: str = ""


# =============================================================================
# STRATEGY EVENTS
# =============================================================================

@dataclass(frozen=True)
class StrategyDetected(Event):
    """Emitted when a repository strategy is detected."""
    run_id: int = 0
    strategy_name: str = ""
    confidence: float = 1.0
    detected_files: List[str] = field(default_factory=list)


# =============================================================================
# EVENT BUS
# =============================================================================

# Type alias for event handlers
EventHandler = Callable[[Event], None]


class EventBus:
    """
    Central event bus implementing the Observer pattern.

    Features:
    - Subscribe to specific event types or all events
    - Synchronous event emission (async can be added later)
    - Thread-safe operation
    - Event history for debugging
    - Wildcard subscriptions

    Usage:
        bus = EventBus()

        # Subscribe to specific event
        bus.subscribe(RunCreated, lambda e: print(f"Run {e.run_id} created"))

        # Subscribe to all events
        bus.subscribe_all(lambda e: db.log_event(e))

        # Emit event
        bus.emit(RunCreated(run_id=1, repo_url="https://github.com/..."))
    """

    _instance: Optional["EventBus"] = None
    _lock = threading.Lock()

    def __new__(cls) -> "EventBus":
        """Singleton pattern - one event bus per application."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the event bus."""
        if self._initialized:
            return

        self._handlers: Dict[Type[Event], List[EventHandler]] = defaultdict(list)
        self._global_handlers: List[EventHandler] = []
        self._history: List[Event] = []
        self._max_history: int = 1000
        self._enabled: bool = True
        self._lock = threading.Lock()
        self._initialized = True

        logger.info("EventBus initialized")

    def subscribe(self, event_type: Type[Event], handler: EventHandler) -> None:
        """
        Subscribe to a specific event type.

        Args:
            event_type: The event class to subscribe to
            handler: Callback function that receives the event
        """
        with self._lock:
            self._handlers[event_type].append(handler)
            logger.debug(f"Subscribed handler to {event_type.__name__}")

    def subscribe_all(self, handler: EventHandler) -> None:
        """
        Subscribe to all events.

        Args:
            handler: Callback function that receives all events
        """
        with self._lock:
            self._global_handlers.append(handler)
            logger.debug("Subscribed global handler")

    def unsubscribe(self, event_type: Type[Event], handler: EventHandler) -> bool:
        """
        Unsubscribe a handler from an event type.

        Args:
            event_type: The event class to unsubscribe from
            handler: The handler to remove

        Returns:
            True if handler was found and removed
        """
        with self._lock:
            handlers = self._handlers.get(event_type, [])
            if handler in handlers:
                handlers.remove(handler)
                return True
            return False

    def unsubscribe_all(self, handler: EventHandler) -> bool:
        """
        Unsubscribe a global handler.

        Args:
            handler: The handler to remove

        Returns:
            True if handler was found and removed
        """
        with self._lock:
            if handler in self._global_handlers:
                self._global_handlers.remove(handler)
                return True
            return False

    def emit(self, event: Event) -> None:
        """
        Emit an event to all subscribers.

        Args:
            event: The event to emit
        """
        if not self._enabled:
            return

        # Add to history
        with self._lock:
            self._history.append(event)
            if len(self._history) > self._max_history:
                self._history = self._history[-self._max_history:]

        logger.debug(f"Emitting {event.event_type}: {event}")

        # Notify type-specific handlers
        handlers = self._handlers.get(type(event), [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Error in event handler for {event.event_type}: {e}")

        # Notify global handlers
        for handler in self._global_handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Error in global event handler: {e}")

    def get_history(self,
                   event_type: Optional[Type[Event]] = None,
                   run_id: Optional[int] = None,
                   limit: int = 100) -> List[Event]:
        """
        Get event history with optional filtering.

        Args:
            event_type: Filter by event type
            run_id: Filter by run ID
            limit: Maximum events to return

        Returns:
            List of matching events (most recent first)
        """
        with self._lock:
            events = list(reversed(self._history))

            if event_type:
                events = [e for e in events if isinstance(e, event_type)]

            if run_id is not None:
                events = [e for e in events if getattr(e, "run_id", None) == run_id]

            return events[:limit]

    def clear_history(self) -> None:
        """Clear event history."""
        with self._lock:
            self._history.clear()

    def enable(self) -> None:
        """Enable event emission."""
        self._enabled = True

    def disable(self) -> None:
        """Disable event emission (useful for testing)."""
        self._enabled = False

    def reset(self) -> None:
        """Reset the event bus (clear all handlers and history)."""
        with self._lock:
            self._handlers.clear()
            self._global_handlers.clear()
            self._history.clear()
        logger.info("EventBus reset")

    @classmethod
    def get_instance(cls) -> "EventBus":
        """Get the singleton instance."""
        return cls()

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance (for testing)."""
        with cls._lock:
            if cls._instance:
                cls._instance.reset()
                cls._instance = None


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def get_event_bus() -> EventBus:
    """Get the global event bus instance."""
    return EventBus.get_instance()


def emit(event: Event) -> None:
    """Emit an event on the global bus."""
    get_event_bus().emit(event)


def subscribe(event_type: Type[Event], handler: EventHandler) -> None:
    """Subscribe to an event type on the global bus."""
    get_event_bus().subscribe(event_type, handler)


def subscribe_all(handler: EventHandler) -> None:
    """Subscribe to all events on the global bus."""
    get_event_bus().subscribe_all(handler)
