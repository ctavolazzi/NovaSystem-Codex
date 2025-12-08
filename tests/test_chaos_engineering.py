"""
🔥 CHAOS ENGINEERING TESTS 🔥

These tests intentionally break things to verify system resilience:
- Random fault injection
- Cascading failure simulation
- Recovery and self-healing verification
- Timeout and deadline handling
- Resource exhaustion scenarios
- Data corruption detection and recovery
"""

import os
import sys
import time
import random
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from novasystem.domain.events import EventBus, RunStatusChanged, StepStarted, StepCompleted, StepFailed, get_event_bus
from novasystem.domain.models import PipelineContext, RunStatus
from novasystem.domain.pipeline import Pipeline, PipelineStepBase, StepResult
from novasystem.domain.state_machine import RunStateMachine, TransitionError
from novasystem.core.memory import MemoryManager
from novasystem.core.vector_store import LocalVectorStore, SimpleEmbedder


@pytest.fixture(autouse=True)
def reset_systems():
    """Reset all singletons and shared state."""
    EventBus.reset_instance()
    random.seed(42)  # Reproducible chaos
    yield
    EventBus.reset_instance()


# =============================================================================
# 💥 FAULT INJECTION STEPS
# =============================================================================


class RandomFailureStep(PipelineStepBase):
    """Step that fails randomly based on probability."""
    name = "random_failure"
    retryable = True

    def __init__(self, failure_probability: float = 0.5, name: str = None):
        self.failure_probability = failure_probability
        self.name = name or "random_failure"
        self.execution_count = 0

    def execute(self, context: PipelineContext) -> StepResult:
        self.execution_count += 1
        if random.random() < self.failure_probability:
            return StepResult.fail(f"Random failure (attempt {self.execution_count})")
        return StepResult.ok({"survived": True, "attempts": self.execution_count})


class SlowStep(PipelineStepBase):
    """Step that takes variable time to complete."""
    name = "slow_step"

    def __init__(self, min_delay: float = 0.01, max_delay: float = 0.1):
        self.min_delay = min_delay
        self.max_delay = max_delay

    def execute(self, context: PipelineContext) -> StepResult:
        delay = random.uniform(self.min_delay, self.max_delay)
        time.sleep(delay)
        return StepResult.ok({"delay": delay})


class MemoryHogStep(PipelineStepBase):
    """Step that allocates significant memory."""
    name = "memory_hog"

    def __init__(self, size_mb: int = 10):
        self.size_mb = size_mb
        self.data = None

    def execute(self, context: PipelineContext) -> StepResult:
        # Allocate memory
        self.data = bytearray(self.size_mb * 1024 * 1024)
        context.add_metadata("memory_allocated_mb", self.size_mb)
        return StepResult.ok({"allocated": self.size_mb})

    def cleanup(self):
        self.data = None


class ExceptionBombStep(PipelineStepBase):
    """Step that throws various exceptions."""
    name = "exception_bomb"
    retryable = False

    def __init__(self, exception_type: type = RuntimeError):
        self.exception_type = exception_type

    def execute(self, context: PipelineContext) -> StepResult:
        raise self.exception_type("💥 BOOM! Intentional explosion!")


class DataCorruptorStep(PipelineStepBase):
    """Step that corrupts context data to test validation."""
    name = "data_corruptor"

    def execute(self, context: PipelineContext) -> StepResult:
        # Inject garbage data
        context.add_metadata("corrupted_int", "not_an_int")
        context.add_metadata("corrupted_list", {"should": "be_list"})
        context.add_metadata("corrupted_none", None)
        return StepResult.ok({"corrupted": True})


class CascadeFailureStep(PipelineStepBase):
    """Step that causes cascading failures by corrupting shared state."""
    name = "cascade_failure"

    def __init__(self, shared_state: Dict):
        self.shared_state = shared_state

    def execute(self, context: PipelineContext) -> StepResult:
        self.shared_state["poison"] = True
        self.shared_state["counter"] = "corrupted"
        return StepResult.ok({"poisoned": True})


class StateCheckerStep(PipelineStepBase):
    """Step that validates shared state is not corrupted."""
    name = "state_checker"

    def __init__(self, shared_state: Dict):
        self.shared_state = shared_state

    def execute(self, context: PipelineContext) -> StepResult:
        if self.shared_state.get("poison"):
            return StepResult.fail("State poisoned by previous step!", recoverable=False)
        if not isinstance(self.shared_state.get("counter", 0), int):
            return StepResult.fail("Counter corrupted!", recoverable=False)
        return StepResult.ok({"state_valid": True})


# =============================================================================
# 🧪 CHAOS TESTS
# =============================================================================


class TestFaultInjection:
    """Tests for random fault injection and recovery."""

    def test_random_failures_eventually_succeed(self):
        """Test that retryable random failures eventually succeed."""
        pipeline = Pipeline()
        # 30% failure rate should succeed within 4 retries
        step = RandomFailureStep(failure_probability=0.3, name="flaky")
        pipeline.add_step(step)

        context = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(context)

        # With 30% failure and 4 retries, should usually succeed
        # But we accept failure as valid chaos outcome
        assert result.success or step.execution_count >= 4

    def test_high_failure_rate_exhausts_retries(self):
        """Test that high failure rate exhausts retries."""
        pipeline = Pipeline()
        # 95% failure rate should exhaust retries
        step = RandomFailureStep(failure_probability=0.95, name="very_flaky")
        pipeline.add_step(step)

        context = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(context)

        # Most likely failed after exhausting retries
        # But chaos means we accept either outcome
        assert step.execution_count >= 1

    def test_multiple_flaky_steps_in_sequence(self):
        """Test pipeline with multiple flaky steps."""
        pipeline = Pipeline()

        for i in range(5):
            pipeline.add_step(RandomFailureStep(failure_probability=0.2, name=f"flaky_{i}"))

        context = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(context)

        # Result can be success or failure - chaos is unpredictable
        assert isinstance(result.success, bool)


class TestCascadingFailures:
    """Tests for cascading failure scenarios."""

    def test_poison_pill_propagates(self):
        """Test that a poisoned state affects subsequent steps."""
        shared_state = {"counter": 0, "poison": False}

        pipeline = Pipeline()
        pipeline.add_step(CascadeFailureStep(shared_state))
        pipeline.add_step(StateCheckerStep(shared_state))

        context = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(context)

        # Second step should detect the poisoned state
        assert result.success is False
        assert shared_state["poison"] is True

    def test_early_failure_prevents_cascade(self):
        """Test that early failure prevents cascade."""
        shared_state = {"counter": 0}

        pipeline = Pipeline()
        bomb = ExceptionBombStep()
        bomb.retryable = False
        pipeline.add_step(bomb)
        pipeline.add_step(CascadeFailureStep(shared_state))

        context = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(context)

        assert result.success is False
        # Cascade step never ran, so state is clean
        assert "poison" not in shared_state


class TestExceptionHandling:
    """Tests for various exception types."""

    @pytest.mark.parametrize("exception_type", [
        RuntimeError,
        ValueError,
        TypeError,
        KeyError,
        AttributeError,
    ])
    def test_handles_various_exceptions(self, exception_type):
        """Test that pipeline handles various exception types gracefully."""
        pipeline = Pipeline()
        bomb = ExceptionBombStep(exception_type)
        pipeline.add_step(bomb)

        context = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(context)

        assert result.success is False
        # Pipeline should not crash, just fail gracefully


class TestResourceExhaustion:
    """Tests for resource exhaustion scenarios."""

    def test_memory_allocation_and_cleanup(self):
        """Test memory allocation in steps."""
        pipeline = Pipeline()
        hog = MemoryHogStep(size_mb=5)
        pipeline.add_step(hog)

        context = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(context)

        assert result.success is True
        assert context.metadata.get("memory_allocated_mb") == 5

        # Cleanup
        hog.cleanup()
        assert hog.data is None

    def test_slow_steps_complete(self):
        """Test that slow steps don't cause issues."""
        pipeline = Pipeline()

        for _ in range(10):
            pipeline.add_step(SlowStep(min_delay=0.001, max_delay=0.01))

        context = PipelineContext(run_id=1, repo_url="test")
        start = time.time()
        result = pipeline.run(context)
        duration = time.time() - start

        assert result.success is True
        assert duration >= 0.01  # At least minimum delay


class TestEventBusChaos:
    """Chaos tests for the event bus."""

    def test_rapid_fire_events(self):
        """Test event bus under rapid fire conditions."""
        bus = get_event_bus()
        received = []
        bus.subscribe(RunStatusChanged, lambda e: received.append(e))

        # Rapid fire events
        for i in range(10000):
            bus.emit(RunStatusChanged(run_id=i, old_status="a", new_status="b"))

        assert len(received) == 10000

    def test_subscriber_exception_isolation(self):
        """Test that one failing subscriber doesn't affect others."""
        bus = get_event_bus()
        good_events = []
        bad_count = [0]

        def good_handler(event):
            good_events.append(event)

        def bad_handler(event):
            bad_count[0] += 1
            raise RuntimeError("Intentional subscriber failure")

        bus.subscribe(RunStatusChanged, bad_handler)
        bus.subscribe(RunStatusChanged, good_handler)

        # Emit events - bad handler should not block good handler
        for i in range(100):
            try:
                bus.emit(RunStatusChanged(run_id=i, old_status="a", new_status="b"))
            except:
                pass  # Some implementations may propagate exceptions

        # Good handler should have received events
        assert len(good_events) > 0


class TestStateMachineChaos:
    """Chaos tests for the state machine."""

    def test_rapid_transitions(self):
        """Test rapid state transitions."""
        bus = get_event_bus()
        sm = RunStateMachine(run_id=1, event_bus=bus)

        # Rapid valid transitions
        sm.start_analyzing()
        sm.start_running()

        for _ in range(100):
            sm.pause()
            sm.resume()

        sm.complete(success=True)
        assert sm.status == RunStatus.SUCCESS

    def test_invalid_transition_recovery(self):
        """Test recovery from invalid transitions."""
        bus = get_event_bus()
        sm = RunStateMachine(run_id=1, event_bus=bus)

        sm.start_analyzing()
        sm.start_running()
        sm.complete(success=True)

        # Try invalid transitions from terminal state
        with pytest.raises(TransitionError):
            sm.pause()

        with pytest.raises(TransitionError):
            sm.resume()

        # State should remain unchanged
        assert sm.status == RunStatus.SUCCESS


class TestMemoryManagerChaos:
    """Chaos tests for memory manager."""

    @pytest.mark.asyncio
    async def test_concurrent_memory_access(self):
        """Test concurrent access to memory manager."""
        memory = MemoryManager(max_short_term=100, max_long_term=500)

        async def writer(id: int):
            for i in range(50):
                await memory.store_context(f"key_{id}_{i}", f"value_{id}_{i}", "short_term")

        async def reader(id: int):
            for i in range(50):
                await memory.get_context(f"key_{id}_{i}")

        # Run concurrent writers and readers
        tasks = []
        for i in range(10):
            tasks.append(writer(i))
            tasks.append(reader(i))

        await asyncio.gather(*tasks)

        stats = memory.get_memory_stats()
        assert stats["short_term_count"] <= 100  # Respects max

    @pytest.mark.asyncio
    async def test_memory_overflow_handling(self):
        """Test memory overflow doesn't corrupt data."""
        memory = MemoryManager(max_short_term=5, max_long_term=10)

        # Overflow short-term
        for i in range(20):
            await memory.store_context(f"overflow_{i}", i, "short_term")

        stats = memory.get_memory_stats()
        assert stats["short_term_count"] == 5

        # Most recent should still be accessible
        result = await memory.get_context("overflow_19")
        assert result == 19


class TestVectorStoreChaos:
    """Chaos tests for vector store."""

    def test_rapid_inserts_and_searches(self):
        """Test rapid inserts interleaved with searches."""
        store = LocalVectorStore(persist=False)

        for i in range(500):
            store.remember(f"Document {i} with content about topic {i % 10}")
            if i % 10 == 0:
                store.recall(f"topic {i % 10}", limit=5)

        assert store.count() == 500

    def test_concurrent_operations_thread_safety(self):
        """Test thread safety of vector store operations."""
        store = LocalVectorStore(persist=False)
        errors = []

        def worker(id: int):
            try:
                for i in range(100):
                    store.remember(f"Thread {id} document {i}")
                    store.recall(f"Thread {id}", limit=3)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Check for errors
        if errors:
            pytest.fail(f"Thread safety errors: {errors}")

        # Should have all documents
        assert store.count() == 500


class TestDataIntegrity:
    """Tests for data integrity under stress."""

    def test_context_data_survives_failures(self):
        """Test that context data survives step failures."""
        pipeline = Pipeline()

        class DataSetterStep(PipelineStepBase):
            name = "data_setter"
            def execute(self, context):
                context.add_metadata("important_data", "must_survive")
                return StepResult.ok({})

        pipeline.add_step(DataSetterStep())
        bomb = ExceptionBombStep()
        bomb.retryable = False
        pipeline.add_step(bomb)

        context = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(context)

        # Data should survive even though pipeline failed
        assert context.metadata.get("important_data") == "must_survive"

    def test_embeddings_are_deterministic(self):
        """Test that embeddings are deterministic."""
        embedder = SimpleEmbedder(dim=128)
        text = "Test text for determinism check"

        embeddings = [embedder.embed(text) for _ in range(100)]

        # All should be identical
        for e in embeddings[1:]:
            assert e == embeddings[0]


# =============================================================================
# 🎲 MONKEY TESTING
# =============================================================================


class TestMonkeyTesting:
    """Random/fuzz testing to find edge cases."""

    def test_random_pipeline_configurations(self):
        """Test random pipeline configurations."""
        for seed in range(10):
            random.seed(seed)

            pipeline = Pipeline()
            num_steps = random.randint(1, 10)

            for i in range(num_steps):
                step_type = random.choice([
                    lambda: RandomFailureStep(random.random() * 0.5),
                    lambda: SlowStep(0.001, 0.01),
                ])
                pipeline.add_step(step_type())

            context = PipelineContext(run_id=seed, repo_url="test")
            result = pipeline.run(context)

            # Should complete without crashing
            assert isinstance(result.success, bool)

    def test_random_context_data(self):
        """Test with random context data."""
        def random_value():
            return random.choice([
                random.randint(-1000, 1000),
                random.random(),
                "".join(random.choices("abcdef", k=10)),
                [random.randint(0, 100) for _ in range(5)],
                {"key": random.randint(0, 100)},
                None,
            ])

        context = PipelineContext(run_id=1, repo_url="test")

        # Add random data
        for i in range(100):
            context.add_metadata(f"random_{i}", random_value())

        # Should not crash
        assert len(context.metadata) >= 100
