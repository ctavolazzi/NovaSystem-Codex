"""Embeddings and vector store interfaces for future RAG support."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


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


# TODO: Implement concrete stores once a vector database is selected.
# Gemini's `gemini-embedding-001` model produces 768-dimensional vectors.
# Planned uses:
# - Recall: storing past solution logs for retrieval in follow-up sessions.
# - Routing: using SEMANTIC_SIMILARITY to dispatch prompts to the best expert.
