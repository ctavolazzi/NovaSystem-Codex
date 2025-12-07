"""Local long-term memory (JSON + cosine similarity).

Provides a zero-cost vector store so Nova can remember facts between runs.
Embeddings are hashed into a fixed-size vector and stored alongside text.
"""

import hashlib
import json
import math
import os
import re
import threading
import time
import uuid
from abc import ABC, abstractmethod
from collections import Counter
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_MEMORY_FILE = ".nova_memory.json"
DEFAULT_EMBEDDING_DIM = 256


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


def _normalize(vector: List[float]) -> List[float]:
    norm = math.sqrt(sum(x * x for x in vector))
    if norm == 0:
        return [0.0] * len(vector)
    return [x / norm for x in vector]


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    if len(vec_a) != len(vec_b):
        raise ValueError(f"Vector dimensions must match: {len(vec_a)} vs {len(vec_b)}")

    denom = math.sqrt(sum(a * a for a in vec_a)) * math.sqrt(sum(b * b for b in vec_b))
    if denom == 0:
        return 0.0
    return sum(a * b for a, b in zip(vec_a, vec_b)) / denom


class SimpleEmbedder(Embedder):
    """Lightweight local embedder using a hashing trick (no API calls)."""

    def __init__(self, dim: int = DEFAULT_EMBEDDING_DIM):
        self._dim = dim
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
        tokens = re.findall(r"[a-z0-9']+", text.lower())
        return [t for t in tokens if len(t) > 2 and t not in self._stopwords]

    def _bucket(self, token: str, seed: int) -> int:
        digest = hashlib.blake2b(f"{token}:{seed}".encode(), digest_size=4).digest()
        return int.from_bytes(digest, "big") % self._dim

    def embed(self, text: str) -> List[float]:
        """Generate a normalized embedding vector."""
        tokens = self._tokenize(text)
        if not tokens:
            return [0.0] * self._dim

        counts = Counter(tokens)
        total = sum(counts.values())
        vector = [0.0] * self._dim

        for token, count in counts.items():
            weight = count / total
            for seed in range(2):
                idx = self._bucket(token, seed)
                # Alternate sign to reduce collisions
                sign = 1 if (idx + seed) % 2 == 0 else -1
                vector[idx] += sign * weight

        return _normalize(vector)


@dataclass
class MemoryDocument:
    """A stored memory entry."""

    id: str
    text: str
    vector: List[float]
    created_at: float = field(default_factory=lambda: time.time())
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class LocalVectorStore(VectorStore):
    """JSON-backed vector store with cosine similarity search."""

    def __init__(
        self,
        memory_file: str | Path | None = None,
        embedder: Embedder | None = None,
        persist: bool = True,
    ):
        self._path = Path(memory_file or DEFAULT_MEMORY_FILE)
        self._embedder = embedder or SimpleEmbedder()
        self._persist = persist
        self._documents: Dict[str, MemoryDocument] = {}
        self._lock = threading.Lock()

        if self._persist:
            self._load()

    # ------------------------------------------------------------------
    # VectorStore interface
    # ------------------------------------------------------------------
    def embed_text(self, text: str) -> List[float]:
        return self._embedder.embed(text)

    def search(self, query_vector: List[float], limit: int = 3) -> List[Dict[str, Any]]:
        """Return top matches for a query vector."""
        if len(query_vector) != self._embedder.dimension:
            raise ValueError(f"Query vector must have {self._embedder.dimension} dimensions")

        normalized_query = _normalize(query_vector)

        with self._lock:
            documents = list(self._documents.values())

        scored: List[Tuple[float, MemoryDocument]] = []
        for doc in documents:
            score = cosine_similarity(normalized_query, doc.vector)
            if score > 0:
                scored.append((score, doc))

        scored.sort(key=lambda item: item[0], reverse=True)
        top = scored[:limit]

        return [
            {
                "id": doc.id,
                "text": doc.text,
                "score": round(score, 6),
                "tags": doc.tags,
                "metadata": doc.metadata,
                "created_at": doc.created_at,
            }
            for score, doc in top
        ]

    def add_document(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Persist a document and return its identifier."""
        metadata = metadata or {}
        tags = metadata.get("tags", [])
        if tags and not isinstance(tags, list):
            tags = [str(tags)]

        record = MemoryDocument(
            id=self._generate_id(),
            text=text,
            vector=self.embed_text(text),
            metadata=metadata,
            tags=tags,
        )

        with self._lock:
            self._documents[record.id] = record
            if self._persist:
                self._save_locked()

        return record.id

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------
    def remember(
        self,
        text: str,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
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
        tags: Optional[List[str]] = None,
    ) -> List[Tuple[Dict[str, Any], float]]:
        """Search for related memories with optional tag and score filters."""
        results = self.search(self.embed_text(query), limit=max(limit * 2, limit))

        filtered: List[Tuple[Dict[str, Any], float]] = []
        for item in results:
            score = item["score"]
            if score < min_score:
                continue
            if tags and not all(tag in item.get("tags", []) for tag in tags):
                continue
            filtered.append((item, score))
            if len(filtered) >= limit:
                break

        return filtered

    def forget(self, doc_id: str) -> bool:
        """Remove a memory by ID."""
        with self._lock:
            existed = self._documents.pop(doc_id, None) is not None
            if existed and self._persist:
                self._save_locked()
        return existed

    def clear(self) -> int:
        """Clear all memories and delete persisted file."""
        with self._lock:
            count = len(self._documents)
            self._documents.clear()

            if self._persist and self._path.exists():
                self._path.unlink()

        return count

    def list_all(self, limit: int = 100) -> List[Dict[str, Any]]:
        """List stored memories (most recent first)."""
        with self._lock:
            docs = sorted(
                self._documents.values(),
                key=lambda d: d.created_at,
                reverse=True,
            )[:limit]

        return [
            {
                "id": doc.id,
                "text": (doc.text[:100] + "...") if len(doc.text) > 100 else doc.text,
                "tags": doc.tags,
                "created_at": doc.created_at,
            }
            for doc in docs
        ]

    def count(self) -> int:
        """Return the number of stored documents."""
        with self._lock:
            return len(self._documents)

    def stats(self) -> Dict[str, Any]:
        """Return memory statistics."""
        with self._lock:
            docs = list(self._documents.values())

        if not docs:
            return {"count": 0, "tags": {}, "avg_length": 0, "embedder_dim": self._embedder.dimension}

        tag_counts = Counter(tag for doc in docs for tag in doc.tags)
        avg_length = sum(len(doc.text) for doc in docs) / len(docs)

        return {
            "count": len(docs),
            "tags": dict(tag_counts.most_common(20)),
            "avg_length": round(avg_length),
            "embedder_dim": self._embedder.dimension,
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _generate_id(self) -> str:
        return f"mem-{uuid.uuid4().hex[:8]}"

    def _load(self) -> None:
        """Load documents from disk, skipping malformed entries."""
        if not self._path.exists():
            return

        try:
            with open(self._path, "r") as f:
                data = json.load(f)

            stored_dim = data.get("embedder_dim") or data.get("dimension") or self._embedder.dimension
            raw_docs = data.get("documents") or data.get("records") or []

            loaded: Dict[str, MemoryDocument] = {}
            for item in raw_docs:
                vector = item.get("vector") or item.get("embedding")
                if not isinstance(vector, list):
                    continue

                # Re-embed if dimensions changed
                if len(vector) != self._embedder.dimension and stored_dim != self._embedder.dimension:
                    vector = self.embed_text(item.get("text", ""))
                elif len(vector) == self._embedder.dimension:
                    vector = _normalize([float(v) for v in vector])
                else:
                    continue

                metadata = item.get("metadata") or {}
                if not isinstance(metadata, dict):
                    metadata = {}

                doc = MemoryDocument(
                    id=item.get("id") or self._generate_id(),
                    text=item.get("text", ""),
                    vector=vector,
                    created_at=float(item.get("created_at", time.time())),
                    tags=item.get("tags", []) or [],
                    metadata=metadata,
                )
                loaded[doc.id] = doc

            self._documents = loaded
            if self._documents:
                print(f"✅ Memory loaded ({len(self._documents)} documents)")

        except Exception as e:
            print(f"⚠️ Failed to load memory (starting fresh): {e}")
            self._documents = {}

    def _save_locked(self) -> None:
        """Persist documents to disk using an atomic write + merge strategy."""
        if not self._persist:
            return

        disk_docs: Dict[str, Dict[str, Any]] = {}
        if self._path.exists():
            try:
                with open(self._path, "r") as f:
                    data = json.load(f)
                for item in data.get("documents", []):
                    doc_id = item.get("id")
                    if doc_id:
                        disk_docs[doc_id] = item
            except Exception:
                pass

        merged = {**disk_docs, **{doc.id: asdict(doc) for doc in self._documents.values()}}

        payload = {
            "version": "1.1",
            "embedder_dim": self._embedder.dimension,
            "document_count": len(merged),
            "documents": list(merged.values()),
        }

        temp_path = self._path.with_suffix(self._path.suffix + ".tmp")
        self._path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(temp_path, "w") as f:
                json.dump(payload, f, indent=2)
            os.replace(temp_path, self._path)
        except Exception as e:
            if temp_path.exists():
                try:
                    os.remove(temp_path)
                except Exception:
                    pass
            print(f"⚠️ Failed to save memory: {e}")


# Global instance
_memory_store: Optional[LocalVectorStore] = None


def get_memory_store(memory_file: str | None = None) -> LocalVectorStore:
    """Get the global memory store instance."""
    global _memory_store
    if _memory_store is None:
        _memory_store = LocalVectorStore(memory_file=memory_file)
    return _memory_store
