"""Memory system for Nova - Long-term knowledge persistence.

Provides vector storage and semantic search capabilities:
- LocalVectorStore: JSON-backed storage with cosine similarity
- SimpleEmbedder: Lightweight local embeddings (no API costs)
- Future: GeminiEmbedder for higher quality (768-dim vectors)

Usage:
    from backend.core.memory import get_memory_store
    
    store = get_memory_store()
    
    # Remember something
    doc_id = store.remember("Python uses indentation for blocks", tags=["python", "syntax"])
    
    # Recall related memories
    results = store.recall("How does Python handle code blocks?", limit=3)
    for doc, score in results:
        print(f"{score:.2f}: {doc['text']}")
"""

import hashlib
import json
import math
import os
import re
import time
from abc import ABC, abstractmethod
from collections import Counter
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# =============================================================================
# CONFIGURATION
# =============================================================================

DEFAULT_MEMORY_FILE = ".nova_memory.json"
DEFAULT_EMBEDDING_DIM = 256  # Simple embedder dimension


# =============================================================================
# ABSTRACT INTERFACES
# =============================================================================


class Embedder(ABC):
    """Abstract interface for text embedding."""

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Return the embedding vector dimension."""

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Generate an embedding vector for the provided text."""


class VectorStore(ABC):
    """Abstract interface for vector storage backends."""

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """Generate an embedding vector for the provided text."""

    @abstractmethod
    def search(self, query_vector: List[float], limit: int = 3) -> List[Dict[str, Any]]:
        """Return the top matching documents for the query vector."""

    @abstractmethod
    def add_document(self, text: str, metadata: Dict[str, Any]) -> str:
        """Persist a document and return its identifier."""


# =============================================================================
# SIMPLE EMBEDDER (No API costs)
# =============================================================================


class SimpleEmbedder(Embedder):
    """Lightweight local embedder using hash-based features.
    
    This embedder creates vectors without any API calls by:
    1. Tokenizing text into words
    2. Computing hash-based features for each word
    3. Aggregating into a fixed-dimension vector
    
    Not as good as neural embeddings, but:
    - Zero cost
    - Zero latency
    - Works offline
    - Good enough for keyword-based recall
    """

    def __init__(self, dim: int = DEFAULT_EMBEDDING_DIM):
        self._dim = dim
        # Common English stopwords to ignore
        self._stopwords = {
            "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "must", "shall", "can", "need", "dare",
            "ought", "used", "to", "of", "in", "for", "on", "with", "at", "by",
            "from", "as", "into", "through", "during", "before", "after", "above",
            "below", "between", "under", "again", "further", "then", "once", "here",
            "there", "when", "where", "why", "how", "all", "each", "few", "more",
            "most", "other", "some", "such", "no", "nor", "not", "only", "own",
            "same", "so", "than", "too", "very", "just", "and", "but", "if", "or",
            "because", "until", "while", "this", "that", "these", "those", "i",
            "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
            "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she",
            "her", "hers", "herself", "it", "its", "itself", "they", "them", "their",
            "theirs", "themselves", "what", "which", "who", "whom", "whose",
        }

    @property
    def dimension(self) -> int:
        return self._dim

    def _tokenize(self, text: str) -> List[str]:
        """Extract meaningful tokens from text."""
        # Lowercase and extract words
        words = re.findall(r'\b[a-z][a-z0-9]*\b', text.lower())
        # Filter stopwords and very short words
        return [w for w in words if w not in self._stopwords and len(w) > 2]

    def _hash_to_index(self, word: str, seed: int = 0) -> int:
        """Hash a word to an index in the embedding space."""
        h = hashlib.md5(f"{word}:{seed}".encode()).hexdigest()
        return int(h, 16) % self._dim

    def embed(self, text: str) -> List[float]:
        """Generate a hash-based embedding vector."""
        tokens = self._tokenize(text)
        if not tokens:
            # Return zero vector for empty text
            return [0.0] * self._dim

        # Initialize vector
        vector = [0.0] * self._dim

        # Count token frequencies
        token_counts = Counter(tokens)
        total_tokens = sum(token_counts.values())

        # For each unique token, add weighted contributions
        for token, count in token_counts.items():
            weight = count / total_tokens  # TF-like weight

            # Use multiple hash functions for better distribution
            for seed in range(3):
                idx = self._hash_to_index(token, seed)
                # Alternate sign based on another hash
                sign = 1 if int(hashlib.md5(f"{token}:sign:{seed}".encode()).hexdigest(), 16) % 2 == 0 else -1
                vector[idx] += sign * weight

        # Normalize to unit vector
        magnitude = math.sqrt(sum(x * x for x in vector))
        if magnitude > 0:
            vector = [x / magnitude for x in vector]

        return vector


# =============================================================================
# VECTOR MATH
# =============================================================================


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two vectors."""
    if len(vec_a) != len(vec_b):
        raise ValueError(f"Vector dimensions must match: {len(vec_a)} vs {len(vec_b)}")

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a * a for a in vec_a))
    mag_b = math.sqrt(sum(b * b for b in vec_b))

    if mag_a == 0 or mag_b == 0:
        return 0.0

    return dot_product / (mag_a * mag_b)


# =============================================================================
# LOCAL VECTOR STORE
# =============================================================================


@dataclass
class MemoryDocument:
    """A document stored in memory."""
    id: str
    text: str
    vector: List[float]
    created_at: float
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class LocalVectorStore(VectorStore):
    """JSON-backed vector store with cosine similarity search.
    
    Features:
    - Persistent storage in JSON file
    - Automatic loading on init
    - Cosine similarity search
    - Tag-based filtering
    - Configurable embedder
    """

    def __init__(
        self,
        memory_file: str | None = None,
        embedder: Embedder | None = None,
    ):
        self._memory_file = memory_file or DEFAULT_MEMORY_FILE
        self._embedder = embedder or SimpleEmbedder()
        self._documents: Dict[str, MemoryDocument] = {}
        self._load()

    def _load(self) -> None:
        """Load documents from disk."""
        if not os.path.exists(self._memory_file):
            return

        try:
            with open(self._memory_file, "r") as f:
                data = json.load(f)

            for doc_data in data.get("documents", []):
                doc = MemoryDocument(
                    id=doc_data["id"],
                    text=doc_data["text"],
                    vector=doc_data["vector"],
                    created_at=doc_data["created_at"],
                    tags=doc_data.get("tags", []),
                    metadata=doc_data.get("metadata", {}),
                )
                self._documents[doc.id] = doc

            if self._documents:
                print(f"✅ Memory loaded ({len(self._documents)} documents)")

        except Exception as e:
            print(f"⚠️ Failed to load memory (starting fresh): {e}")
            self._documents = {}

    def _save(self) -> None:
        """Persist documents to disk using atomic write."""
        data = {
            "version": "1.0",
            "embedder_dim": self._embedder.dimension,
            "document_count": len(self._documents),
            "documents": [asdict(doc) for doc in self._documents.values()],
        }

        # Atomic write: temp file then rename
        temp_file = f"{self._memory_file}.tmp"
        try:
            with open(temp_file, "w") as f:
                json.dump(data, f, indent=2)
            os.replace(temp_file, self._memory_file)
        except Exception as e:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            print(f"⚠️ Failed to save memory: {e}")

    def _generate_id(self, text: str) -> str:
        """Generate a unique document ID."""
        timestamp = str(time.time()).replace(".", "")
        text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
        return f"mem_{timestamp}_{text_hash}"

    # =========================================================================
    # VectorStore Interface
    # =========================================================================

    def embed_text(self, text: str) -> List[float]:
        """Generate an embedding vector for the provided text."""
        return self._embedder.embed(text)

    def search(self, query_vector: List[float], limit: int = 3) -> List[Dict[str, Any]]:
        """Return the top matching documents for the query vector."""
        if not self._documents:
            return []

        # Compute similarities
        scored = []
        for doc in self._documents.values():
            sim = cosine_similarity(query_vector, doc.vector)
            scored.append((doc, sim))

        # Sort by similarity (descending)
        scored.sort(key=lambda x: x[1], reverse=True)

        # Return top results
        results = []
        for doc, score in scored[:limit]:
            results.append({
                "id": doc.id,
                "text": doc.text,
                "score": round(score, 4),
                "tags": doc.tags,
                "metadata": doc.metadata,
                "created_at": doc.created_at,
            })

        return results

    def add_document(self, text: str, metadata: Dict[str, Any] | None = None) -> str:
        """Persist a document and return its identifier."""
        doc_id = self._generate_id(text)
        vector = self._embedder.embed(text)

        doc = MemoryDocument(
            id=doc_id,
            text=text,
            vector=vector,
            created_at=time.time(),
            tags=metadata.get("tags", []) if metadata else [],
            metadata=metadata or {},
        )

        self._documents[doc_id] = doc
        self._save()

        return doc_id

    # =========================================================================
    # Convenience Methods
    # =========================================================================

    def remember(
        self,
        text: str,
        tags: List[str] | None = None,
        metadata: Dict[str, Any] | None = None,
    ) -> str:
        """Store a memory. Returns the document ID."""
        meta = metadata or {}
        if tags:
            meta["tags"] = tags
        return self.add_document(text, meta)

    def recall(
        self,
        query: str,
        limit: int = 5,
        min_score: float = 0.1,
        tags: List[str] | None = None,
    ) -> List[Tuple[Dict[str, Any], float]]:
        """Search for related memories.
        
        Args:
            query: The search query
            limit: Maximum number of results
            min_score: Minimum similarity score (0-1)
            tags: Optional tag filter (documents must have ALL tags)
            
        Returns:
            List of (document, score) tuples
        """
        query_vector = self.embed_text(query)
        results = self.search(query_vector, limit=limit * 2)  # Get extra for filtering

        # Filter by score and tags
        filtered = []
        for doc in results:
            if doc["score"] < min_score:
                continue
            if tags and not all(t in doc.get("tags", []) for t in tags):
                continue
            filtered.append((doc, doc["score"]))
            if len(filtered) >= limit:
                break

        return filtered

    def forget(self, doc_id: str) -> bool:
        """Remove a memory by ID. Returns True if found and removed."""
        if doc_id in self._documents:
            del self._documents[doc_id]
            self._save()
            return True
        return False

    def clear(self) -> int:
        """Clear all memories. Returns count of removed documents."""
        count = len(self._documents)
        self._documents.clear()
        if os.path.exists(self._memory_file):
            os.remove(self._memory_file)
        return count

    def list_all(self, limit: int = 100) -> List[Dict[str, Any]]:
        """List all stored memories."""
        docs = sorted(
            self._documents.values(),
            key=lambda d: d.created_at,
            reverse=True
        )[:limit]

        return [
            {
                "id": doc.id,
                "text": doc.text[:100] + "..." if len(doc.text) > 100 else doc.text,
                "tags": doc.tags,
                "created_at": doc.created_at,
            }
            for doc in docs
        ]

    def count(self) -> int:
        """Return the number of stored documents."""
        return len(self._documents)

    def stats(self) -> Dict[str, Any]:
        """Return memory statistics."""
        if not self._documents:
            return {"count": 0, "tags": {}, "avg_length": 0}

        all_tags: Counter = Counter()
        total_length = 0

        for doc in self._documents.values():
            all_tags.update(doc.tags)
            total_length += len(doc.text)

        return {
            "count": len(self._documents),
            "tags": dict(all_tags.most_common(20)),
            "avg_length": round(total_length / len(self._documents)),
            "embedder_dim": self._embedder.dimension,
        }


# =============================================================================
# GLOBAL INSTANCE
# =============================================================================

_memory_store: Optional[LocalVectorStore] = None


def get_memory_store(memory_file: str | None = None) -> LocalVectorStore:
    """Get the global memory store instance."""
    global _memory_store
    if _memory_store is None:
        _memory_store = LocalVectorStore(memory_file=memory_file)
    return _memory_store


# =============================================================================
# FUTURE: Gemini Embedder (placeholder)
# =============================================================================

# class GeminiEmbedder(Embedder):
#     """High-quality embeddings using Gemini's embedding model.
#     
#     Model: gemini-embedding-001
#     Dimension: 768
#     Cost: ~$0.00001 per 1K characters
#     """
#     
#     @property
#     def dimension(self) -> int:
#         return 768
#     
#     def embed(self, text: str) -> List[float]:
#         # TODO: Implement with google.generativeai
#         pass
