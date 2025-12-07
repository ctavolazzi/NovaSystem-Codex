"""
Rate Limiter for Gemini API.

Handles rate limits gracefully:
- RPM (requests per minute)
- TPM (tokens per minute)
- RPD (requests per day)

Features:
- Automatic retry with exponential backoff
- Usage tracking and logging
- Batch request queuing
- Quota tier awareness

Usage Tiers:
- Free: Basic limits for eligible countries
- Tier 1: Paid billing account linked
- Tier 2: >$250 total spend + 30 days
- Tier 3: >$1000 total spend + 30 days

Requires: pip install google-genai
"""

import os
import sys
import asyncio
import time
import random
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Callable, TypeVar, Awaitable
from dataclasses import dataclass, field
from collections import deque
from functools import wraps
import logging
from enum import Enum

logger = logging.getLogger(__name__)

T = TypeVar('T')


def rate_log(emoji: str, category: str, message: str, details: dict = None):
    """Log a rate limiter event."""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"{timestamp} | {emoji} [RATE/{category}] {message}")
    if details:
        for key, value in details.items():
            val_str = str(value)[:60] + "..." if len(str(value)) > 60 else str(value)
            print(f"           └─ {key}: {val_str}")


class QuotaTier(Enum):
    """Gemini API usage tiers."""
    FREE = "free"
    TIER_1 = "tier_1"  # Paid billing linked
    TIER_2 = "tier_2"  # >$250 spend + 30 days
    TIER_3 = "tier_3"  # >$1000 spend + 30 days


@dataclass
class RateLimitConfig:
    """Configuration for rate limits."""
    rpm: int = 15  # Requests per minute (conservative default)
    tpm: int = 1_000_000  # Tokens per minute
    rpd: int = 1500  # Requests per day

    # Retry settings
    max_retries: int = 5
    base_delay: float = 1.0  # seconds
    max_delay: float = 60.0  # seconds
    jitter: float = 0.1  # Random jitter factor

    # Batch settings
    batch_concurrent_limit: int = 100
    batch_enqueued_tokens: int = 3_000_000  # Tier 1 default for Flash


# Pre-configured limits by tier and model
TIER_LIMITS = {
    QuotaTier.FREE: RateLimitConfig(rpm=10, tpm=100_000, rpd=500),
    QuotaTier.TIER_1: RateLimitConfig(rpm=60, tpm=4_000_000, rpd=10_000),
    QuotaTier.TIER_2: RateLimitConfig(rpm=1000, tpm=10_000_000, rpd=50_000),
    QuotaTier.TIER_3: RateLimitConfig(rpm=2000, tpm=20_000_000, rpd=100_000),
}


@dataclass
class UsageStats:
    """Tracks API usage statistics."""
    requests_this_minute: int = 0
    tokens_this_minute: int = 0
    requests_today: int = 0
    tokens_today: int = 0
    total_requests: int = 0
    total_tokens: int = 0
    rate_limit_hits: int = 0
    last_request_time: Optional[datetime] = None
    minute_start: Optional[datetime] = None
    day_start: Optional[datetime] = None

    # Request timestamps for accurate RPM tracking
    request_timestamps: deque = field(default_factory=lambda: deque(maxlen=1000))

    def record_request(self, tokens: int = 0):
        """Record a new request."""
        now = datetime.now()

        # Reset minute counter if needed
        if self.minute_start is None or (now - self.minute_start).seconds >= 60:
            self.minute_start = now
            self.requests_this_minute = 0
            self.tokens_this_minute = 0

        # Reset day counter if needed (midnight Pacific)
        if self.day_start is None or (now - self.day_start).days >= 1:
            self.day_start = now
            self.requests_today = 0
            self.tokens_today = 0

        # Update counts
        self.requests_this_minute += 1
        self.tokens_this_minute += tokens
        self.requests_today += 1
        self.tokens_today += tokens
        self.total_requests += 1
        self.total_tokens += tokens
        self.last_request_time = now
        self.request_timestamps.append(now)

    def get_rpm(self) -> int:
        """Get actual requests per minute (rolling window)."""
        now = datetime.now()
        cutoff = now - timedelta(minutes=1)
        return sum(1 for ts in self.request_timestamps if ts > cutoff)


class RateLimitError(Exception):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str, retry_after: float = None):
        super().__init__(message)
        self.retry_after = retry_after


class RateLimiter:
    """
    Manages rate limits for Gemini API calls.

    Features:
    - Pre-request checking against limits
    - Automatic retry with exponential backoff
    - Usage tracking and statistics
    - Configurable per tier

    Usage:
        limiter = RateLimiter(tier=QuotaTier.TIER_1)

        # Wrap API calls
        @limiter.limit
        async def call_api(prompt):
            return await gemini.generate(prompt)

        # Or use context manager
        async with limiter.acquire(estimated_tokens=1000):
            result = await gemini.generate(prompt)
    """

    def __init__(
        self,
        config: Optional[RateLimitConfig] = None,
        tier: QuotaTier = QuotaTier.TIER_1
    ):
        """
        Initialize rate limiter.

        Args:
            config: Custom rate limit configuration
            tier: Usage tier (uses predefined limits if config not provided)
        """
        self.config = config or TIER_LIMITS.get(tier, TIER_LIMITS[QuotaTier.TIER_1])
        self.tier = tier
        self.stats = UsageStats()
        self._lock = asyncio.Lock()
        self._semaphore = asyncio.Semaphore(self.config.rpm)

        rate_log("✅", "INIT", f"RateLimiter initialized", {
            "tier": tier.value,
            "rpm": self.config.rpm,
            "tpm": f"{self.config.tpm:,}",
            "rpd": f"{self.config.rpd:,}"
        })

    def can_proceed(self, estimated_tokens: int = 0) -> tuple[bool, Optional[str]]:
        """
        Check if a request can proceed without hitting limits.

        Returns:
            Tuple of (can_proceed, reason_if_not)
        """
        # Check RPM
        current_rpm = self.stats.get_rpm()
        if current_rpm >= self.config.rpm:
            return False, f"RPM limit reached ({current_rpm}/{self.config.rpm})"

        # Check TPM
        if self.stats.tokens_this_minute + estimated_tokens > self.config.tpm:
            return False, f"TPM limit would be exceeded"

        # Check RPD
        if self.stats.requests_today >= self.config.rpd:
            return False, f"RPD limit reached ({self.stats.requests_today}/{self.config.rpd})"

        return True, None

    def get_wait_time(self) -> float:
        """Calculate time to wait before next request is allowed."""
        if not self.stats.request_timestamps:
            return 0.0

        now = datetime.now()
        cutoff = now - timedelta(minutes=1)

        # Count requests in last minute
        recent = [ts for ts in self.stats.request_timestamps if ts > cutoff]

        if len(recent) < self.config.rpm:
            return 0.0

        # Wait until oldest request falls outside window
        oldest = min(recent)
        wait = (oldest + timedelta(minutes=1) - now).total_seconds()
        return max(0.0, wait)

    async def wait_if_needed(self, estimated_tokens: int = 0):
        """Wait if necessary to respect rate limits."""
        can_go, reason = self.can_proceed(estimated_tokens)

        if not can_go:
            wait_time = self.get_wait_time()
            if wait_time > 0:
                rate_log("⏳", "WAIT", f"Rate limit: {reason}", {
                    "wait_seconds": f"{wait_time:.2f}"
                })
                await asyncio.sleep(wait_time)

    async def acquire(self, estimated_tokens: int = 0):
        """Async context manager for rate-limited operations."""
        return RateLimitContext(self, estimated_tokens)

    def limit(self, func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        """
        Decorator to apply rate limiting to an async function.

        Usage:
            @limiter.limit
            async def call_gemini(prompt):
                return await client.generate(prompt)
        """
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            async with RateLimitContext(self, estimated_tokens=0):
                return await func(*args, **kwargs)
        return wrapper

    async def execute_with_retry(
        self,
        func: Callable[..., Awaitable[T]],
        *args,
        estimated_tokens: int = 0,
        **kwargs
    ) -> T:
        """
        Execute a function with automatic retry on rate limit errors.

        Uses exponential backoff with jitter.

        Args:
            func: Async function to execute
            *args: Function arguments
            estimated_tokens: Estimated token count for the request
            **kwargs: Function keyword arguments

        Returns:
            Function result

        Raises:
            RateLimitError: If max retries exceeded
        """
        last_error = None

        for attempt in range(self.config.max_retries + 1):
            try:
                # Wait if needed
                await self.wait_if_needed(estimated_tokens)

                # Execute
                async with self._lock:
                    result = await func(*args, **kwargs)
                    self.stats.record_request(estimated_tokens)
                    return result

            except Exception as e:
                error_str = str(e).lower()

                # Check if it's a rate limit error
                if "429" in str(e) or "rate" in error_str or "quota" in error_str:
                    self.stats.rate_limit_hits += 1
                    last_error = e

                    if attempt < self.config.max_retries:
                        # Calculate backoff
                        delay = min(
                            self.config.base_delay * (2 ** attempt),
                            self.config.max_delay
                        )
                        # Add jitter
                        delay *= (1 + random.uniform(-self.config.jitter, self.config.jitter))

                        rate_log("🔄", "RETRY", f"Rate limited, retrying", {
                            "attempt": f"{attempt + 1}/{self.config.max_retries}",
                            "delay": f"{delay:.2f}s",
                            "error": str(e)[:50]
                        })

                        await asyncio.sleep(delay)
                        continue
                    else:
                        raise RateLimitError(
                            f"Max retries exceeded: {e}",
                            retry_after=delay
                        )
                else:
                    # Not a rate limit error, re-raise
                    raise

        raise RateLimitError(f"Max retries exceeded: {last_error}")

    def get_stats(self) -> Dict[str, Any]:
        """Get current usage statistics."""
        return {
            "tier": self.tier.value,
            "limits": {
                "rpm": self.config.rpm,
                "tpm": self.config.tpm,
                "rpd": self.config.rpd
            },
            "usage": {
                "requests_this_minute": self.stats.requests_this_minute,
                "tokens_this_minute": self.stats.tokens_this_minute,
                "requests_today": self.stats.requests_today,
                "tokens_today": self.stats.tokens_today,
                "total_requests": self.stats.total_requests,
                "total_tokens": self.stats.total_tokens,
                "rate_limit_hits": self.stats.rate_limit_hits
            },
            "current_rpm": self.stats.get_rpm()
        }

    def log_stats(self):
        """Log current usage statistics."""
        stats = self.get_stats()
        rate_log("📊", "STATS", "Current usage", {
            "rpm": f"{stats['current_rpm']}/{stats['limits']['rpm']}",
            "requests_today": f"{stats['usage']['requests_today']}/{stats['limits']['rpd']}",
            "rate_limit_hits": stats['usage']['rate_limit_hits']
        })


class RateLimitContext:
    """Async context manager for rate-limited operations."""

    def __init__(self, limiter: RateLimiter, estimated_tokens: int = 0):
        self.limiter = limiter
        self.estimated_tokens = estimated_tokens

    async def __aenter__(self):
        await self.limiter.wait_if_needed(self.estimated_tokens)
        await self.limiter._semaphore.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.limiter._semaphore.release()
        if exc_type is None:
            self.limiter.stats.record_request(self.estimated_tokens)
        return False


class BatchProcessor:
    """
    Batch processor for Gemini API with rate limiting.

    Processes multiple requests efficiently while respecting limits.

    Batch API Limits (Tier 1):
    - Concurrent batch requests: 100
    - Input file size: 2GB
    - File storage: 20GB
    - Enqueued tokens: varies by model (3M-10M for Flash)
    """

    def __init__(
        self,
        limiter: Optional[RateLimiter] = None,
        max_concurrent: int = 10,
        batch_size: int = 50
    ):
        """
        Initialize batch processor.

        Args:
            limiter: Rate limiter to use
            max_concurrent: Max concurrent requests
            batch_size: Requests per batch
        """
        self.limiter = limiter or RateLimiter()
        self.max_concurrent = max_concurrent
        self.batch_size = batch_size
        self._semaphore = asyncio.Semaphore(max_concurrent)

        rate_log("✅", "BATCH", "BatchProcessor initialized", {
            "max_concurrent": max_concurrent,
            "batch_size": batch_size
        })

    async def process_batch(
        self,
        items: List[Any],
        processor: Callable[[Any], Awaitable[Any]],
        on_progress: Optional[Callable[[int, int], None]] = None
    ) -> List[Any]:
        """
        Process a batch of items with rate limiting.

        Args:
            items: Items to process
            processor: Async function to process each item
            on_progress: Optional callback(completed, total)

        Returns:
            List of results in same order as items
        """
        total = len(items)
        completed = 0
        results = [None] * total

        rate_log("🚀", "BATCH", f"Starting batch", {
            "items": total,
            "concurrent": self.max_concurrent
        })

        async def process_one(index: int, item: Any):
            nonlocal completed
            async with self._semaphore:
                try:
                    result = await self.limiter.execute_with_retry(
                        processor,
                        item
                    )
                    results[index] = result
                except Exception as e:
                    results[index] = {"error": str(e)}

                completed += 1
                if on_progress:
                    on_progress(completed, total)

        # Process all items
        tasks = [
            process_one(i, item)
            for i, item in enumerate(items)
        ]

        await asyncio.gather(*tasks)

        rate_log("✅", "BATCH", f"Batch complete", {
            "processed": completed,
            "errors": sum(1 for r in results if isinstance(r, dict) and "error" in r)
        })

        return results


# Convenience functions

def create_limiter(tier: str = "tier_1") -> RateLimiter:
    """Create a rate limiter for the specified tier."""
    tier_map = {
        "free": QuotaTier.FREE,
        "tier_1": QuotaTier.TIER_1,
        "tier_2": QuotaTier.TIER_2,
        "tier_3": QuotaTier.TIER_3,
    }
    return RateLimiter(tier=tier_map.get(tier.lower(), QuotaTier.TIER_1))


async def with_rate_limit(
    func: Callable[..., Awaitable[T]],
    *args,
    tier: str = "tier_1",
    **kwargs
) -> T:
    """Execute a function with rate limiting."""
    limiter = create_limiter(tier)
    return await limiter.execute_with_retry(func, *args, **kwargs)
