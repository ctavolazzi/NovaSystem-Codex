"""
NovaSystem CLI Tools
"""

from .main import main
from .session_cli import main as session_cli

# Backwards compatibility: expose Nova class from tools
from ..nova import Nova


def show_run(args):
    """
    Display run details including documentation.
    
    Backwards compatibility shim for older CLI tests.
    
    Args:
        args: Namespace with run_id, verbose, output attributes
        
    Returns:
        int: Exit code (0 for success)
    """
    nova = Nova()
    details = nova.get_run_details(args.run_id)
    
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
            if args.verbose:
                print(f"    Content: {doc.get('content', '')[:100]}...")
    
    return 0


__all__ = ['main', 'session_cli', 'Nova', 'show_run']
