"""
Memory and Context Management for Nova Process.

This module provides context management and memory storage for the Nova Process,
enabling agents to maintain awareness of previous work and build upon it.
"""

from typing import Dict, List, Any, Optional
import json
import logging
from datetime import datetime
from collections import deque

logger = logging.getLogger(__name__)

class MemoryManager:
    """
    Manages memory and context for the Nova Process.

    Provides short-term and long-term memory storage, context retrieval,
    and memory compression for efficient context management.
    """

    def __init__(self, max_short_term: int = 10, max_long_term: int = 100):
        """
        Initialize the memory manager.

        Args:
            max_short_term: Maximum number of short-term memories
            max_long_term: Maximum number of long-term memories
        """
        self.short_term_memory = deque(maxlen=max_short_term)
        self.long_term_memory = deque(maxlen=max_long_term)
        self.context_index = {}  # For quick context lookup

    async def store_context(self, key: str, data: Any, memory_type: str = "short_term") -> None:
        """
        Store context data in memory.

        Args:
            key: Unique identifier for the context
            data: Data to store
            memory_type: "short_term" or "long_term"
        """
        memory_entry = {
            "key": key,
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "type": memory_type
        }

        if memory_type == "short_term":
            self.short_term_memory.append(memory_entry)
        else:
            self.long_term_memory.append(memory_entry)

        # Update index
        self.context_index[key] = memory_entry

        logger.debug(f"Stored context: {key} in {memory_type} memory")

    async def get_context(self, key: str) -> Optional[Any]:
        """
        Retrieve context data by key.

        Args:
            key: Context identifier

        Returns:
            Context data or None if not found
        """
        if key in self.context_index:
            return self.context_index[key]["data"]
        return None

    async def get_relevant_context(self, query: str, limit: int = 5) -> str:
        """
        Get relevant context based on a query.

        Args:
            query: Query to find relevant context
            limit: Maximum number of context entries to return

        Returns:
            Formatted relevant context
        """
        relevant_contexts = []

        # Search through short-term memory first (more recent)
        for entry in reversed(self.short_term_memory):
            if self._is_relevant(entry["data"], query):
                relevant_contexts.append(entry)
                if len(relevant_contexts) >= limit:
                    break

        # Search through long-term memory if needed
        if len(relevant_contexts) < limit:
            for entry in reversed(self.long_term_memory):
                if self._is_relevant(entry["data"], query):
                    relevant_contexts.append(entry)
                    if len(relevant_contexts) >= limit:
                        break

        # Format the context
        formatted_context = []
        for entry in relevant_contexts:
            formatted_context.append(f"**{entry['key']}** ({entry['timestamp']}):")
            formatted_context.append(str(entry['data']))
            formatted_context.append("")

        return "\n".join(formatted_context)

    async def get_all_context(self) -> Dict[str, Any]:
        """
        Get all stored context.

        Returns:
            Dictionary of all context data
        """
        all_context = {}

        # Add short-term memory
        for entry in self.short_term_memory:
            all_context[entry["key"]] = entry["data"]

        # Add long-term memory
        for entry in self.long_term_memory:
            all_context[entry["key"]] = entry["data"]

        return all_context

    def _is_relevant(self, data: Any, query: str) -> bool:
        """
        Check if data is relevant to the query.

        Args:
            data: Data to check
            query: Query string

        Returns:
            True if relevant, False otherwise
        """
        # Simple relevance check - can be enhanced with semantic similarity
        data_str = str(data).lower()
        query_str = query.lower()

        # Check for keyword matches
        query_words = query_str.split()
        return any(word in data_str for word in query_words if len(word) > 2)

    async def compress_memory(self) -> None:
        """
        Compress memory by moving important items to long-term storage
        and removing less important items.
        """
        # Move important short-term memories to long-term
        important_entries = []
        for entry in list(self.short_term_memory):
            if self._is_important(entry):
                important_entries.append(entry)
                self.short_term_memory.remove(entry)

        # Add to long-term memory
        for entry in important_entries:
            entry["type"] = "long_term"
            self.long_term_memory.append(entry)

        logger.info(f"Compressed memory: moved {len(important_entries)} entries to long-term")

    def _is_important(self, entry: Dict[str, Any]) -> bool:
        """
        Determine if a memory entry is important enough for long-term storage.

        Args:
            entry: Memory entry to evaluate

        Returns:
            True if important, False otherwise
        """
        # Simple importance heuristic - can be enhanced
        key = entry["key"]
        data = entry["data"]

        # Important keys
        important_keys = [
            "problem", "final_result", "solution", "decision"
        ]

        if any(imp_key in key.lower() for imp_key in important_keys):
            return True

        # Important data patterns
        data_str = str(data).lower()
        important_patterns = [
            "final", "complete", "solution", "decision", "recommendation"
        ]

        return any(pattern in data_str for pattern in important_patterns)

    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get memory usage statistics.

        Returns:
            Dictionary with memory statistics
        """
        return {
            "short_term_count": len(self.short_term_memory),
            "long_term_count": len(self.long_term_memory),
            "total_contexts": len(self.context_index),
            "short_term_max": self.short_term_memory.maxlen,
            "long_term_max": self.long_term_memory.maxlen
        }

    def clear_memory(self) -> None:
        """Clear all memory."""
        self.short_term_memory.clear()
        self.long_term_memory.clear()
        self.context_index.clear()
        logger.info("Cleared all memory")
