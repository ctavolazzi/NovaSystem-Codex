"""Local rate limit tracking and enforcement with JSON persistence."""

import atexit
import json
import os
import time
from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict, List, Tuple

from .pricing import CostEstimator


# Default state file location (relative to working directory)
DEFAULT_STATE_FILE = ".nova_traffic_state.json"


@dataclass
class ModelLimits:
    """Per-model rate and token ceilings for a sliding window."""

    rpm: int  # Requests per minute
    tpm: int  # Tokens per minute


class RateLimitExceeded(Exception):
    """Raised when a request would exceed configured rate limits."""

    def __init__(self, message: str, retry_after: float):
        super().__init__(message)
        self.retry_after = retry_after


class TrafficController:
    """Track outgoing requests to avoid server-side 429 responses.

    Persists state to JSON so rate limits survive restarts.
    """

    DEFAULT_LIMITS: Dict[str, ModelLimits] = {
        # Tier 1 defaults (sliding 60-second window)
        "gemini-2.5-flash": ModelLimits(rpm=15, tpm=1_000_000),
        "gemini-2.5-flash-lite": ModelLimits(rpm=20, tpm=750_000),
        "gemini-3-pro": ModelLimits(rpm=2, tpm=32_000),
        "gemini-2.5-pro": ModelLimits(rpm=5, tpm=512_000),
    }

    def __init__(
        self,
        limits: Dict[str, ModelLimits] | None = None,
        window_seconds: int = 60,
        state_file: str | None = None,
        persist: bool = True,
    ):
        self.window_seconds = window_seconds
        self.limits = limits or self.DEFAULT_LIMITS
        self._requests: Dict[str, Deque[Tuple[float, int]]] = {}
        self._state_file = state_file or DEFAULT_STATE_FILE
        self._persist = persist

        # Load previous state on startup
        if persist:
            self._load_state()
            atexit.register(self._save_state)

    def check_allowance(
        self,
        model: str,
        tokens: int,
        estimated_output_tokens: int = 0,
        commit: bool = True,
    ) -> None:
        """Verify whether a request is allowed and optionally reserve capacity.

        Args:
            model: Target model identifier.
            tokens: Estimated input tokens.
            estimated_output_tokens: Anticipated output tokens for TPM tracking.
            commit: If True, record the request; otherwise, perform a dry run.

        Raises:
            RateLimitExceeded: When RPM or TPM ceilings would be exceeded.
        """

        normalized_model = model.lower()
        limits = self.limits.get(normalized_model)
        if limits is None:
            # Unknown model defaults to the loosest Gemini flash tier
            limits = ModelLimits(rpm=15, tpm=1_000_000)
            self.limits[normalized_model] = limits

        now = time.time()
        window = self._requests.setdefault(normalized_model, deque())
        self._prune(window, now)

        total_tokens = tokens + estimated_output_tokens

        if self._exceeds_rpm(window, limits):
            retry_after = self._retry_after_for_rpm(window, now)
            raise RateLimitExceeded("Requests per minute limit exceeded", retry_after)

        if self._exceeds_tpm(window, limits, total_tokens):
            retry_after = self._retry_after_for_tpm(window, limits, total_tokens, now)
            raise RateLimitExceeded("Tokens per minute limit exceeded", retry_after)

        if commit:
            window.append((now, total_tokens))

    def _prune(self, window: Deque[Tuple[float, int]], now: float) -> None:
        """Remove entries outside the sliding window."""

        cutoff = now - self.window_seconds
        while window and window[0][0] < cutoff:
            window.popleft()

    def _exceeds_rpm(self, window: Deque[Tuple[float, int]], limits: ModelLimits) -> bool:
        return len(window) + 1 > limits.rpm

    def _retry_after_for_rpm(self, window: Deque[Tuple[float, int]], now: float) -> float:
        oldest_time = window[0][0]
        return max(0, self.window_seconds - (now - oldest_time))

    def _exceeds_tpm(
        self, window: Deque[Tuple[float, int]], limits: ModelLimits, incoming_tokens: int
    ) -> bool:
        current_tokens = sum(tokens for _, tokens in window)
        return current_tokens + incoming_tokens > limits.tpm

    def _retry_after_for_tpm(
        self,
        window: Deque[Tuple[float, int]],
        limits: ModelLimits,
        incoming_tokens: int,
        now: float,
    ) -> float:
        """Determine wait time until enough tokens expire to allow the request."""

        tokens_accumulated = incoming_tokens
        for timestamp, tokens in window:
            tokens_accumulated += tokens
            if tokens_accumulated > limits.tpm:
                return max(0, self.window_seconds - (now - timestamp))
        return self.window_seconds

    def _save_state(self) -> None:
        """Persist current window state to JSON."""
        if not self._persist:
            return

        # Convert deques to lists for JSON serialization
        data = {
            "window_seconds": self.window_seconds,
            "requests": {
                model: list(entries)
                for model, entries in self._requests.items()
            }
        }

        try:
            with open(self._state_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            # Fail silently - persistence is nice-to-have, not critical
            print(f"⚠️ Failed to save traffic state: {e}")

    def _load_state(self) -> None:
        """Load window state from JSON if it exists."""
        if not os.path.exists(self._state_file):
            return

        try:
            with open(self._state_file, "r") as f:
                data = json.load(f)

            now = time.time()
            cutoff = now - self.window_seconds
            loaded_count = 0

            for model, entries in data.get("requests", {}).items():
                # Filter out expired entries on load
                valid_entries = [
                    (ts, tokens) for ts, tokens in entries
                    if ts > cutoff
                ]
                if valid_entries:
                    self._requests[model] = deque(valid_entries)
                    loaded_count += len(valid_entries)

            if loaded_count > 0:
                print(f"✅ Traffic state loaded ({loaded_count} active requests)")

        except Exception as e:
            # Start fresh on error
            print(f"⚠️ Failed to load traffic state (starting fresh): {e}")
            self._requests = {}

    def clear(self) -> None:
        """Clear all tracked requests and remove state file."""
        self._requests.clear()
        if self._persist and os.path.exists(self._state_file):
            os.remove(self._state_file)


def estimate_tokens(text: str) -> int:
    """Helper to reuse the CostEstimator token heuristic."""

    estimator = CostEstimator()
    return estimator._estimate_tokens(text)


# Shared controller for application-wide coordination
traffic_controller = TrafficController()
