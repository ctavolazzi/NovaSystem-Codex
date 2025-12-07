"""
NovaSystem MCP Server Module.

This module provides Model Context Protocol (MCP) server functionality
for NovaSystem, allowing external tools and clients to interact with
NovaSystem's problem-solving capabilities.
"""

from .server import NovaMCPServer

__all__ = ["NovaMCPServer"]

