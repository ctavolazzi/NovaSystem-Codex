"""
Performance Metrics and Monitoring for NovaSystem.

This module provides comprehensive performance monitoring, metrics collection,
and analytics for the NovaSystem framework.
"""

import time
import psutil
import logging
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from collections import defaultdict, deque
import json
import threading
from functools import wraps

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Container for performance metrics."""

    # Timing metrics
    total_time: float = 0.0
    llm_response_time: float = 0.0
    processing_time: float = 0.0
    memory_processing_time: float = 0.0

    # Memory metrics
    peak_memory_mb: float = 0.0
    current_memory_mb: float = 0.0
    memory_growth_mb: float = 0.0

    # Model metrics
    model_used: str = ""
    model_loading_time: float = 0.0
    tokens_generated: int = 0
    tokens_input: int = 0

    # Process metrics
    iterations_completed: int = 0
    agents_used: int = 0
    errors_encountered: int = 0

    # Timestamps
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary."""
        return {
            'timing': {
                'total_time': self.total_time,
                'llm_response_time': self.llm_response_time,
                'processing_time': self.processing_time,
                'memory_processing_time': self.memory_processing_time,
            },
            'memory': {
                'peak_memory_mb': self.peak_memory_mb,
                'current_memory_mb': self.current_memory_mb,
                'memory_growth_mb': self.memory_growth_mb,
            },
            'model': {
                'model_used': self.model_used,
                'model_loading_time': self.model_loading_time,
                'tokens_generated': self.tokens_generated,
                'tokens_input': self.tokens_input,
            },
            'process': {
                'iterations_completed': self.iterations_completed,
                'agents_used': self.agents_used,
                'errors_encountered': self.errors_encountered,
            },
            'timestamps': {
                'start_time': self.start_time.isoformat(),
                'end_time': self.end_time.isoformat() if self.end_time else None,
            }
        }

class MetricsCollector:
    """Collects and manages performance metrics."""

    def __init__(self, max_history: int = 1000):
        """
        Initialize metrics collector.

        Args:
            max_history: Maximum number of historical metrics to keep
        """
        self.max_history = max_history
        self.current_metrics: Optional[PerformanceMetrics] = None
        self.historical_metrics: deque = deque(maxlen=max_history)
        self.session_metrics: Dict[str, List[PerformanceMetrics]] = defaultdict(list)
        self.lock = threading.Lock()

        # System monitoring
        self.system_metrics = {
            'cpu_percent': deque(maxlen=100),
            'memory_percent': deque(maxlen=100),
            'disk_io': deque(maxlen=100),
        }

        # Start system monitoring
        self._start_system_monitoring()

    def start_session(self, session_id: str) -> PerformanceMetrics:
        """Start monitoring a new session."""
        with self.lock:
            self.current_metrics = PerformanceMetrics()
            self.current_metrics.start_time = datetime.now()
            logger.info(f"Started metrics collection for session {session_id}")
            return self.current_metrics

    def end_session(self, session_id: str) -> Optional[PerformanceMetrics]:
        """End monitoring for a session."""
        with self.lock:
            if self.current_metrics:
                self.current_metrics.end_time = datetime.now()
                self.current_metrics.total_time = (
                    self.current_metrics.end_time - self.current_metrics.start_time
                ).total_seconds()

                # Store in history
                self.historical_metrics.append(self.current_metrics)
                self.session_metrics[session_id].append(self.current_metrics)

                logger.info(f"Ended metrics collection for session {session_id}")
                logger.info(f"Total time: {self.current_metrics.total_time:.2f}s")

                completed_metrics = self.current_metrics
                self.current_metrics = None
                return completed_metrics
            return None

    def record_llm_call(self, model: str, response_time: float,
                       tokens_input: int = 0, tokens_generated: int = 0):
        """Record an LLM call."""
        if self.current_metrics:
            self.current_metrics.model_used = model
            self.current_metrics.llm_response_time += response_time
            self.current_metrics.tokens_input += tokens_input
            self.current_metrics.tokens_generated += tokens_generated

    def record_iteration(self):
        """Record a completed iteration."""
        if self.current_metrics:
            self.current_metrics.iterations_completed += 1

    def record_agent_usage(self, agent_count: int = 1):
        """Record agent usage."""
        if self.current_metrics:
            self.current_metrics.agents_used += agent_count

    def record_error(self):
        """Record an error."""
        if self.current_metrics:
            self.current_metrics.errors_encountered += 1

    def record_memory_usage(self):
        """Record current memory usage."""
        if self.current_metrics:
            process = psutil.Process()
            memory_info = process.memory_info()
            current_mb = memory_info.rss / 1024 / 1024

            self.current_metrics.current_memory_mb = current_mb
            if current_mb > self.current_metrics.peak_memory_mb:
                self.current_metrics.peak_memory_mb = current_mb

    def _start_system_monitoring(self):
        """Start background system monitoring."""
        def monitor():
            while True:
                try:
                    # CPU and memory
                    cpu_percent = psutil.cpu_percent(interval=1)
                    memory_percent = psutil.virtual_memory().percent

                    # Disk I/O
                    disk_io = psutil.disk_io_counters()
                    disk_io_mb = (disk_io.read_bytes + disk_io.write_bytes) / 1024 / 1024 if disk_io else 0

                    with self.lock:
                        self.system_metrics['cpu_percent'].append(cpu_percent)
                        self.system_metrics['memory_percent'].append(memory_percent)
                        self.system_metrics['disk_io'].append(disk_io_mb)

                    time.sleep(5)  # Monitor every 5 seconds
                except Exception as e:
                    logger.error(f"System monitoring error: {e}")
                    time.sleep(10)

        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()

    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get summary metrics for a session."""
        if session_id not in self.session_metrics:
            return {}

        metrics_list = self.session_metrics[session_id]
        if not metrics_list:
            return {}

        # Calculate averages and totals
        total_time = sum(m.total_time for m in metrics_list)
        avg_llm_time = sum(m.llm_response_time for m in metrics_list) / len(metrics_list)
        total_tokens = sum(m.tokens_generated for m in metrics_list)
        total_iterations = sum(m.iterations_completed for m in metrics_list)

        return {
            'session_id': session_id,
            'total_sessions': len(metrics_list),
            'total_time': total_time,
            'average_llm_response_time': avg_llm_time,
            'total_tokens_generated': total_tokens,
            'total_iterations': total_iterations,
            'models_used': list(set(m.model_used for m in metrics_list)),
            'last_session': metrics_list[-1].to_dict() if metrics_list else None
        }

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics."""
        with self.lock:
            return {
                'cpu_percent': list(self.system_metrics['cpu_percent'])[-10:],  # Last 10 readings
                'memory_percent': list(self.system_metrics['memory_percent'])[-10:],
                'disk_io_mb': list(self.system_metrics['disk_io'])[-10:],
                'timestamp': datetime.now().isoformat()
            }

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get overall performance summary."""
        if not self.historical_metrics:
            return {'message': 'No metrics available yet'}

        recent_metrics = list(self.historical_metrics)[-100:]  # Last 100 sessions

        avg_total_time = sum(m.total_time for m in recent_metrics) / len(recent_metrics)
        avg_llm_time = sum(m.llm_response_time for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m.peak_memory_mb for m in recent_metrics) / len(recent_metrics)

        model_usage = defaultdict(int)
        for m in recent_metrics:
            model_usage[m.model_used] += 1

        return {
            'total_sessions': len(self.historical_metrics),
            'recent_sessions': len(recent_metrics),
            'average_total_time': avg_total_time,
            'average_llm_response_time': avg_llm_time,
            'average_peak_memory_mb': avg_memory,
            'model_usage': dict(model_usage),
            'system_metrics': self.get_system_metrics()
        }

# Global metrics collector instance
_metrics_collector = MetricsCollector()

def get_metrics_collector() -> MetricsCollector:
    """Get the global metrics collector instance."""
    return _metrics_collector

def monitor_performance(func: Callable) -> Callable:
    """Decorator to monitor function performance."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024

        try:
            result = func(*args, **kwargs)
            return result
        finally:
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024

            execution_time = end_time - start_time
            memory_used = end_memory - start_memory

            logger.info(f"Function {func.__name__} executed in {execution_time:.2f}s, "
                       f"memory change: {memory_used:+.2f}MB")

    return wrapper

def log_metrics(metrics: PerformanceMetrics, session_id: str = None):
    """Log performance metrics."""
    logger.info(f"Performance Metrics for session {session_id or 'unknown'}:")
    logger.info(f"  Total Time: {metrics.total_time:.2f}s")
    logger.info(f"  LLM Response Time: {metrics.llm_response_time:.2f}s")
    logger.info(f"  Peak Memory: {metrics.peak_memory_mb:.2f}MB")
    logger.info(f"  Model Used: {metrics.model_used}")
    logger.info(f"  Tokens Generated: {metrics.tokens_generated}")
    logger.info(f"  Iterations: {metrics.iterations_completed}")

# Export main classes and functions
__all__ = [
    'PerformanceMetrics',
    'MetricsCollector',
    'get_metrics_collector',
    'monitor_performance',
    'log_metrics'
]
