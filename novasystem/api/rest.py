"""
REST API for NovaSystem.

This module provides FastAPI-based REST endpoints for interacting with
the Nova Process.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from ..config.models import get_default_model
import asyncio
import logging
import uuid
from datetime import datetime

from ..core.process import NovaProcess
from ..core.memory import MemoryManager
from .websocket import WebSocketManager

logger = logging.getLogger(__name__)

# Pydantic models
class ProblemRequest(BaseModel):
    problem: str
    domains: Optional[List[str]] = None
    max_iterations: Optional[int] = 5
    model: Optional[str] = get_default_model()

class ProblemResponse(BaseModel):
    session_id: str
    status: str
    message: str

class SessionStatus(BaseModel):
    session_id: str
    status: str
    current_iteration: int
    total_iterations: int
    is_active: bool
    problem_statement: str

class SessionResult(BaseModel):
    session_id: str
    result: Dict[str, Any]
    solution_history: List[Dict[str, Any]]
    completed_at: datetime

# Global session storage (in production, use a proper database)
active_sessions: Dict[str, Dict[str, Any]] = {}
completed_sessions: Dict[str, Dict[str, Any]] = {}

class NovaAPI:
    """Nova Process API handler."""

    def __init__(self):
        self.websocket_manager = WebSocketManager()

    async def start_problem_solving(self, request: ProblemRequest) -> ProblemResponse:
        """Start a new problem-solving session."""
        session_id = str(uuid.uuid4())

        # Create Nova Process instance
        memory_manager = MemoryManager()
        nova_process = NovaProcess(
            domains=request.domains,
            model=request.model,
            memory_manager=memory_manager
        )

        # Store session
        active_sessions[session_id] = {
            "nova_process": nova_process,
            "request": request,
            "started_at": datetime.now(),
            "status": "running"
        }

        # Start background task
        asyncio.create_task(self._run_problem_solving(session_id, request))

        return ProblemResponse(
            session_id=session_id,
            status="started",
            message="Problem-solving session started"
        )

    async def _run_problem_solving(self, session_id: str, request: ProblemRequest):
        """Run the problem-solving process in the background."""
        try:
            session = active_sessions[session_id]
            nova_process = session["nova_process"]

            # Stream results to WebSocket
            async for update in nova_process.solve_problem(
                request.problem,
                request.max_iterations,
                stream=True
            ):
                # Send update via WebSocket
                await self.websocket_manager.send_to_session(session_id, update)

            # Get final result
            final_result = await nova_process.get_solution_history()

            # Move to completed sessions
            completed_sessions[session_id] = {
                "result": final_result,
                "solution_history": nova_process.get_solution_history(),
                "completed_at": datetime.now(),
                "request": request
            }

            # Remove from active sessions
            del active_sessions[session_id]

            # Send completion notification
            await self.websocket_manager.send_to_session(session_id, {
                "type": "session_complete",
                "session_id": session_id
            })

        except Exception as e:
            logger.error(f"Error in problem-solving session {session_id}: {str(e)}")

            # Send error notification
            await self.websocket_manager.send_to_session(session_id, {
                "type": "error",
                "error": str(e)
            })

            # Remove from active sessions
            if session_id in active_sessions:
                del active_sessions[session_id]

    async def get_session_status(self, session_id: str) -> SessionStatus:
        """Get the status of a problem-solving session."""
        if session_id in active_sessions:
            session = active_sessions[session_id]
            nova_process = session["nova_process"]
            status = nova_process.get_status()

            return SessionStatus(
                session_id=session_id,
                status="running",
                current_iteration=status["current_iteration"],
                total_iterations=status["total_iterations"],
                is_active=status["is_active"],
                problem_statement=status["problem_statement"]
            )
        elif session_id in completed_sessions:
            return SessionStatus(
                session_id=session_id,
                status="completed",
                current_iteration=0,
                total_iterations=0,
                is_active=False,
                problem_statement=completed_sessions[session_id]["request"].problem
            )
        else:
            raise HTTPException(status_code=404, detail="Session not found")

    async def get_session_result(self, session_id: str) -> SessionResult:
        """Get the result of a completed session."""
        if session_id not in completed_sessions:
            raise HTTPException(status_code=404, detail="Session not found or not completed")

        session_data = completed_sessions[session_id]

        return SessionResult(
            session_id=session_id,
            result=session_data["result"],
            solution_history=session_data["solution_history"],
            completed_at=session_data["completed_at"]
        )

    async def list_sessions(self) -> List[Dict[str, Any]]:
        """List all sessions (active and completed)."""
        sessions = []

        # Add active sessions
        for session_id, session_data in active_sessions.items():
            sessions.append({
                "session_id": session_id,
                "status": "active",
                "started_at": session_data["started_at"],
                "problem": session_data["request"].problem[:100] + "..."
            })

        # Add completed sessions
        for session_id, session_data in completed_sessions.items():
            sessions.append({
                "session_id": session_id,
                "status": "completed",
                "started_at": session_data["completed_at"],
                "problem": session_data["request"].problem[:100] + "..."
            })

        return sessions

# Create FastAPI app
def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="NovaSystem API",
        description="API for the Nova Process multi-agent problem-solving framework",
        version="0.3.1"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize API handler
    api = NovaAPI()

    @app.post("/api/solve", response_model=ProblemResponse)
    async def solve_problem(request: ProblemRequest):
        """Start a new problem-solving session."""
        return await api.start_problem_solving(request)

    @app.get("/api/sessions/{session_id}/status", response_model=SessionStatus)
    async def get_session_status(session_id: str):
        """Get session status."""
        return await api.get_session_status(session_id)

    @app.get("/api/sessions/{session_id}/result", response_model=SessionResult)
    async def get_session_result(session_id: str):
        """Get session result."""
        return await api.get_session_result(session_id)

    @app.get("/api/sessions")
    async def list_sessions():
        """List all sessions."""
        return await api.list_sessions()

    @app.websocket("/ws/{session_id}")
    async def websocket_endpoint(websocket, session_id: str):
        """WebSocket endpoint for real-time updates."""
        await api.websocket_manager.connect(websocket, session_id)

    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "message": "NovaSystem API",
            "version": "0.3.1",
            "endpoints": {
                "solve": "/api/solve",
                "session_status": "/api/sessions/{session_id}/status",
                "session_result": "/api/sessions/{session_id}/result",
                "list_sessions": "/api/sessions",
                "websocket": "/ws/{session_id}"
            }
        }

    return app

# For running the API directly
if __name__ == "__main__":
    import uvicorn
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
