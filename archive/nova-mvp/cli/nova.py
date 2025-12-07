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
    UsageLedger,
    get_llm,
    get_usage_ledger,
    get_memory_store,
    traffic_controller,
    play_sleeping_wizard,
    generate_wizard_animation,
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


def print_agent_header(agent_name: str, agent_type: str, model: str):
    """Print agent header before streaming content."""
    type_colors = {
        "dce": Colors.GREEN,
        "cae": Colors.YELLOW,
    }

    col = Colors.BLUE
    if agent_type in type_colors:
        col = type_colors[agent_type]
    elif "domain" in agent_type:
        col = Colors.CYAN

    print(f"\n{col}{'─' * 60}")
    print(f"  {Colors.BOLD}{agent_name}{Colors.RESET} {Colors.DIM}({model}){Colors.RESET}")
    print(f"{col}{'─' * 60}{Colors.RESET}")
    print("  ", end="", flush=True)


def print_streaming_token(token: str):
    """Print a streaming token in real-time."""
    import sys
    # Handle newlines with proper indentation
    if '\n' in token:
        parts = token.split('\n')
        for i, part in enumerate(parts):
            if i > 0:
                print()  # Newline
                print("  ", end="", flush=True)  # Indent
            sys.stdout.write(part)
            sys.stdout.flush()
    else:
        sys.stdout.write(token)
        sys.stdout.flush()


def _get_ledger(db_path: str | None) -> UsageLedger:
    """Return a usage ledger, optionally pointing at a custom database file."""
    return UsageLedger(db_path) if db_path else get_usage_ledger()


def _format_money(value: float) -> str:
    """Format currency for small spend amounts."""
    return f"${value:,.6f}"


def usage_report(db_path: str | None = None, limit: int = 5) -> int:
    """Print a usage/cost report from the SQLite ledger."""
    print_header()
    limit = max(limit, 1)
    ledger = _get_ledger(db_path)
    db_label = Path(getattr(ledger, "_db_file", db_path or ".nova_usage.db")).resolve()
    total_txn = ledger.count()

    print(f"{Colors.BOLD}Usage Ledger Report{Colors.RESET}")
    print(f"{Colors.DIM}Database: {db_label}{Colors.RESET}")

    if total_txn == 0:
        print(f"\n{Colors.YELLOW}No usage records found yet. Run a solve to generate data.{Colors.RESET}")
        return 0

    summary = ledger.summary()
    by_model = summary.get("by_model", {})
    top_model = max(by_model.items(), key=lambda item: item[1]) if by_model else None
    avg_drift = summary.get("average_drift_pct")

    print(f"\n{Colors.GREEN}Totals{Colors.RESET}")
    print(f"  Spend: {_format_money(summary['total_spend'])}")
    print(f"  Estimated: {_format_money(summary['total_estimated'])}")
    print(f"  Actual: {_format_money(summary['total_actual'])}")
    print(f"  Transactions: {summary['total_transactions']}")

    print(f"\n{Colors.CYAN}Top Model by Spend{Colors.RESET}")
    if top_model:
        model, spend = top_model
        print(f"  {model} → {_format_money(spend)}")
    else:
        print("  No model spend recorded yet.")

    print(f"\n{Colors.CYAN}Average Drift (actual vs. estimate){Colors.RESET}")
    if avg_drift is None:
        print("  N/A (no reconciled usage yet)")
    else:
        drift_color = Colors.GREEN if avg_drift <= 5 else Colors.YELLOW if avg_drift <= 20 else Colors.RED
        print(f"  {drift_color}{avg_drift:+.2f}%{Colors.RESET}")

    print(f"\n{Colors.CYAN}Last {limit} Transactions{Colors.RESET}")
    recent = ledger.recent(limit)
    for txn in recent:
        ts = datetime.fromtimestamp(txn.timestamp).strftime("%Y-%m-%d %H:%M:%S")
        drift = txn.drift_pct
        drift_display = "n/a" if drift is None else f"{drift:+.1f}%"
        actual_display = "n/a" if txn.actual_cost is None else _format_money(txn.actual_cost)
        print(
            f"  {Colors.DIM}{ts}{Colors.RESET} | "
            f"{txn.provider}/{txn.model} | "
            f"est {_format_money(txn.estimated_cost)} | "
            f"act {actual_display} | "
            f"drift {drift_display} | "
            f"{txn.input_tokens}/{txn.output_tokens} tokens | "
            f"context: {txn.context}"
        )

    if total_txn > limit:
        print(f"{Colors.DIM}  …and {total_txn - limit} more rows (use --limit to see more){Colors.RESET}")

    return 0


# =============================================================================
# MEMORY COMMANDS
# =============================================================================


def remember_command(text: str, tags_str: str) -> int:
    """Store a memory."""
    store = get_memory_store()
    tags = [t.strip() for t in tags_str.split(",") if t.strip()] if tags_str else []

    doc_id = store.remember(text, tags=tags)

    print(f"{Colors.GREEN}✓ Memory stored{Colors.RESET}")
    print(f"  ID: {doc_id}")
    print(f"  Text: {text[:60]}{'...' if len(text) > 60 else ''}")
    if tags:
        print(f"  Tags: {', '.join(tags)}")
    print(f"  Total memories: {store.count()}")

    return 0


def recall_command(query: str, limit: int, tags_str: str) -> int:
    """Search memories."""
    store = get_memory_store()
    tags = [t.strip() for t in tags_str.split(",") if t.strip()] if tags_str else None

    results = store.recall(query, limit=limit, tags=tags)

    print(f"{Colors.CYAN}🔍 Searching: \"{query}\"{Colors.RESET}")
    if tags:
        print(f"{Colors.DIM}   Tags filter: {', '.join(tags)}{Colors.RESET}")

    if not results:
        print(f"\n{Colors.YELLOW}No memories found matching your query.{Colors.RESET}")
        print(f"{Colors.DIM}Try different keywords or add memories with 'nova remember'.{Colors.RESET}")
        return 0

    print(f"\n{Colors.GREEN}Found {len(results)} result(s):{Colors.RESET}\n")

    for i, (doc, score) in enumerate(results, 1):
        score_color = Colors.GREEN if score > 0.5 else Colors.YELLOW if score > 0.3 else Colors.DIM
        print(f"{Colors.BOLD}{i}. [{score_color}{score:.2f}{Colors.RESET}{Colors.BOLD}]{Colors.RESET} {doc['text']}")
        if doc.get('tags'):
            print(f"   {Colors.DIM}Tags: {', '.join(doc['tags'])}{Colors.RESET}")
        print()

    return 0


def memory_command(action: str | None) -> int:
    """Memory management commands."""
    store = get_memory_store()

    if action == "list":
        memories = store.list_all(limit=20)
        if not memories:
            print(f"{Colors.YELLOW}No memories stored yet.{Colors.RESET}")
            print(f"{Colors.DIM}Add one with: nova remember \"something important\"{Colors.RESET}")
            return 0

        print(f"{Colors.CYAN}📚 Stored Memories ({store.count()} total){Colors.RESET}\n")
        for mem in memories:
            ts = datetime.fromtimestamp(mem['created_at']).strftime("%Y-%m-%d %H:%M")
            tags_str = f" [{', '.join(mem['tags'])}]" if mem.get('tags') else ""
            print(f"  {Colors.DIM}{ts}{Colors.RESET} {mem['text']}{Colors.CYAN}{tags_str}{Colors.RESET}")

        return 0

    elif action == "stats":
        stats = store.stats()
        print(f"{Colors.CYAN}📊 Memory Statistics{Colors.RESET}\n")
        print(f"  Documents: {stats['count']}")
        print(f"  Avg Length: {stats['avg_length']} chars")
        print(f"  Embedding Dim: {stats['embedder_dim']}")

        if stats.get('tags'):
            print(f"\n  {Colors.BOLD}Top Tags:{Colors.RESET}")
            for tag, count in list(stats['tags'].items())[:10]:
                print(f"    {tag}: {count}")

        return 0

    elif action == "clear":
        count = store.count()
        if count == 0:
            print(f"{Colors.YELLOW}Memory is already empty.{Colors.RESET}")
            return 0

        print(f"{Colors.RED}⚠️  This will delete {count} memories permanently.{Colors.RESET}")
        confirm = input("Type 'yes' to confirm: ")
        if confirm.lower() == 'yes':
            deleted = store.clear()
            print(f"{Colors.GREEN}✓ Cleared {deleted} memories.{Colors.RESET}")
        else:
            print(f"{Colors.DIM}Cancelled.{Colors.RESET}")

        return 0

    else:
        print(f"{Colors.YELLOW}Usage: nova memory <list|stats|clear>{Colors.RESET}")
        return 1


def sleep_command(image: str | None, width: int, fps: float, message: str) -> int:
    """Display the sleeping wizard ASCII animation."""
    print_header()
    print(f"\n{Colors.CYAN}🧙 Sleeping Wizard Animation{Colors.RESET}")
    print(f"{Colors.DIM}Press any key to wake the wizard...{Colors.RESET}\n")

    try:
        interrupted = play_sleeping_wizard(
            image_path=image,
            width=width,
            fps=fps,
            message=message
        )
        if interrupted:
            print(f"\n{Colors.GREEN}✨ The wizard awakens!{Colors.RESET}")
        return 0
    except FileNotFoundError as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        print(f"{Colors.DIM}Generate a wizard with: nova wizard generate{Colors.RESET}")
        return 1
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        return 1


def wizard_command(action: str | None, prompt: str | None, frames: int, output: str) -> int:
    """Wizard animation management."""
    if action == "generate":
        print_header()
        print(f"\n{Colors.CYAN}🎨 Generating Wizard with PixelLab API{Colors.RESET}")

        api_key = os.getenv("PIXELLAB_API_KEY")
        if not api_key:
            print(f"\n{Colors.RED}Error: PIXELLAB_API_KEY not set{Colors.RESET}")
            print(f"{Colors.DIM}Get your API key at https://pixellab.ai{Colors.RESET}")
            print(f"{Colors.DIM}Then: export PIXELLAB_API_KEY=your_key{Colors.RESET}")
            return 1

        print(f"\n{Colors.DIM}Prompt: {prompt or 'sleeping wizard (default)'}")
        print(f"Frames: {frames}")
        print(f"Output: {output}{Colors.RESET}\n")

        result = asyncio.run(generate_wizard_animation(
            num_frames=frames,
            output_dir=output,
            prompt=prompt
        ))

        if result.success:
            print(f"{Colors.GREEN}✓ Generated {result.total_frames} frames{Colors.RESET}")
            for frame in result.frames:
                print(f"  {Colors.DIM}→ {output}/{frame.filename}{Colors.RESET}")
            print(f"\n{Colors.CYAN}View with: nova sleep --image {output}/frame_00.png{Colors.RESET}")
            return 0
        else:
            print(f"{Colors.RED}Error: {result.error}{Colors.RESET}")
            return 1

    elif action == "list":
        print_header()
        print(f"\n{Colors.CYAN}🖼️  Available Wizard Images{Colors.RESET}\n")

        search_dirs = [
            Path.cwd(),
            Path(__file__).parent.parent.parent,
            Path.home() / "wizard_frames",
        ]

        found = []
        for d in search_dirs:
            if d.exists():
                for p in d.glob("*wizard*.png"):
                    found.append(p)
                for p in d.glob("**/frame_*.png"):
                    found.append(p)

        if not found:
            print(f"{Colors.YELLOW}No wizard images found.{Colors.RESET}")
            print(f"{Colors.DIM}Generate with: nova wizard generate{Colors.RESET}")
        else:
            for p in found[:20]:
                print(f"  {Colors.DIM}→{Colors.RESET} {p}")

        return 0

    else:
        print(f"{Colors.YELLOW}Usage: nova wizard <generate|list>{Colors.RESET}")
        return 1


async def solve_command(problem: str, domains: list, provider: str, verbose: bool, stream: bool = False):
    """Execute the solve command."""
    print_header()

    print(f"\n{Colors.BOLD}Problem:{Colors.RESET}")
    print(f"  {problem}")
    print(f"\n{Colors.DIM}Domains: {', '.join(domains)}")
    print(f"Provider: {provider}")
    if stream:
        print(f"Streaming: enabled{Colors.RESET}")
    else:
        print(f"{Colors.RESET}")

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
        if verbose and not stream:
            print_agent_response(response)
        elif not stream:
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

    if stream:
        # Use streaming mode
        try:
            result = None
            async for event in process.solve_streaming(problem, domains):
                if event["type"] == "phase_change":
                    print_phase(event["phase"])
                elif event["type"] == "agent_response":
                    # Print header and stream content
                    print_agent_header(
                        event["agent_name"],
                        event["agent_type"],
                        event["model"]
                    )
                    # The content arrives complete in current implementation
                    # For true token streaming, we'd need to modify solve_streaming
                    content = event.get("content", "")
                    for line in content.split('\n'):
                        print(f"{line}")
                        if line != content.split('\n')[-1]:
                            print("  ", end="")
                    print()  # End the streamed content
                elif event["type"] == "complete":
                    result = type('SessionState', (), event["session"])()
                    result.phase = ProcessPhase(event["session"]["phase"])
                    result.session_id = event["session"]["session_id"]
                    result.execution_time = event["session"]["execution_time"]
                    result.analysis_results = event["session"]["analysis_results"]
                    result.synthesis_result = None
                    if event["session"].get("synthesis_result"):
                        result.synthesis_result = type('AgentResponse', (), event["session"]["synthesis_result"])()

            if result is None:
                print(f"{Colors.RED}No result received from streaming{Colors.RESET}")
                return 1

        except RateLimitExceeded as exc:
            cooldown = int(exc.retry_after) + (1 if exc.retry_after % 1 else 0)
            print(f"{Colors.RED}Rate limit exceeded. Please retry in {cooldown}s{Colors.RESET}")
            return 1
    else:
        # Non-streaming mode
        try:
            result = await process.solve(problem, domains)
        except RateLimitExceeded as exc:
            cooldown = int(exc.retry_after) + (1 if exc.retry_after % 1 else 0)
            print(f"{Colors.RED}Rate limit exceeded. Please retry in {cooldown}s{Colors.RESET}")
            return 1

    # Print final synthesis if not verbose (verbose already shows it)
    if not verbose and not stream and result.synthesis_result:
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
    print("  /provider <name> - Set provider (claude, openai, gemini, mock)")
    print("  /verbose         - Toggle verbose output")
    print("  /stream          - Toggle streaming output")
    print("  /help            - Show this help")
    print("  /quit            - Exit{Colors.RESET}\n")

    domains = ["technology", "business"]
    provider = "auto"
    verbose = True
    stream = True  # Default to streaming in interactive mode

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
                    if arg in ["claude", "openai", "gemini", "mock", "auto"]:
                        provider = arg
                        print(f"{Colors.DIM}Provider set to: {provider}{Colors.RESET}")
                    else:
                        print(f"{Colors.RED}Invalid provider. Use: claude, openai, gemini, mock, auto{Colors.RESET}")
                elif cmd == "/verbose":
                    verbose = not verbose
                    print(f"{Colors.DIM}Verbose: {'on' if verbose else 'off'}{Colors.RESET}")
                elif cmd == "/stream":
                    stream = not stream
                    print(f"{Colors.DIM}Streaming: {'on' if stream else 'off'}{Colors.RESET}")
                elif cmd == "/help":
                    print(f"{Colors.DIM}Commands:")
                    print("  /domains <list>  - Set domains")
                    print("  /provider <name> - Set provider")
                    print("  /verbose         - Toggle verbose")
                    print("  /stream          - Toggle streaming")
                    print(f"  /quit            - Exit{Colors.RESET}")
                else:
                    print(f"{Colors.YELLOW}Unknown command: {cmd}{Colors.RESET}")
                continue

            # Solve the problem
            await solve_command(user_input, domains, provider, verbose, stream)
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
  nova solve "What's our go-to-market strategy?" --domains business,ux --stream
  nova solve "Explain quantum computing" --provider gemini --stream
  nova interactive

Environment variables:
  ANTHROPIC_API_KEY - For Claude provider
  OPENAI_API_KEY    - For OpenAI provider
  GEMINI_API_KEY    - For Gemini provider
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
        choices=["claude", "openai", "gemini", "mock", "auto"],
        default="auto",
        help="LLM provider (default: auto)"
    )
    solve_parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show full agent responses"
    )
    solve_parser.add_argument(
        "--stream", "-s",
        action="store_true",
        help="Stream responses in real-time as they are generated"
    )

    # Interactive command
    subparsers.add_parser("interactive", help="Start interactive mode")

    # Usage report command
    report_parser = subparsers.add_parser("report", help="Show usage/cost report from the ledger")
    report_parser.add_argument(
        "--db",
        help="Path to a usage database (default: .nova_usage.db in current working directory)"
    )
    report_parser.add_argument(
        "--limit", "-n",
        type=int,
        default=5,
        help="Number of recent transactions to display (default: 5)"
    )

    # Memory commands
    remember_parser = subparsers.add_parser("remember", help="Store a memory")
    remember_parser.add_argument("text", help="The text to remember")
    remember_parser.add_argument(
        "--tags", "-t",
        default="",
        help="Comma-separated tags (e.g., python,api,tips)"
    )

    recall_parser = subparsers.add_parser("recall", help="Search memories")
    recall_parser.add_argument("query", help="Search query")
    recall_parser.add_argument(
        "--limit", "-n",
        type=int,
        default=5,
        help="Maximum results (default: 5)"
    )
    recall_parser.add_argument(
        "--tags", "-t",
        default="",
        help="Filter by tags (comma-separated)"
    )

    memory_parser = subparsers.add_parser("memory", help="Memory management")
    memory_sub = memory_parser.add_subparsers(dest="memory_action")
    memory_sub.add_parser("list", help="List all memories")
    memory_sub.add_parser("stats", help="Show memory statistics")
    memory_sub.add_parser("clear", help="Clear all memories")

    # Sleep command (ASCII wizard animation)
    sleep_parser = subparsers.add_parser("sleep", help="Display sleeping wizard animation")
    sleep_parser.add_argument(
        "--image", "-i",
        help="Path to wizard image (auto-detected if not specified)"
    )
    sleep_parser.add_argument(
        "--width", "-w",
        type=int,
        default=50,
        help="ASCII width in characters (default: 50)"
    )
    sleep_parser.add_argument(
        "--fps", "-f",
        type=float,
        default=1.5,
        help="Animation speed (default: 1.5)"
    )
    sleep_parser.add_argument(
        "--message", "-m",
        default="💤 Wizard sleeping... Press any key to wake",
        help="Message to display"
    )

    # Wizard command (PixelLab integration)
    wizard_parser = subparsers.add_parser("wizard", help="Wizard animation management")
    wizard_sub = wizard_parser.add_subparsers(dest="wizard_action")

    wizard_gen = wizard_sub.add_parser("generate", help="Generate wizard with PixelLab API")
    wizard_gen.add_argument(
        "--prompt", "-p",
        help="Custom prompt for generation"
    )
    wizard_gen.add_argument(
        "--frames", "-n",
        type=int,
        default=4,
        help="Number of frames (default: 4)"
    )
    wizard_gen.add_argument(
        "--output", "-o",
        default="wizard_frames",
        help="Output directory (default: wizard_frames)"
    )

    wizard_sub.add_parser("list", help="List available wizard images")

    # Parse args
    args = parser.parse_args()

    if args.command == "solve":
        domains = [d.strip() for d in args.domains.split(",")]
        return asyncio.run(solve_command(
            args.problem,
            domains,
            args.provider,
            args.verbose,
            args.stream
        ))
    elif args.command == "interactive":
        return asyncio.run(interactive_mode())
    elif args.command == "report":
        return usage_report(args.db, args.limit)
    elif args.command == "remember":
        return remember_command(args.text, args.tags)
    elif args.command == "recall":
        return recall_command(args.query, args.limit, args.tags)
    elif args.command == "memory":
        return memory_command(args.memory_action)
    elif args.command == "sleep":
        return sleep_command(args.image, args.width, args.fps, args.message)
    elif args.command == "wizard":
        return wizard_command(
            args.wizard_action,
            getattr(args, 'prompt', None),
            getattr(args, 'frames', 4),
            getattr(args, 'output', 'wizard_frames')
        )
    else:
        print_header()
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
