#!/usr/bin/env python3
"""
NovaSystem Session CLI Tool

Command-line interface for managing NovaSystem sessions.
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from novasystem.session import get_session_manager
from novasystem.config import get_config

def list_sessions(args):
    """List all sessions."""
    session_manager = get_session_manager()
    sessions = session_manager.list_sessions(limit=args.limit)

    if not sessions:
        print("No sessions found.")
        return

    print(f"Found {len(sessions)} sessions:")
    print("-" * 80)
    print(f"{'Filename':<40} {'Created':<20} {'Size':<10}")
    print("-" * 80)

    for session in sessions:
        size_kb = session['size_bytes'] / 1024
        print(f"{session['filename']:<40} {session['created_at'].strftime('%Y-%m-%d %H:%M'):<20} {size_kb:.1f}KB")

def show_session(args):
    """Show session details."""
    session_manager = get_session_manager()

    if args.session_id:
        # Find session by ID
        sessions = session_manager.list_sessions()
        session_file = None
        for session in sessions:
            if session['session_id'] == args.session_id:
                session_file = session['file_path']
                break

        if not session_file:
            print(f"Session with ID {args.session_id} not found.")
            return
    else:
        session_file = args.file

    try:
        session = session_manager.load_session(session_file)

        print(f"Session: {session.metadata.title or 'Untitled'}")
        print(f"ID: {session.metadata.session_id}")
        print(f"Created: {session.metadata.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Updated: {session.metadata.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Messages: {session.metadata.total_messages}")
        print(f"Tokens: {session.metadata.total_tokens}")
        print(f"Model: {session.metadata.model_used}")
        print(f"Tags: {', '.join(session.metadata.tags)}")

        if args.content:
            print("\n" + "="*50)
            print("SESSION CONTENT")
            print("="*50)
            print(session.to_markdown())

    except Exception as e:
        print(f"Error loading session: {e}")

def create_session(args):
    """Create a new session."""
    session_manager = get_session_manager()

    session = session_manager.create_session(
        title=args.title,
        description=args.description,
        tags=args.tags.split(',') if args.tags else []
    )

    print(f"Created new session: {session.metadata.session_id}")
    print(f"Title: {session.metadata.title}")
    print(f"Description: {session.metadata.description}")
    print(f"Tags: {', '.join(session.metadata.tags)}")

def config_info(args):
    """Show configuration information."""
    config = get_config()

    print("NovaSystem Configuration:")
    print("-" * 40)
    print(f"Session directory: {config.get_session_dir()}")
    print(f"Data directory: {config.get_data_dir()}")
    print(f"Logs directory: {config.get_logs_dir()}")
    print(f"Default model: {config.llm.default_model}")
    print(f"Auto-save sessions: {config.session.auto_save_sessions}")
    print(f"Session retention: {config.session.session_retention_days} days")

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="NovaSystem Session Management CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # List sessions command
    list_parser = subparsers.add_parser('list', help='List all sessions')
    list_parser.add_argument('--limit', type=int, default=20, help='Maximum number of sessions to show')
    list_parser.set_defaults(func=list_sessions)

    # Show session command
    show_parser = subparsers.add_parser('show', help='Show session details')
    show_group = show_parser.add_mutually_exclusive_group(required=True)
    show_group.add_argument('--file', help='Session file path')
    show_group.add_argument('--session-id', help='Session ID')
    show_parser.add_argument('--content', action='store_true', help='Show full session content')
    show_parser.set_defaults(func=show_session)

    # Create session command
    create_parser = subparsers.add_parser('create', help='Create a new session')
    create_parser.add_argument('--title', help='Session title')
    create_parser.add_argument('--description', help='Session description')
    create_parser.add_argument('--tags', help='Comma-separated tags')
    create_parser.set_defaults(func=create_session)

    # Config command
    config_parser = subparsers.add_parser('config', help='Show configuration information')
    config_parser.set_defaults(func=config_info)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
