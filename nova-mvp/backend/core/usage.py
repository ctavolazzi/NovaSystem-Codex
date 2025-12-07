"""Usage tracking with SQLite persistence - The Accountant.

Records all LLM transactions to enable:
- Actual vs estimated cost tracking (drift analysis)
- Spend summaries by model, provider, time period
- Budget alerts and usage analytics
- Circuit breaker for runaway costs
"""

import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

# Database file location (relative to working directory)
DEFAULT_DB_FILE = ".nova_usage.db"

# Default budget limits (can be overridden)
DEFAULT_DAILY_BUDGET = 10.00  # USD
DEFAULT_HOURLY_BUDGET = 2.00  # USD


class BudgetExceededError(Exception):
    """Raised when spending would exceed configured budget limits."""

    def __init__(self, message: str, current_spend: float, budget: float, period: str):
        super().__init__(message)
        self.current_spend = current_spend
        self.budget = budget
        self.period = period


@dataclass
class Transaction:
    """A single LLM API transaction."""
    timestamp: float
    model: str
    provider: str
    input_tokens: int
    output_tokens: int
    estimated_cost: float
    actual_cost: Optional[float] = None  # Filled if API returns usage
    context: str = "general"

    @property
    def cost(self) -> float:
        """Best available cost (actual if known, else estimated)."""
        return self.actual_cost if self.actual_cost is not None else self.estimated_cost

    @property
    def drift(self) -> Optional[float]:
        """Cost drift: actual - estimated. Positive = underestimated."""
        if self.actual_cost is None:
            return None
        return self.actual_cost - self.estimated_cost

    @property
    def drift_pct(self) -> Optional[float]:
        """Drift as percentage of estimated cost."""
        if self.drift is None or self.estimated_cost == 0:
            return None
        return (self.drift / self.estimated_cost) * 100


class UsageLedger:
    """SQLite-backed ledger for tracking LLM spend.

    Records every transaction with estimated and actual costs,
    enabling drift analysis and spend reporting.

    Includes circuit breaker to prevent runaway costs.
    """

    def __init__(
        self,
        db_file: str | None = None,
        daily_budget: float | None = DEFAULT_DAILY_BUDGET,
        hourly_budget: float | None = DEFAULT_HOURLY_BUDGET,
    ):
        self._db_file = db_file or DEFAULT_DB_FILE
        self._daily_budget = daily_budget
        self._hourly_budget = hourly_budget
        self._init_db()

    def _init_db(self) -> None:
        """Create tables if they don't exist."""
        with sqlite3.connect(self._db_file) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL NOT NULL,
                    model TEXT NOT NULL,
                    provider TEXT NOT NULL,
                    input_tokens INTEGER NOT NULL,
                    output_tokens INTEGER NOT NULL,
                    estimated_cost REAL NOT NULL,
                    actual_cost REAL,
                    context TEXT DEFAULT 'general'
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp
                ON transactions(timestamp)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_model
                ON transactions(model)
            """)

    def record(self, txn: Transaction) -> int:
        """Record a transaction. Returns the transaction ID."""
        with sqlite3.connect(self._db_file) as conn:
            cursor = conn.execute("""
                INSERT INTO transactions
                (timestamp, model, provider, input_tokens, output_tokens,
                 estimated_cost, actual_cost, context)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                txn.timestamp, txn.model, txn.provider,
                txn.input_tokens, txn.output_tokens,
                txn.estimated_cost, txn.actual_cost, txn.context
            ))
            return cursor.lastrowid

    def update_actual(self, txn_id: int, actual_cost: float) -> None:
        """Update a transaction with actual cost (reconciliation)."""
        with sqlite3.connect(self._db_file) as conn:
            conn.execute("""
                UPDATE transactions SET actual_cost = ? WHERE id = ?
            """, (actual_cost, txn_id))

    def total_spend(self, since: Optional[float] = None) -> float:
        """Total spend (using best available cost per transaction)."""
        query = """
            SELECT SUM(COALESCE(actual_cost, estimated_cost))
            FROM transactions
        """
        params = []
        if since:
            query += " WHERE timestamp > ?"
            params.append(since)

        with sqlite3.connect(self._db_file) as conn:
            result = conn.execute(query, params).fetchone()[0]
            return result or 0.0

    def total_estimated(self, since: Optional[float] = None) -> float:
        """Total estimated spend."""
        query = "SELECT SUM(estimated_cost) FROM transactions"
        params = []
        if since:
            query += " WHERE timestamp > ?"
            params.append(since)

        with sqlite3.connect(self._db_file) as conn:
            result = conn.execute(query, params).fetchone()[0]
            return result or 0.0

    def total_actual(self, since: Optional[float] = None) -> float:
        """Total actual spend (only transactions with actual_cost)."""
        query = "SELECT SUM(actual_cost) FROM transactions WHERE actual_cost IS NOT NULL"
        params = []
        if since:
            query += " AND timestamp > ?"
            params.append(since)

        with sqlite3.connect(self._db_file) as conn:
            result = conn.execute(query, params).fetchone()[0]
            return result or 0.0

    def average_drift_pct(self) -> Optional[float]:
        """Average drift percentage across reconciled transactions."""
        with sqlite3.connect(self._db_file) as conn:
            result = conn.execute("""
                SELECT AVG((actual_cost - estimated_cost) / estimated_cost * 100)
                FROM transactions
                WHERE actual_cost IS NOT NULL AND estimated_cost > 0
            """).fetchone()[0]
            return result

    def spend_by_model(self, since: Optional[float] = None) -> dict:
        """Spend breakdown by model."""
        query = """
            SELECT model, SUM(COALESCE(actual_cost, estimated_cost))
            FROM transactions
        """
        params = []
        if since:
            query += " WHERE timestamp > ?"
            params.append(since)
        query += " GROUP BY model"

        with sqlite3.connect(self._db_file) as conn:
            rows = conn.execute(query, params).fetchall()
            return {row[0]: row[1] or 0.0 for row in rows}

    def spend_by_provider(self, since: Optional[float] = None) -> dict:
        """Spend breakdown by provider."""
        query = """
            SELECT provider, SUM(COALESCE(actual_cost, estimated_cost))
            FROM transactions
        """
        params = []
        if since:
            query += " WHERE timestamp > ?"
            params.append(since)
        query += " GROUP BY provider"

        with sqlite3.connect(self._db_file) as conn:
            rows = conn.execute(query, params).fetchall()
            return {row[0]: row[1] or 0.0 for row in rows}

    def recent(self, limit: int = 10) -> List[Transaction]:
        """Get recent transactions."""
        with sqlite3.connect(self._db_file) as conn:
            rows = conn.execute("""
                SELECT timestamp, model, provider, input_tokens, output_tokens,
                       estimated_cost, actual_cost, context
                FROM transactions
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,)).fetchall()

        return [
            Transaction(
                timestamp=row[0], model=row[1], provider=row[2],
                input_tokens=row[3], output_tokens=row[4],
                estimated_cost=row[5], actual_cost=row[6], context=row[7]
            )
            for row in rows
        ]

    def count(self) -> int:
        """Total transaction count."""
        with sqlite3.connect(self._db_file) as conn:
            return conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]

    def summary(self) -> dict:
        """Full usage summary."""
        return {
            "total_transactions": self.count(),
            "total_spend": round(self.total_spend(), 6),
            "total_estimated": round(self.total_estimated(), 6),
            "total_actual": round(self.total_actual(), 6),
            "average_drift_pct": self.average_drift_pct(),
            "by_model": self.spend_by_model(),
            "by_provider": self.spend_by_provider(),
        }

    def clear(self) -> None:
        """Clear all transactions (use with caution)."""
        with sqlite3.connect(self._db_file) as conn:
            conn.execute("DELETE FROM transactions")

    def check_budget(self, estimated_cost: float = 0.0) -> None:
        """Check if spending is within budget limits.

        Call this BEFORE making an API request to prevent overspending.

        Args:
            estimated_cost: The estimated cost of the upcoming request.

        Raises:
            BudgetExceededError: If budget would be exceeded.
        """
        now = time.time()

        # Check hourly budget
        if self._hourly_budget is not None:
            hour_ago = now - 3600
            hourly_spend = self.total_spend(since=hour_ago)
            if hourly_spend + estimated_cost > self._hourly_budget:
                raise BudgetExceededError(
                    f"Hourly budget exceeded: ${hourly_spend:.4f} spent + "
                    f"${estimated_cost:.4f} request > ${self._hourly_budget:.2f} limit",
                    current_spend=hourly_spend,
                    budget=self._hourly_budget,
                    period="hourly"
                )

        # Check daily budget
        if self._daily_budget is not None:
            day_ago = now - 86400
            daily_spend = self.total_spend(since=day_ago)
            if daily_spend + estimated_cost > self._daily_budget:
                raise BudgetExceededError(
                    f"Daily budget exceeded: ${daily_spend:.4f} spent + "
                    f"${estimated_cost:.4f} request > ${self._daily_budget:.2f} limit",
                    current_spend=daily_spend,
                    budget=self._daily_budget,
                    period="daily"
                )

    def budget_status(self) -> dict:
        """Get current budget status."""
        now = time.time()
        hour_ago = now - 3600
        day_ago = now - 86400

        hourly_spend = self.total_spend(since=hour_ago)
        daily_spend = self.total_spend(since=day_ago)

        return {
            "hourly_spend": hourly_spend,
            "hourly_budget": self._hourly_budget,
            "hourly_remaining": (self._hourly_budget - hourly_spend) if self._hourly_budget else None,
            "daily_spend": daily_spend,
            "daily_budget": self._daily_budget,
            "daily_remaining": (self._daily_budget - daily_spend) if self._daily_budget else None,
        }


# Global ledger instance
_ledger: Optional[UsageLedger] = None


def get_usage_ledger() -> UsageLedger:
    """Get the global usage ledger."""
    global _ledger
    if _ledger is None:
        _ledger = UsageLedger()
    return _ledger
