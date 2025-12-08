"""
Comprehensive tests for the MemoryManager system.

Tests cover:
- Short-term and long-term memory storage
- Context retrieval and relevance filtering
- Memory compression and importance detection
- Stats and clearing functionality
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from novasystem.core.memory import MemoryManager


@pytest.fixture
def memory_manager():
    """Create a fresh MemoryManager for each test."""
    return MemoryManager(max_short_term=5, max_long_term=10)


class TestMemoryStorage:
    """Tests for basic memory storage operations."""

    @pytest.mark.asyncio
    async def test_store_and_retrieve_short_term(self, memory_manager):
        """Test storing and retrieving from short-term memory."""
        await memory_manager.store_context("test_key", {"value": 42}, "short_term")
        result = await memory_manager.get_context("test_key")
        assert result == {"value": 42}

    @pytest.mark.asyncio
    async def test_store_and_retrieve_long_term(self, memory_manager):
        """Test storing and retrieving from long-term memory."""
        await memory_manager.store_context("important_key", "critical data", "long_term")
        result = await memory_manager.get_context("important_key")
        assert result == "critical data"

    @pytest.mark.asyncio
    async def test_short_term_overflow(self, memory_manager):
        """Test that short-term memory respects max size (deque behavior)."""
        # Fill beyond capacity
        for i in range(7):
            await memory_manager.store_context(f"key_{i}", f"value_{i}", "short_term")

        stats = memory_manager.get_memory_stats()
        assert stats["short_term_count"] == 5  # Max is 5
        assert stats["short_term_max"] == 5

        # Note: context_index retains all keys, but deque loses oldest entries
        # This tests deque behavior - oldest entries are removed from the deque
        # The newest should definitely exist
        assert await memory_manager.get_context("key_6") == "value_6"
        assert await memory_manager.get_context("key_5") == "value_5"

    @pytest.mark.asyncio
    async def test_context_not_found_returns_none(self, memory_manager):
        """Test that missing context returns None."""
        result = await memory_manager.get_context("nonexistent")
        assert result is None


class TestRelevanceFiltering:
    """Tests for context relevance and retrieval."""

    @pytest.mark.asyncio
    async def test_get_relevant_context_basic(self, memory_manager):
        """Test basic relevance filtering."""
        await memory_manager.store_context("python_tips", "Python uses list comprehensions for cleaner code", "short_term")
        await memory_manager.store_context("java_tips", "Java uses streams for functional programming", "short_term")
        await memory_manager.store_context("database_tips", "Index frequently queried columns", "short_term")

        # Query with "python" - should match python_tips
        result = await memory_manager.get_relevant_context("python", limit=2)
        # The relevance check looks for keywords in data, and "python" should match
        assert "python" in result.lower() or "Python" in result

    @pytest.mark.asyncio
    async def test_get_relevant_context_searches_both_memories(self, memory_manager):
        """Test that relevance search checks both short and long term memory."""
        await memory_manager.store_context("short_api", "REST API design patterns", "short_term")
        await memory_manager.store_context("long_api", "GraphQL schema best practices", "long_term")

        result = await memory_manager.get_relevant_context("API design", limit=5)
        assert "short_api" in result or "long_api" in result

    @pytest.mark.asyncio
    async def test_get_relevant_context_respects_limit(self, memory_manager):
        """Test that limit parameter is respected."""
        for i in range(5):
            await memory_manager.store_context(f"code_{i}", f"Python code example {i}", "short_term")

        result = await memory_manager.get_relevant_context("Python code", limit=2)
        # Should contain at most 2 entries
        assert result.count("code_") <= 2

    @pytest.mark.asyncio
    async def test_relevance_ignores_short_words(self, memory_manager):
        """Test that very short words are ignored in relevance matching."""
        await memory_manager.store_context("test", "This is a test value", "short_term")
        # Query with only short words should return nothing relevant
        result = await memory_manager.get_relevant_context("is a", limit=5)
        # The _is_relevant method ignores words with len <= 2
        assert "test" not in result.lower() or result == ""


class TestMemoryCompression:
    """Tests for memory compression and importance detection."""

    @pytest.mark.asyncio
    async def test_compress_moves_important_to_long_term(self, memory_manager):
        """Test that compression moves important items to long-term."""
        # Store items with important keywords
        await memory_manager.store_context("final_report", "This is the final solution", "short_term")
        await memory_manager.store_context("draft_notes", "Some random notes", "short_term")

        initial_short = memory_manager.get_memory_stats()["short_term_count"]
        await memory_manager.compress_memory()

        stats = memory_manager.get_memory_stats()
        # Important item should have moved
        assert stats["long_term_count"] >= 1

    @pytest.mark.asyncio
    async def test_importance_detection_by_key(self, memory_manager):
        """Test that keys with important words are detected."""
        # These should be considered important
        important_keys = ["problem_statement", "final_decision", "solution_v1"]
        for key in important_keys:
            await memory_manager.store_context(key, "content", "short_term")

        await memory_manager.compress_memory()
        stats = memory_manager.get_memory_stats()
        assert stats["long_term_count"] >= 1

    @pytest.mark.asyncio
    async def test_importance_detection_by_content(self, memory_manager):
        """Test that content with important patterns is detected."""
        await memory_manager.store_context(
            "generic_key",
            "This contains a final recommendation for the project",
            "short_term"
        )
        await memory_manager.compress_memory()
        stats = memory_manager.get_memory_stats()
        assert stats["long_term_count"] >= 1


class TestMemoryStats:
    """Tests for memory statistics and management."""

    @pytest.mark.asyncio
    async def test_get_memory_stats(self, memory_manager):
        """Test memory statistics reporting."""
        await memory_manager.store_context("short1", "data", "short_term")
        await memory_manager.store_context("short2", "data", "short_term")
        await memory_manager.store_context("long1", "data", "long_term")

        stats = memory_manager.get_memory_stats()
        assert stats["short_term_count"] == 2
        assert stats["long_term_count"] == 1
        assert stats["total_contexts"] == 3
        assert stats["short_term_max"] == 5
        assert stats["long_term_max"] == 10

    @pytest.mark.asyncio
    async def test_get_all_context(self, memory_manager):
        """Test retrieving all context."""
        await memory_manager.store_context("key1", "value1", "short_term")
        await memory_manager.store_context("key2", "value2", "long_term")

        all_ctx = await memory_manager.get_all_context()
        assert all_ctx["key1"] == "value1"
        assert all_ctx["key2"] == "value2"

    def test_clear_memory(self, memory_manager):
        """Test clearing all memory."""
        # Add some data synchronously via deque (bypassing async for simplicity)
        memory_manager.short_term_memory.append({"key": "test", "data": "test"})
        memory_manager.context_index["test"] = {"key": "test", "data": "test"}

        memory_manager.clear_memory()

        stats = memory_manager.get_memory_stats()
        assert stats["short_term_count"] == 0
        assert stats["long_term_count"] == 0
        assert stats["total_contexts"] == 0


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    @pytest.mark.asyncio
    async def test_store_complex_data_types(self, memory_manager):
        """Test storing various data types."""
        await memory_manager.store_context("dict_data", {"nested": {"key": [1, 2, 3]}}, "short_term")
        await memory_manager.store_context("list_data", [1, 2, {"a": "b"}], "short_term")
        await memory_manager.store_context("string_data", "simple string", "short_term")
        await memory_manager.store_context("number_data", 42.5, "short_term")

        assert await memory_manager.get_context("dict_data") == {"nested": {"key": [1, 2, 3]}}
        assert await memory_manager.get_context("list_data") == [1, 2, {"a": "b"}]
        assert await memory_manager.get_context("string_data") == "simple string"
        assert await memory_manager.get_context("number_data") == 42.5

    @pytest.mark.asyncio
    async def test_overwrite_same_key(self, memory_manager):
        """Test that storing with same key overwrites in index."""
        await memory_manager.store_context("key", "value1", "short_term")
        await memory_manager.store_context("key", "value2", "short_term")

        # Index should have latest value
        result = await memory_manager.get_context("key")
        assert result == "value2"

    @pytest.mark.asyncio
    async def test_empty_query_relevance(self, memory_manager):
        """Test relevance search with empty query."""
        await memory_manager.store_context("test", "some data", "short_term")
        result = await memory_manager.get_relevant_context("", limit=5)
        # Empty query should return empty or minimal results
        assert isinstance(result, str)
