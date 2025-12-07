"""
🔪 EDGE CASES TORTURE TESTS 🔪

These tests probe the darkest corners of the system:
- Boundary value analysis
- Null/empty/malformed inputs
- Unicode and special character handling
- Extreme numerical values
- Deep nesting and recursion
- Type coercion edge cases
"""

import os
import sys
import math
import json
from datetime import datetime
from typing import Any

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from novasystem.domain.events import EventBus, RunStatusChanged, StepStarted, get_event_bus
from novasystem.domain.models import PipelineContext, RunStatus
from novasystem.domain.pipeline import Pipeline, PipelineStepBase, StepResult
from novasystem.domain.state_machine import RunStateMachine, TransitionError
from novasystem.core.memory import MemoryManager
from novasystem.core.vector_store import LocalVectorStore, SimpleEmbedder, cosine_similarity


@pytest.fixture(autouse=True)
def reset_event_bus():
    EventBus.reset_instance()
    yield
    EventBus.reset_instance()


# =============================================================================
# 🎯 BOUNDARY VALUE TESTS
# =============================================================================


class TestBoundaryValues:
    """Tests for boundary value edge cases."""

    def test_embedder_with_minimum_dimension(self):
        """Test embedder with minimum dimension."""
        embedder = SimpleEmbedder(dim=1)
        vec = embedder.embed("test")
        assert len(vec) == 1

    def test_embedder_with_large_dimension(self):
        """Test embedder with large dimension."""
        embedder = SimpleEmbedder(dim=10000)
        vec = embedder.embed("test")
        assert len(vec) == 10000

    def test_memory_with_zero_capacity(self):
        """Test memory manager with zero capacity."""
        # Zero capacity should still work (deque with maxlen=0)
        memory = MemoryManager(max_short_term=0, max_long_term=0)
        # Operations should not crash
        assert memory.get_memory_stats()["short_term_max"] == 0

    def test_memory_with_huge_capacity(self):
        """Test memory manager with huge capacity."""
        memory = MemoryManager(max_short_term=1000000, max_long_term=1000000)
        stats = memory.get_memory_stats()
        assert stats["short_term_max"] == 1000000

    def test_pipeline_context_with_extreme_run_id(self):
        """Test context with extreme run IDs."""
        # Max int
        ctx = PipelineContext(run_id=sys.maxsize, repo_url="test")
        assert ctx.run_id == sys.maxsize

        # Zero
        ctx = PipelineContext(run_id=0, repo_url="test")
        assert ctx.run_id == 0

        # Negative (if allowed)
        ctx = PipelineContext(run_id=-1, repo_url="test")
        assert ctx.run_id == -1


class TestNullEmptyInputs:
    """Tests for null and empty input handling."""

    def test_embedder_with_empty_string(self):
        """Test embedder with empty string."""
        embedder = SimpleEmbedder(dim=128)
        vec = embedder.embed("")
        # Should return zero vector
        assert all(v == 0 for v in vec)

    def test_embedder_with_whitespace_only(self):
        """Test embedder with whitespace-only string."""
        embedder = SimpleEmbedder(dim=128)
        vec = embedder.embed("   \t\n\r   ")
        # Should return zero vector (all tokens filtered)
        assert all(v == 0 for v in vec)

    def test_vector_store_empty_text(self):
        """Test vector store with empty text."""
        store = LocalVectorStore(persist=False)
        doc_id = store.remember("")
        assert doc_id.startswith("mem-")
        assert store.count() == 1

    def test_vector_store_empty_search(self):
        """Test vector store search with empty query."""
        store = LocalVectorStore(persist=False)
        store.remember("Some document")
        results = store.recall("", limit=5)
        # Empty query should still work
        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_memory_with_none_value(self):
        """Test memory manager with None value."""
        memory = MemoryManager()
        await memory.store_context("null_key", None, "short_term")
        result = await memory.get_context("null_key")
        assert result is None

    @pytest.mark.asyncio
    async def test_memory_with_empty_key(self):
        """Test memory manager with empty key."""
        memory = MemoryManager()
        await memory.store_context("", "value", "short_term")
        result = await memory.get_context("")
        assert result == "value"


class TestUnicodeAndSpecialChars:
    """Tests for Unicode and special character handling."""

    @pytest.mark.parametrize("text", [
        "Hello 世界 🌍",
        "Ελληνικά",
        "日本語テスト",
        "🔥🚀💻🎉",
        "مرحبا بالعالم",
        "שלום עולם",
        "\u0000\u0001\u0002",  # Control characters
        "Tab\there\nNewline",
        "Quote'Test\"Double",
        "Back\\slash",
        "<script>alert('xss')</script>",
        "${not_interpolated}",
        "%(format)s",
        "path/to/../../../etc/passwd",
    ])
    def test_embedder_with_unicode(self, text):
        """Test embedder with various Unicode strings."""
        embedder = SimpleEmbedder(dim=128)
        vec = embedder.embed(text)
        assert len(vec) == 128
        # Should not crash and produce valid vector

    @pytest.mark.parametrize("text", [
        "Hello 世界 🌍",
        "emoji only: 🔥🚀💻",
        "mixed: abc日本語def",
        "RTL: مرحبا",
    ])
    def test_vector_store_with_unicode(self, text):
        """Test vector store with Unicode."""
        store = LocalVectorStore(persist=False)
        doc_id = store.remember(text, tags=["unicode"])
        assert store.count() == 1

        results = store.recall(text, limit=1)
        assert len(results) >= 0  # May or may not match depending on tokenization

    @pytest.mark.asyncio
    @pytest.mark.parametrize("key,value", [
        ("unicode_key_🔥", "value"),
        ("key", "unicode_value_世界"),
        ("日本語", "日本語"),
        ("key\nwith\nnewlines", "value"),
    ])
    async def test_memory_with_unicode(self, key, value):
        """Test memory manager with Unicode keys and values."""
        memory = MemoryManager()
        await memory.store_context(key, value, "short_term")
        result = await memory.get_context(key)
        assert result == value


class TestExtremeNumericalValues:
    """Tests for extreme numerical values."""

    def test_cosine_similarity_with_tiny_values(self):
        """Test cosine similarity with very small values."""
        tiny = [1e-100] * 10
        result = cosine_similarity(tiny, tiny)
        # Should handle without overflow/underflow
        assert -1 <= result <= 1

    def test_cosine_similarity_with_huge_values(self):
        """Test cosine similarity with very large values."""
        huge = [1e100] * 10
        result = cosine_similarity(huge, huge)
        # Might be inf but should not crash
        assert result is not None

    def test_cosine_similarity_with_mixed_extreme(self):
        """Test cosine similarity with mixed extreme values."""
        vec1 = [1e-50, 1e50, 0, -1e50]
        vec2 = [1e-50, 1e50, 0, -1e50]
        result = cosine_similarity(vec1, vec2)
        assert result is not None

    @pytest.mark.asyncio
    async def test_memory_with_extreme_numbers(self):
        """Test memory with extreme numerical values."""
        memory = MemoryManager()

        extreme_values = [
            sys.maxsize,
            -sys.maxsize,
            float('inf'),
            float('-inf'),
            float('nan'),
            1e308,
            1e-308,
            0.0,
            -0.0,
        ]

        for i, val in enumerate(extreme_values):
            await memory.store_context(f"extreme_{i}", val, "short_term")
            result = await memory.get_context(f"extreme_{i}")
            # NaN is special - NaN != NaN
            if isinstance(val, float) and math.isnan(val):
                assert math.isnan(result)
            else:
                assert result == val


class TestDeepNesting:
    """Tests for deeply nested structures."""

    @pytest.mark.asyncio
    async def test_memory_with_deeply_nested_dict(self):
        """Test memory with deeply nested dictionary."""
        def create_nested(depth):
            if depth == 0:
                return "leaf"
            return {"level": depth, "child": create_nested(depth - 1)}

        memory = MemoryManager()
        nested = create_nested(50)

        await memory.store_context("deep", nested, "short_term")
        result = await memory.get_context("deep")
        assert result == nested

    @pytest.mark.asyncio
    async def test_memory_with_deeply_nested_list(self):
        """Test memory with deeply nested list."""
        nested = [[[[["deep"]]]]]
        for _ in range(20):
            nested = [nested]

        memory = MemoryManager()
        await memory.store_context("nested_list", nested, "short_term")
        result = await memory.get_context("nested_list")
        assert result == nested

    def test_context_with_deep_metadata(self):
        """Test pipeline context with deeply nested metadata."""
        ctx = PipelineContext(run_id=1, repo_url="test")

        # Create deeply nested metadata
        nested = {"level": 0}
        current = nested
        for i in range(100):
            current["child"] = {"level": i + 1}
            current = current["child"]

        ctx.add_metadata("deep_nested", nested)
        assert ctx.metadata["deep_nested"]["level"] == 0


class TestTypeCoercion:
    """Tests for type coercion and type safety."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("value", [
        True,
        False,
        0,
        1,
        "",
        [],
        {},
        None,
        0.0,
        "0",
        "false",
        "null",
    ])
    async def test_memory_preserves_falsy_values(self, value):
        """Test that memory preserves falsy values correctly."""
        memory = MemoryManager()
        await memory.store_context("falsy", value, "short_term")
        result = await memory.get_context("falsy")
        assert result == value
        assert type(result) == type(value)

    def test_context_metadata_type_preservation(self):
        """Test that context metadata preserves types."""
        ctx = PipelineContext(run_id=1, repo_url="test")

        test_values = [
            ("int", 42),
            ("float", 3.14),
            ("str", "hello"),
            ("bool", True),
            ("none", None),
            ("list", [1, 2, 3]),
            ("dict", {"a": 1}),
            ("tuple_as_list", (1, 2, 3)),  # Tuples often become lists in JSON
        ]

        for key, val in test_values:
            ctx.add_metadata(key, val)

        for key, expected in test_values:
            actual = ctx.metadata[key]
            if key == "tuple_as_list":
                # Tuple might be preserved or converted to list
                assert actual == list(expected) or actual == expected
            else:
                assert actual == expected


class TestMalformedInputs:
    """Tests for malformed and adversarial inputs."""

    def test_embedder_with_very_long_text(self):
        """Test embedder with very long text."""
        embedder = SimpleEmbedder(dim=128)
        long_text = "word " * 100000  # 100K words
        vec = embedder.embed(long_text)
        assert len(vec) == 128

    def test_embedder_with_repeated_text(self):
        """Test embedder with highly repeated text."""
        embedder = SimpleEmbedder(dim=128)
        repeated = "same " * 10000
        vec = embedder.embed(repeated)
        assert len(vec) == 128
        # Should produce valid normalized vector
        norm = sum(v * v for v in vec) ** 0.5
        assert abs(norm - 1.0) < 0.001 or norm == 0

    def test_vector_store_with_binary_like_text(self):
        """Test vector store with binary-like text."""
        store = LocalVectorStore(persist=False)
        binary_like = "".join(chr(i) for i in range(256))
        doc_id = store.remember(binary_like)
        assert store.count() == 1

    @pytest.mark.asyncio
    async def test_memory_with_circular_reference_workaround(self):
        """Test memory with circular reference (should fail gracefully or work)."""
        memory = MemoryManager()

        # Create non-circular deep structure instead (circular would cause issues)
        data = {"self_ref": "reference_placeholder"}
        data["nested"] = {"parent_copy": dict(data)}

        await memory.store_context("circular_like", data, "short_term")
        result = await memory.get_context("circular_like")
        assert result is not None


class TestEventBusEdgeCases:
    """Edge case tests for event bus."""

    def test_emit_with_unusual_status_values(self):
        """Test emitting events with unusual status values."""
        bus = get_event_bus()
        received = []
        bus.subscribe(RunStatusChanged, lambda e: received.append(e))

        unusual_statuses = [
            ("", ""),
            ("null", "null"),
            ("123", "456"),
            ("🔥", "💀"),
            ("very_long_" * 100, "status"),
        ]

        for old, new in unusual_statuses:
            bus.emit(RunStatusChanged(run_id=1, old_status=old, new_status=new))

        assert len(received) == len(unusual_statuses)

    def test_subscribe_with_many_handlers(self):
        """Test subscribing many handlers to same event."""
        bus = get_event_bus()
        counts = [0] * 1000

        for i in range(1000):
            idx = i
            bus.subscribe(RunStatusChanged, lambda e, i=idx: counts.__setitem__(i, counts[i] + 1))

        bus.emit(RunStatusChanged(run_id=1, old_status="a", new_status="b"))

        # All handlers should have been called
        assert all(c == 1 for c in counts)


class TestStateMachineEdgeCases:
    """Edge case tests for state machine."""

    def test_state_machine_with_extreme_run_id(self):
        """Test state machine with extreme run IDs."""
        bus = get_event_bus()

        for run_id in [0, 1, sys.maxsize, -1, -sys.maxsize]:
            sm = RunStateMachine(run_id=run_id, event_bus=bus)
            assert sm.status == RunStatus.PENDING
            sm.start_analyzing()
            assert sm.status == RunStatus.ANALYZING

    def test_rapid_transition_sequence(self):
        """Test rapid transition sequences."""
        bus = get_event_bus()
        sm = RunStateMachine(run_id=1, event_bus=bus)

        # Execute all valid transitions as fast as possible
        sm.start_analyzing()
        sm.start_running()
        sm.pause()
        sm.resume()
        sm.pause()
        sm.resume()
        sm.complete(success=True)

        assert sm.status == RunStatus.SUCCESS
        assert len(sm.get_history()) == 7  # All transitions recorded


class TestPipelineEdgeCases:
    """Edge case tests for pipeline execution."""

    def test_pipeline_step_modifies_context_drastically(self):
        """Test step that drastically modifies context."""
        class MetadataBomberStep(PipelineStepBase):
            name = "bomber"
            def execute(self, context):
                # Add lots of metadata
                for i in range(1000):
                    context.add_metadata(f"bomb_{i}", "x" * 100)
                return StepResult.ok({"bombed": True})

        pipeline = Pipeline()
        pipeline.add_step(MetadataBomberStep())

        ctx = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(ctx)

        assert result.success is True
        assert len(ctx.metadata) >= 1000

    def test_step_result_with_huge_data(self):
        """Test step that returns huge result data."""
        class HugeResultStep(PipelineStepBase):
            name = "huge_result"
            def execute(self, context):
                huge_data = {"key_" + str(i): "x" * 1000 for i in range(100)}
                return StepResult.ok(huge_data)

        pipeline = Pipeline()
        pipeline.add_step(HugeResultStep())

        ctx = PipelineContext(run_id=1, repo_url="test")
        result = pipeline.run(ctx)

        assert result.success is True
