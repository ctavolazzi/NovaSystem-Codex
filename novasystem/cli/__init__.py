"""
NovaSystem CLI package.

Exports:
- `main` (Typer-powered primary CLI)
- `session_cli` (session-aware variant)
- `show_run` (lightweight helper used by legacy tests)
- `legacy_main` (alias to the Typer entry for python -m novasystem.cli)
"""

from __future__ import annotations

import argparse
import json
import logging
from typing import List, Optional

from ..nova import Nova
from .main import main
from .session_cli import main as session_cli

logger = logging.getLogger(__name__)


def show_run(args: argparse.Namespace) -> int:
    """Display run details including documentation (legacy helper used in tests)."""
    try:
        nova = Nova()
        details = nova.get_run_details(args.run_id)
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}")
        return 1

    if details is None:
        print(f"Run {args.run_id} not found")
        return 1

    run_info = details.get("run", {})
    print(f"Run ID: {run_info.get('id', 'N/A')}")
    print(f"Repository: {run_info.get('repo_url', 'N/A')}")
    print(f"Status: {run_info.get('status', 'N/A')}")
    print(f"Started: {run_info.get('start_time', 'N/A')}")

    commands = details.get("commands", [])
    if commands:
        print(f"\nCommands ({len(commands)}):")
        for cmd in commands:
            print(f"  - {cmd.get('command', 'N/A')}")

    docs = details.get("documentation", [])
    if docs:
        print(f"\nDocumentation Files ({len(docs)}):")
        for doc in docs:
            print(f"  - {doc.get('file_path', 'N/A')}")
            if getattr(args, "verbose", False):
                print(f"    Content: {doc.get('content', '')[:100]}...")

    return 0


def legacy_main(args: Optional[List[str]] = None) -> int:
    """Alias to the Typer CLI so `python -m novasystem.cli` works."""
    return main(args)


__all__ = ["main", "session_cli", "Nova", "show_run", "legacy_main"]
