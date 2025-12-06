"""REST API routes for Nova MVP."""

import asyncio
from typing import List, Optional
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field

from ..core import (
    CostEstimator,
    NovaProcess,
    RateLimitExceeded,
    SessionState,
    get_llm,
    traffic_controller,
)

# In-memory session storage (replace with database in production)
sessions: dict[str, SessionState] = {}

router = APIRouter(prefix="/api", tags=["nova"])


class SolveRequest(BaseModel):
    """Request body for problem solving."""
    problem: str = Field(..., min_length=1, description="The problem to solve")
    domains: Optional[List[str]] = Field(
        default=["technology", "business"],
        description="Domain expertise to include"
    )
    provider: Optional[str] = Field(
        default="auto",
        description="LLM provider: claude, openai, mock, or auto"
    )


class SolveResponse(BaseModel):
    """Response for async solve request."""
    session_id: str
    status: str
    message: str


class SessionResponse(BaseModel):
    """Full session state response."""
    session_id: str
    problem: str
    domains: List[str]
    phase: str
    created_at: str
    updated_at: str
    unpack_result: Optional[dict] = None
    analysis_results: List[dict] = []
    synthesis_result: Optional[dict] = None
    error: Optional[str] = None
    execution_time: float = 0.0


class StatusRequest(BaseModel):
    """Request body for checking cost and rate limit status."""

    prompt: str = Field(..., description="Prompt to evaluate")
    model: str = Field(..., description="Model identifier")


class StatusResponse(BaseModel):
    """Response describing projected cost and rate limit status."""

    cost_estimate: dict
    rate_limit_status: str
    retry_after: float = 0.0


@router.post("/solve", response_model=SolveResponse)
async def start_solve(request: SolveRequest, background_tasks: BackgroundTasks):
    """
    Start an async problem-solving session.

    Returns immediately with a session_id.
    Use /sessions/{session_id} or WebSocket to get results.
    """
    llm = get_llm(request.provider)
    process = NovaProcess(llm_provider=llm)

    try:
        result = await asyncio.wait_for(
            asyncio.create_task(
                process.solve(request.problem, request.domains)
            ),
            timeout=300  # 5 minute timeout
        )
    except RateLimitExceeded as exc:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Retry after {exc.retry_after:.0f}s",
            headers={"Retry-After": str(int(exc.retry_after))},
        )

    sessions[result.session_id] = result

    return SolveResponse(
        session_id=result.session_id,
        status=result.phase.value,
        message="Processing complete" if result.phase.value == "completed" else f"Phase: {result.phase.value}"
    )


@router.post("/solve/sync", response_model=SessionResponse)
async def solve_sync(request: SolveRequest):
    """
    Synchronous problem solving - waits for full result.

    Use for simpler integrations that don't need streaming.
    """
    llm = get_llm(request.provider)
    process = NovaProcess(llm_provider=llm)

    try:
        result = await asyncio.wait_for(
            process.solve(request.problem, request.domains),
            timeout=300
        )
        sessions[result.session_id] = result
        return SessionResponse(**result.to_dict())

    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Request timed out")
    except RateLimitExceeded as exc:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Retry after {exc.retry_after:.0f}s",
            headers={"Retry-After": str(int(exc.retry_after))},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str):
    """Get the current state of a session."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    return SessionResponse(**sessions[session_id].to_dict())


@router.get("/sessions")
async def list_sessions(limit: int = 10, offset: int = 0):
    """List recent sessions."""
    all_sessions = list(sessions.values())
    # Sort by created_at descending
    all_sessions.sort(key=lambda s: s.created_at, reverse=True)

    return {
        "total": len(all_sessions),
        "sessions": [
            {
                "session_id": s.session_id,
                "problem": s.problem[:100] + "..." if len(s.problem) > 100 else s.problem,
                "phase": s.phase.value,
                "created_at": s.created_at
            }
            for s in all_sessions[offset:offset + limit]
        ]
    }


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a session."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    del sessions[session_id]
    return {"message": "Session deleted", "session_id": session_id}


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "nova-mvp",
        "version": "0.1.0"
    }


@router.get("/providers")
async def list_providers():
    """List available LLM providers and their status."""
    from ..core.llm import ClaudeProvider, OpenAIProvider, MockProvider

    return {
        "providers": [
            {
                "name": "claude",
                "available": ClaudeProvider().is_available(),
                "model": "claude-sonnet-4-20250514"
            },
            {
                "name": "openai",
                "available": OpenAIProvider().is_available(),
                "model": "gpt-4o"
            },
            {
                "name": "mock",
                "available": True,
                "model": "mock-v1"
            }
        ]
    }


@router.post("/check-status", response_model=StatusResponse)
async def check_status(request: StatusRequest):
    """Return projected cost and current rate limit posture for a prompt."""

    estimator = CostEstimator()
    estimated_output_tokens = 1000

    try:
        cost_estimate = estimator.estimate(
            request.model,
            request.prompt,
            estimated_output_tokens=estimated_output_tokens,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    rate_limit_status = "ok"
    retry_after = 0.0

    try:
        traffic_controller.check_allowance(
            request.model,
            cost_estimate.input_tokens,
            estimated_output_tokens=estimated_output_tokens,
            commit=False,
        )
    except RateLimitExceeded as exc:
        rate_limit_status = "blocked"
        retry_after = exc.retry_after

    return StatusResponse(
        cost_estimate=cost_estimate.__dict__,
        rate_limit_status=rate_limit_status,
        retry_after=retry_after,
    )
