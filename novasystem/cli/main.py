#!/usr/bin/env python3
"""
NovaSystem CLI - Professional Multi-Agent Problem Solving Interface

Features:
- Rich terminal output (tables, panels, progress)
- Configuration management (~/.novasystem/config.yaml)
- Shell completion (bash/zsh/fish)
- Multiple verbosity levels (-v, -vv, -vvv)
- Output formats (text, json, markdown)
- Command history and context
- Streaming with live display
"""

import asyncio
import json
import logging
import os
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import typer
from rich import box
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.tree import Tree
from rich.theme import Theme

from dotenv import load_dotenv

# Suppress noisy loggers before any imports
import logging

# Set root to WARNING to suppress most debug noise
logging.basicConfig(level=logging.WARNING)

# Specifically silence verbose libraries
for noisy in ["PIL", "httpcore", "httpx", "gradio", "urllib3", "asyncio", "fsspec"]:
    logging.getLogger(noisy).setLevel(logging.ERROR)

# Load environment
load_dotenv()

# =============================================================================
# CONFIGURATION
# =============================================================================

APP_NAME = "novasystem"
APP_VERSION = "0.3.2"
CONFIG_DIR = Path.home() / ".novasystem"
CONFIG_FILE = CONFIG_DIR / "config.yaml"
HISTORY_FILE = CONFIG_DIR / "history.json"

# Custom theme
NOVA_THEME = Theme({
    "info": "cyan",
    "success": "green",
    "warning": "yellow",
    "error": "red bold",
    "agent.dce": "cyan bold",
    "agent.cae": "yellow bold",
    "agent.domain": "green bold",
    "prompt": "bold magenta",
    "dim": "dim white",
})

# Console instance
console = Console(theme=NOVA_THEME)

# Typer app
app = typer.Typer(
    name=APP_NAME,
    help="🧠 NovaSystem - Multi-Agent Problem Solving CLI",
    add_completion=True,
    rich_markup_mode="rich",
    no_args_is_help=True,
)

# Sub-apps for command groups
models_app = typer.Typer(help="🤖 Model management commands")
config_app = typer.Typer(help="⚙️  Configuration commands")
history_app = typer.Typer(help="📜 History commands")

app.add_typer(models_app, name="models")
app.add_typer(config_app, name="config")
app.add_typer(history_app, name="history")


# =============================================================================
# GLOBAL STATE
# =============================================================================

class AppState:
    """Global application state."""
    def __init__(self):
        self.verbose = 0
        self.quiet = False
        self.output_format = "text"
        self.no_color = False
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load configuration from file."""
        if CONFIG_FILE.exists():
            try:
                import yaml
                with open(CONFIG_FILE) as f:
                    return yaml.safe_load(f) or {}
            except Exception:
                pass
        return {
            "default_model": "gemini-2.5-flash",
            "default_domains": ["Software", "Design"],
            "max_history": 100,
            "streaming": True,
        }

    def get(self, key: str, default=None):
        return self.config.get(key, default)


state = AppState()


# =============================================================================
# UTILITIES
# =============================================================================

def get_logger():
    """Get logger with appropriate level based on verbosity."""
    logger = logging.getLogger("novasystem")
    if state.verbose >= 3:
        logger.setLevel(logging.DEBUG)
    elif state.verbose >= 2:
        logger.setLevel(logging.INFO)
    elif state.verbose >= 1:
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.ERROR)
    return logger


def ensure_config_dir():
    """Ensure config directory exists."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def save_to_history(command: str, input_text: str, output: str):
    """Save command to history."""
    ensure_config_dir()
    history = []

    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE) as f:
                history = json.load(f)
        except Exception:
            pass

    history.append({
        "timestamp": datetime.now().isoformat(),
        "command": command,
        "input": input_text[:500],
        "output": output[:1000] if output else None,
    })

    # Keep only last N entries
    max_history = state.get("max_history", 100)
    history = history[-max_history:]

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def print_banner():
    """Print the NovaSystem banner."""
    if state.quiet:
        return

    banner = """
[cyan]╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   ███╗   ██╗ ██████╗ ██╗   ██╗ █████╗                         ║
║   ████╗  ██║██╔═══██╗██║   ██║██╔══██╗                        ║
║   ██╔██╗ ██║██║   ██║██║   ██║███████║                        ║
║   ██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║                        ║
║   ██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║                        ║
║   ╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝                        ║
║                                                                ║
║   [green]Multi-Agent Problem Solving System[/green]              v0.3.1  ║
╚══════════════════════════════════════════════════════════════╝[/cyan]
"""
    console.print(banner)


def create_status_table(title: str, items: dict) -> Table:
    """Create a status table."""
    table = Table(title=title, box=box.ROUNDED, show_header=False, padding=(0, 1))
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="white")

    for key, value in items.items():
        table.add_row(key, str(value))

    return table


def format_output(data, format_type: str = None) -> str:
    """Format output based on requested format."""
    fmt = format_type or state.output_format

    if fmt == "json":
        return json.dumps(data, indent=2, default=str)
    elif fmt == "markdown":
        if isinstance(data, str):
            return data
        return f"```json\n{json.dumps(data, indent=2, default=str)}\n```"
    else:
        if isinstance(data, str):
            return data
        return str(data)


# =============================================================================
# SERVICE INITIALIZATION
# =============================================================================

def get_llm_service():
    """Get LLM service with lazy loading."""
    from ..utils.llm_service import LLMService
    return LLMService()


def get_memory_manager():
    """Get memory manager with lazy loading."""
    from ..core.memory import MemoryManager
    return MemoryManager()


def get_nova_process(domains: List[str], model: str):
    """Get Nova Process instance."""
    from ..core.process import NovaProcess
    return NovaProcess(
        domains=domains,
        model=model,
        memory_manager=get_memory_manager(),
        llm_service=get_llm_service()
    )


# =============================================================================
# CALLBACKS
# =============================================================================

def version_callback(value: bool):
    """Show version and exit."""
    if value:
        console.print(f"[bold cyan]NovaSystem[/] version [green]{APP_VERSION}[/]")
        raise typer.Exit()


def verbose_callback(value: int):
    """Set verbosity level."""
    state.verbose = value
    return value


# =============================================================================
# MAIN APP COMMANDS
# =============================================================================

@app.callback()
def main_callback(
    verbose: int = typer.Option(0, "--verbose", "-v", count=True,
                                 help="Increase verbosity (-v, -vv, -vvv)"),
    quiet: bool = typer.Option(False, "--quiet", "-q",
                                help="Suppress non-essential output"),
    output: str = typer.Option("text", "--output", "-o",
                                help="Output format: text, json, markdown"),
    no_color: bool = typer.Option(False, "--no-color",
                                   help="Disable colored output"),
    version: bool = typer.Option(False, "--version", "-V",
                                  callback=version_callback, is_eager=True,
                                  help="Show version and exit"),
):
    """
    🧠 NovaSystem - Multi-Agent Problem Solving CLI

    A comprehensive AI-powered problem-solving framework with multiple
    expert agents including DCE (Discussion Continuity Expert),
    CAE (Critical Analysis Expert), and domain specialists.
    """
    state.verbose = verbose
    state.quiet = quiet
    state.output_format = output
    state.no_color = no_color

    if no_color:
        console.no_color = True


@app.command("ask")
def ask_command(
    question: str = typer.Argument(..., help="Question to ask"),
    model: str = typer.Option(None, "--model", "-m", help="Model to use"),
    system: str = typer.Option(None, "--system", "-s", help="System instruction"),
    no_stream: bool = typer.Option(False, "--no-stream", help="Disable streaming"),
    raw: bool = typer.Option(False, "--raw", help="Raw output (no formatting)"),
):
    """
    💬 Ask a quick question with streaming response.

    Example:
        novasystem ask "What is machine learning?"
        novasystem ask "Explain quantum computing" -m gemini-2.5-pro
    """
    try:
        llm = get_llm_service()
        model = model or state.get("default_model", "gemini-2.5-flash")

        # Validate model
        if not llm.is_model_available(model):
            available = llm.get_available_models()
            if available:
                console.print(f"[warning]⚠️  Model '{model}' not available, using {available[0]}[/]")
                model = available[0]
            else:
                console.print("[error]❌ No models available[/]")
                raise typer.Exit(1)

        messages = [
            {"role": "system", "content": system or "Be concise and direct."},
            {"role": "user", "content": question}
        ]

        if not state.quiet:
            console.print(Panel(question, title="📤 Question", border_style="cyan"))
            console.print(f"[dim]Model: {model}[/]\n")

        if no_stream or raw:
            # Non-streaming
            with console.status("[bold cyan]Thinking...[/]"):
                response = asyncio.run(llm.get_completion(messages, model=model))

            if raw:
                print(response)
            else:
                console.print(Panel(Markdown(response), title="📥 Answer", border_style="green"))
        else:
            # Streaming with live display
            response_text = []

            async def stream():
                async for chunk in llm.stream_completion(messages, model=model):
                    response_text.append(chunk)
                    yield chunk

            console.print("[green]📥 Answer:[/]")

            async def run_stream():
                async for chunk in stream():
                    console.print(chunk, end="")

            asyncio.run(run_stream())
            console.print("\n")

            save_to_history("ask", question, "".join(response_text))

    except Exception as e:
        console.print(f"[error]❌ Error: {e}[/]")
        raise typer.Exit(1)


@app.command("chat")
def chat_command(
    model: str = typer.Option(None, "--model", "-m", help="Model to use"),
    system: str = typer.Option(None, "--system", "-s", help="System instruction"),
):
    """
    💭 Start an interactive chat session.

    Commands during chat:
        /help    - Show help
        /clear   - Clear history
        /model   - Change model
        /export  - Export conversation
        /quit    - Exit chat

    Example:
        novasystem chat
        novasystem chat -m gemini-2.5-pro
    """
    print_banner()

    try:
        llm = get_llm_service()
        model = model or state.get("default_model", "gemini-2.5-flash")

        if not llm.is_model_available(model):
            available = llm.get_available_models()
            if available:
                model = available[0]

        console.print(Panel(
            "[bold]Interactive Chat Session[/]\n\n"
            "[dim]Commands: /help, /clear, /model, /export, /quit[/]\n"
            f"[dim]Model: {model}[/]",
            title="💭 Chat",
            border_style="cyan"
        ))

        history = []
        system_msg = system or "You are a helpful AI assistant."

        while True:
            try:
                user_input = Prompt.ask("\n[prompt]You[/]")

                if not user_input:
                    continue

                # Handle commands
                if user_input.startswith("/"):
                    cmd = user_input.lower().split()[0]

                    if cmd in ["/quit", "/exit", "/q"]:
                        console.print("[dim]Goodbye! 👋[/]")
                        break

                    elif cmd == "/clear":
                        history = []
                        console.print("[success]✅ History cleared[/]")
                        continue

                    elif cmd == "/help":
                        help_table = Table(box=box.SIMPLE)
                        help_table.add_column("Command", style="cyan")
                        help_table.add_column("Description")
                        help_table.add_row("/help", "Show this help")
                        help_table.add_row("/clear", "Clear conversation history")
                        help_table.add_row("/model <name>", "Change model")
                        help_table.add_row("/export", "Export conversation to file")
                        help_table.add_row("/quit", "Exit chat")
                        console.print(help_table)
                        continue

                    elif cmd == "/model":
                        parts = user_input.split(maxsplit=1)
                        if len(parts) > 1:
                            new_model = parts[1]
                            if llm.is_model_available(new_model):
                                model = new_model
                                console.print(f"[success]✅ Switched to {model}[/]")
                            else:
                                console.print(f"[error]❌ Model not available[/]")
                        else:
                            console.print(f"[info]Current model: {model}[/]")
                        continue

                    elif cmd == "/export":
                        ensure_config_dir()
                        export_file = CONFIG_DIR / f"chat_{datetime.now():%Y%m%d_%H%M%S}.json"
                        with open(export_file, "w") as f:
                            json.dump({"model": model, "messages": history}, f, indent=2)
                        console.print(f"[success]✅ Exported to {export_file}[/]")
                        continue

                    else:
                        console.print(f"[warning]Unknown command: {cmd}[/]")
                        continue

                # Build messages
                messages = [{"role": "system", "content": system_msg}]
                messages.extend(history)
                messages.append({"role": "user", "content": user_input})

                # Stream response
                console.print("\n[green]Assistant:[/] ", end="")
                response_chunks = []

                async def stream():
                    async for chunk in llm.stream_completion(messages, model=model):
                        console.print(chunk, end="")
                        response_chunks.append(chunk)

                asyncio.run(stream())
                console.print()

                # Update history
                full_response = "".join(response_chunks)
                history.append({"role": "user", "content": user_input})
                history.append({"role": "assistant", "content": full_response})

                # Keep history manageable
                if len(history) > 40:
                    history = history[-40:]

            except KeyboardInterrupt:
                console.print("\n[dim]Use /quit to exit[/]")
                continue

    except Exception as e:
        console.print(f"[error]❌ Error: {e}[/]")
        raise typer.Exit(1)


@app.command("experts")
def experts_command(
    problem: str = typer.Argument(..., help="Problem to analyze"),
    domains: str = typer.Option("Software,Design", "--domains", "-d",
                                 help="Comma-separated domain experts"),
    model: str = typer.Option(None, "--model", "-m", help="Model to use"),
    brief: bool = typer.Option(False, "--brief", "-b", help="Brief output"),
):
    """
    🎭 Run expert panel analysis with DCE, CAE, and domain specialists.

    The expert panel includes:
    • DCE (Discussion Continuity Expert) - Orchestrates analysis
    • Domain Experts - Specialized perspectives
    • CAE (Critical Analysis Expert) - Identifies issues

    Example:
        novasystem experts "Design a REST API"
        novasystem experts "Scale our system" -d "Cloud,Security,DevOps"
    """
    print_banner()

    try:
        from ..core.agents import AgentFactory

        llm = get_llm_service()
        model = model or state.get("default_model", "gemini-2.5-flash")

        if not llm.is_model_available(model):
            available = llm.get_available_models()
            if available:
                model = available[0]

        domain_list = [d.strip() for d in domains.split(",") if d.strip()]

        # Show problem panel
        console.print(Panel(
            f"[bold]{problem}[/]\n\n"
            f"[dim]Model: {model}[/]\n"
            f"[dim]Experts: DCE, CAE, {', '.join(domain_list)}[/]",
            title="🎭 Expert Panel Analysis",
            border_style="cyan"
        ))

        # Create agents
        dce = AgentFactory.create_dce(model=model, llm_service=llm)
        cae = AgentFactory.create_cae(model=model, llm_service=llm)
        domain_experts = [
            AgentFactory.create_domain_expert(d, model=model, llm_service=llm)
            for d in domain_list
        ]

        accumulated_context = f"Problem: {problem}\n\n"

        # Progress through phases
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            console=console,
        ) as progress:

            total_phases = 3 + len(domain_experts)
            task = progress.add_task("Expert Panel", total=total_phases)

            # Phase 1: DCE
            progress.update(task, description="[agent.dce]DCE analyzing...")
            dce_response = asyncio.run(dce.process(
                f"Analyze this problem:\n\n{problem}",
                context=None
            ))
            progress.advance(task)

            console.print(Panel(
                dce_response if brief else Markdown(dce_response),
                title="[agent.dce]📋 DCE Initial Analysis[/]",
                border_style="cyan"
            ))
            accumulated_context += f"DCE Analysis:\n{dce_response}\n\n"

            # Phase 2: Domain Experts
            for expert in domain_experts:
                progress.update(task, description=f"[agent.domain]{expert.name} analyzing...")
                expert_response = asyncio.run(expert.process(
                    f"Provide your specialized perspective:\n\n{problem}",
                    context=accumulated_context
                ))
                progress.advance(task)

                console.print(Panel(
                    expert_response if brief else Markdown(expert_response),
                    title=f"[agent.domain]🎓 {expert.name}[/]",
                    border_style="green"
                ))
                accumulated_context += f"{expert.name}:\n{expert_response}\n\n"

            # Phase 3: CAE
            progress.update(task, description="[agent.cae]CAE reviewing...")
            cae_response = asyncio.run(cae.process(
                "Review all insights and identify issues, risks, or alternatives.",
                context=accumulated_context
            ))
            progress.advance(task)

            console.print(Panel(
                cae_response if brief else Markdown(cae_response),
                title="[agent.cae]⚠️ CAE Critical Analysis[/]",
                border_style="yellow"
            ))
            accumulated_context += f"CAE Analysis:\n{cae_response}\n\n"

            # Phase 4: Synthesis
            progress.update(task, description="[agent.dce]Synthesizing...")
            synthesis = asyncio.run(dce.process(
                "Synthesize all insights into a comprehensive final response.",
                context=accumulated_context
            ))
            progress.advance(task)

        # Final synthesis
        console.print(Panel(
            synthesis if brief else Markdown(synthesis),
            title="[bold green]✨ Final Synthesis[/]",
            border_style="green",
            padding=(1, 2)
        ))

        save_to_history("experts", problem, synthesis)
        console.print("\n[success]✅ Expert Panel Complete![/]")

    except Exception as e:
        console.print(f"[error]❌ Error: {e}[/]")
        raise typer.Exit(1)


@app.command("solve")
def solve_command(
    problem: str = typer.Argument(..., help="Problem to solve"),
    domains: str = typer.Option("General,Technology", "--domains", "-d",
                                 help="Comma-separated domains"),
    iterations: int = typer.Option(3, "--iterations", "-i", help="Max iterations"),
    model: str = typer.Option(None, "--model", "-m", help="Model to use"),
):
    """
    🚀 Run the full Nova Process for complex problem solving.

    The Nova Process uses iterative refinement with multiple agents
    to develop comprehensive solutions.

    Example:
        novasystem solve "How do we scale our API?"
        novasystem solve "Design auth system" -d "Security,Backend" -i 5
    """
    print_banner()

    try:
        model = model or state.get("default_model", "gemini-2.5-flash")
        domain_list = [d.strip() for d in domains.split(",")]

        console.print(Panel(
            f"[bold]{problem}[/]\n\n"
            f"[dim]Model: {model}[/]\n"
            f"[dim]Domains: {', '.join(domain_list)}[/]\n"
            f"[dim]Max Iterations: {iterations}[/]",
            title="🚀 Nova Process",
            border_style="cyan"
        ))

        nova = get_nova_process(domain_list, model)
        session_id = str(uuid.uuid4())[:8]

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TimeElapsedColumn(),
            console=console,
        ) as progress:

            task = progress.add_task("Solving...", total=None)

            async def run():
                result = await nova.solve_problem(
                    problem,
                    max_iterations=iterations,
                    stream=True,
                    session_id=session_id
                )

                if hasattr(result, '__aiter__'):
                    final = None
                    async for update in result:
                        if isinstance(update, dict):
                            if 'iteration' in update:
                                progress.update(task, description=f"Iteration {update['iteration']}...")

                            if 'agent' in update and 'response' in update and state.verbose > 0:
                                console.print(f"\n[dim]{update['agent']}:[/]")
                                console.print(update['response'][:200] + "...")

                            if 'final_synthesis' in update:
                                final = update
                    return final
                return result

            result = asyncio.run(run())

        if result:
            if 'final_synthesis' in result:
                console.print(Panel(
                    Markdown(result['final_synthesis']),
                    title="[bold green]🎯 Solution[/]",
                    border_style="green",
                    padding=(1, 2)
                ))

            save_to_history("solve", problem, result.get('final_synthesis', ''))

        console.print("\n[success]✅ Nova Process Complete![/]")

    except Exception as e:
        console.print(f"[error]❌ Error: {e}[/]")
        raise typer.Exit(1)


@app.command("status")
def status_command():
    """
    📊 Show system status and configuration.

    Displays:
    • Available models and providers
    • API key status
    • Configuration settings
    • Recent activity
    """
    console.print("\n[bold cyan]📊 NovaSystem Status[/]\n")

    try:
        llm = get_llm_service()

        # API Keys status
        api_table = Table(title="🔑 API Keys", box=box.ROUNDED)
        api_table.add_column("Provider", style="cyan")
        api_table.add_column("Status")
        api_table.add_column("Models")

        providers = {
            "OpenAI": os.getenv("OPENAI_API_KEY"),
            "Anthropic": os.getenv("ANTHROPIC_API_KEY"),
            "Gemini": os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"),
            "Ollama": "local",
        }

        for provider, key in providers.items():
            if key == "local":
                status = "[green]✅ Local[/]"
            elif key:
                status = "[green]✅ Configured[/]"
            else:
                status = "[dim]❌ Not set[/]"

            # Count models for this provider
            all_models = llm.get_available_models()
            provider_models = [m for m in all_models if provider.lower() in m.lower()]
            model_count = str(len(provider_models)) if provider_models else "-"

            api_table.add_row(provider, status, model_count)

        console.print(api_table)

        # Configuration
        config_table = Table(title="⚙️ Configuration", box=box.ROUNDED)
        config_table.add_column("Setting", style="cyan")
        config_table.add_column("Value")

        config_table.add_row("Default Model", state.get("default_model", "gemini-2.5-flash"))
        config_table.add_row("Default Domains", ", ".join(state.get("default_domains", ["Software"])))
        config_table.add_row("Streaming", "✅" if state.get("streaming", True) else "❌")
        config_table.add_row("Config Dir", str(CONFIG_DIR))

        console.print(config_table)

        # Models summary
        models = llm.get_available_models()
        console.print(f"\n[info]📦 {len(models)} models available[/]")
        console.print(f"[dim]Run 'novasystem models list' for details[/]")

    except Exception as e:
        console.print(f"[error]❌ Error: {e}[/]")


# =============================================================================
# MODELS SUBCOMMANDS
# =============================================================================

@models_app.command("list")
def models_list(
    detailed: bool = typer.Option(False, "--detailed", "-d", help="Show detailed info"),
    provider: str = typer.Option(None, "--provider", "-p", help="Filter by provider"),
):
    """
    📋 List available models.

    Example:
        novasystem models list
        novasystem models list --detailed
        novasystem models list -p gemini
    """
    try:
        llm = get_llm_service()
        models = llm.get_available_models()

        if provider:
            models = [m for m in models if provider.lower() in m.lower()]

        if not models:
            console.print("[warning]No models found[/]")
            return

        table = Table(title=f"🤖 Available Models ({len(models)})", box=box.ROUNDED)
        table.add_column("#", style="dim", width=3)
        table.add_column("Model", style="cyan")
        table.add_column("Provider", style="green")

        if detailed:
            table.add_column("Context", justify="right")
            table.add_column("Speed", justify="center")

        for i, model in enumerate(models, 1):
            # Determine provider
            if "gemini" in model.lower():
                prov = "Gemini"
            elif "gpt" in model.lower():
                prov = "OpenAI"
            elif "claude" in model.lower():
                prov = "Anthropic"
            elif model.startswith("ollama:"):
                prov = "Ollama"
            else:
                prov = "Other"

            if detailed:
                caps = llm.get_model_capabilities(model)
                ctx = f"{caps.get('context_length', 0):,}"
                speed = "⚡" * min(3, caps.get('speed', 50) // 30)
                table.add_row(str(i), model, prov, ctx, speed)
            else:
                table.add_row(str(i), model, prov)

        console.print(table)

        default = state.get("default_model", "gemini-2.5-flash")
        console.print(f"\n[dim]Default: {default}[/]")

    except Exception as e:
        console.print(f"[error]❌ Error: {e}[/]")


@models_app.command("info")
def models_info(model: str = typer.Argument(..., help="Model name")):
    """
    🔍 Show detailed model information.

    Example:
        novasystem models info gemini-2.5-flash
    """
    try:
        llm = get_llm_service()
        info = llm.get_model_info(model)
        caps = llm.get_model_capabilities(model)

        console.print(Panel(
            f"[bold]{model}[/]\n\n"
            f"[dim]{info}[/]",
            title="🔍 Model Information",
            border_style="cyan"
        ))

        if caps:
            table = Table(title="Capabilities", box=box.SIMPLE)
            table.add_column("Metric", style="cyan")
            table.add_column("Value", justify="right")

            table.add_row("Context Length", f"{caps.get('context_length', 0):,} tokens")
            table.add_row("Reasoning", f"{caps.get('reasoning', 0)}/100")
            table.add_row("Coding", f"{caps.get('coding', 0)}/100")
            table.add_row("Speed", f"{caps.get('speed', 0)}/100")

            console.print(table)

    except Exception as e:
        console.print(f"[error]❌ Error: {e}[/]")


@models_app.command("set-default")
def models_set_default(model: str = typer.Argument(..., help="Model to set as default")):
    """
    ⭐ Set the default model.

    Example:
        novasystem models set-default gemini-2.5-pro
    """
    try:
        llm = get_llm_service()
        if not llm.is_model_available(model):
            console.print(f"[error]❌ Model '{model}' not available[/]")
            raise typer.Exit(1)

        state.config["default_model"] = model

        # Save config
        ensure_config_dir()
        try:
            import yaml
            with open(CONFIG_FILE, "w") as f:
                yaml.dump(state.config, f)
        except ImportError:
            with open(CONFIG_FILE, "w") as f:
                json.dump(state.config, f, indent=2)

        console.print(f"[success]✅ Default model set to {model}[/]")

    except Exception as e:
        console.print(f"[error]❌ Error: {e}[/]")


# =============================================================================
# CONFIG SUBCOMMANDS
# =============================================================================

@config_app.command("show")
def config_show():
    """
    📄 Show current configuration.
    """
    console.print(Panel(
        Syntax(json.dumps(state.config, indent=2), "json"),
        title="⚙️ Configuration",
        border_style="cyan"
    ))
    console.print(f"\n[dim]Config file: {CONFIG_FILE}[/]")


@config_app.command("edit")
def config_edit():
    """
    ✏️ Open configuration in editor.
    """
    ensure_config_dir()

    if not CONFIG_FILE.exists():
        import yaml
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(state.config, f)

    editor = os.environ.get("EDITOR", "nano")
    os.system(f"{editor} {CONFIG_FILE}")
    console.print(f"[success]✅ Config saved[/]")


@config_app.command("reset")
def config_reset():
    """
    🔄 Reset configuration to defaults.
    """
    if Confirm.ask("Reset configuration to defaults?"):
        if CONFIG_FILE.exists():
            CONFIG_FILE.unlink()
        state.config = state._load_config()
        console.print("[success]✅ Configuration reset[/]")


# =============================================================================
# HISTORY SUBCOMMANDS
# =============================================================================

@history_app.command("list")
def history_list(
    limit: int = typer.Option(10, "--limit", "-n", help="Number of entries"),
):
    """
    📜 Show command history.
    """
    if not HISTORY_FILE.exists():
        console.print("[dim]No history yet[/]")
        return

    with open(HISTORY_FILE) as f:
        history = json.load(f)

    if not history:
        console.print("[dim]No history yet[/]")
        return

    table = Table(title=f"📜 Recent Commands ({len(history)} total)", box=box.ROUNDED)
    table.add_column("Time", style="dim", width=16)
    table.add_column("Command", style="cyan", width=10)
    table.add_column("Input", max_width=50)

    for entry in history[-limit:]:
        ts = datetime.fromisoformat(entry["timestamp"]).strftime("%Y-%m-%d %H:%M")
        table.add_row(ts, entry["command"], entry["input"][:50])

    console.print(table)


@history_app.command("clear")
def history_clear():
    """
    🗑️ Clear command history.
    """
    if Confirm.ask("Clear all history?"):
        if HISTORY_FILE.exists():
            HISTORY_FILE.unlink()
        console.print("[success]✅ History cleared[/]")


# =============================================================================
# WIZARD COMMANDS
# =============================================================================

@app.command("sleep")
def sleep_command(
    image: str = typer.Option(None, "--image", "-i", help="Path to wizard image (auto-detected if not specified)"),
    width: int = typer.Option(50, "--width", "-w", help="ASCII width in characters"),
    fps: float = typer.Option(1.5, "--fps", "-f", help="Animation speed"),
    message: str = typer.Option("💤 Wizard sleeping... Press any key to wake", "--message", "-m", help="Message to display"),
):
    """
    🧙 Display sleeping wizard ASCII animation.

    Shows an animated sleeping wizard with typewriter messages.
    Press any key to wake the wizard and exit.

    Example:
        novasystem sleep
        novasystem sleep --width 60 --fps 2.0
    """
    try:
        from ..core import play_sleeping_wizard, ASCII_AVAILABLE

        if not ASCII_AVAILABLE:
            console.print("[error]❌ ASCII animation not available (Pillow not installed)[/]")
            raise typer.Exit(1)

        console.print("[cyan]🧙 Sleeping Wizard Animation[/]")
        console.print("[dim]Press any key to wake the wizard...[/]\n")

        interrupted = play_sleeping_wizard(
            image_path=image,
            width=width,
            fps=fps,
            message=message
        )

        if interrupted:
            console.print("\n[green]✨ The wizard awakens![/]")

    except FileNotFoundError as e:
        console.print(f"[error]❌ Error: {e}[/]")
        console.print("[dim]Generate a wizard with: novasystem wizard generate[/]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[error]❌ Error: {e}[/]")
        raise typer.Exit(1)


wizard_app = typer.Typer(help="🎨 Wizard animation management")
app.add_typer(wizard_app, name="wizard")


@wizard_app.command("generate")
def wizard_generate(
    prompt: str = typer.Option(None, "--prompt", "-p", help="Custom prompt for generation"),
    frames: int = typer.Option(4, "--frames", "-n", help="Number of frames"),
    output: str = typer.Option("wizard_frames", "--output", "-o", help="Output directory"),
):
    """
    🎨 Generate wizard animation frames using PixelLab API.

    Requires PIXELLAB_API_KEY environment variable.

    Example:
        novasystem wizard generate
        novasystem wizard generate --prompt "sleeping dragon" --frames 8
    """
    try:
        from ..core import generate_wizard_animation, PIXELLAB_AVAILABLE
        import os

        if not PIXELLAB_AVAILABLE:
            console.print("[error]❌ PixelLab integration not available (httpx not installed)[/]")
            raise typer.Exit(1)

        api_key = os.getenv("PIXELLAB_API_KEY")
        if not api_key:
            console.print("[error]❌ PIXELLAB_API_KEY not set[/]")
            console.print("[dim]Get your API key at https://pixellab.ai[/]")
            console.print("[dim]Then: export PIXELLAB_API_KEY=your_key[/]")
            raise typer.Exit(1)

        console.print("[cyan]🎨 Generating Wizard with PixelLab API[/]")
        console.print(f"[dim]Prompt: {prompt or 'sleeping wizard (default)'}[/]")
        console.print(f"[dim]Frames: {frames}[/]")
        console.print(f"[dim]Output: {output}[/]\n")

        result = asyncio.run(generate_wizard_animation(
            num_frames=frames,
            output_dir=output,
            prompt=prompt
        ))

        if result.success:
            console.print(f"[green]✓ Generated {result.total_frames} frames[/]")
            for frame in result.frames:
                console.print(f"  [dim]→ {output}/{frame.filename}[/]")
            console.print(f"\n[cyan]View with: novasystem sleep --image {output}/frame_00.png[/]")
        else:
            console.print(f"[error]❌ Error: {result.error}[/]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[error]❌ Error: {e}[/]")
        raise typer.Exit(1)


@wizard_app.command("list")
def wizard_list():
    """
    🖼️  List available wizard images.

    Searches for wizard images in common locations.
    """
    from pathlib import Path

    console.print("\n[cyan]🖼️  Available Wizard Images[/]\n")

    search_dirs = [
        Path.cwd(),
        Path(__file__).parent.parent.parent.parent,  # repo root
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
        console.print("[warning]No wizard images found.[/]")
        console.print("[dim]Generate with: novasystem wizard generate[/]")
    else:
        for p in found[:20]:
            console.print(f"  [dim]→[/] {p}")


# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
