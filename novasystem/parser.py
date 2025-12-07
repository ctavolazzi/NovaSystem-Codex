"""
Backwards compatibility shim for novasystem.parser.

This module existed in novasystem v0.1.1. It has been moved to:
    novasystem.tools.parser

This shim allows old code to continue working.
"""

from .tools.parser import (
    Command,
    CommandSource,
    CommandType,
    DocumentationParser,
)

__all__ = [
    "Command",
    "CommandSource",
    "CommandType",
    "DocumentationParser",
]
