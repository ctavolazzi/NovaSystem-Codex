#!/usr/bin/env python3
"""
NovaSystem Entry Point.

Allows running NovaSystem as a module:
    python -m novasystem                    # Launch interactive mode
    python -m novasystem interactive        # Launch interactive mode (explicit)
    python -m novasystem solve "problem"    # Use CLI
    python -m novasystem --help             # Show CLI help
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
from pathlib import Path


def main():
    """Main entry point - launches interactive mode by default."""
    # Add project root to path for novasystem_interactive
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    # No args or 'interactive' = launch interactive mode
    if len(sys.argv) == 1 or (len(sys.argv) > 1 and sys.argv[1].lower() == "interactive"):
        try:
            from novasystem_interactive import main as interactive_main
            interactive_main()
            return 0
        except ImportError:
            print("Interactive mode not available. Falling back to CLI.")
            print("Run: python -m novasystem --help")
            return 1
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return 0

    # Otherwise, use CLI
    from .cli import main as cli_main
    return cli_main()


if __name__ == "__main__":
    sys.exit(main())
