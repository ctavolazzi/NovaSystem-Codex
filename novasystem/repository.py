"""
Backwards compatibility shim for novasystem.repository.

This module existed in novasystem v0.1.1. It has been moved to:
    novasystem.tools.repository

This shim allows old code to continue working.
"""

from .tools.repository import RepositoryHandler

__all__ = ["RepositoryHandler"]
