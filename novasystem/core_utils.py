"""
Backwards compatibility shim for novasystem.core_utils.

This module existed in novasystem v0.1.1. It has been moved to:
    novasystem.tools.decision_matrix

This shim allows old code to continue working.
"""

from .tools.decision_matrix import (
    DecisionMatrix,
    DecisionResult,
    make_decision,
    compare_methods,
    generate_doc_map,
)

__all__ = [
    "DecisionMatrix",
    "DecisionResult",
    "make_decision",
    "compare_methods",
    "generate_doc_map",
]
