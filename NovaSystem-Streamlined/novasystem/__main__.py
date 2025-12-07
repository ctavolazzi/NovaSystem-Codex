#!/usr/bin/env python3
"""
NovaSystem CLI Entry Point.

Allows running NovaSystem as a module:
    python -m novasystem solve "Your problem here"
    python -m novasystem interactive
    python -m novasystem list-models
"""

# ============================================================================
# CRITICAL: Suppress noisy loggers BEFORE any other imports
# This must happen first to prevent import-time logging spam
# ============================================================================
import logging
import os

# Disable most debug logging globally
logging.basicConfig(level=logging.WARNING, format='%(message)s')

# Silence specific noisy libraries
_noisy_loggers = [
    "PIL", "PIL.Image", "PIL.PngImagePlugin",
    "httpcore", "httpcore.http11", "httpcore.connection",
    "httpx", "urllib3", "urllib3.connectionpool",
    "gradio", "gradio_client", "gradio.utils",
    "asyncio", "fsspec", "filelock", "aiohttp",
    "multipart", "werkzeug",
]
for logger_name in _noisy_loggers:
    logging.getLogger(logger_name).setLevel(logging.ERROR)

# Also set via environment variable for libraries that check at import
os.environ.setdefault("GRADIO_ANALYTICS_ENABLED", "False")

# ============================================================================
# Now we can safely import and run
# ============================================================================

import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())
