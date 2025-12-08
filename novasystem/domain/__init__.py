"""
NovaSystem Domain Layer

Event-driven architecture components for the repository processing system.
"""

from .events import (
    Event,
    EventBus,
    # Run events
    RunCreated,
    RunStatusChanged,
    RunCompleted,
    # Pipeline events
    StepStarted,
    StepCompleted,
    StepFailed,
    # Command events
    CommandQueued,
    CommandStarted,
    CommandOutput,
    CommandCompleted,
    # Policy events
    PolicyViolation,
    PolicyOverride,
)
from .state_machine import RunStateMachine
from .models import Run, CommandLog, Documentation, RunStatus

__all__ = [
    # Event Bus
    "Event",
    "EventBus",
    # Run events
    "RunCreated",
    "RunStatusChanged",
    "RunCompleted",
    # Pipeline events
    "StepStarted",
    "StepCompleted",
    "StepFailed",
    # Command events
    "CommandQueued",
    "CommandStarted",
    "CommandOutput",
    "CommandCompleted",
    # Policy events
    "PolicyViolation",
    "PolicyOverride",
    # State Machine
    "RunStateMachine",
    "RunStatus",
    # Models
    "Run",
    "CommandLog",
    "Documentation",
]
