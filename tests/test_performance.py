"""
Performance and stress tests for NovaSystem components.

Tests cover:
- Embedder performance with large texts
- Vector store scalability
- Event bus throughput
- Memory manager under load
- Pipeline execution speed
"""

import os
import sys
import time
import statistics
from datetime import datetime
from typing import List

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from novasystem.core.vector_store import SimpleEmbedder, LocalVectorStore, cosine_similarity
from novasystem.core.memory import MemoryManager
from novasystem.domain.events import EventBus, RunStatusChanged, get_event_bus
from novasystem.domain.pipeline import Pipeline, PipelineStepBase, StepResult
from novasystem.domain.models import PipelineContext


@pytest.fixture(autouse=True)
def reset_event_bus():
    """Reset event bus between tests."""
    EventBus.reset_instance()
    yield
    EventBus.reset_instance()


# =============================================================================
# Embedder Performance Tests
# =============================================================================


class TestEmbedderPerformance:
    """Performance tests for the SimpleEmbedder."""

    @pytest.fixture
    def embedder(self):
        return SimpleEmbedder(dim=256)

    def test_embed_short_text_speed(self, embedder):
        """Test embedding speed for short text."""
        text = "This is a short test sentence."

        start = time.time()
        for _ in range(1000):
            embedder.embed(text)
        duration = time.time() - start

        # Should complete 1000 embeddings in under 1 second
        assert duration < 1.0, f"1000 short embeddings took {duration:.2f}s (target: <1s)"

    def test_embed_medium_text_speed(self, embedder):
        """Test embedding speed for medium text."""
        text = " ".join(["word"] * 100)  # 100 words

        start = time.time()
        for _ in range(500):
            embedder.embed(text)
        duration = time.time() - start

        # Should complete 500 embeddings in under 1 second
        assert duration < 1.0, f"500 medium embeddings took {duration:.2f}s (target: <1s)"

    def test_embed_long_text_speed(self, embedder):
        """Test embedding speed for long text."""
        text = " ".join(["word"] * 1000)  # 1000 words

        start = time.time()
        for _ in range(100):
            embedder.embed(text)
        duration = time.time() - start

        # Should complete 100 embeddings in under 2 seconds
        assert duration < 2.0, f"100 long embeddings took {duration:.2f}s (target: <2s)"

    def test_embed_consistency(self, embedder):
        """Test that embedding the same text produces consistent results."""
        text = "Consistent embedding test"

        embeddings = [embedder.embed(text) for _ in range(10)]

        # All embeddings should be identical
        for i in range(1, len(embeddings)):
            assert embeddings[0] == embeddings[i], "Embeddings should be deterministic"

    def test_different_dimensions_performance(self):
        """Test performance across different embedding dimensions."""
        dims = [64, 128, 256, 512]
        text = "Test text for dimension comparison"

        times = {}
        for dim in dims:
            embedder = SimpleEmbedder(dim=dim)
            start = time.time()
            for _ in range(500):
                embedder.embed(text)
            times[dim] = time.time() - start

        # All should complete in reasonable time
        for dim, duration in times.items():
            assert duration < 1.0, f"Dim {dim}: {duration:.2f}s (target: <1s)"


# =============================================================================
# Vector Store Scalability Tests
# =============================================================================


class TestVectorStoreScalability:
    """Scalability tests for LocalVectorStore."""

    @pytest.fixture
    def store(self):
        return LocalVectorStore(persist=False)

    def test_bulk_insert_performance(self, store):
        """Test bulk document insertion speed."""
        documents = [f"Document number {i} with some content" for i in range(1000)]

        start = time.time()
        for doc in documents:
            store.remember(doc, tags=["bulk"])
        duration = time.time() - start

        assert store.count() == 1000
        # Should insert 1000 documents in under 2 seconds
        assert duration < 2.0, f"1000 inserts took {duration:.2f}s (target: <2s)"

    def test_search_performance_small_store(self, store):
        """Test search performance with small store."""
        # Insert 100 documents
        for i in range(100):
            store.remember(f"Document about topic {i % 10}", tags=[f"topic{i % 10}"])

        start = time.time()
        for _ in range(100):
            store.recall("topic 5", limit=5)
        duration = time.time() - start

        # 100 searches should complete in under 1 second
        assert duration < 1.0, f"100 searches took {duration:.2f}s (target: <1s)"

    def test_search_performance_medium_store(self, store):
        """Test search performance with medium store."""
        # Insert 500 documents
        for i in range(500):
            store.remember(f"Document about various topics including {i}")

        start = time.time()
        for _ in range(50):
            store.recall("topics", limit=10)
        duration = time.time() - start

        # 50 searches should complete in under 2 seconds
        assert duration < 2.0, f"50 searches took {duration:.2f}s (target: <2s)"

    def test_tag_filtering_performance(self, store):
        """Test performance of tag-filtered searches."""
        # Insert documents with various tags
        for i in range(500):
            tags = [f"tag{i % 5}", f"category{i % 10}"]
            store.remember(f"Document {i}", tags=tags)

        start = time.time()
        for _ in range(50):
            store.recall("Document", limit=10, tags=["tag3"])
        duration = time.time() - start

        assert duration < 2.0, f"50 filtered searches took {duration:.2f}s (target: <2s)"


# =============================================================================
# Event Bus Throughput Tests
# =============================================================================


class TestEventBusThroughput:
    """Throughput tests for the EventBus."""

    def test_high_volume_event_emission(self):
        """Test emitting many events."""
        bus = get_event_bus()
        received = []
        bus.subscribe(RunStatusChanged, lambda e: received.append(e))

        start = time.time()
        for i in range(10000):
            bus.emit(RunStatusChanged(
                run_id=i,
                old_status="pending",
                new_status="running"
            ))
        duration = time.time() - start

        assert len(received) == 10000
        # Should handle 10000 events in under 1 second
        assert duration < 1.0, f"10000 events took {duration:.2f}s (target: <1s)"

    def test_multiple_subscribers_performance(self):
        """Test performance with multiple subscribers."""
        bus = get_event_bus()
        counters = [0] * 10

        # Add 10 subscribers
        for i in range(10):
            idx = i
            bus.subscribe(RunStatusChanged, lambda e, i=idx: counters.__setitem__(i, counters[i] + 1))

        start = time.time()
        for _ in range(1000):
            bus.emit(RunStatusChanged(run_id=1, old_status="a", new_status="b"))
        duration = time.time() - start

        # Each subscriber should receive all events
        assert all(c == 1000 for c in counters)
        assert duration < 1.0, f"1000 events to 10 subscribers took {duration:.2f}s"

    def test_event_history_performance(self):
        """Test event history retrieval performance."""
        bus = get_event_bus()
        bus._max_history = 5000

        # Emit many events
        for i in range(5000):
            bus.emit(RunStatusChanged(run_id=i, old_status="a", new_status="b"))

        start = time.time()
        for _ in range(100):
            bus.get_history(event_type=RunStatusChanged)
        duration = time.time() - start

        assert duration < 0.5, f"100 history retrievals took {duration:.2f}s"


# =============================================================================
# Memory Manager Load Tests
# =============================================================================


class TestMemoryManagerLoad:
    """Load tests for MemoryManager."""

    @pytest.fixture
    def memory(self):
        return MemoryManager(max_short_term=1000, max_long_term=5000)

    @pytest.mark.asyncio
    async def test_rapid_store_retrieve(self, memory):
        """Test rapid store and retrieve cycles."""
        start = time.time()
        for i in range(500):
            await memory.store_context(f"key_{i}", f"value_{i}", "short_term")
            await memory.get_context(f"key_{i}")
        duration = time.time() - start

        assert duration < 1.0, f"500 store/retrieve cycles took {duration:.2f}s"

    @pytest.mark.asyncio
    async def test_relevance_search_under_load(self, memory):
        """Test relevance search with many entries."""
        # Fill memory
        topics = ["python", "javascript", "rust", "go", "java"]
        for i in range(500):
            topic = topics[i % len(topics)]
            await memory.store_context(
                f"entry_{i}",
                f"Information about {topic} programming language feature {i}",
                "short_term"
            )

        start = time.time()
        for _ in range(50):
            await memory.get_relevant_context("python programming", limit=10)
        duration = time.time() - start

        assert duration < 1.0, f"50 relevance searches took {duration:.2f}s"

    @pytest.mark.asyncio
    async def test_compression_performance(self, memory):
        """Test memory compression performance."""
        # Fill with important and non-important entries
        for i in range(200):
            key = f"final_solution_{i}" if i % 5 == 0 else f"draft_{i}"
            await memory.store_context(key, f"Content {i}", "short_term")

        start = time.time()
        for _ in range(10):
            await memory.compress_memory()
        duration = time.time() - start

        assert duration < 1.0, f"10 compression cycles took {duration:.2f}s"


# =============================================================================
# Pipeline Execution Speed Tests
# =============================================================================


class FastStep(PipelineStepBase):
    """Minimal step for speed testing."""
    name = "fast_step"

    def __init__(self, step_id: int):
        self.step_id = step_id
        self.name = f"fast_step_{step_id}"

    def execute(self, context: PipelineContext) -> StepResult:
        context.add_metadata(f"step_{self.step_id}", True)
        return StepResult.ok({"step_id": self.step_id})


class TestPipelineSpeed:
    """Speed tests for pipeline execution."""

    def test_many_steps_execution_speed(self):
        """Test pipeline with many steps."""
        pipeline = Pipeline()
        for i in range(100):
            pipeline.add_step(FastStep(i))

        context = PipelineContext(run_id=1, repo_url="test")

        start = time.time()
        result = pipeline.run(context)
        duration = time.time() - start

        assert result.success is True
        # 100 steps should complete in under 0.5 seconds
        assert duration < 0.5, f"100 steps took {duration:.2f}s (target: <0.5s)"

    def test_repeated_pipeline_runs(self):
        """Test repeated pipeline execution."""
        pipeline = Pipeline()
        for i in range(10):
            pipeline.add_step(FastStep(i))

        start = time.time()
        for run_id in range(100):
            context = PipelineContext(run_id=run_id, repo_url="test")
            pipeline.run(context)
        duration = time.time() - start

        # 100 runs of 10 steps each should complete in under 1 second
        assert duration < 1.0, f"100 runs took {duration:.2f}s (target: <1s)"


# =============================================================================
# Cosine Similarity Performance Tests
# =============================================================================


class TestCosineSimilarityPerformance:
    """Performance tests for cosine similarity calculations."""

    def test_many_comparisons(self):
        """Test many cosine similarity calculations."""
        import random
        random.seed(42)

        # Generate random vectors
        dim = 256
        vectors = [[random.random() for _ in range(dim)] for _ in range(100)]

        start = time.time()
        count = 0
        for i in range(len(vectors)):
            for j in range(i + 1, len(vectors)):
                cosine_similarity(vectors[i], vectors[j])
                count += 1
        duration = time.time() - start

        # Should complete ~5000 comparisons quickly
        assert count == 4950  # n*(n-1)/2
        assert duration < 1.0, f"{count} comparisons took {duration:.2f}s"


# =============================================================================
# Benchmark Summary Test
# =============================================================================


class TestBenchmarkSummary:
    """Run a comprehensive benchmark and report results."""

    def test_benchmark_summary(self, capsys):
        """Run all benchmarks and print summary."""
        results = {}

        # Embedder benchmark
        embedder = SimpleEmbedder(dim=256)
        text = "Benchmark test sentence with moderate length"

        start = time.time()
        for _ in range(1000):
            embedder.embed(text)
        results["embedder_1k"] = time.time() - start

        # Vector store benchmark
        store = LocalVectorStore(persist=False)
        start = time.time()
        for i in range(500):
            store.remember(f"Document {i}")
        results["store_insert_500"] = time.time() - start

        start = time.time()
        for _ in range(50):
            store.recall("Document", limit=10)
        results["store_search_50"] = time.time() - start

        # Event bus benchmark
        bus = get_event_bus()
        received = []
        bus.subscribe(RunStatusChanged, lambda e: received.append(1))

        start = time.time()
        for i in range(5000):
            bus.emit(RunStatusChanged(run_id=i, old_status="a", new_status="b"))
        results["events_5k"] = time.time() - start

        # Pipeline benchmark
        pipeline = Pipeline()
        for i in range(50):
            pipeline.add_step(FastStep(i))

        start = time.time()
        for run_id in range(50):
            context = PipelineContext(run_id=run_id, repo_url="test")
            pipeline.run(context)
        results["pipeline_50x50"] = time.time() - start

        # Print summary
        print("\n" + "=" * 60)
        print("NOVASYSTEM PERFORMANCE BENCHMARK SUMMARY")
        print("=" * 60)
        for name, duration in results.items():
            status = "✅" if duration < 1.0 else "⚠️"
            print(f"{status} {name}: {duration:.4f}s")
        print("=" * 60)

        # All benchmarks should pass
        assert all(v < 2.0 for v in results.values()), "Some benchmarks exceeded threshold"
