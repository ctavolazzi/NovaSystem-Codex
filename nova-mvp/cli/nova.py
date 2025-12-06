#!/usr/bin/env python3
"""Nova MVP CLI - Command-line interface for multi-agent problem solving.

Usage:
    nova solve "How do we scale our API?" --domains tech,security
    nova interactive
    nova --help
"""

import argparse
import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

# Load environment variables from .env files
# Priority: local .env > root .env > system environment
try:
    from dotenv import load_dotenv

    # Get paths
    cli_dir = Path(__file__).parent
    nova_mvp_dir = cli_dir.parent
    root_dir = nova_mvp_dir.parent

    # Load root .env first (lower priority)
    root_env = root_dir / ".env"
    if root_env.exists():
        load_dotenv(root_env)

    # Load local .env second (higher priority, overrides root)
    local_env = nova_mvp_dir / ".env"
    if local_env.exists():
        load_dotenv(local_env, override=True)

except ImportError:
    pass  # dotenv not installed, rely on system environment

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.core import (
    CostEstimator,
    NovaProcess,
    ProcessPhase,
    RateLimitExceeded,
    get_llm,
    traffic_controller,
)
from backend.agents.base import AgentResponse


# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'


def color(text: str, code: str) -> str:
    """Apply color code to text."""
    return f"{code}{text}{Colors.RESET}"


def print_header():
    """Print the Nova ASCII header."""
    header = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   ███╗   ██╗ ██████╗ ██╗   ██╗ █████╗     ███╗   ███╗██╗   ██╗ ║
║   ████╗  ██║██╔═══██╗██║   ██║██╔══██╗    ████╗ ████║██║   ██║ ║
║   ██╔██╗ ██║██║   ██║██║   ██║███████║    ██╔████╔██║██║   ██║ ║
║   ██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║    ██║╚██╔╝██║╚██╗ ██╔╝ ║
║   ██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║    ██║ ╚═╝ ██║ ╚████╔╝  ║
║   ╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═══╝   ║
║                                                                ║
║   {Colors.GREEN}Multi-Agent Problem Solving System{Colors.CYAN}               v0.1.0  ║
╚══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(header)


def print_phase(phase: str):
    """Print phase transition."""
    phase_display = {
        "pending": ("◯", Colors.DIM),
        "unpacking": ("⟳", Colors.YELLOW),
        "analyzing": ("⟳", Colors.BLUE),
        "synthesizing": ("⟳", Colors.CYAN),
        "completed": ("✓", Colors.GREEN),
        "error": ("✗", Colors.RED)
    }
    icon, col = phase_display.get(phase, ("?", Colors.RESET))
    print(f"\n{col}{icon} Phase: {phase.upper()}{Colors.RESET}")


def print_agent_response(response: AgentResponse):
    """Print an agent's response with formatting."""
    # Agent type colors
    type_colors = {
        "dce": Colors.GREEN,
        "cae": Colors.YELLOW,
    }

    col = Colors.BLUE  # Default for domain experts
    if response.agent_type in type_colors:
        col = type_colors[response.agent_type]
    elif "domain" in response.agent_type:
        col = Colors.CYAN

    print(f"\n{col}{'─' * 60}")
    print(f"  {Colors.BOLD}{response.agent_name}{Colors.RESET} {Colors.DIM}({response.model}){Colors.RESET}")
    print(f"{col}{'─' * 60}{Colors.RESET}")

    if response.success:
        # Print content with proper indentation
        for line in response.content.split('\n'):
            print(f"  {line}")
    else:
        print(f"  {Colors.RED}Error: {response.error}{Colors.RESET}")


async def solve_command(problem: str, domains: list, provider: str, verbose: bool):
    """Execute the solve command."""
    print_header()

    print(f"\n{Colors.BOLD}Problem:{Colors.RESET}")
    print(f"  {problem}")
    print(f"\n{Colors.DIM}Domains: {', '.join(domains)}")
    print(f"Provider: {provider}{Colors.RESET}")

    # Get LLM provider
    llm = get_llm(provider)
    if not llm.is_available() and provider != "mock":
        print(f"\n{Colors.YELLOW}⚠ Provider '{provider}' not available (no API key)")
        print(f"  Falling back to mock provider{Colors.RESET}")
        llm = get_llm("mock")

    # Pre-flight checks
    estimator = CostEstimator()
    model_name = llm.get_model_name()
    estimated_output_tokens = 1000

    try:
        cost_estimate = estimator.estimate(
            model_name, problem, estimated_output_tokens=estimated_output_tokens
        )
        total_tokens = cost_estimate.input_tokens + estimated_output_tokens
        print(
            f"\n💰 Est. Cost: ${cost_estimate.projected_cost:.4f} | "
            f"Tokens: {total_tokens}"
        )
    except ValueError as exc:
        print(f"\n{Colors.YELLOW}⚠ {exc}{Colors.RESET}")
        cost_estimate = None

    input_tokens = (
        cost_estimate.input_tokens if cost_estimate else estimator._estimate_tokens(problem)
    )

    try:
        traffic_controller.check_allowance(
            model_name,
            input_tokens,
            estimated_output_tokens=estimated_output_tokens,
            commit=False,
        )
    except RateLimitExceeded as exc:
        cooldown = int(exc.retry_after) + (1 if exc.retry_after % 1 else 0)
        print(f"{Colors.YELLOW}⏳ Rate Limit Reached. Cooldown: {cooldown}s...{Colors.RESET}")
        return 1

    # Create callbacks for progress display
    def on_phase_change(state):
        print_phase(state.phase.value)

    def on_agent_response(response):
        if verbose:
            print_agent_response(response)
        else:
            status = "✓" if response.success else "✗"
            col = Colors.GREEN if response.success else Colors.RED
            print(f"  {col}{status}{Colors.RESET} {response.agent_name} {Colors.DIM}({response.model}){Colors.RESET}")

    # Run the process
    process = NovaProcess(
        llm_provider=llm,
        on_phase_change=on_phase_change,
        on_agent_response=on_agent_response
    )

    print(f"\n{Colors.DIM}Starting Nova process...{Colors.RESET}")
    try:
        result = await process.solve(problem, domains)
    except RateLimitExceeded as exc:
        cooldown = int(exc.retry_after) + (1 if exc.retry_after % 1 else 0)
        print(f"{Colors.RED}Rate limit exceeded. Please retry in {cooldown}s{Colors.RESET}")
        return 1

    # Print final synthesis if not verbose (verbose already shows it)
    if not verbose and result.synthesis_result:
        print(f"\n{Colors.GREEN}{'═' * 60}")
        print(f"  {Colors.BOLD}SYNTHESIS{Colors.RESET}")
        print(f"{Colors.GREEN}{'═' * 60}{Colors.RESET}")
        for line in result.synthesis_result.content.split('\n'):
            print(f"  {line}")

    # Print summary
    print(f"\n{Colors.DIM}{'─' * 60}")
    print(f"Session: {result.session_id}")
    print(f"Time: {result.execution_time:.2f}s")
    print(f"Agents: {len(result.analysis_results) + 2}")  # +2 for DCE (unpack + synth)
    status = "SUCCESS" if result.phase == ProcessPhase.COMPLETED else "ERROR"
    col = Colors.GREEN if result.phase == ProcessPhase.COMPLETED else Colors.RED
    print(f"Status: {col}{status}{Colors.RESET}")
    print(f"{'─' * 60}{Colors.RESET}")

    return 0 if result.phase == ProcessPhase.COMPLETED else 1


async def interactive_mode():
    """Run interactive mode."""
    print_header()
    print(f"\n{Colors.CYAN}Interactive Mode{Colors.RESET}")
    print(f"{Colors.DIM}Type your problem and press Enter. Commands:")
    print("  /domains <list>  - Set domains (e.g., /domains tech,security)")
    print("  /provider <name> - Set provider (claude, openai, mock)")
    print("  /verbose         - Toggle verbose output")
    print("  /help            - Show this help")
    print("  /quit            - Exit{Colors.RESET}\n")

    domains = ["technology", "business"]
    provider = "auto"
    verbose = True

    while True:
        try:
            # Prompt
            prompt = f"{Colors.GREEN}nova>{Colors.RESET} "
            user_input = input(prompt).strip()

            if not user_input:
                continue

            # Commands
            if user_input.startswith("/"):
                parts = user_input.split(maxsplit=1)
                cmd = parts[0].lower()
                arg = parts[1] if len(parts) > 1 else ""

                if cmd == "/quit" or cmd == "/exit":
                    print(f"{Colors.DIM}Goodbye!{Colors.RESET}")
                    break
                elif cmd == "/domains":
                    if arg:
                        domains = [d.strip() for d in arg.split(",")]
                        print(f"{Colors.DIM}Domains set to: {', '.join(domains)}{Colors.RESET}")
                    else:
                        print(f"{Colors.DIM}Current domains: {', '.join(domains)}{Colors.RESET}")
                elif cmd == "/provider":
                    if arg in ["claude", "openai", "mock", "auto"]:
                        provider = arg
                        print(f"{Colors.DIM}Provider set to: {provider}{Colors.RESET}")
                    else:
                        print(f"{Colors.RED}Invalid provider. Use: claude, openai, mock, auto{Colors.RESET}")
                elif cmd == "/verbose":
                    verbose = not verbose
                    print(f"{Colors.DIM}Verbose: {'on' if verbose else 'off'}{Colors.RESET}")
                elif cmd == "/help":
                    print(f"{Colors.DIM}Commands:")
                    print("  /domains <list>  - Set domains")
                    print("  /provider <name> - Set provider")
                    print("  /verbose         - Toggle verbose")
                    print(f"  /quit            - Exit{Colors.RESET}")
                else:
                    print(f"{Colors.YELLOW}Unknown command: {cmd}{Colors.RESET}")
                continue

            # Solve the problem
            await solve_command(user_input, domains, provider, verbose)
            print()  # Extra newline after result

        except KeyboardInterrupt:
            print(f"\n{Colors.DIM}Use /quit to exit{Colors.RESET}")
        except EOFError:
            print(f"\n{Colors.DIM}Goodbye!{Colors.RESET}")
            break


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Nova MVP - Multi-Agent Problem Solving CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  nova solve "How do we scale our API?" --domains tech,security
  nova solve "What's our go-to-market strategy?" --domains business,ux
  nova interactive

Environment variables:
  ANTHROPIC_API_KEY - For Claude provider
  OPENAI_API_KEY    - For OpenAI provider
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command")

    # Solve command
    solve_parser = subparsers.add_parser("solve", help="Solve a problem")
    solve_parser.add_argument("problem", help="The problem to solve")
    solve_parser.add_argument(
        "--domains", "-d",
        default="technology,business",
        help="Comma-separated list of domains (default: technology,business)"
    )
    solve_parser.add_argument(
        "--provider", "-p",
        choices=["claude", "openai", "mock", "auto"],
        default="auto",
        help="LLM provider (default: auto)"
    )
    solve_parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show full agent responses"
    )

    # Interactive command
    subparsers.add_parser("interactive", help="Start interactive mode")

    # Parse args
    args = parser.parse_args()

    if args.command == "solve":
        domains = [d.strip() for d in args.domains.split(",")]
        return asyncio.run(solve_command(
            args.problem,
            domains,
            args.provider,
            args.verbose
        ))
    elif args.command == "interactive":
        return asyncio.run(interactive_mode())
    else:
        print_header()
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
