"""
Comprehensive tests for the LocalVectorStore and embedding system.

Tests cover:
- SimpleEmbedder tokenization and hashing
- LocalVectorStore CRUD operations
- Cosine similarity search
- Tag filtering and scoring
- Persistence and loading
"""

import os
import sys
import json
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from novasystem.core.vector_store import (
    SimpleEmbedder,
    LocalVectorStore,
    cosine_similarity,
    _normalize,
)


class TestSimpleEmbedder:
    """Tests for the SimpleEmbedder hashing-based embedder."""

    @pytest.fixture
    def embedder(self):
        return SimpleEmbedder(dim=128)

    def test_embed_returns_correct_dimension(self, embedder):
        """Test that embeddings have the correct dimension."""
        vec = embedder.embed("Hello world, this is a test.")
        assert len(vec) == 128

    def test_embed_is_normalized(self, embedder):
        """Test that embeddings are normalized (unit length)."""
        vec = embedder.embed("Python programming language")
        norm = sum(x * x for x in vec) ** 0.5
        assert abs(norm - 1.0) < 0.0001 or norm == 0  # Either unit or zero vector

    def test_empty_text_returns_zero_vector(self, embedder):
        """Test that empty text returns a zero vector."""
        vec = embedder.embed("")
        assert all(x == 0 for x in vec)

    def test_stopwords_only_returns_zero_vector(self, embedder):
        """Test that text with only stopwords returns zero vector."""
        vec = embedder.embed("the a an is are")
        # All stopwords should be filtered out
        assert all(x == 0 for x in vec)

    def test_similar_texts_have_similar_embeddings(self, embedder):
        """Test that semantically similar texts produce similar vectors."""
        vec1 = embedder.embed("Python is a programming language")
        vec2 = embedder.embed("Python programming language code")
        vec3 = embedder.embed("Cooking recipes for dinner meals")

        sim_similar = cosine_similarity(vec1, vec2)
        sim_different = cosine_similarity(vec1, vec3)

        assert sim_similar > sim_different

    def test_tokenization_removes_short_words(self, embedder):
        """Test that tokenization filters short words."""
        tokens = embedder._tokenize("I am a big fan of AI")
        # 'I', 'am', 'a', 'of', 'AI' should be filtered (len <= 2 or stopword)
        assert "big" in tokens
        assert "fan" in tokens
        assert "i" not in tokens
        assert "am" not in tokens

    def test_different_dimensions(self):
        """Test embedders with different dimensions."""
        embedder_64 = SimpleEmbedder(dim=64)
        embedder_512 = SimpleEmbedder(dim=512)

        vec_64 = embedder_64.embed("test text")
        vec_512 = embedder_512.embed("test text")

        assert len(vec_64) == 64
        assert len(vec_512) == 512


class TestCosineSimilarity:
    """Tests for the cosine similarity function."""

    def test_identical_vectors_have_similarity_one(self):
        """Test that identical vectors have similarity 1.0."""
        vec = [0.5, 0.5, 0.5, 0.5]
        sim = cosine_similarity(vec, vec)
        assert abs(sim - 1.0) < 0.0001

    def test_orthogonal_vectors_have_similarity_zero(self):
        """Test that orthogonal vectors have similarity 0."""
        vec1 = [1.0, 0.0, 0.0, 0.0]
        vec2 = [0.0, 1.0, 0.0, 0.0]
        sim = cosine_similarity(vec1, vec2)
        assert abs(sim) < 0.0001

    def test_opposite_vectors_have_similarity_negative_one(self):
        """Test that opposite vectors have similarity -1."""
        vec1 = [1.0, 0.0]
        vec2 = [-1.0, 0.0]
        sim = cosine_similarity(vec1, vec2)
        assert abs(sim + 1.0) < 0.0001

    def test_mismatched_dimensions_raise_error(self):
        """Test that mismatched dimensions raise ValueError."""
        vec1 = [1.0, 2.0, 3.0]
        vec2 = [1.0, 2.0]
        with pytest.raises(ValueError):
            cosine_similarity(vec1, vec2)

    def test_zero_vector_returns_zero(self):
        """Test that zero vector returns 0 similarity."""
        zero_vec = [0.0, 0.0, 0.0]
        other_vec = [1.0, 2.0, 3.0]
        sim = cosine_similarity(zero_vec, other_vec)
        assert sim == 0.0


class TestLocalVectorStore:
    """Tests for LocalVectorStore operations."""

    @pytest.fixture
    def temp_store(self, tmp_path):
        """Create a temporary vector store for testing."""
        store_path = tmp_path / "test_memory.json"
        return LocalVectorStore(memory_file=store_path, persist=True)

    @pytest.fixture
    def memory_store(self):
        """Create an in-memory store (no persistence)."""
        return LocalVectorStore(persist=False)

    def test_add_and_retrieve_document(self, memory_store):
        """Test basic document storage and retrieval."""
        doc_id = memory_store.add_document(
            "Python is great for data science",
            metadata={"tags": ["python", "data"]}
        )

        assert doc_id.startswith("mem-")
        assert memory_store.count() == 1

    def test_remember_and_recall(self, memory_store):
        """Test the remember/recall convenience methods."""
        memory_store.remember(
            "Machine learning models need training data",
            tags=["ml", "data"],
            metadata={"source": "textbook"}
        )
        memory_store.remember(
            "Neural networks are a type of ML model",
            tags=["ml", "neural"],
        )
        memory_store.remember(
            "Cooking requires fresh ingredients",
            tags=["cooking"],
        )

        results = memory_store.recall("machine learning training", limit=2)
        assert len(results) >= 1
        # ML-related should score higher than cooking
        texts = [r[0]["text"] for r in results]
        assert any("machine" in t.lower() or "neural" in t.lower() for t in texts)

    def test_recall_with_tag_filter(self, memory_store):
        """Test that recall respects tag filters."""
        memory_store.remember("Python web frameworks", tags=["python", "web"])
        memory_store.remember("Python machine learning", tags=["python", "ml"])
        memory_store.remember("Java enterprise applications", tags=["java", "enterprise"])

        results = memory_store.recall("programming frameworks", limit=5, tags=["python"])
        for result, score in results:
            assert "python" in result["tags"]

    def test_recall_with_min_score(self, memory_store):
        """Test that recall respects minimum score threshold."""
        memory_store.remember("Quantum computing fundamentals", tags=["quantum"])
        memory_store.remember("Classical physics principles", tags=["physics"])

        # High min_score should filter out weak matches
        results = memory_store.recall("quantum", limit=5, min_score=0.5)
        for result, score in results:
            assert score >= 0.5

    def test_forget_removes_document(self, memory_store):
        """Test that forget removes documents."""
        doc_id = memory_store.remember("Temporary note to delete")
        assert memory_store.count() == 1

        removed = memory_store.forget(doc_id)
        assert removed is True
        assert memory_store.count() == 0

    def test_forget_nonexistent_returns_false(self, memory_store):
        """Test that forgetting nonexistent doc returns False."""
        result = memory_store.forget("nonexistent-id")
        assert result is False

    def test_clear_removes_all(self, memory_store):
        """Test that clear removes all documents."""
        for i in range(5):
            memory_store.remember(f"Document number {i}")

        assert memory_store.count() == 5
        cleared = memory_store.clear()
        assert cleared == 5
        assert memory_store.count() == 0

    def test_list_all_returns_recent_first(self, memory_store):
        """Test that list_all returns documents in reverse chronological order."""
        import time
        memory_store.remember("First document")
        time.sleep(0.01)  # Small delay to ensure different timestamps
        memory_store.remember("Second document")
        time.sleep(0.01)
        memory_store.remember("Third document")

        docs = memory_store.list_all(limit=3)
        assert "Third" in docs[0]["text"]
        assert "First" in docs[2]["text"]

    def test_stats_reports_correct_info(self, memory_store):
        """Test that stats returns accurate information."""
        memory_store.remember("Doc 1", tags=["python"])
        memory_store.remember("Doc 2", tags=["python", "ml"])
        memory_store.remember("Doc 3", tags=["java"])

        stats = memory_store.stats()
        assert stats["count"] == 3
        assert stats["tags"]["python"] == 2
        assert stats["tags"]["ml"] == 1
        assert stats["tags"]["java"] == 1
        assert stats["avg_length"] > 0


class TestVectorStorePersistence:
    """Tests for vector store persistence."""

    def test_save_and_load(self, tmp_path):
        """Test that documents persist across store instances."""
        store_path = tmp_path / "persist_test.json"

        # Create and populate store
        store1 = LocalVectorStore(memory_file=store_path, persist=True)
        store1.remember("Persistent memory test", tags=["test"])
        store1.remember("Another persistent entry", tags=["test"])

        # Create new instance pointing to same file
        store2 = LocalVectorStore(memory_file=store_path, persist=True)
        assert store2.count() == 2

        results = store2.recall("persistent memory", limit=2)
        assert len(results) >= 1

    def test_atomic_write_creates_file(self, tmp_path):
        """Test that saving creates the persistence file."""
        store_path = tmp_path / "new_store.json"
        assert not store_path.exists()

        store = LocalVectorStore(memory_file=store_path, persist=True)
        store.remember("Test document")

        assert store_path.exists()

    def test_corrupt_file_handled_gracefully(self, tmp_path):
        """Test that corrupt JSON is handled gracefully."""
        store_path = tmp_path / "corrupt.json"
        store_path.write_text("{ invalid json }")

        # Should not raise, should start fresh
        store = LocalVectorStore(memory_file=store_path, persist=True)
        assert store.count() == 0

    def test_clear_removes_persistence_file(self, tmp_path):
        """Test that clear removes the persistence file."""
        store_path = tmp_path / "to_clear.json"

        store = LocalVectorStore(memory_file=store_path, persist=True)
        store.remember("Test")
        assert store_path.exists()

        store.clear()
        assert not store_path.exists()


class TestSearchQuality:
    """Tests for search result quality."""

    @pytest.fixture
    def populated_store(self):
        """Create a store with diverse documents."""
        store = LocalVectorStore(persist=False)

        documents = [
            ("Python is excellent for data analysis and machine learning", ["python", "ml"]),
            ("JavaScript powers modern web applications", ["javascript", "web"]),
            ("Docker containers simplify deployment", ["docker", "devops"]),
            ("PostgreSQL is a powerful relational database", ["database", "sql"]),
            ("React and Vue are popular frontend frameworks", ["javascript", "frontend"]),
            ("TensorFlow and PyTorch are deep learning frameworks", ["python", "ml"]),
            ("Kubernetes orchestrates container deployments", ["docker", "devops"]),
            ("MongoDB is a NoSQL document database", ["database", "nosql"]),
        ]

        for text, tags in documents:
            store.remember(text, tags=tags)

        return store

    def test_search_returns_relevant_results(self, populated_store):
        """Test that search returns contextually relevant results."""
        results = populated_store.recall("machine learning Python", limit=3)

        # Should prioritize ML and Python related documents
        texts = [r[0]["text"].lower() for r in results]
        assert any("machine learning" in t or "tensorflow" in t for t in texts)

    def test_search_ranking_makes_sense(self, populated_store):
        """Test that search ranking reflects relevance."""
        results = populated_store.recall("container deployment orchestration", limit=5)

        # Docker/Kubernetes docs should rank higher than unrelated
        if len(results) >= 2:
            top_result = results[0][0]["text"].lower()
            assert "docker" in top_result or "kubernetes" in top_result or "container" in top_result

    def test_search_with_no_matches_returns_empty(self, populated_store):
        """Test that unrelated queries return low scores."""
        results = populated_store.recall(
            "underwater basket weaving",
            limit=5,
            min_score=0.3  # Require reasonable similarity
        )
        # Should return very few or no results
        assert len(results) <= 2
