"""
Model Caching System for NovaSystem.

This module provides intelligent model caching to improve performance
by reducing model loading times and optimizing memory usage.
"""

import asyncio
import logging
import time
import threading
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import OrderedDict
import json
import os
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class ModelCacheEntry:
    """Represents a cached model entry."""

    model_name: str
    model_type: str  # 'ollama', 'openai', etc.
    last_used: datetime
    access_count: int = 0
    load_time: float = 0.0
    memory_usage_mb: float = 0.0
    is_loaded: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'model_name': self.model_name,
            'model_type': self.model_type,
            'last_used': self.last_used.isoformat(),
            'access_count': self.access_count,
            'load_time': self.load_time,
            'memory_usage_mb': self.memory_usage_mb,
            'is_loaded': self.is_loaded,
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelCacheEntry':
        """Create from dictionary."""
        entry = cls(
            model_name=data['model_name'],
            model_type=data['model_type'],
            last_used=datetime.fromisoformat(data['last_used']),
            access_count=data.get('access_count', 0),
            load_time=data.get('load_time', 0.0),
            memory_usage_mb=data.get('memory_usage_mb', 0.0),
            is_loaded=data.get('is_loaded', False),
            metadata=data.get('metadata', {})
        )
        return entry

class ModelCache:
    """Intelligent model caching system."""

    def __init__(self,
                 max_cache_size: int = 3,
                 max_memory_mb: float = 8192,  # 8GB
                 cache_ttl_hours: int = 24,
                 cache_dir: Optional[str] = None):
        """
        Initialize the model cache.

        Args:
            max_cache_size: Maximum number of models to keep in cache
            max_memory_mb: Maximum memory usage in MB
            cache_ttl_hours: Cache time-to-live in hours
            cache_dir: Directory to store cache metadata
        """
        self.max_cache_size = max_cache_size
        self.max_memory_mb = max_memory_mb
        self.cache_ttl = timedelta(hours=cache_ttl_hours)
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / '.novasystem' / 'cache'

        # Create cache directory
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Cache storage
        self.cache: OrderedDict[str, ModelCacheEntry] = OrderedDict()
        self.lock = threading.RLock()

        # Statistics
        self.stats = {
            'cache_hits': 0,
            'cache_misses': 0,
            'models_loaded': 0,
            'models_unloaded': 0,
            'total_load_time': 0.0,
            'total_memory_saved': 0.0
        }

        # Load existing cache
        self._load_cache_metadata()

        # Start cleanup task
        self._start_cleanup_task()

    def _load_cache_metadata(self):
        """Load cache metadata from disk."""
        metadata_file = self.cache_dir / 'cache_metadata.json'
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r') as f:
                    data = json.load(f)
                    for model_name, entry_data in data.get('entries', {}).items():
                        entry = ModelCacheEntry.from_dict(entry_data)
                        # Only load metadata, not actual models
                        entry.is_loaded = False
                        self.cache[model_name] = entry
                    self.stats.update(data.get('stats', {}))
                logger.info(f"Loaded cache metadata for {len(self.cache)} models")
            except Exception as e:
                logger.warning(f"Failed to load cache metadata: {e}")

    def _save_cache_metadata(self):
        """Save cache metadata to disk."""
        metadata_file = self.cache_dir / 'cache_metadata.json'
        try:
            data = {
                'entries': {name: entry.to_dict() for name, entry in self.cache.items()},
                'stats': self.stats,
                'last_updated': datetime.now().isoformat()
            }
            with open(metadata_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.warning(f"Failed to save cache metadata: {e}")

    def _start_cleanup_task(self):
        """Start background cleanup task."""
        def cleanup():
            while True:
                try:
                    time.sleep(3600)  # Run every hour
                    self._cleanup_expired_entries()
                except Exception as e:
                    logger.error(f"Cache cleanup error: {e}")

        cleanup_thread = threading.Thread(target=cleanup, daemon=True)
        cleanup_thread.start()

    def _cleanup_expired_entries(self):
        """Remove expired cache entries."""
        with self.lock:
            now = datetime.now()
            expired_models = []

            for model_name, entry in self.cache.items():
                if now - entry.last_used > self.cache_ttl:
                    expired_models.append(model_name)

            for model_name in expired_models:
                self._unload_model(model_name)
                del self.cache[model_name]
                logger.info(f"Removed expired cache entry: {model_name}")

            if expired_models:
                self._save_cache_metadata()

    def _unload_model(self, model_name: str):
        """Unload a model from memory."""
        if model_name in self.cache:
            entry = self.cache[model_name]
            if entry.is_loaded:
                # For Ollama models, we can't actually unload them, but we can mark as unloaded
                # For OpenAI models, there's nothing to unload
                entry.is_loaded = False
                self.stats['models_unloaded'] += 1
                logger.info(f"Unloaded model: {model_name}")

    def _evict_lru_model(self):
        """Evict least recently used model."""
        if not self.cache:
            return

        # Find LRU model
        lru_model = min(self.cache.keys(),
                       key=lambda k: self.cache[k].last_used)

        self._unload_model(lru_model)
        del self.cache[lru_model]
        logger.info(f"Evicted LRU model: {lru_model}")

    def _check_memory_limit(self):
        """Check if we need to evict models due to memory limits."""
        total_memory = sum(entry.memory_usage_mb for entry in self.cache.values()
                          if entry.is_loaded)

        if total_memory > self.max_memory_mb:
            # Evict models until we're under the limit
            while (total_memory > self.max_memory_mb and
                   any(entry.is_loaded for entry in self.cache.values())):
                self._evict_lru_model()
                total_memory = sum(entry.memory_usage_mb for entry in self.cache.values()
                                  if entry.is_loaded)

    def get_model(self, model_name: str, model_type: str = "ollama") -> Optional[ModelCacheEntry]:
        """
        Get a model from cache.

        Args:
            model_name: Name of the model
            model_type: Type of model (ollama, openai, etc.)

        Returns:
            ModelCacheEntry if found, None otherwise
        """
        with self.lock:
            if model_name in self.cache:
                entry = self.cache[model_name]
                entry.last_used = datetime.now()
                entry.access_count += 1

                # Move to end (most recently used)
                self.cache.move_to_end(model_name)

                self.stats['cache_hits'] += 1
                logger.debug(f"Cache hit for model: {model_name}")
                return entry
            else:
                self.stats['cache_misses'] += 1
                logger.debug(f"Cache miss for model: {model_name}")
                return None

    def put_model(self, model_name: str, model_type: str = "ollama",
                  load_time: float = 0.0, memory_usage_mb: float = 0.0,
                  metadata: Optional[Dict[str, Any]] = None) -> ModelCacheEntry:
        """
        Add a model to cache.

        Args:
            model_name: Name of the model
            model_type: Type of model
            load_time: Time taken to load the model
            memory_usage_mb: Memory usage of the model
            metadata: Additional metadata

        Returns:
            ModelCacheEntry that was added
        """
        with self.lock:
            # Check if we need to evict models
            if len(self.cache) >= self.max_cache_size:
                self._evict_lru_model()

            # Create new entry
            entry = ModelCacheEntry(
                model_name=model_name,
                model_type=model_type,
                last_used=datetime.now(),
                access_count=1,
                load_time=load_time,
                memory_usage_mb=memory_usage_mb,
                is_loaded=True,
                metadata=metadata or {}
            )

            # Add to cache
            self.cache[model_name] = entry
            self.cache.move_to_end(model_name)

            # Update stats
            self.stats['models_loaded'] += 1
            self.stats['total_load_time'] += load_time
            self.stats['total_memory_saved'] += memory_usage_mb

            # Check memory limits
            self._check_memory_limit()

            # Save metadata
            self._save_cache_metadata()

            logger.info(f"Cached model: {model_name} (load time: {load_time:.2f}s, memory: {memory_usage_mb:.1f}MB)")
            return entry

    async def preload_model(self, model_name: str, model_type: str = "ollama") -> bool:
        """
        Preload a model into cache.

        Args:
            model_name: Name of the model to preload
            model_type: Type of model

        Returns:
            True if preloaded successfully, False otherwise
        """
        # Check if already cached
        if self.get_model(model_name, model_type):
            return True

        try:
            # For now, we'll just create a cache entry
            # In a real implementation, you might want to actually load the model
            start_time = time.time()

            # Simulate model loading (replace with actual loading logic)
            await asyncio.sleep(0.1)  # Simulate loading time

            load_time = time.time() - start_time

            # Estimate memory usage based on model type
            memory_usage = self._estimate_memory_usage(model_name, model_type)

            self.put_model(model_name, model_type, load_time, memory_usage)
            return True

        except Exception as e:
            logger.error(f"Failed to preload model {model_name}: {e}")
            return False

    def _estimate_memory_usage(self, model_name: str, model_type: str) -> float:
        """Estimate memory usage for a model."""
        # Rough estimates based on model names and types
        if model_type == "ollama":
            if "phi3" in model_name.lower():
                return 2200  # ~2.2GB
            elif "gpt-oss" in model_name.lower() or "20b" in model_name.lower():
                return 13000  # ~13GB
            elif "gemma" in model_name.lower():
                return 7500  # ~7.5GB
            else:
                return 4000  # Default estimate
        else:
            return 0  # OpenAI models don't use local memory

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self.lock:
            total_requests = self.stats['cache_hits'] + self.stats['cache_misses']
            hit_rate = (self.stats['cache_hits'] / total_requests * 100) if total_requests > 0 else 0

            return {
                'cache_size': len(self.cache),
                'max_cache_size': self.max_cache_size,
                'loaded_models': sum(1 for entry in self.cache.values() if entry.is_loaded),
                'total_memory_mb': sum(entry.memory_usage_mb for entry in self.cache.values() if entry.is_loaded),
                'max_memory_mb': self.max_memory_mb,
                'hit_rate_percent': hit_rate,
                'cache_hits': self.stats['cache_hits'],
                'cache_misses': self.stats['cache_misses'],
                'models_loaded': self.stats['models_loaded'],
                'models_unloaded': self.stats['models_unloaded'],
                'average_load_time': (self.stats['total_load_time'] / self.stats['models_loaded']
                                    if self.stats['models_loaded'] > 0 else 0),
                'cached_models': [entry.to_dict() for entry in self.cache.values()]
            }

    def clear_cache(self):
        """Clear all cached models."""
        with self.lock:
            for model_name in list(self.cache.keys()):
                self._unload_model(model_name)

            self.cache.clear()
            self._save_cache_metadata()
            logger.info("Cache cleared")

    def get_recommended_models(self, task_type: str = "general") -> List[str]:
        """
        Get recommended models for a task type based on cache performance.

        Args:
            task_type: Type of task (reasoning, coding, analysis, etc.)

        Returns:
            List of recommended model names
        """
        with self.lock:
            # Sort models by access count and recency
            sorted_models = sorted(
                self.cache.items(),
                key=lambda x: (x[1].access_count, x[1].last_used),
                reverse=True
            )

            # Filter by task type if metadata available
            if task_type != "general":
                filtered_models = [
                    (name, entry) for name, entry in sorted_models
                    if task_type in entry.metadata.get('capabilities', [])
                ]
                if filtered_models:
                    return [name for name, _ in filtered_models[:3]]

            # Return top 3 most used models
            return [name for name, _ in sorted_models[:3]]

# Global cache instance
_model_cache = None

def get_model_cache() -> ModelCache:
    """Get the global model cache instance."""
    global _model_cache
    if _model_cache is None:
        _model_cache = ModelCache()
    return _model_cache

def clear_model_cache():
    """Clear the global model cache."""
    global _model_cache
    if _model_cache:
        _model_cache.clear_cache()

# Export main classes and functions
__all__ = [
    'ModelCacheEntry',
    'ModelCache',
    'get_model_cache',
    'clear_model_cache'
]
