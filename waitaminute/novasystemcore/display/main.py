"""Utility entry point for running the NovaSystem API locally."""
from __future__ import annotations

import os

import uvicorn

from ..app import create_app


def main() -> None:
    """Launch the FastAPI application using uvicorn."""

    app = create_app()
    host = os.environ.get("NOVASYSTEM_HOST", "0.0.0.0")
    port = int(os.environ.get("NOVASYSTEM_PORT", "8000"))
    reload_enabled = os.environ.get("NOVASYSTEM_RELOAD", "false").lower() == "true"
    log_level = os.environ.get("NOVASYSTEM_LOG_LEVEL", "info")

    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=reload_enabled,
        log_level=log_level,
    )


if __name__ == "__main__":
    main()
