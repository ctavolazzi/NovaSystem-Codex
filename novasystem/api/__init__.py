"""
API layer for NovaSystem.

This module provides REST API endpoints and WebSocket support for
interacting with the Nova Process.
"""

from .rest import create_app, NovaAPI
from .websocket import WebSocketManager

__all__ = [
    "create_app",
    "NovaAPI",
    "WebSocketManager",
]
