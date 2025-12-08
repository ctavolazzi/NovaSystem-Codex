"""
NovaSystem CLI package.

Provides the Typer-powered CLI (main) and a lightweight legacy helper used by
tests (`legacy_main` and `show_run`).
"""

from __future__ import annotations

import argparse
import json
import logging
from typing import List, Optional

from .. import __version__
from ..nova import Nova
from .main import main
from .session_cli import main as session_cli

logger = logging.getLogger(__name__)


def configure_parser() -> argparse.ArgumentParser:
    """Minimal argparse parser mirroring the classic CLI surface."""
    parser = argparse.ArgumentParser(
        description=f"NovaSystem CLI (legacy compatibility) v{__version__}"
    )
    parser.add_argument(
        "--db-path",
        help="Path to the NovaSystem SQLite database (optional).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("install", help="Analyze repository docs and execute install commands.")
    subparsers.add_parser("list-runs", help="List previous NovaSystem runs.")
    subparsers.add_parser("delete-run", help="Delete a stored run by ID.")
    subparsers.add_parser("cleanup", help="Cleanup runs older than N days.")

    show_parser = subparsers.add_parser("show-run", help="Show details for a stored run.")
    show_parser.add_argument("run_id", type=int, help="Run ID to inspect.")
    show_parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="Output format.",
    )

    return parser


def show_run(args: argparse.Namespace) -> int:
    """Display run details, focusing on stored documentation."""
    try:
        if getattr(args, "verbose", False):
            logging.getLogger().setLevel(logging.DEBUG)

        logger.debug("Showing run %s", args.run_id)
        nova = Nova(db_path=getattr(args, "db_path", None))
        result = nova.get_run_details(args.run_id)
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}")
        return 1

    if "error" in result:
        print(f"Error: {result['error']}")
        return 1

    if getattr(args, "output", "text") == "json":
        print(json.dumps(result, indent=2))
        return 0

    run = result.get("run", {})
    docs = result.get("documentation") or []

    print("\n=== NovaSystem Run Details ===")
    if run:
        print(f"Run ID: {run.get('id')}")
        if run.get("repo_url"):
            print(f"Repository: {run['repo_url']}")
        if run.get("status"):
            print(f"Status: {run['status']}")

    print(f"\nDocumentation Files ({len(docs)}):")
    for idx, doc in enumerate(docs, 1):
        path = doc.get("file_path", "<unknown>")
        content = doc.get("content") or ""
        print(f"{idx}. {path} ({len(content)} bytes)")

    return 0


def legacy_main(args: Optional[List[str]] = None) -> int:
    """Entry point used for `python -m novasystem.cli --help` in tests."""
    parser = configure_parser()
    parsed = parser.parse_args(args)

    if not parsed.command:
        parser.print_help()
        return 0

    if parsed.command == "show-run":
        return show_run(parsed)

    # Stub handlers for legacy commands to keep help output stable.
    print(f"Command '{parsed.command}' is not implemented in the compatibility CLI.")
    return 0


__all__ = ["main", "session_cli", "legacy_main", "configure_parser", "show_run", "Nova"]
