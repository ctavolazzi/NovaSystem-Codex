#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         NovaSystem v0.3 Demo                                  ║
║                    Multi-Agent Problem-Solving Framework                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

This demo showcases the key capabilities of NovaSystem. Run from the project root:

    python demo.py

For the full experience, first install the package:

    pip install -e .
    python demo.py
"""

import sys
import time
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import json
import tempfile


# =============================================================================
# DEMO UTILITIES
# =============================================================================

class Colors:
    """ANSI color codes for terminal output."""
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    DIM = '\033[90m'
    RESET = '\033[0m'


def print_header(text: str):
    """Print a section header."""
    width = 70
    print(f"\n{Colors.CYAN}{'='*width}")
    print(f"  {Colors.BOLD}{text}{Colors.RESET}{Colors.CYAN}")
    print(f"{'='*width}{Colors.RESET}\n")


def print_subheader(text: str):
    """Print a subsection header."""
    print(f"\n{Colors.YELLOW}>>> {text}{Colors.RESET}\n")


def print_success(text: str):
    """Print a success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_info(text: str):
    """Print an info message."""
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")


def print_code(code: str):
    """Print code with syntax highlighting simulation."""
    print(f"{Colors.DIM}```python{Colors.RESET}")
    for line in code.strip().split('\n'):
        print(f"  {Colors.GREEN}{line}{Colors.RESET}")
    print(f"{Colors.DIM}```{Colors.RESET}")


def pause(seconds: float = 0.5):
    """Pause for dramatic effect."""
    time.sleep(seconds)


# =============================================================================
# SELF-CONTAINED DECISION MATRIX (Demonstrates the concept)
# =============================================================================

@dataclass
class DecisionResult:
    """Results from a decision matrix analysis."""
    winner: str
    rankings: List[Tuple[str, float]]
    scores_breakdown: Dict[str, Dict[str, float]]
    total_score: Dict[str, float]
    confidence_score: float = 0.0

    def __str__(self) -> str:
        lines = [
            f"\n{Colors.CYAN}{'='*60}{Colors.RESET}",
            f"{Colors.BOLD}DECISION MATRIX RESULTS{Colors.RESET}",
            f"{Colors.CYAN}{'='*60}{Colors.RESET}",
            f"\n{Colors.GREEN}🏆 WINNER: {self.winner}{Colors.RESET}",
            f"   Confidence: {self.confidence_score:.1f}%",
            f"\n{Colors.YELLOW}📊 RANKINGS:{Colors.RESET}",
        ]
        for i, (option, score) in enumerate(self.rankings, 1):
            lines.append(f"   {i}. {option:20s} Score: {score:6.2f}")
        return "\n".join(lines)


def make_decision(
    options: List[str],
    criteria: List[str],
    scores: Dict[str, List[float]],
    weights: Optional[List[float]] = None
) -> DecisionResult:
    """
    Make a data-driven decision using a weighted decision matrix.

    Args:
        options: List of options to compare
        criteria: List of criteria to evaluate against
        scores: Dict mapping each option to a list of scores (1-10) for each criterion
        weights: Optional list of weights for each criterion (should sum to 1.0)

    Returns:
        DecisionResult with winner and analysis
    """
    if weights is None:
        weights = [1.0 / len(criteria)] * len(criteria)

    # Calculate weighted scores
    total_scores = {}
    scores_breakdown = {}

    for option in options:
        option_scores = scores[option]
        weighted = {}
        total = 0

        for i, criterion in enumerate(criteria):
            raw = option_scores[i]
            weighted_score = raw * weights[i]
            weighted[criterion] = weighted_score
            total += weighted_score

        scores_breakdown[option] = weighted
        total_scores[option] = total

    # Rank options
    rankings = sorted(total_scores.items(), key=lambda x: x[1], reverse=True)
    winner = rankings[0][0]

    # Calculate confidence (gap between 1st and 2nd)
    if len(rankings) > 1:
        gap = rankings[0][1] - rankings[1][1]
        confidence = min(100, (gap / rankings[0][1]) * 200)
    else:
        confidence = 100

    return DecisionResult(
        winner=winner,
        rankings=rankings,
        scores_breakdown=scores_breakdown,
        total_score=total_scores,
        confidence_score=confidence
    )


def demo_decision_matrix():
    """Demonstrate the Decision Matrix tool for multi-criteria decision making."""
    print_header("DEMO 1: Decision Matrix")

    print("""The Decision Matrix is a powerful tool for making data-driven decisions
by scoring options against multiple weighted criteria.
""")

    print_subheader("Example: Choosing a Programming Language for a New Project")

    # Define the decision
    options = ["Python", "Rust", "Go", "TypeScript"]
    criteria = ["Learning Curve", "Performance", "Ecosystem", "Hiring Pool", "Maintenance"]

    # Scores from 1-10 for each option on each criterion
    scores = {
        "Python":     [9, 5, 10, 9, 8],   # Easy to learn, slower, huge ecosystem
        "Rust":       [4, 10, 6, 5, 9],   # Hard to learn, very fast, smaller ecosystem
        "Go":         [7, 8, 7, 6, 9],    # Moderate learning, fast, good ecosystem
        "TypeScript": [7, 6, 9, 8, 7],    # Moderate, decent perf, great for web
    }

    # Weights: how important is each criterion? (should sum to 1.0)
    weights = [0.15, 0.25, 0.20, 0.20, 0.20]

    print_info("Input Configuration:")
    print(f"  Options: {options}")
    print(f"  Criteria: {criteria}")
    print(f"  Weights: {dict(zip(criteria, weights))}")
    print()

    pause()

    # Make the decision
    result = make_decision(
        options=options,
        criteria=criteria,
        scores=scores,
        weights=weights
    )

    print_success("Decision Matrix Analysis Complete!")
    print(result)

    # Show the code
    print_subheader("Code (when package is installed):")
    print_code("""
from novasystem.core_utils import make_decision

result = make_decision(
    options=["Python", "Rust", "Go", "TypeScript"],
    criteria=["Learning Curve", "Performance", "Ecosystem", "Hiring Pool", "Maintenance"],
    scores={
        "Python":     [9, 5, 10, 9, 8],
        "Rust":       [4, 10, 6, 5, 9],
        "Go":         [7, 8, 7, 6, 9],
        "TypeScript": [7, 6, 9, 8, 7],
    },
    weights=[0.15, 0.25, 0.20, 0.20, 0.20]
)
print(result.winner)  # "Python"
""")

    return True


# =============================================================================
# SELF-CONTAINED TECHNICAL DEBT TRACKER
# =============================================================================

class Severity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Status(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"


@dataclass
class TechnicalDebtItem:
    id: str
    title: str
    severity: Severity
    description: str
    status: Status = Status.OPEN


class TechnicalDebtTracker:
    """Track and manage technical debt in your projects."""

    def __init__(self):
        self.items: List[TechnicalDebtItem] = []
        self._id_counter = 0

    def add_item(self, title: str, severity: Severity, description: str) -> TechnicalDebtItem:
        self._id_counter += 1
        item = TechnicalDebtItem(
            id=f"TD-{self._id_counter:04d}",
            title=title,
            severity=severity,
            description=description
        )
        self.items.append(item)
        return item

    def get_summary(self) -> Dict:
        by_severity = {}
        for item in self.items:
            key = item.severity.name
            by_severity[key] = by_severity.get(key, 0) + 1
        return {
            "total": len(self.items),
            "by_severity": by_severity,
            "open": sum(1 for i in self.items if i.status == Status.OPEN)
        }

    def resolve_item(self, item_id: str, resolution: str):
        for item in self.items:
            if item.id == item_id:
                item.status = Status.RESOLVED
                return item
        return None


def demo_technical_debt():
    """Demonstrate the Technical Debt tracking system."""
    print_header("DEMO 2: Technical Debt Tracker")

    print("""Track and manage technical debt in your projects with structured
severity levels, status tracking, and reporting.
""")

    tracker = TechnicalDebtTracker()

    print_subheader("Adding Technical Debt Items")

    # Add some debt items
    items = [
        ("Refactor authentication module", Severity.HIGH,
         "Current auth is monolithic and hard to test"),
        ("Update deprecated API calls", Severity.MEDIUM,
         "Several endpoints use deprecated v1 API"),
        ("Add comprehensive logging", Severity.LOW,
         "Improve observability for production debugging"),
        ("Database query optimization", Severity.HIGH,
         "N+1 queries in user dashboard"),
    ]

    for title, severity, description in items:
        item = tracker.add_item(title, severity, description)
        print_success(f"Added: [{severity.name}] {title}")

    pause()

    # Show summary
    print_subheader("Debt Summary")
    summary = tracker.get_summary()
    print(f"  Total Items: {summary['total']}")
    print(f"  Open: {summary['open']}")
    print(f"  By Severity:")
    for sev, count in summary.get('by_severity', {}).items():
        color = Colors.RED if sev == 'HIGH' or sev == 'CRITICAL' else Colors.YELLOW if sev == 'MEDIUM' else Colors.GREEN
        print(f"    {color}{sev}: {count}{Colors.RESET}")

    # Resolve one
    print_subheader("Resolving an Item")
    if tracker.items:
        resolved = tracker.resolve_item(tracker.items[0].id, "Implemented new modular auth system")
        print_success(f"Resolved: {tracker.items[0].title}")

    # Show the code
    print_subheader("Code (when package is installed):")
    print_code("""
from novasystem.tools.technical_debt import TechnicalDebtManager, Severity

manager = TechnicalDebtManager("tech_debt.json")

# Add a debt item
manager.add_item(
    title="Refactor authentication module",
    severity=Severity.HIGH,
    description="Current auth is monolithic"
)

# Get summary
summary = manager.get_summary()
print(f"Total debt items: {summary['total']}")
""")

    return True


# =============================================================================
# DEMO 3: DOCUMENTATION PARSER (Conceptual)
# =============================================================================

def demo_doc_parser():
    """Demonstrate the Documentation Parser concept."""
    print_header("DEMO 3: Documentation Parser")

    print("""The Documentation Parser extracts commands and code snippets from
markdown and documentation files for automation.
""")

    # Sample markdown content
    sample_doc = '''
# Project Setup Guide

## Installation

First, clone the repository:

```bash
git clone https://github.com/example/project.git
cd project
```

Then install dependencies:

```bash
pip install -r requirements.txt
npm install
```

## Running Tests

```bash
pytest tests/ -v
npm test
```
'''

    print_subheader("Sample Documentation:")
    print(f"{Colors.DIM}{sample_doc.strip()}{Colors.RESET}")

    pause()

    print_subheader("Extracted Commands:")

    # Simple extraction demo
    import re
    code_blocks = re.findall(r'```(?:bash|shell|sh)?\n(.*?)```', sample_doc, re.DOTALL)

    commands = []
    for block in code_blocks:
        for line in block.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                commands.append(line)

    for cmd in commands:
        print(f"  📋 {Colors.GREEN}{cmd}{Colors.RESET}")

    print()
    print_success(f"Extracted {len(commands)} commands from documentation")

    # Show the code
    print_subheader("Code (when package is installed):")
    print_code("""
from novasystem.tools.parser import DocumentationParser

parser = DocumentationParser()
commands = parser.get_installation_commands(markdown_content)

for cmd in commands:
    print(f"Command: {cmd.command}")
    print(f"Type: {cmd.command_type}")
""")

    return True


# =============================================================================
# DEMO 4: CLI SHOWCASE
# =============================================================================

def demo_cli():
    """Show available CLI commands."""
    print_header("DEMO 4: CLI Commands")

    print("""NovaSystem provides a rich CLI interface for problem-solving.
Here are the main commands available:
""")

    commands = [
        ("novasystem", "Launch the main CLI (alias: nova)"),
        ("novasystem ask 'question'", "Quick Q&A with AI"),
        ("novasystem chat", "Interactive chat session"),
        ("novasystem solve 'problem'", "Full Nova Process problem-solving"),
        ("novasystem models list", "List available AI models"),
        ("novasystem config show", "Show current configuration"),
        ("python -m novasystem", "Launch interactive terminal with animations"),
    ]

    print(f"{'Command':<40} {'Description'}")
    print(f"{'-'*40} {'-'*30}")

    for cmd, desc in commands:
        print(f"{Colors.GREEN}{cmd:<40}{Colors.RESET} {desc}")

    print()
    print_info("To see all options, run: novasystem --help")

    # Check if CLI is available
    print_subheader("Testing CLI Availability")

    try:
        from novasystem import __version__
        print_success(f"NovaSystem version: {__version__}")
        print_success("Package is installed correctly!")
    except ImportError as e:
        print(f"{Colors.YELLOW}⚠ Package not fully installed: {e}{Colors.RESET}")
        print("  Run: pip install -e . to install all dependencies")

    return True


# =============================================================================
# DEMO 5: INTERACTIVE MODE PREVIEW
# =============================================================================

def demo_interactive_preview():
    """Preview the interactive terminal features."""
    print_header("DEMO 5: Interactive Terminal Preview")

    print("""NovaSystem includes a beautiful interactive terminal with:
- ASCII art animations
- Screensaver mode
- Command history
- Session statistics
""")

    # Show a mini ASCII animation
    print_subheader("ASCII Art Preview")

    print(f"""{Colors.CYAN}
   ███╗   ██╗ ██████╗ ██╗   ██╗ █████╗
   ████╗  ██║██╔═══██╗██║   ██║██╔══██╗
   ██╔██╗ ██║██║   ██║██║   ██║███████║
   ██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║
   ██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║
   ╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝
{Colors.RESET}""")

    print(f"{Colors.MAGENTA}  🧠 Multi-Agent Problem Solving System{Colors.RESET}")
    print()

    print_info("Launch interactive mode with: python -m novasystem")
    print_info("Or explicitly: python -m novasystem interactive")

    return True


# =============================================================================
# DEMO 6: API KEYS CHECK
# =============================================================================

def demo_api_check():
    """Check for API keys and show setup instructions."""
    print_header("DEMO 6: API Configuration")

    print("""NovaSystem supports multiple AI providers. Here's your current setup:
""")

    providers = [
        ("ANTHROPIC_API_KEY", "Claude (Anthropic)", "claude-3-sonnet"),
        ("OPENAI_API_KEY", "OpenAI GPT", "gpt-4"),
        ("GOOGLE_API_KEY", "Gemini (Google)", "gemini-2.5-flash"),
    ]

    any_configured = False

    for env_var, provider, model in providers:
        is_set = bool(os.environ.get(env_var))
        status = f"{Colors.GREEN}✓ Configured{Colors.RESET}" if is_set else f"{Colors.DIM}○ Not set{Colors.RESET}"
        print(f"  {status}  {provider} ({model})")
        if is_set:
            any_configured = True

    print()

    if any_configured:
        print_success("You have at least one provider configured!")
        print("  Try: novasystem ask 'What is the meaning of life?'")
    else:
        print(f"{Colors.YELLOW}⚠ No API keys configured{Colors.RESET}")
        print()
        print("To use AI features, set at least one API key:")
        print()
        print(f"  {Colors.CYAN}# For Claude (recommended):{Colors.RESET}")
        print("  export ANTHROPIC_API_KEY='your-key-here'")
        print()
        print(f"  {Colors.CYAN}# For Gemini (free tier available):{Colors.RESET}")
        print("  export GOOGLE_API_KEY='your-key-here'")
        print()
        print(f"  {Colors.CYAN}# Or create a .env file:{Colors.RESET}")
        print("  cp .env.example .env")
        print("  # Then edit .env with your keys")

    return True


# =============================================================================
# MAIN DEMO RUNNER
# =============================================================================

def print_banner():
    """Print the demo banner."""
    banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   {Colors.BOLD}███╗   ██╗ ██████╗ ██╗   ██╗ █████╗ {Colors.RESET}{Colors.CYAN}                                       ║
║   {Colors.BOLD}████╗  ██║██╔═══██╗██║   ██║██╔══██╗{Colors.RESET}{Colors.CYAN}   SYSTEM                              ║
║   {Colors.BOLD}██╔██╗ ██║██║   ██║██║   ██║███████║{Colors.RESET}{Colors.CYAN}                                       ║
║   {Colors.BOLD}██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║{Colors.RESET}{Colors.CYAN}   {Colors.GREEN}Interactive Demo{Colors.CYAN}                      ║
║   {Colors.BOLD}██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║{Colors.RESET}{Colors.CYAN}   v0.3.x                               ║
║   {Colors.BOLD}╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝{Colors.RESET}{Colors.CYAN}                                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)


def main():
    """Run all demos."""
    print_banner()

    print(f"""
{Colors.BOLD}Welcome to the NovaSystem Demo!{Colors.RESET}

This demo showcases the key features of NovaSystem,
a multi-agent problem-solving framework.

{Colors.DIM}Press Ctrl+C at any time to exit.{Colors.RESET}
""")

    pause(1)

    demos = [
        ("Decision Matrix", demo_decision_matrix),
        ("Technical Debt Tracker", demo_technical_debt),
        ("Documentation Parser", demo_doc_parser),
        ("CLI Commands", demo_cli),
        ("Interactive Terminal", demo_interactive_preview),
        ("API Configuration", demo_api_check),
    ]

    results = []

    try:
        for name, demo_func in demos:
            try:
                success = demo_func()
                results.append((name, success))
            except Exception as e:
                print(f"{Colors.RED}✗ Error in {name}: {e}{Colors.RESET}")
                results.append((name, False))

            pause(0.5)

        # Summary
        print_header("Demo Summary")

        passed = sum(1 for _, s in results if s)
        total = len(results)

        print(f"  Demos completed: {passed}/{total}")
        print()

        for name, success in results:
            status = f"{Colors.GREEN}✓{Colors.RESET}" if success else f"{Colors.RED}✗{Colors.RESET}"
            print(f"  {status} {name}")

        print()
        print(f"{Colors.CYAN}{'='*70}{Colors.RESET}")
        print()
        print(f"{Colors.BOLD}Next Steps:{Colors.RESET}")
        print()
        print("  1. Install the package:    pip install -e .")
        print("  2. Set up API keys:        See .env.example")
        print("  3. Try the CLI:            novasystem --help")
        print("  4. Launch interactive:     python -m novasystem")
        print("  5. Read the docs:          See README.md")
        print()
        print(f"{Colors.GREEN}Happy problem-solving! 🧠{Colors.RESET}")
        print()

    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Demo interrupted. Goodbye! 👋{Colors.RESET}\n")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
