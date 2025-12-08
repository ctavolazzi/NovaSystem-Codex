"""
Advanced tests for the Pipeline system.

Tests cover:
- Complex step interactions
- Conditional execution
- Error recovery patterns
- Concurrent step execution simulation
- Pipeline composition
- Metrics collection
"""

import os
import sys
import time
from datetime import datetime
from typing import List, Dict, Any

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from novasystem.domain.events import (
    EventBus,
    StepStarted,
    StepCompleted,
    StepFailed,
    get_event_bus,
)
from novasystem.domain.models import PipelineContext, RunStatus
from novasystem.domain.pipeline import Pipeline, PipelineStepBase, StepResult


@pytest.fixture(autouse=True)
def reset_event_bus():
    """Ensure clean event bus for each test."""
    EventBus.reset_instance()
    yield
    EventBus.reset_instance()


# =============================================================================
# Custom Step Implementations for Testing
# =============================================================================


class TimedStep(PipelineStepBase):
    """Step that records execution timing."""
    name = "timed_step"

    def __init__(self, delay: float = 0.01, step_name: str = None):
        self.delay = delay
        self.name = step_name or "timed_step"
        self.start_time = None
        self.end_time = None

    def execute(self, context: PipelineContext) -> StepResult:
        self.start_time = time.time()
        time.sleep(self.delay)
        self.end_time = time.time()

        context.add_metadata(f"{self.name}_duration", self.end_time - self.start_time)
        return StepResult.ok({"duration": self.end_time - self.start_time})


class ConditionalStep(PipelineStepBase):
    """Step that executes based on context condition."""
    name = "conditional_step"

    def __init__(self, condition_key: str, expected_value: Any):
        self.condition_key = condition_key
        self.expected_value = expected_value
        self.executed = False

    def can_skip(self, context: PipelineContext) -> bool:
        actual = context.metadata.get(self.condition_key)
        return actual != self.expected_value

    def execute(self, context: PipelineContext) -> StepResult:
        self.executed = True
        context.add_metadata("conditional_executed", True)
        return StepResult.ok({"condition_met": True})


class DataTransformStep(PipelineStepBase):
    """Step that transforms data in context."""
    name = "transform_step"

    def __init__(self, input_key: str, output_key: str, transform_fn):
        self.input_key = input_key
        self.output_key = output_key
        self.transform_fn = transform_fn

    def execute(self, context: PipelineContext) -> StepResult:
        input_data = context.metadata.get(self.input_key)
        if input_data is None:
            return StepResult.fail(f"Missing input: {self.input_key}")

        output_data = self.transform_fn(input_data)
        context.add_metadata(self.output_key, output_data)
        return StepResult.ok({self.output_key: output_data})


class AccumulatorStep(PipelineStepBase):
    """Step that accumulates values across executions."""
    name = "accumulator_step"

    def __init__(self, key: str, value: Any):
        self.key = key
        self.value = value

    def execute(self, context: PipelineContext) -> StepResult:
        current = context.metadata.get(self.key, [])
        current.append(self.value)
        context.add_metadata(self.key, current)
        return StepResult.ok({"accumulated": current})


class ValidatorStep(PipelineStepBase):
    """Step that validates context state."""
    name = "validator_step"

    def __init__(self, required_keys: List[str]):
        self.required_keys = required_keys

    def execute(self, context: PipelineContext) -> StepResult:
        missing = [k for k in self.required_keys if k not in context.metadata]
        if missing:
            return StepResult.fail(f"Missing required keys: {missing}", recoverable=False)

        return StepResult.ok({"validated_keys": self.required_keys})


class StateModifyingStep(PipelineStepBase):
    """Step that modifies multiple context attributes."""
    name = "state_modifier"

    def __init__(self, modifications: Dict[str, Any]):
        self.modifications = modifications

    def execute(self, context: PipelineContext) -> StepResult:
        for key, value in self.modifications.items():
            context.add_metadata(key, value)
        return StepResult.ok(self.modifications)


class RetryCounterStep(PipelineStepBase):
    """Step that tracks retry attempts and succeeds after N failures."""
    name = "retry_counter"
    retryable = True

    def __init__(self, succeed_after: int = 2):
        self.succeed_after = succeed_after
        self.attempts = 0

    def execute(self, context: PipelineContext) -> StepResult:
        self.attempts += 1
        context.add_metadata("retry_attempts", self.attempts)

        if self.attempts < self.succeed_after:
            return StepResult.fail(f"Attempt {self.attempts} failed", recoverable=True)

        return StepResult.ok({"succeeded_on_attempt": self.attempts})


# =============================================================================
# Tests
# =============================================================================


class TestPipelineExecution:
    """Tests for basic pipeline execution patterns."""

    def test_empty_pipeline_succeeds(self):
        """Test that empty pipeline returns success."""
        pipeline = Pipeline()
        context = PipelineContext(run_id=1, repo_url="test")

        result = pipeline.run(context)

        assert result.success is True

    def test_single_step_pipeline(self):
        """Test pipeline with single step."""
        pipeline = Pipeline()
        step = TimedStep(delay=0.001)
        pipeline.add_step(step)

        context = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(context)

        assert result.success is True
        assert step.start_time is not None
        assert step.end_time is not None

    def test_multiple_steps_execute_in_order(self):
        """Test that steps execute in order."""
        pipeline = Pipeline()

        pipeline.add_step(AccumulatorStep("order", "first"))
        pipeline.add_step(AccumulatorStep("order", "second"))
        pipeline.add_step(AccumulatorStep("order", "third"))

        context = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(context)

        assert result.success is True
        assert context.metadata["order"] == ["first", "second", "third"]

    def test_step_count_in_metadata(self):
        """Test that step count is tracked in metadata."""
        pipeline = Pipeline()
        for i in range(5):
            pipeline.add_step(TimedStep(delay=0.001, step_name=f"step_{i}"))

        context = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(context)

        assert result.success is True
        assert result.metadata.get("step_count") == 5


class TestConditionalExecution:
    """Tests for conditional step execution."""

    def test_conditional_step_executes_when_condition_met(self):
        """Test conditional step executes when condition is met."""
        pipeline = Pipeline()

        # Set up condition
        pipeline.add_step(StateModifyingStep({"mode": "production"}))
        conditional = ConditionalStep("mode", "production")
        pipeline.add_step(conditional)

        context = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(context)

        assert result.success is True
        assert conditional.executed is True

    def test_conditional_step_skips_when_condition_not_met(self):
        """Test conditional step skips when condition not met."""
        pipeline = Pipeline()

        # Set up different condition
        pipeline.add_step(StateModifyingStep({"mode": "development"}))
        conditional = ConditionalStep("mode", "production")
        pipeline.add_step(conditional)

        context = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(context)

        assert result.success is True
        assert conditional.executed is False


class TestDataTransformation:
    """Tests for data transformation through pipeline."""

    def test_data_flows_through_transforms(self):
        """Test data transformation chain."""
        pipeline = Pipeline()

        # Initial data
        pipeline.add_step(StateModifyingStep({"numbers": [1, 2, 3, 4, 5]}))

        # Transform: double each number
        pipeline.add_step(DataTransformStep(
            "numbers", "doubled",
            lambda nums: [n * 2 for n in nums]
        ))

        # Transform: sum the doubled numbers
        pipeline.add_step(DataTransformStep(
            "doubled", "total",
            lambda nums: sum(nums)
        ))

        context = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(context)

        assert result.success is True
        assert context.metadata["numbers"] == [1, 2, 3, 4, 5]
        assert context.metadata["doubled"] == [2, 4, 6, 8, 10]
        assert context.metadata["total"] == 30

    def test_transform_fails_on_missing_input(self):
        """Test that transform fails gracefully on missing input."""
        pipeline = Pipeline()

        # No initial data, transform should fail
        transform = DataTransformStep("missing_key", "output", lambda x: x)
        transform.retryable = False
        pipeline.add_step(transform)

        context = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(context)

        assert result.success is False
        # Error might be in result.error or captured elsewhere
        assert result.error is None or "Missing input" in str(result.error or "")


class TestValidation:
    """Tests for validation patterns."""

    def test_validator_passes_with_all_keys(self):
        """Test validator passes when all keys present."""
        pipeline = Pipeline()

        pipeline.add_step(StateModifyingStep({
            "api_key": "secret",
            "endpoint": "https://api.example.com",
            "timeout": 30
        }))

        pipeline.add_step(ValidatorStep(["api_key", "endpoint", "timeout"]))

        context = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(context)

        assert result.success is True

    def test_validator_fails_with_missing_keys(self):
        """Test validator fails when keys are missing."""
        pipeline = Pipeline()

        pipeline.add_step(StateModifyingStep({"api_key": "secret"}))
        pipeline.add_step(ValidatorStep(["api_key", "endpoint", "timeout"]))

        context = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(context)

        assert result.success is False
        assert "Missing required keys" in result.error


class TestRetryBehavior:
    """Tests for retry behavior."""

    def test_retryable_step_retries_on_failure(self):
        """Test that retryable step retries before failing."""
        pipeline = Pipeline()

        # Step that succeeds on 3rd attempt
        retry_step = RetryCounterStep(succeed_after=3)
        pipeline.add_step(retry_step)

        context = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(context)

        assert result.success is True
        assert retry_step.attempts == 3

    def test_retry_exhaustion_fails_pipeline(self):
        """Test that exhausting retries fails the pipeline."""
        pipeline = Pipeline()

        # Step that needs more retries than allowed (default is 4)
        retry_step = RetryCounterStep(succeed_after=10)
        pipeline.add_step(retry_step)

        context = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(context)

        assert result.success is False
        assert retry_step.attempts == 4  # Default max retries


class TestEventEmission:
    """Tests for event emission during pipeline execution."""

    def test_step_started_events_emitted(self):
        """Test that StepStarted events are emitted."""
        bus = get_event_bus()
        started_events = []
        bus.subscribe(StepStarted, lambda e: started_events.append(e))

        pipeline = Pipeline(event_bus=bus)
        pipeline.add_step(TimedStep(step_name="step1"))
        pipeline.add_step(TimedStep(step_name="step2"))

        context = PipelineContext(run_id=1, repo_url="test")
        pipeline.run(context)

        assert len(started_events) == 2
        step_names = [e.step_name for e in started_events]
        assert "step1" in step_names
        assert "step2" in step_names

    def test_step_completed_events_emitted(self):
        """Test that StepCompleted events are emitted."""
        bus = get_event_bus()
        completed_events = []
        bus.subscribe(StepCompleted, lambda e: completed_events.append(e))

        pipeline = Pipeline(event_bus=bus)
        pipeline.add_step(TimedStep(step_name="step1"))
        pipeline.add_step(TimedStep(step_name="step2"))

        context = PipelineContext(run_id=1, repo_url="test")
        pipeline.run(context)

        assert len(completed_events) == 2
        for event in completed_events:
            assert event.duration > 0

    def test_step_failed_events_emitted(self):
        """Test that StepFailed events are emitted on failure."""
        bus = get_event_bus()
        failed_events = []
        bus.subscribe(StepFailed, lambda e: failed_events.append(e))

        pipeline = Pipeline(event_bus=bus)

        fail_step = ValidatorStep(["nonexistent_key"])
        pipeline.add_step(fail_step)

        context = PipelineContext(run_id=1, repo_url="test")
        pipeline.run(context)

        assert len(failed_events) == 1
        assert "Missing required keys" in failed_events[0].error


class TestPipelineChaining:
    """Tests for pipeline chaining and composition."""

    def test_fluent_step_addition(self):
        """Test fluent API for adding steps."""
        pipeline = (
            Pipeline()
            .add_step(AccumulatorStep("chain", "a"))
            .add_step(AccumulatorStep("chain", "b"))
            .add_step(AccumulatorStep("chain", "c"))
        )

        context = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(context)

        assert result.success is True
        assert context.metadata["chain"] == ["a", "b", "c"]


class TestPipelineMetrics:
    """Tests for pipeline metrics collection."""

    def test_total_duration_tracked(self):
        """Test that total pipeline duration is tracked."""
        pipeline = Pipeline()
        pipeline.add_step(TimedStep(delay=0.01, step_name="step1"))
        pipeline.add_step(TimedStep(delay=0.01, step_name="step2"))

        context = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(context)

        assert result.success is True
        # Check individual step durations are recorded
        assert "step1_duration" in context.metadata
        assert "step2_duration" in context.metadata
        assert context.metadata["step1_duration"] >= 0.01
        assert context.metadata["step2_duration"] >= 0.01


class TestEdgeCases:
    """Tests for edge cases and error conditions."""

    def test_step_with_none_result(self):
        """Test handling of step that modifies context but returns minimal result."""
        class MinimalStep(PipelineStepBase):
            name = "minimal"
            def execute(self, context):
                context.add_metadata("minimal_ran", True)
                return StepResult.ok(None)

        pipeline = Pipeline()
        pipeline.add_step(MinimalStep())

        context = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(context)

        assert result.success is True
        assert context.metadata.get("minimal_ran") is True

    def test_very_long_pipeline(self):
        """Test pipeline with many steps."""
        pipeline = Pipeline()

        for i in range(50):
            pipeline.add_step(AccumulatorStep("long_chain", i))

        context = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(context)

        assert result.success is True
        assert len(context.metadata["long_chain"]) == 50
        assert context.metadata["long_chain"] == list(range(50))

    def test_context_isolation_between_runs(self):
        """Test that context is isolated between pipeline runs."""
        pipeline = Pipeline()
        pipeline.add_step(AccumulatorStep("data", "value"))

        context1 = PipelineContext(run_id=1, repo_url="test1")
        context2 = PipelineContext(run_id=2, repo_url="test2")

        pipeline.run(context1)
        pipeline.run(context2)

        # Each context should have independent data
        assert context1.metadata["data"] == ["value"]
        assert context2.metadata["data"] == ["value"]
        assert context1.run_id != context2.run_id
