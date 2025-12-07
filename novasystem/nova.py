"""
Backwards compatibility shim for novasystem.nova.

This module existed in novasystem v0.1.1. It has been moved to:
    novasystem.tools.nova

This shim allows old code to continue working.
"""

from .tools.nova import Nova

__all__ = ["Nova"]
