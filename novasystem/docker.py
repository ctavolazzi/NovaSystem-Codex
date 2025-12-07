"""
Backwards compatibility shim for novasystem.docker.

This module existed in novasystem v0.1.1. It has been moved to:
    novasystem.tools.docker

This shim allows old code to continue working.
"""

from .tools.docker import DockerExecutor, CommandResult

__all__ = ["DockerExecutor", "CommandResult"]
