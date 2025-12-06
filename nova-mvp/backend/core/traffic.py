"""Rate limit tracking for outbound LLM calls."""

import math
import time
import threading
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Deque, Dict, Tuple

from .pricing import normalize_model_name


@dataclass
class RateLimit:
    rpm: int  # Requests per minute
    tpm: int  # Tokens per minute


class RateLimitExceeded(Exception):
    """Raised when a model-specific rate limit is hit."""

    def __init__(self, message: str, retry_after: float):
        super().__init__(message)
        self.retry_after = max(0, retry_after)


DEFAULT_RATE_LIMITS: Dict[str, RateLimit] = {
    # Tier 1 baseline values (configurable)
    "gemini-2.5-flash": RateLimit(rpm=15, tpm=1_000_000),
    "gemini-2.5-flash-lite": RateLimit(rpm=15, tpm=1_000_000),
    "gemini-3-pro-preview": RateLimit(rpm=2, tpm=32_000),
    "gemini-2.5-pro": RateLimit(rpm=10, tpm=1_000_000),
    "default": RateLimit(rpm=60, tpm=1_000_000),
}


class TrafficController:
    """
    Sliding-window rate limiter with per-model tracking.

    Uses a 60-second leaky bucket (deque-based) to enforce RPM + TPM.
    """

    def __init__(
        self,
        limits: Dict[str, RateLimit] | None = None,
        window_seconds: int = 60,
    ):
        self.limits = limits or DEFAULT_RATE_LIMITS
        self.window = window_seconds
        self._request_log: Dict[str, Deque[float]] = defaultdict(deque)
        self._token_log: Dict[str, Deque[Tuple[float, int]]] = defaultdict(deque)
        self._lock = threading.Lock()

    def _get_limit(self, model_key: str) -> RateLimit:
        return self.limits.get(model_key) or self.limits.get("default") or RateLimit(rpm=60, tpm=1_000_000)

    def _prune(self, model_key: str, now: float):
        """Drop entries outside the sliding window."""
        reqs = self._request_log[model_key]
        tokens = self._token_log[model_key]

        while reqs and (now - reqs[0]) > self.window:
            reqs.popleft()

        while tokens and (now - tokens[0][0]) > self.window:
            tokens.popleft()

    def _current_usage(self, model_key: str) -> tuple[int, int]:
        """Return (rpm, tpm) usage inside the window."""
        reqs = self._request_log[model_key]
        tokens = self._token_log[model_key]
        tpm = sum(entry[1] for entry in tokens)
        return len(reqs), tpm

    def _calculate_retry_after(self, model_key: str, limit: RateLimit, tokens: int, now: float) -> float:
        """
        Compute the earliest time (seconds) until a new request can fit.
        Considers both RPM and TPM over a 60-second sliding window.
        """
        waits = []
        reqs = self._request_log[model_key]
        token_entries = self._token_log[model_key]

        if len(reqs) >= limit.rpm and reqs:
            waits.append(self.window - (now - reqs[0]))

        current_tpm = sum(t for _, t in token_entries)
        over_tokens = (current_tpm + tokens) - limit.tpm

        if over_tokens > 0 and token_entries:
            # Find the earliest point where enough tokens leak out
            running = current_tpm
            for ts, spent in token_entries:
                running -= spent
                if running + tokens <= limit.tpm:
                    waits.append(self.window - (now - ts))
                    break
            else:
                waits.append(self.window)

        # Never return zero; 1s is a reasonable minimum backoff
        positive_waits = [w for w in waits if w > 0]
        return max(1, math.ceil(min(positive_waits))) if positive_waits else 1

    def check_allowance(self, model: str, tokens: int, consume: bool = True):
        """
        Verify the request can proceed within RPM/TPM budgets.

        Args:
            model: Model identifier (normalized to Gemini keys)
            tokens: Input + estimated output tokens
            consume: When True, record usage; when False, only validate.
        """
        now = time.time()
        model_key = normalize_model_name(model)
        limit = self._get_limit(model_key)

        with self._lock:
            self._prune(model_key, now)
            rpm_used, tpm_used = self._current_usage(model_key)

            if rpm_used >= limit.rpm or (tpm_used + tokens) > limit.tpm:
                retry_after = self._calculate_retry_after(model_key, limit, tokens, now)
                raise RateLimitExceeded(
                    f"Rate limit exceeded for model '{model_key}' (rpm={limit.rpm}, tpm={limit.tpm})",
                    retry_after,
                )

            if consume:
                self._request_log[model_key].append(now)
                self._token_log[model_key].append((now, tokens))


# Shared controller for the process
traffic_controller = TrafficController()


def get_traffic_controller() -> TrafficController:
    """Return a shared TrafficController instance."""
    return traffic_controller

