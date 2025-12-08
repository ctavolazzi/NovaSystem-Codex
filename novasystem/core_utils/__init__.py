"""
Package wrapper for backwards compatibility.

The original implementation lived in novasystem.core_utils (module). This
package re-exports the same helpers from novasystem.tools.decision_matrix so
imports of either `novasystem.core_utils` or `novasystem.core_utils.*` work.
"""

from ..tools.decision_matrix import (
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
