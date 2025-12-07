"""
Backwards compatibility shim for novasystem.technical_debt.

This module existed in novasystem v0.1.1. It has been moved to:
    novasystem.tools.technical_debt

This shim allows old code to continue working.
"""

from .tools.technical_debt import (
    TechnicalDebtManager,
    TechnicalDebtItem,
    Severity,
    Status,
)

__all__ = [
    "TechnicalDebtManager",
    "TechnicalDebtItem",
    "Severity",
    "Status",
]
