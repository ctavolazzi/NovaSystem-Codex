"""
WebSocket support for NovaSystem.

This module provides WebSocket functionality for real-time communication
with the Nova Process.
"""

from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, Any
import json
import logging
import asyncio

logger = logging.getLogger(__name__)

class WebSocketManager:
    """Manages WebSocket connections for real-time updates."""

    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        """Accept a WebSocket connection for a session."""
        await websocket.accept()

        if session_id not in self.active_connections:
            self.active_connections[session_id] = []

        self.active_connections[session_id].append(websocket)
        logger.info(f"WebSocket connected for session {session_id}")

        try:
            while True:
                # Keep connection alive and handle any incoming messages
                data = await websocket.receive_text()
                # Echo back for now - can be extended for bidirectional communication
                await websocket.send_text(f"Echo: {data}")
        except WebSocketDisconnect:
            self.disconnect(websocket, session_id)

    def disconnect(self, websocket: WebSocket, session_id: str):
        """Remove a WebSocket connection."""
        if session_id in self.active_connections:
            if websocket in self.active_connections[session_id]:
                self.active_connections[session_id].remove(websocket)

            # Clean up empty session
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

        logger.info(f"WebSocket disconnected for session {session_id}")

    async def send_to_session(self, session_id: str, message: Dict[str, Any]):
        """Send a message to all WebSocket connections for a session."""
        if session_id not in self.active_connections:
            return

        message_json = json.dumps(message)
        disconnected = []

        for websocket in self.active_connections[session_id]:
            try:
                await websocket.send_text(message_json)
            except Exception as e:
                logger.warning(f"Failed to send message to WebSocket: {str(e)}")
                disconnected.append(websocket)

        # Remove disconnected WebSockets
        for websocket in disconnected:
            self.disconnect(websocket, session_id)

    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast a message to all active connections."""
        for session_id in list(self.active_connections.keys()):
            await self.send_to_session(session_id, message)

    def get_connection_count(self, session_id: str = None) -> int:
        """Get the number of active connections."""
        if session_id:
            return len(self.active_connections.get(session_id, []))
        else:
            return sum(len(connections) for connections in self.active_connections.values())

    def get_active_sessions(self) -> List[str]:
        """Get list of sessions with active connections."""
        return list(self.active_connections.keys())
