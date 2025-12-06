"""Nova MVP - FastAPI Backend Entry Point.

Multi-agent problem solving with parallel processing.

Run with: uvicorn main:app --reload --port 8000
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import api_router
from backend.api.websocket import websocket_endpoint


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    print("\n" + "=" * 60)
    print("  NOVA MVP - Multi-Agent Problem Solving System")
    print("=" * 60)
    print(f"  API: http://localhost:{os.environ.get('PORT', 8000)}")
    print(f"  Docs: http://localhost:{os.environ.get('PORT', 8000)}/docs")
    print("=" * 60 + "\n")
    yield
    print("\nShutting down Nova MVP...")


app = FastAPI(
    title="Nova MVP",
    description="""
## Multi-Agent Problem Solving System

Nova MVP orchestrates multiple AI agents to solve complex problems:

### Agents
- **DCE (Discussion Continuity Expert)**: Unpacks problems and synthesizes solutions
- **CAE (Critical Analysis Expert)**: Identifies risks and edge cases
- **Domain Experts**: Provide specialized knowledge (Technology, Business, Security, etc.)

### Three-Phase Process
1. **Unpack**: DCE breaks down the problem
2. **Analyze**: All experts analyze in parallel
3. **Synthesize**: DCE combines insights into recommendations

### Endpoints
- `POST /api/solve` - Async solve (returns session_id)
- `POST /api/solve/sync` - Synchronous solve (waits for result)
- `GET /api/sessions/{id}` - Get session status/results
- `WS /api/ws/{id}` - Real-time streaming updates
""",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include REST routes
app.include_router(api_router)

# WebSocket route
app.websocket("/api/ws/{session_id}")(websocket_endpoint)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "Nova MVP",
        "version": "0.1.0",
        "description": "Multi-Agent Problem Solving System",
        "endpoints": {
            "solve_async": "POST /api/solve",
            "solve_sync": "POST /api/solve/sync",
            "get_session": "GET /api/sessions/{session_id}",
            "list_sessions": "GET /api/sessions",
            "websocket": "WS /api/ws/{session_id}",
            "health": "GET /api/health",
            "providers": "GET /api/providers",
            "docs": "GET /docs"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=True
    )
