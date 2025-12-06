"""Usage Tracking Module - Reconciliation between estimates and actuals.

Building blocks for tracking actual API usage vs estimates.
Simple, composable, no over-engineering.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
import json


@dataclass
class UsageRecord:
    """A single API usage record."""
    timestamp: datetime
    model: str
    estimated_tokens: int
    actual_tokens: Optional[int] = None
    estimated_cost: float = 0.0
    actual_cost: Optional[float] = None
    
    @property
    def drift(self) -> Optional[int]:
        """How far off was the estimate? (actual - estimated)"""
        if self.actual_tokens is None:
            return None
        return self.actual_tokens - self.estimated_tokens
    
    @property
    def drift_pct(self) -> Optional[float]:
        """Drift as percentage of estimate."""
        if self.drift is None or self.estimated_tokens == 0:
            return None
        return (self.drift / self.estimated_tokens) * 100
    
    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "model": self.model,
            "estimated_tokens": self.estimated_tokens,
            "actual_tokens": self.actual_tokens,
            "estimated_cost": self.estimated_cost,
            "actual_cost": self.actual_cost,
            "drift": self.drift,
            "drift_pct": self.drift_pct,
        }


class UsageTracker:
    """
    Tracks API usage with reconciliation support.
    
    Simple in-memory tracker. Can be extended for persistence later.
    """
    
    def __init__(self, max_records: int = 1000):
        self._records: List[UsageRecord] = []
        self._max_records = max_records
    
    def record(
        self,
        model: str,
        estimated_tokens: int,
        actual_tokens: Optional[int] = None,
        estimated_cost: float = 0.0,
        actual_cost: Optional[float] = None,
    ) -> UsageRecord:
        """Record a usage event."""
        rec = UsageRecord(
            timestamp=datetime.now(),
            model=model,
            estimated_tokens=estimated_tokens,
            actual_tokens=actual_tokens,
            estimated_cost=estimated_cost,
            actual_cost=actual_cost,
        )
        self._records.append(rec)
        
        # Trim if over limit
        if len(self._records) > self._max_records:
            self._records = self._records[-self._max_records:]
        
        return rec
    
    def update_actual(self, record: UsageRecord, actual_tokens: int, actual_cost: Optional[float] = None):
        """Update a record with actual usage (reconciliation)."""
        record.actual_tokens = actual_tokens
        if actual_cost is not None:
            record.actual_cost = actual_cost
    
    @property
    def total_estimated(self) -> int:
        """Total estimated tokens across all records."""
        return sum(r.estimated_tokens for r in self._records)
    
    @property
    def total_actual(self) -> int:
        """Total actual tokens (only records with actuals)."""
        return sum(r.actual_tokens for r in self._records if r.actual_tokens)
    
    @property
    def average_drift_pct(self) -> Optional[float]:
        """Average drift percentage across all reconciled records."""
        drifts = [r.drift_pct for r in self._records if r.drift_pct is not None]
        if not drifts:
            return None
        return sum(drifts) / len(drifts)
    
    def summary(self) -> dict:
        """Get usage summary."""
        return {
            "total_records": len(self._records),
            "total_estimated_tokens": self.total_estimated,
            "total_actual_tokens": self.total_actual,
            "average_drift_pct": self.average_drift_pct,
            "records_with_actuals": sum(1 for r in self._records if r.actual_tokens),
        }
    
    def recent(self, n: int = 10) -> List[UsageRecord]:
        """Get n most recent records."""
        return self._records[-n:]
    
    def clear(self):
        """Clear all records."""
        self._records.clear()


def extract_usage(response: Any, provider: str = "auto") -> Optional[Dict[str, int]]:
    """
    Extract usage data from API response.
    
    Returns dict with 'input_tokens', 'output_tokens', 'total_tokens' if available.
    
    Supports:
    - Claude (Anthropic): response.usage
    - OpenAI: response.usage
    - Gemini: response.usage_metadata
    """
    try:
        # Claude / Anthropic
        if hasattr(response, 'usage') and hasattr(response.usage, 'input_tokens'):
            return {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
            }
        
        # OpenAI
        if hasattr(response, 'usage') and hasattr(response.usage, 'prompt_tokens'):
            return {
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }
        
        # Gemini (via google.generativeai)
        if hasattr(response, 'usage_metadata'):
            meta = response.usage_metadata
            return {
                "input_tokens": getattr(meta, 'prompt_token_count', 0),
                "output_tokens": getattr(meta, 'candidates_token_count', 0),
                "total_tokens": getattr(meta, 'total_token_count', 0),
            }
        
        # Dict-like response (some APIs return dicts)
        if isinstance(response, dict):
            if 'usage' in response:
                usage = response['usage']
                return {
                    "input_tokens": usage.get('prompt_tokens') or usage.get('input_tokens', 0),
                    "output_tokens": usage.get('completion_tokens') or usage.get('output_tokens', 0),
                    "total_tokens": usage.get('total_tokens', 0),
                }
        
        return None
        
    except Exception:
        return None


# Global tracker instance
_usage_tracker: Optional[UsageTracker] = None


def get_usage_tracker() -> UsageTracker:
    """Get the global usage tracker."""
    global _usage_tracker
    if _usage_tracker is None:
        _usage_tracker = UsageTracker()
    return _usage_tracker
