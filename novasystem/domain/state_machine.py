"""
State Machine for Run Lifecycle.

Encodes run status transitions to support:
- Pause/resume semantics
- Error recovery
- Clear state management

State Diagram:
    Pending → Analyzing → Gated → Running → Paused → (Finalized)
                           ↓                   ↓
                        (user)              (resume)

Terminal States: Success, Failed, Cancelled, Archived, Error
"""

import logging
from datetime import datetime
from enum import Enum
from typing import Callable, Dict, List, Optional, Set, Tuple

from .models import RunStatus
from .events import EventBus, RunStatusChanged, get_event_bus

logger = logging.getLogger(__name__)


class TransitionError(Exception):
    """Raised when an invalid state transition is attempted."""

    def __init__(self, current: RunStatus, target: RunStatus, reason: str = ""):
        self.current = current
        self.target = target
        self.reason = reason
        message = f"Cannot transition from {current.value} to {target.value}"
        if reason:
            message += f": {reason}"
        super().__init__(message)


class RunStateMachine:
    """
    State machine for run lifecycle management.

    Enforces valid state transitions and emits events on state changes.

    Valid transitions:
        PENDING → ANALYZING
        ANALYZING → GATED, RUNNING, ERROR
        GATED → RUNNING, CANCELLED
        RUNNING → PAUSED, SUCCESS, FAILED, ERROR
        PAUSED → RUNNING, CANCELLED

    Terminal states (no transitions out):
        SUCCESS, FAILED, CANCELLED, ARCHIVED, ERROR

    Usage:
        sm = RunStateMachine(run_id=1)
        sm.transition_to(RunStatus.ANALYZING)
        sm.transition_to(RunStatus.RUNNING)
        sm.transition_to(RunStatus.SUCCESS)
    """

    # Define valid transitions: from_state -> set of valid to_states
    TRANSITIONS: Dict[RunStatus, Set[RunStatus]] = {
        RunStatus.PENDING: {RunStatus.ANALYZING, RunStatus.ERROR, RunStatus.CANCELLED},
        RunStatus.ANALYZING: {RunStatus.GATED, RunStatus.RUNNING, RunStatus.ERROR, RunStatus.CANCELLED},
        RunStatus.GATED: {RunStatus.RUNNING, RunStatus.CANCELLED},
        RunStatus.RUNNING: {RunStatus.PAUSED, RunStatus.SUCCESS, RunStatus.FAILED, RunStatus.ERROR},
        RunStatus.PAUSED: {RunStatus.RUNNING, RunStatus.CANCELLED},
        # Terminal states have no outgoing transitions
        RunStatus.SUCCESS: set(),
        RunStatus.FAILED: set(),
        RunStatus.CANCELLED: set(),
        RunStatus.ARCHIVED: set(),
        RunStatus.ERROR: set(),
    }

    def __init__(self,
                 run_id: int,
                 initial_status: RunStatus = RunStatus.PENDING,
                 event_bus: Optional[EventBus] = None,
                 on_transition: Optional[Callable[[RunStatus, RunStatus], None]] = None):
        """
        Initialize the state machine.

        Args:
            run_id: The run ID this state machine manages
            initial_status: Starting status
            event_bus: Event bus for emitting events (uses global if None)
            on_transition: Optional callback on successful transitions
        """
        self.run_id = run_id
        self._status = initial_status
        self._event_bus = event_bus or get_event_bus()
        self._on_transition = on_transition
        self._history: List[Tuple[RunStatus, RunStatus, datetime]] = []

        logger.debug(f"RunStateMachine initialized for run {run_id} with status {initial_status.value}")

    @property
    def status(self) -> RunStatus:
        """Get current status."""
        return self._status

    @property
    def is_terminal(self) -> bool:
        """Check if current state is terminal."""
        return self._status.is_terminal

    @property
    def is_active(self) -> bool:
        """Check if current state is active."""
        return self._status.is_active

    @property
    def can_resume(self) -> bool:
        """Check if run can be resumed."""
        return self._status == RunStatus.PAUSED

    @property
    def can_pause(self) -> bool:
        """Check if run can be paused."""
        return self._status == RunStatus.RUNNING

    def can_transition_to(self, target: RunStatus) -> bool:
        """
        Check if transition to target state is valid.

        Args:
            target: Target status

        Returns:
            True if transition is valid
        """
        valid_targets = self.TRANSITIONS.get(self._status, set())
        return target in valid_targets

    def get_valid_transitions(self) -> Set[RunStatus]:
        """Get all valid next states from current state."""
        return self.TRANSITIONS.get(self._status, set()).copy()

    def transition_to(self, target: RunStatus, reason: str = "") -> None:
        """
        Transition to a new state.

        Args:
            target: Target status
            reason: Optional reason for the transition

        Raises:
            TransitionError: If transition is not valid
        """
        if not self.can_transition_to(target):
            raise TransitionError(self._status, target, reason)

        old_status = self._status
        self._status = target

        # Record in history
        self._history.append((old_status, target, datetime.now()))

        logger.info(f"Run {self.run_id}: {old_status.value} → {target.value}" +
                   (f" ({reason})" if reason else ""))

        # Emit event
        self._event_bus.emit(RunStatusChanged(
            run_id=self.run_id,
            old_status=old_status.value,
            new_status=target.value,
            reason=reason,
        ))

        # Call callback if provided
        if self._on_transition:
            try:
                self._on_transition(old_status, target)
            except Exception as e:
                logger.error(f"Error in transition callback: {e}")

    def start_analyzing(self) -> None:
        """Convenience: transition to ANALYZING."""
        self.transition_to(RunStatus.ANALYZING, "Starting analysis")

    def start_running(self) -> None:
        """Convenience: transition to RUNNING."""
        self.transition_to(RunStatus.RUNNING, "Starting execution")

    def pause(self) -> None:
        """Convenience: transition to PAUSED."""
        self.transition_to(RunStatus.PAUSED, "Paused by user")

    def resume(self) -> None:
        """Convenience: transition from PAUSED to RUNNING."""
        if self._status != RunStatus.PAUSED:
            raise TransitionError(self._status, RunStatus.RUNNING, "Can only resume from PAUSED state")
        self.transition_to(RunStatus.RUNNING, "Resumed by user")

    def gate(self, reason: str = "Policy violation") -> None:
        """Convenience: transition to GATED."""
        self.transition_to(RunStatus.GATED, reason)

    def complete(self, success: bool) -> None:
        """Convenience: transition to SUCCESS or FAILED."""
        target = RunStatus.SUCCESS if success else RunStatus.FAILED
        self.transition_to(target, "Execution completed")

    def cancel(self, reason: str = "Cancelled by user") -> None:
        """Convenience: transition to CANCELLED."""
        self.transition_to(RunStatus.CANCELLED, reason)

    def error(self, reason: str) -> None:
        """Convenience: transition to ERROR."""
        self.transition_to(RunStatus.ERROR, reason)

    def get_history(self) -> List[Tuple[RunStatus, RunStatus, datetime]]:
        """Get transition history."""
        return self._history.copy()

    def __repr__(self) -> str:
        return f"RunStateMachine(run_id={self.run_id}, status={self._status.value})"


# =============================================================================
# FACTORY FUNCTION
# =============================================================================

def create_state_machine(run_id: int,
                        initial_status: RunStatus = RunStatus.PENDING) -> RunStateMachine:
    """
    Factory function to create a state machine.

    Args:
        run_id: The run ID
        initial_status: Starting status

    Returns:
        Configured RunStateMachine instance
    """
    return RunStateMachine(run_id=run_id, initial_status=initial_status)
