"""
Tests for the event-driven domain architecture (event bus, state machine, pipeline).
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from novasystem.domain.events import (
    EventBus,
    RunCreated,
    RunStatusChanged,
    StepCompleted,
    StepFailed,
    StepStarted,
    get_event_bus,
)
from novasystem.domain.models import PipelineContext, RunStatus
from novasystem.domain.pipeline import Pipeline, PipelineStepBase, StepResult
from novasystem.domain.state_machine import RunStateMachine, TransitionError


@pytest.fixture(autouse=True)
def reset_event_bus():
    """Ensure a clean singleton event bus for every test."""
    EventBus.reset_instance()
    yield
    EventBus.reset_instance()


@pytest.fixture
def event_bus():
    return get_event_bus()


class SkipStep(PipelineStepBase):
    name = "skip_step"

    def can_skip(self, context: PipelineContext) -> bool:  # type: ignore[override]
        return True

    def execute(self, context: PipelineContext) -> StepResult:  # pragma: no cover
        raise AssertionError("SkipStep should never execute")


class FlakyStep(PipelineStepBase):
    name = "flaky_step"

    def __init__(self, fail_times: int = 1):
        self.fail_times = fail_times
        self.calls = 0

    def execute(self, context: PipelineContext) -> StepResult:  # type: ignore[override]
        self.calls += 1
        if self.calls <= self.fail_times:
            return StepResult.fail("transient error")

        context.add_metadata("flaky_attempts", self.calls)
        return StepResult.ok({"attempt": self.calls})


class FinalStep(PipelineStepBase):
    name = "final_step"

    def __init__(self):
        self.calls = 0

    def execute(self, context: PipelineContext) -> StepResult:  # type: ignore[override]
        self.calls += 1
        context.add_metadata("final_ran", True)
        return StepResult.ok("done")


class FatalStep(PipelineStepBase):
    name = "fatal_step"
    retryable = False

    def execute(self, context: PipelineContext) -> StepResult:  # type: ignore[override]
        return StepResult.fail("boom", recoverable=False)


def test_event_bus_routes_and_filters(event_bus: EventBus):
    specific_events = []
    global_events = []

    def on_run_created(event):
        specific_events.append(event)

    def on_any_event(event):
        global_events.append(event)

    event_bus.subscribe(RunCreated, on_run_created)
    event_bus.subscribe_all(on_any_event)

    first = RunCreated(run_id=1, repo_url="https://example.com/repo.git")
    second = RunCreated(run_id=2, repo_url="https://example.com/another.git")

    event_bus.emit(first)
    event_bus.unsubscribe(RunCreated, on_run_created)
    event_bus.emit(second)

    assert specific_events == [first]
    assert len(global_events) == 2

    # History should keep the most recent items in reverse-chronological order.
    event_bus._max_history = 2  # Narrow history for the test
    third = RunStatusChanged(run_id=10, old_status="pending", new_status="analyzing")
    fourth = RunStatusChanged(run_id=11, old_status="analyzing", new_status="running")
    event_bus.emit(third)
    event_bus.emit(fourth)

    history = event_bus.get_history()
    assert len(history) == 2
    assert history[0] == fourth
    assert history[1] == third

    filtered = event_bus.get_history(event_type=RunStatusChanged, run_id=11)
    assert filtered == [fourth]


def test_state_machine_transitions_emit_events(event_bus: EventBus):
    transitions = []
    event_bus.subscribe(
        RunStatusChanged,
        lambda e: transitions.append((e.old_status, e.new_status, e.reason)),
    )

    sm = RunStateMachine(run_id=123, event_bus=event_bus)
    sm.start_analyzing()
    sm.start_running()
    sm.pause()
    sm.resume()
    sm.complete(success=False)

    assert sm.status == RunStatus.FAILED
    assert [t[:2] for t in transitions] == [
        ("pending", "analyzing"),
        ("analyzing", "running"),
        ("running", "paused"),
        ("paused", "running"),
        ("running", "failed"),
    ]
    assert len(sm.get_history()) == 5

    with pytest.raises(TransitionError):
        sm.resume()


def test_pipeline_runs_steps_with_retry_and_skip(event_bus: EventBus):
    starts = []
    completions = []

    event_bus.subscribe(
        StepStarted, lambda e: starts.append((e.step_name, e.metadata.get("attempt")))
    )
    event_bus.subscribe(StepCompleted, lambda e: completions.append(e.step_name))

    pipeline = Pipeline(event_bus=event_bus)
    flaky = FlakyStep(fail_times=1)
    final = FinalStep()

    result = (
        pipeline.add_step(SkipStep())
        .add_step(flaky)
        .add_step(final)
        .run(PipelineContext(run_id=1, repo_url="/tmp/repo"))
    )

    assert result.success is True
    assert result.metadata["step_count"] == 3  # skip + flaky + final

    # Skip step never emits a StepStarted event; flaky retries once.
    assert starts == [("flaky_step", 1), ("flaky_step", 2), ("final_step", 1)]
    assert completions == ["flaky_step", "final_step"]
    assert flaky.calls == 2
    assert final.calls == 1

    failed_events = event_bus.get_history(event_type=StepFailed)
    assert failed_events == []


def test_pipeline_emits_failure_and_stops(event_bus: EventBus):
    starts = []
    failures = []

    event_bus.subscribe(StepStarted, lambda e: starts.append(e.step_name))
    event_bus.subscribe(StepFailed, lambda e: failures.append((e.step_name, e.error)))

    pipeline = Pipeline(event_bus=event_bus)
    final = FinalStep()

    result = (
        pipeline.add_step(FatalStep())
        .add_step(final)
        .run(PipelineContext(run_id=2, repo_url="/tmp/repo"))
    )

    assert result.success is False
    assert "fatal_step" in result.error
    assert starts == ["fatal_step"]
    assert failures == [("fatal_step", "boom")]
    assert final.calls == 0
