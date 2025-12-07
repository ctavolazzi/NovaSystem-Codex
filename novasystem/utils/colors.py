"""
Shared terminal colors and logging utilities.

Single source of truth for ANSI colors and console output formatting.
"""

from datetime import datetime
from typing import Optional


class Colors:
    """ANSI color codes for terminal output."""
    # Basic colors
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[35m'
    WHITE = '\033[97m'

    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'

    # Reset
    END = '\033[0m'
    RESET = '\033[0m'

    @classmethod
    def disable(cls):
        """Disable all colors (for non-TTY output)."""
        for attr in dir(cls):
            if attr.isupper() and not attr.startswith('_'):
                setattr(cls, attr, '')


# Agent-specific colors
AGENT_COLORS = {
    "DCE": Colors.CYAN,
    "CAE": Colors.YELLOW,
    "Domain Expert": Colors.GREEN,
    "System": Colors.MAGENTA,
}


def colorize(text: str, color: str) -> str:
    """Apply color to text."""
    return f"{color}{text}{Colors.END}"


def format_timestamp() -> str:
    """Get formatted timestamp for logs."""
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


def console_log(emoji: str, category: str, message: str, details: Optional[dict] = None, color: str = ""):
    """
    Log a message with consistent formatting.

    Args:
        emoji: Emoji prefix (e.g., "🎯", "✅", "❌")
        category: Category label (e.g., "LLM/INIT", "AGENT/DCE")
        message: Main message
        details: Optional dict of additional details
        color: Optional color code
    """
    timestamp = format_timestamp()
    prefix = f"{color}" if color else ""
    suffix = f"{Colors.END}" if color else ""

    print(f"{timestamp} | {prefix}{emoji} [{category}] {message}{suffix}")

    if details:
        for key, value in details.items():
            val_str = str(value)
            if len(val_str) > 100:
                val_str = val_str[:100] + "..."
            print(f"           └─ {key}: {val_str}")


def print_separator(char: str = "=", width: int = 80, color: str = ""):
    """Print a separator line."""
    prefix = f"{color}" if color else ""
    suffix = f"{Colors.END}" if color else ""
    print(f"{prefix}{char * width}{suffix}")


def print_header(title: str, width: int = 60, color: str = Colors.CYAN):
    """Print a formatted header."""
    print(f"\n{color}{Colors.BOLD}{title.center(width, '=')}{Colors.END}")
