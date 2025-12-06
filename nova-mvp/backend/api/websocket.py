"""WebSocket endpoint for real-time streaming updates."""

import asyncio
import json
from typing import Optional
from fastapi import WebSocket, WebSocketDisconnect

from ..core import NovaProcess, SessionState, get_llm
from ..agents.base import AgentResponse


class ConnectionManager:
    """Manages WebSocket connections."""

    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]

    async def send_json(self, session_id: str, data: dict):
        if session_id in self.active_connections:
            try:
                await self.active_connections[session_id].send_json(data)
            except Exception:
                self.disconnect(session_id)


manager = ConnectionManager()


async def websocket_endpoint(
    websocket: WebSocket,
    session_id: str,
    problem: Optional[str] = None,
    domains: Optional[str] = None,
    provider: str = "auto"
):
    """
    WebSocket endpoint for real-time problem solving.

    Connect to: ws://host/api/ws/{session_id}?problem=...&domains=tech,business&provider=auto

    Receives JSON messages:
    - {"type": "phase_change", "phase": "...", "session_id": "..."}
    - {"type": "agent_response", "agent_name": "...", "content": "..."}
    - {"type": "complete", "session": {...}}
    - {"type": "error", "message": "..."}
    """
    await manager.connect(websocket, session_id)

    try:
        if problem:
            # Start solving immediately if problem provided in query
            domain_list = domains.split(",") if domains else ["technology", "business"]

            llm = get_llm(provider)

            # Create callbacks that send via WebSocket
            async def on_phase_change(state: SessionState):
                await manager.send_json(session_id, {
                    "type": "phase_change",
                    "phase": state.phase.value,
                    "session_id": state.session_id,
                    "timestamp": state.updated_at
                })

            async def on_agent_response(response: AgentResponse):
                await manager.send_json(session_id, {
                    "type": "agent_response",
                    "agent_id": response.agent_id,
                    "agent_type": response.agent_type,
                    "agent_name": response.agent_name,
                    "content": response.content,
                    "success": response.success,
                    "error": response.error,
                    "timestamp": response.timestamp
                })

            # Wrapper to make callbacks async-safe
            def phase_cb(state):
                asyncio.create_task(on_phase_change(state))

            def agent_cb(response):
                asyncio.create_task(on_agent_response(response))

            process = NovaProcess(
                llm_provider=llm,
                on_phase_change=phase_cb,
                on_agent_response=agent_cb
            )

            # Run the solve process
            result = await process.solve(problem, domain_list)

            # Send final result
            await manager.send_json(session_id, {
                "type": "complete",
                "session": result.to_dict()
            })

        else:
            # Wait for commands via WebSocket
            while True:
                data = await websocket.receive_text()

                try:
                    message = json.loads(data)

                    if message.get("action") == "solve":
                        problem = message.get("problem", "")
                        domain_list = message.get("domains", ["technology", "business"])
                        provider_name = message.get("provider", "auto")

                        if not problem:
                            await manager.send_json(session_id, {
                                "type": "error",
                                "message": "Problem is required"
                            })
                            continue

                        llm = get_llm(provider_name)

                        # Create callbacks
                        def phase_cb(state):
                            asyncio.create_task(manager.send_json(session_id, {
                                "type": "phase_change",
                                "phase": state.phase.value,
                                "session_id": state.session_id
                            }))

                        def agent_cb(response):
                            asyncio.create_task(manager.send_json(session_id, {
                                "type": "agent_response",
                                "agent_name": response.agent_name,
                                "agent_type": response.agent_type,
                                "content": response.content,
                                "success": response.success
                            }))

                        process = NovaProcess(
                            llm_provider=llm,
                            on_phase_change=phase_cb,
                            on_agent_response=agent_cb
                        )

                        result = await process.solve(problem, domain_list)

                        await manager.send_json(session_id, {
                            "type": "complete",
                            "session": result.to_dict()
                        })

                    elif message.get("action") == "ping":
                        await manager.send_json(session_id, {"type": "pong"})

                except json.JSONDecodeError:
                    await manager.send_json(session_id, {
                        "type": "error",
                        "message": "Invalid JSON"
                    })

    except WebSocketDisconnect:
        manager.disconnect(session_id)
    except Exception as e:
        await manager.send_json(session_id, {
            "type": "error",
            "message": str(e)
        })
        manager.disconnect(session_id)
