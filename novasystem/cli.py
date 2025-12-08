"""
Lightweight legacy CLI shim to satisfy backward-compatible workflows and tests.

This module surfaces a small argparse-based interface with the classic commands
(`install`, `list-runs`, `show-run`, `delete-run`, `cleanup`) and delegates
data access to the current Nova/Database implementations. It does not aim to
replace the richer Typer-powered CLI under novasystem/cli/main.py; it simply
provides help text and a minimal `show_run` helper used in tests.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import List, Optional

from . import __version__
from .nova import Nova

# Allow submodules under novasystem/cli/ to remain importable (e.g., Typer app).
__path__ = [str(Path(__file__).with_suffix(""))]

logger = logging.getLogger(__name__)


def configure_parser() -> argparse.ArgumentParser:
    """Build a minimal argparse parser exposing legacy commands."""
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


def main(args: Optional[List[str]] = None) -> int:
    """Entry point used by `python -m novasystem.cli --help` and console scripts."""
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


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["configure_parser", "show_run", "main", "Nova"]
