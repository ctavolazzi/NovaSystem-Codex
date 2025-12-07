"""
⚡ CONCURRENCY & STRESS TESTS ⚡

Push NovaSystem to its limits with:
- Parallel pipeline execution
- Race condition detection
- Deadlock prevention verification
- High-throughput scenarios
- Resource contention handling
"""

import os
import sys
import time
import asyncio
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from typing import List, Dict, Any
from queue import Queue
import random

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from novasystem.domain.events import EventBus, RunStatusChanged, StepStarted, StepCompleted, get_event_bus
from novasystem.domain.models import PipelineContext, RunStatus
from novasystem.domain.pipeline import Pipeline, PipelineStepBase, StepResult
from novasystem.domain.state_machine import RunStateMachine
from novasystem.core.memory import MemoryManager
from novasystem.core.vector_store import LocalVectorStore, SimpleEmbedder


@pytest.fixture(autouse=True)
def reset_systems():
    """Reset singletons between tests."""
    EventBus.reset_instance()
    yield
    EventBus.reset_instance()


# =============================================================================
# 🏃 CONCURRENT STEP IMPLEMENTATIONS
# =============================================================================


class CounterStep(PipelineStepBase):
    """Thread-safe counter step for verifying execution count."""
    name = "counter"

    _lock = threading.Lock()
    _global_count = 0

    def __init__(self, step_id: int = 0):
        self.step_id = step_id
        self.name = f"counter_{step_id}"

    def execute(self, context: PipelineContext) -> StepResult:
        with CounterStep._lock:
            CounterStep._global_count += 1
            current = CounterStep._global_count

        context.add_metadata(f"counter_{self.step_id}", current)
        return StepResult.ok({"count": current})

    @classmethod
    def reset_global_count(cls):
        with cls._lock:
            cls._global_count = 0

    @classmethod
    def get_global_count(cls):
        with cls._lock:
            return cls._global_count


class SharedResourceStep(PipelineStepBase):
    """Step that accesses a shared resource with locking."""
    name = "shared_resource"

    def __init__(self, resource: Dict, lock: threading.Lock):
        self.resource = resource
        self.lock = lock

    def execute(self, context: PipelineContext) -> StepResult:
        with self.lock:
            self.resource["access_count"] = self.resource.get("access_count", 0) + 1
            time.sleep(0.001)  # Simulate work while holding lock
            count = self.resource["access_count"]

        return StepResult.ok({"access_count": count})


class AsyncWorkStep(PipelineStepBase):
    """Step that does async-style work."""
    name = "async_work"

    def __init__(self, work_duration: float = 0.01):
        self.work_duration = work_duration

    def execute(self, context: PipelineContext) -> StepResult:
        time.sleep(self.work_duration)
        return StepResult.ok({"worked": self.work_duration})


# =============================================================================
# 🧪 PARALLEL EXECUTION TESTS
# =============================================================================


class TestParallelPipelineExecution:
    """Tests for running multiple pipelines in parallel."""

    def test_parallel_pipeline_runs(self):
        """Test running multiple pipelines in parallel threads."""
        CounterStep.reset_global_count()
        results = []
        errors = []

        def run_pipeline(run_id: int):
            try:
                pipeline = Pipeline()
                for i in range(5):
                    pipeline.add_step(CounterStep(run_id * 100 + i))

                context = PipelineContext(run_id=run_id, repo_url=f"test_{run_id}")
                result = pipeline.run(context)
                results.append((run_id, result.success))
            except Exception as e:
                errors.append((run_id, str(e)))

        # Run 10 pipelines in parallel
        threads = [threading.Thread(target=run_pipeline, args=(i,)) for i in range(10)]

        start = time.time()
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        duration = time.time() - start

        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(results) == 10
        assert all(success for _, success in results)

        # Should have executed all steps
        total_steps = 10 * 5  # 10 pipelines * 5 steps each
        assert CounterStep.get_global_count() == total_steps

    def test_thread_pool_pipeline_execution(self):
        """Test using ThreadPoolExecutor for pipeline execution."""
        CounterStep.reset_global_count()

        def run_single_pipeline(run_id: int) -> bool:
            pipeline = Pipeline()
            for i in range(3):
                pipeline.add_step(CounterStep(run_id * 10 + i))

            context = PipelineContext(run_id=run_id, repo_url=f"pool_test_{run_id}")
            result = pipeline.run(context)
            return result.success

        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(run_single_pipeline, i) for i in range(50)]
            results = [f.result() for f in as_completed(futures)]

        assert all(results)
        assert CounterStep.get_global_count() == 50 * 3


class TestSharedResourceContention:
    """Tests for shared resource access patterns."""

    def test_lock_protected_resource(self):
        """Test that lock-protected resources maintain integrity."""
        shared_resource = {"access_count": 0}
        lock = threading.Lock()
        results = []

        def access_resource(thread_id: int):
            pipeline = Pipeline()
            pipeline.add_step(SharedResourceStep(shared_resource, lock))

            for _ in range(10):
                context = PipelineContext(run_id=thread_id, repo_url="shared")
                result = pipeline.run(context)
                results.append(result.success)

        threads = [threading.Thread(target=access_resource, args=(i,)) for i in range(10)]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All accesses should have succeeded
        assert all(results)
        # Exactly 100 accesses (10 threads * 10 iterations)
        assert shared_resource["access_count"] == 100


class TestEventBusConcurrency:
    """Tests for event bus under concurrent load."""

    def test_concurrent_emit_and_subscribe(self):
        """Test concurrent event emission and subscription."""
        bus = get_event_bus()
        received_events = []
        lock = threading.Lock()

        def handler(event):
            with lock:
                received_events.append(event)

        bus.subscribe(RunStatusChanged, handler)

        def emitter(thread_id: int):
            for i in range(100):
                bus.emit(RunStatusChanged(
                    run_id=thread_id * 1000 + i,
                    old_status="pending",
                    new_status="running"
                ))

        threads = [threading.Thread(target=emitter, args=(i,)) for i in range(10)]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Should have received all events
        assert len(received_events) == 1000

    def test_subscribe_unsubscribe_during_emission(self):
        """Test subscribe/unsubscribe while events are being emitted."""
        bus = get_event_bus()
        received = []
        handlers_added = []

        def make_handler(id: int):
            def handler(event):
                received.append((id, event))
            return handler

        # Start emitting events
        emit_done = threading.Event()

        def emitter():
            for i in range(500):
                bus.emit(RunStatusChanged(run_id=i, old_status="a", new_status="b"))
                time.sleep(0.0001)
            emit_done.set()

        def subscriber():
            for i in range(50):
                h = make_handler(i)
                handlers_added.append(h)
                bus.subscribe(RunStatusChanged, h)
                time.sleep(0.001)
                if i % 2 == 0 and len(handlers_added) > 1:
                    bus.unsubscribe(RunStatusChanged, handlers_added[-2])

        emit_thread = threading.Thread(target=emitter)
        sub_thread = threading.Thread(target=subscriber)

        emit_thread.start()
        sub_thread.start()

        emit_thread.join()
        sub_thread.join()

        # Should complete without deadlock or crash
        assert emit_done.is_set()


class TestMemoryManagerConcurrency:
    """Tests for memory manager under concurrent access."""

    @pytest.mark.asyncio
    async def test_high_throughput_memory_operations(self):
        """Test high-throughput memory operations."""
        memory = MemoryManager(max_short_term=1000, max_long_term=5000)

        async def writer(writer_id: int):
            for i in range(100):
                await memory.store_context(
                    f"writer_{writer_id}_key_{i}",
                    {"writer": writer_id, "index": i, "data": "x" * 100},
                    "short_term"
                )

        async def reader(reader_id: int):
            results = []
            for i in range(100):
                result = await memory.get_relevant_context(f"writer_{reader_id % 5}", limit=5)
                results.append(len(result))
            return results

        # Run concurrent writers and readers
        writer_tasks = [writer(i) for i in range(10)]
        reader_tasks = [reader(i) for i in range(10)]

        await asyncio.gather(*writer_tasks, *reader_tasks)

        stats = memory.get_memory_stats()
        # Should have stored up to max capacity
        assert stats["short_term_count"] <= 1000


class TestVectorStoreConcurrency:
    """Tests for vector store under concurrent access."""

    def test_high_throughput_insert_search(self):
        """Test high-throughput insert and search operations."""
        store = LocalVectorStore(persist=False)
        errors = []

        def worker(worker_id: int):
            try:
                for i in range(100):
                    # Insert
                    store.remember(
                        f"Worker {worker_id} document {i} about topic {i % 10}",
                        tags=[f"worker_{worker_id}", f"topic_{i % 10}"]
                    )

                    # Search
                    if i % 5 == 0:
                        results = store.recall(f"topic {i % 10}", limit=5)
                        assert len(results) >= 0
            except Exception as e:
                errors.append((worker_id, str(e)))

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0, f"Errors: {errors}"
        assert store.count() == 1000


# =============================================================================
# 🔄 ASYNC STRESS TESTS
# =============================================================================


class TestAsyncStress:
    """Stress tests for async operations."""

    @pytest.mark.asyncio
    async def test_many_concurrent_coroutines(self):
        """Test many concurrent coroutines."""
        memory = MemoryManager()
        results = []

        async def task(task_id: int):
            await memory.store_context(f"task_{task_id}", {"id": task_id}, "short_term")
            value = await memory.get_context(f"task_{task_id}")
            results.append((task_id, value))

        # Run 500 concurrent tasks
        await asyncio.gather(*[task(i) for i in range(500)])

        assert len(results) == 500

    @pytest.mark.asyncio
    async def test_rapid_context_switching(self):
        """Test rapid context switching between async operations."""
        memory = MemoryManager()
        operations = []

        async def mixed_operations(op_id: int):
            for i in range(50):
                if i % 3 == 0:
                    await memory.store_context(f"op_{op_id}_{i}", i, "short_term")
                elif i % 3 == 1:
                    await memory.get_context(f"op_{op_id}_{i-1}")
                else:
                    await memory.get_relevant_context(f"op_{op_id}", limit=3)
                operations.append((op_id, i))

        await asyncio.gather(*[mixed_operations(i) for i in range(20)])

        assert len(operations) == 20 * 50


# =============================================================================
# 🎯 THROUGHPUT BENCHMARKS
# =============================================================================


class TestThroughputBenchmarks:
    """Throughput benchmarks for various components."""

    def test_pipeline_throughput(self):
        """Measure pipeline execution throughput."""
        CounterStep.reset_global_count()

        def run_pipeline():
            pipeline = Pipeline()
            pipeline.add_step(CounterStep(0))
            context = PipelineContext(run_id=1, repo_url="throughput")
            return pipeline.run(context)

        start = time.time()
        for _ in range(1000):
            run_pipeline()
        duration = time.time() - start

        throughput = 1000 / duration
        print(f"\n📊 Pipeline throughput: {throughput:.0f} runs/second")

        # Should handle at least 500 runs/second
        assert throughput > 500

    def test_event_bus_throughput(self):
        """Measure event bus throughput."""
        bus = get_event_bus()
        count = [0]

        def handler(e):
            count[0] += 1

        bus.subscribe(RunStatusChanged, handler)

        start = time.time()
        for i in range(50000):
            bus.emit(RunStatusChanged(run_id=i, old_status="a", new_status="b"))
        duration = time.time() - start

        throughput = 50000 / duration
        print(f"\n📊 Event bus throughput: {throughput:.0f} events/second")

        assert count[0] == 50000
        # Should handle at least 50,000 events/second
        assert throughput > 50000

    def test_embedder_throughput(self):
        """Measure embedder throughput."""
        embedder = SimpleEmbedder(dim=256)
        texts = [f"Sample text number {i} for embedding" for i in range(1000)]

        start = time.time()
        for text in texts:
            embedder.embed(text)
        duration = time.time() - start

        throughput = 1000 / duration
        print(f"\n📊 Embedder throughput: {throughput:.0f} embeddings/second")

        # Should handle at least 1000 embeddings/second
        assert throughput > 1000

    def test_vector_store_search_throughput(self):
        """Measure vector store search throughput."""
        store = LocalVectorStore(persist=False)

        # Populate store
        for i in range(1000):
            store.remember(f"Document {i} about topic {i % 20}")

        start = time.time()
        for i in range(1000):
            store.recall(f"topic {i % 20}", limit=5)
        duration = time.time() - start

        throughput = 1000 / duration
        print(f"\n📊 Vector search throughput: {throughput:.0f} searches/second")

        # Should handle at least 500 searches/second
        assert throughput > 500


# =============================================================================
# 💀 EXTREME STRESS TESTS
# =============================================================================


class TestExtremeStress:
    """Extreme stress tests - use with caution!"""

    def test_pipeline_under_extreme_load(self):
        """Test pipeline under extreme parallel load."""
        CounterStep.reset_global_count()
        results = Queue()
        error_count = [0]

        def worker():
            try:
                for _ in range(100):
                    pipeline = Pipeline()
                    pipeline.add_step(CounterStep(0))
                    context = PipelineContext(run_id=1, repo_url="extreme")
                    result = pipeline.run(context)
                    results.put(result.success)
            except Exception:
                error_count[0] += 1

        # 50 threads, each running 100 pipelines
        threads = [threading.Thread(target=worker) for _ in range(50)]

        start = time.time()
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        duration = time.time() - start

        total_runs = 50 * 100
        actual_results = []
        while not results.empty():
            actual_results.append(results.get())

        success_rate = sum(actual_results) / len(actual_results) if actual_results else 0
        throughput = total_runs / duration

        print(f"\n💪 Extreme stress results:")
        print(f"   Total runs: {total_runs}")
        print(f"   Duration: {duration:.2f}s")
        print(f"   Throughput: {throughput:.0f} runs/second")
        print(f"   Success rate: {success_rate:.1%}")
        print(f"   Errors: {error_count[0]}")

        # Should maintain high success rate
        assert success_rate > 0.95
        assert error_count[0] == 0

    @pytest.mark.asyncio
    async def test_memory_under_extreme_load(self):
        """Test memory manager under extreme async load."""
        memory = MemoryManager(max_short_term=500, max_long_term=2000)
        operations = [0]
        errors = [0]

        async def worker(worker_id: int):
            for i in range(200):
                try:
                    await memory.store_context(f"w{worker_id}_k{i}", f"v{i}", "short_term")
                    await memory.get_context(f"w{worker_id}_k{i}")
                    operations[0] += 1
                except Exception:
                    errors[0] += 1

        await asyncio.gather(*[worker(i) for i in range(50)])

        print(f"\n💪 Memory extreme stress:")
        print(f"   Operations: {operations[0]}")
        print(f"   Errors: {errors[0]}")

        assert errors[0] == 0
