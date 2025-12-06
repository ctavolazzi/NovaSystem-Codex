"""Memory Module for Nova MVP - Embeddings Architecture Stub.

Defines the interface for Nova's Long-Term Memory system.
This is a forward-looking architecture stub that prepares
for RAG (Retrieval Augmented Generation) implementation.

Target Embedding Model: gemini-embedding-001
- Dimensions: 768
- Task Types: RETRIEVAL_DOCUMENT, RETRIEVAL_QUERY, SEMANTIC_SIMILARITY

Future Use Cases:
1. Recall: Search past solution logs for relevant context
2. Routing: Use SEMANTIC_SIMILARITY to route prompts to the right Domain Expert
3. Knowledge Base: Store and retrieve domain-specific knowledge

Last Updated: 2025-12-06
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime


@dataclass
class Document:
    """A document stored in the vector store."""
    id: str
    text: str
    embedding: List[float] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.metadata:
            self.metadata = {}


@dataclass
class SearchResult:
    """A search result from the vector store."""
    document: Document
    score: float  # Similarity score (higher = more similar)

    def __lt__(self, other: "SearchResult") -> bool:
        return self.score < other.score


class VectorStore(ABC):
    """
    Abstract Base Class for Nova's Long-Term Memory.

    This interface defines the contract for vector storage backends.
    Implementations can use:
    - ChromaDB (local, lightweight)
    - Pinecone (cloud, scalable)
    - Weaviate (open source, feature-rich)
    - FAISS (high performance, local)

    Target Embedding Model: gemini-embedding-001
    - Output Dimensions: 768
    - Supported Task Types:
      - RETRIEVAL_DOCUMENT: For storing documents
      - RETRIEVAL_QUERY: For search queries
      - SEMANTIC_SIMILARITY: For routing/classification
    """

    # Standard embedding dimensions for gemini-embedding-001
    EMBEDDING_DIMENSIONS = 768

    @abstractmethod
    def embed_text(self, text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> List[float]:
        """
        Convert text to vector embedding using Gemini Embeddings.

        Args:
            text: Text to embed
            task_type: One of RETRIEVAL_DOCUMENT, RETRIEVAL_QUERY, SEMANTIC_SIMILARITY

        Returns:
            768-dimensional vector
        """
        pass

    @abstractmethod
    def add_document(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Store a document with its embedding in the vector store.

        Args:
            text: Document text
            metadata: Optional metadata (source, timestamp, tags, etc.)

        Returns:
            Document ID
        """
        pass

    @abstractmethod
    def search(
        self,
        query: str,
        limit: int = 3,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """
        Search for similar documents.

        Args:
            query: Search query text
            limit: Maximum number of results
            filter_metadata: Optional metadata filters

        Returns:
            List of SearchResult sorted by similarity (descending)
        """
        pass

    @abstractmethod
    def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document from the store.

        Args:
            doc_id: Document ID to delete

        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    def clear(self) -> int:
        """
        Clear all documents from the store.

        Returns:
            Number of documents deleted
        """
        pass


class MemoryStub(VectorStore):
    """
    Placeholder implementation for MVP stability.

    Provides a working interface without actual vector operations.
    Use this during development or when embeddings aren't needed.
    """

    def __init__(self):
        self._documents: Dict[str, Document] = {}
        self._counter = 0

    def embed_text(self, text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> List[float]:
        """Return a mock 768-dimensional zero vector."""
        # In production, this would call:
        # genai.embed_content(
        #     model="models/gemini-embedding-001",
        #     content=text,
        #     task_type=task_type
        # )
        return [0.0] * self.EMBEDDING_DIMENSIONS

    def add_document(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Store document in memory (no actual embedding)."""
        self._counter += 1
        doc_id = f"doc_{self._counter}"

        self._documents[doc_id] = Document(
            id=doc_id,
            text=text,
            embedding=self.embed_text(text),
            metadata=metadata or {}
        )

        return doc_id

    def search(
        self,
        query: str,
        limit: int = 3,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """
        Return empty results (no actual similarity search).

        In production, this would:
        1. Embed the query with task_type=RETRIEVAL_QUERY
        2. Compute cosine similarity with stored embeddings
        3. Return top-k results
        """
        # TODO: Implement actual similarity search when ready
        return []

    def delete_document(self, doc_id: str) -> bool:
        """Delete document from memory."""
        if doc_id in self._documents:
            del self._documents[doc_id]
            return True
        return False

    def clear(self) -> int:
        """Clear all documents."""
        count = len(self._documents)
        self._documents.clear()
        self._counter = 0
        return count

    def get_document(self, doc_id: str) -> Optional[Document]:
        """Get a document by ID."""
        return self._documents.get(doc_id)

    def list_documents(self) -> List[Document]:
        """List all stored documents."""
        return list(self._documents.values())


# Future implementation sketch (not active)
"""
class GeminiVectorStore(VectorStore):
    '''Production implementation using Gemini Embeddings + ChromaDB.'''

    def __init__(self, collection_name: str = "nova_memory"):
        import chromadb
        import google.generativeai as genai

        self._genai = genai
        self._client = chromadb.Client()
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def embed_text(self, text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> List[float]:
        result = self._genai.embed_content(
            model="models/gemini-embedding-001",
            content=text,
            task_type=task_type
        )
        return result['embedding']

    def add_document(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        doc_id = f"doc_{datetime.now().timestamp()}"
        embedding = self.embed_text(text, task_type="RETRIEVAL_DOCUMENT")

        self._collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata or {}]
        )
        return doc_id

    def search(
        self,
        query: str,
        limit: int = 3,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        query_embedding = self.embed_text(query, task_type="RETRIEVAL_QUERY")

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
            where=filter_metadata
        )

        search_results = []
        for i, doc_id in enumerate(results['ids'][0]):
            doc = Document(
                id=doc_id,
                text=results['documents'][0][i],
                metadata=results['metadatas'][0][i] if results['metadatas'] else {}
            )
            search_results.append(SearchResult(
                document=doc,
                score=1 - results['distances'][0][i]  # Convert distance to similarity
            ))

        return sorted(search_results, reverse=True)
"""


# Global instance for shared state
_memory_store: Optional[VectorStore] = None


def get_memory_store() -> VectorStore:
    """Get the global memory store instance."""
    global _memory_store
    if _memory_store is None:
        _memory_store = MemoryStub()
    return _memory_store


def set_memory_store(store: VectorStore):
    """Set a custom memory store implementation."""
    global _memory_store
    _memory_store = store
