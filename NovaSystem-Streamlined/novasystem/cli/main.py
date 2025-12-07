"""
Command Line Interface for NovaSystem.

This module provides a comprehensive CLI for interacting with the Nova Process
and all NovaSystem services.

Consolidated from:
- NovaSystem-Streamlined CLI
- nova-mvp CLI (memory, usage tracking)
- novasystem root CLI (utilities)
"""

import argparse
import asyncio
import sys
import json
import logging
import uuid
import os
from typing import List, Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from ..core.process import NovaProcess
from ..core.memory import MemoryManager
from ..core.agents import AgentFactory
from ..utils.llm_service import LLMService
from ..utils.metrics import get_metrics_collector
from ..utils.model_cache import get_model_cache

logger = logging.getLogger(__name__)


# =============================================================================
# TERMINAL COLORS AND FORMATTING
# =============================================================================

class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'


def color(text: str, code: str) -> str:
    """Apply color code to text."""
    return f"{code}{text}{Colors.END}"


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def print_banner():
    """Print the NovaSystem ASCII banner."""
    banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   ███╗   ██╗ ██████╗ ██╗   ██╗ █████╗                         ║
║   ████╗  ██║██╔═══██╗██║   ██║██╔══██╗                        ║
║   ██╔██╗ ██║██║   ██║██║   ██║███████║                        ║
║   ██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║                        ║
║   ██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║                        ║
║   ╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝                        ║
║                                                                ║
║   {Colors.GREEN}Multi-Agent Problem Solving System{Colors.CYAN}                v2.0  ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}
"""
    print(banner)


def print_mini_banner():
    """Print a compact banner for quick commands."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}🧠 NovaSystem{Colors.END}\n")


# =============================================================================
# RESULT FORMATTING
# =============================================================================

def format_result(result: dict) -> str:
    """Format the Nova Process result for CLI display."""
    if not result:
        return "No result available."

    formatted = []
    formatted.append(f"\n{Colors.BOLD}🚀 Nova Process Results{Colors.END}")
    formatted.append("=" * 50)

    if "final_synthesis" in result:
        formatted.append(f"\n{Colors.GREEN}📋 Final Synthesis:{Colors.END}")
        formatted.append("-" * 20)
        formatted.append(result["final_synthesis"])

    if "final_validation" in result:
        formatted.append(f"\n{Colors.YELLOW}✅ Final Validation:{Colors.END}")
        formatted.append("-" * 20)
        formatted.append(result["final_validation"])

    if "total_iterations" in result:
        formatted.append(f"\n{Colors.CYAN}📊 Process Summary:{Colors.END}")
        formatted.append("-" * 20)
        formatted.append(f"Total Iterations: {result['total_iterations']}")
        formatted.append(f"Process Phase: {result.get('phase', 'Unknown')}")

    return "\n".join(formatted)


# =============================================================================
# ASK COMMAND - Quick single question
# =============================================================================

def ask_command(args):
    """Handle the ask command - quick single question with streaming."""
    print_mini_banner()

    try:
        llm_service = LLMService()
        model = args.model

        # Validate model
        if not llm_service.is_model_available(model):
            available = llm_service.get_available_models()
            if available:
                model = available[0]
                print(f"{Colors.YELLOW}⚠️  Using {model} (requested model not available){Colors.END}")
            else:
                print(f"{Colors.RED}❌ No models available{Colors.END}")
                return 1

        messages = [
            {"role": "system", "content": args.system or "You are a helpful assistant. Be concise and direct."},
            {"role": "user", "content": args.question}
        ]

        print(f"{Colors.CYAN}📤 Question:{Colors.END} {args.question}")
        print(f"{Colors.DIM}🤖 Model: {model}{Colors.END}\n")

        if args.stream:
            print(f"{Colors.GREEN}📥 Answer:{Colors.END} ", end="", flush=True)

            async def stream_response():
                async for chunk in llm_service.stream_completion(messages, model=model):
                    print(chunk, end="", flush=True)

            asyncio.run(stream_response())
            print("\n")
        else:
            response = asyncio.run(llm_service.get_completion(messages, model=model))
            print(f"{Colors.GREEN}📥 Answer:{Colors.END}\n{response}\n")

        return 0

    except Exception as e:
        print(f"{Colors.RED}❌ Error: {str(e)}{Colors.END}")
        return 1


# =============================================================================
# CHAT COMMAND - Interactive streaming chat
# =============================================================================

def chat_command(args):
    """Handle the chat command - interactive streaming conversation."""
    print_banner()
    print(f"{Colors.BOLD}💬 Interactive Chat{Colors.END}")
    print(f"{Colors.DIM}Type 'quit' to exit, 'clear' to reset, 'help' for commands{Colors.END}")
    print(f"{Colors.DIM}Model: {args.model}{Colors.END}\n")

    try:
        llm_service = LLMService()
        model = args.model

        # Validate model
        if not llm_service.is_model_available(model):
            available = llm_service.get_available_models()
            if available:
                model = available[0]
                print(f"{Colors.YELLOW}⚠️  Using {model}{Colors.END}\n")
            else:
                print(f"{Colors.RED}❌ No models available{Colors.END}")
                return 1

        history = []
        system_msg = args.system or "You are a helpful AI assistant. Be conversational and helpful."

        while True:
            try:
                user_input = input(f"\n{Colors.CYAN}You:{Colors.END} ").strip()

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print(f"\n{Colors.BOLD}Goodbye! 👋{Colors.END}")
                    break

                if user_input.lower() == 'clear':
                    history = []
                    print(f"{Colors.YELLOW}✅ Chat history cleared{Colors.END}")
                    continue

                if user_input.lower() == 'help':
                    print(f"{Colors.DIM}Commands:")
                    print("  quit/exit/q - Exit chat")
                    print("  clear - Clear history")
                    print(f"  help - Show this help{Colors.END}")
                    continue

                if not user_input:
                    continue

                # Build messages
                messages = [{"role": "system", "content": system_msg}]
                messages.extend(history)
                messages.append({"role": "user", "content": user_input})

                # Stream response
                print(f"\n{Colors.GREEN}Assistant:{Colors.END} ", end="", flush=True)
                response_chunks = []

                async def stream():
                    async for chunk in llm_service.stream_completion(messages, model=model):
                        print(chunk, end="", flush=True)
                        response_chunks.append(chunk)

                asyncio.run(stream())
                print()

                # Update history
                full_response = "".join(response_chunks)
                history.append({"role": "user", "content": user_input})
                history.append({"role": "assistant", "content": full_response})

                # Keep history manageable
                if len(history) > 20:
                    history = history[-20:]

            except KeyboardInterrupt:
                print(f"\n\n{Colors.BOLD}Goodbye! 👋{Colors.END}")
                break

        return 0

    except Exception as e:
        print(f"{Colors.RED}❌ Error: {str(e)}{Colors.END}")
        return 1


# =============================================================================
# EXPERTS COMMAND - Expert panel analysis
# =============================================================================

def experts_command(args):
    """Handle the experts command - run expert panel analysis."""
    print_banner()
    print(f"{Colors.BOLD}🎭 Expert Panel Analysis{Colors.END}\n")

    try:
        llm_service = LLMService()
        model = args.model

        # Validate model
        if not llm_service.is_model_available(model):
            available = llm_service.get_available_models()
            if available:
                model = available[0]
                print(f"{Colors.YELLOW}⚠️  Using {model}{Colors.END}\n")
            else:
                print(f"{Colors.RED}❌ No models available{Colors.END}")
                return 1

        # Parse domains
        domains = [d.strip() for d in args.domains.split(",") if d.strip()]

        print(f"📋 Problem: {args.problem}")
        print(f"🤖 Model: {model}")
        print(f"🎓 Experts: DCE, CAE, {', '.join(domains)}")
        print("\n" + "="*60)

        # Create agents
        dce = AgentFactory.create_dce(model=model, llm_service=llm_service)
        cae = AgentFactory.create_cae(model=model, llm_service=llm_service)
        domain_experts = [
            AgentFactory.create_domain_expert(domain, model=model, llm_service=llm_service)
            for domain in domains
        ]

        accumulated_context = f"Problem: {args.problem}\n\n"

        # Phase 1: DCE Initial Analysis
        print(f"\n{Colors.CYAN}{Colors.BOLD}📋 Phase 1: DCE Initial Analysis{Colors.END}")
        print("-" * 40)

        dce_response = asyncio.run(dce.process(
            f"Analyze this problem and provide an initial assessment:\n\n{args.problem}",
            context=None
        ))
        print(dce_response)
        accumulated_context += f"DCE Analysis:\n{dce_response}\n\n"

        # Phase 2: Domain Experts
        for expert in domain_experts:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎓 {expert.name}{Colors.END}")
            print("-" * 40)

            expert_response = asyncio.run(expert.process(
                f"Provide your specialized perspective:\n\n{args.problem}",
                context=accumulated_context
            ))
            print(expert_response)
            accumulated_context += f"{expert.name}:\n{expert_response}\n\n"

        # Phase 3: CAE Critical Analysis
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️ Phase 3: CAE Critical Analysis{Colors.END}")
        print("-" * 40)

        cae_response = asyncio.run(cae.process(
            "Review all insights and identify potential issues, risks, or alternatives.",
            context=accumulated_context
        ))
        print(cae_response)
        accumulated_context += f"CAE Analysis:\n{cae_response}\n\n"

        # Phase 4: Synthesis
        print(f"\n{Colors.CYAN}{Colors.BOLD}✨ Phase 4: Final Synthesis{Colors.END}")
        print("-" * 40)

        synthesis = asyncio.run(dce.process(
            "Synthesize all insights into a comprehensive final response.",
            context=accumulated_context
        ))
        print(synthesis)

        print("\n" + "="*60)
        print(f"{Colors.BOLD}✅ Expert Panel Complete!{Colors.END}\n")

        return 0

    except Exception as e:
        print(f"{Colors.RED}❌ Error: {str(e)}{Colors.END}")
        return 1


# =============================================================================
# SOLVE COMMAND - Full Nova Process
# =============================================================================

async def run_nova_process(problem: str, domains: List[str], max_iterations: int,
                           model: str, output_format: str, verbose: bool) -> dict:
    """Run the Nova Process."""
    try:
        memory_manager = MemoryManager()
        llm_service = LLMService()

        nova_process = NovaProcess(
            domains=domains,
            model=model,
            memory_manager=memory_manager,
            llm_service=llm_service
        )

        session_id = str(uuid.uuid4())

        if verbose:
            print(f"{Colors.DIM}Session: {session_id}")
            print(f"Domains: {', '.join(domains)}")
            print(f"Model: {model}")
            print(f"Max iterations: {max_iterations}{Colors.END}")
            print()

        print(f"{Colors.BOLD}🚀 Starting Nova Process...{Colors.END}")
        print(f"📋 Problem: {problem[:100]}{'...' if len(problem) > 100 else ''}")
        print("\n" + "="*60)

        result = await nova_process.solve_problem(
            problem,
            max_iterations=max_iterations,
            stream=verbose,
            session_id=session_id
        )

        # Handle streaming results
        if hasattr(result, '__aiter__'):
            final_result = None

            async for update in result:
                if isinstance(update, dict):
                    if 'iteration' in update:
                        print(f"\n{Colors.CYAN}🔄 Iteration {update['iteration']}{Colors.END}")
                        print("-" * 40)

                    if 'agent' in update and 'response' in update:
                        agent_name = update['agent']
                        response = update['response']
                        print(f"\n{Colors.GREEN}🤖 {agent_name}:{Colors.END}")
                        print(f"{response}\n")

                    if 'final_synthesis' in update:
                        print("\n" + "="*60)
                        print(f"{Colors.BOLD}🎯 FINAL SYNTHESIS{Colors.END}")
                        print("="*60)
                        print(update['final_synthesis'])
                        final_result = update

            return final_result or {}
        else:
            return result

    except Exception as e:
        logger.error(f"Error in Nova Process: {str(e)}")
        raise


def solve_command(args):
    """Handle the solve command - full Nova Process."""
    print_banner()

    domains = [d.strip() for d in args.domains.split(",") if d.strip()]

    try:
        result = asyncio.run(run_nova_process(
            problem=args.problem,
            domains=domains,
            max_iterations=args.max_iterations,
            model=args.model,
            output_format=args.output,
            verbose=args.verbose
        ))

        if args.output == "json":
            print(json.dumps(result, indent=2))
        else:
            print(format_result(result))

        return 0

    except Exception as e:
        print(f"{Colors.RED}Error: {str(e)}{Colors.END}")
        return 1


# =============================================================================
# INTERACTIVE MODE
# =============================================================================

def interactive_command(args):
    """Handle the interactive command."""
    print_banner()
    print(f"{Colors.BOLD}🧠 Interactive Mode{Colors.END}")
    print(f"{Colors.DIM}Type 'quit' to exit, 'help' for commands{Colors.END}")
    print()

    memory_manager = MemoryManager()
    llm_service = LLMService()

    nova_process = NovaProcess(
        domains=args.domains.split(",") if args.domains else ["General"],
        model=args.model,
        memory_manager=memory_manager,
        llm_service=llm_service
    )

    while True:
        try:
            problem = input(f"{Colors.GREEN}nova>{Colors.END} ").strip()

            if problem.lower() in ['quit', 'exit', 'q']:
                print(f"{Colors.BOLD}Goodbye! 👋{Colors.END}")
                break

            if problem.lower() == 'help':
                print(f"{Colors.DIM}Commands:")
                print("  help - Show this help")
                print("  quit/exit/q - Exit")
                print("  status - Process status")
                print(f"  history - Solution history{Colors.END}")
                continue

            if problem.lower() == 'status':
                status = nova_process.get_status()
                print(json.dumps(status, indent=2))
                continue

            if problem.lower() == 'history':
                history = nova_process.get_solution_history()
                print(json.dumps(history, indent=2))
                continue

            if not problem:
                continue

            print(f"\n{Colors.DIM}🤔 Thinking...{Colors.END}")
            result = asyncio.run(nova_process.solve_problem(
                problem,
                max_iterations=args.max_iterations,
                stream=False
            ))

            print(format_result(result))
            print("\n" + "="*60 + "\n")

        except KeyboardInterrupt:
            print(f"\n{Colors.BOLD}Goodbye! 👋{Colors.END}")
            break
        except Exception as e:
            print(f"{Colors.RED}Error: {str(e)}{Colors.END}")

    return 0


# =============================================================================
# MODEL COMMANDS
# =============================================================================

def list_models_command(args):
    """Handle the list-models command."""
    print_mini_banner()

    try:
        llm_service = LLMService()
        models = llm_service.get_available_models()

        if not models:
            print(f"{Colors.RED}❌ No models available{Colors.END}")
            print(f"\n{Colors.DIM}To use models:")
            print("1. Set GEMINI_API_KEY for Gemini models")
            print("2. Set OPENAI_API_KEY for OpenAI models")
            print("3. Set ANTHROPIC_API_KEY for Claude models")
            print(f"4. Run 'ollama serve' for local models{Colors.END}")
            return 1

        print(f"{Colors.BOLD}🤖 Available Models ({len(models)}){Colors.END}")
        print("=" * 50)

        for i, model in enumerate(models, 1):
            clean_name = model.replace("ollama:", "")
            caps = llm_service.get_model_capabilities(model)

            print(f"\n{i}. {Colors.CYAN}{clean_name}{Colors.END}")
            print(f"   Type: {caps.get('type', 'unknown').upper()}")
            print(f"   {Colors.DIM}{caps.get('description', 'No description')}{Colors.END}")

            if args.detailed:
                print(f"   Capabilities:")
                print(f"     Reasoning: {caps.get('reasoning', 0)}/100")
                print(f"     Coding: {caps.get('coding', 0)}/100")
                print(f"     Speed: {caps.get('speed', 0)}/100")
                print(f"     Context: {caps.get('context_length', 0):,} tokens")

        print(f"\n{Colors.GREEN}💡 Default: {llm_service.get_default_model()}{Colors.END}")

        return 0

    except Exception as e:
        print(f"{Colors.RED}Error: {str(e)}{Colors.END}")
        return 1


def model_info_command(args):
    """Handle the model-info command."""
    print_mini_banner()

    try:
        llm_service = LLMService()
        model_name = args.model

        if not model_name.startswith(("ollama:", "gpt", "claude", "gemini")):
            model_name = f"ollama:{model_name}"

        info = llm_service.get_model_info(model_name)
        print(f"{Colors.BOLD}🔍 Model Information{Colors.END}")
        print("=" * 50)
        print(info)

        return 0

    except Exception as e:
        print(f"{Colors.RED}Error: {str(e)}{Colors.END}")
        return 1


# =============================================================================
# METRICS AND CACHE COMMANDS
# =============================================================================

def metrics_command(args):
    """Display performance metrics."""
    print_mini_banner()
    print(f"{Colors.BOLD}📊 Performance Metrics{Colors.END}")
    print("=" * 50)

    metrics_collector = get_metrics_collector()

    if args.session_id:
        session_metrics = metrics_collector.get_session_summary(args.session_id)
        if not session_metrics:
            print(f"{Colors.YELLOW}No metrics found for session: {args.session_id}{Colors.END}")
            return 1

        print(f"Session: {session_metrics['session_id']}")
        print(f"Total Time: {session_metrics['total_time']:.2f}s")
        print(f"Tokens Generated: {session_metrics['total_tokens_generated']}")
        print(f"Models Used: {', '.join(session_metrics['models_used'])}")
    else:
        summary = metrics_collector.get_performance_summary()

        if 'message' in summary:
            print(f"{Colors.DIM}{summary['message']}{Colors.END}")
            return 0

        print(f"Total Sessions: {summary['total_sessions']}")
        print(f"Avg Total Time: {summary['average_total_time']:.2f}s")
        print(f"Avg LLM Response: {summary['average_llm_response_time']:.2f}s")

        print(f"\n{Colors.CYAN}Model Usage:{Colors.END}")
        for model, count in summary['model_usage'].items():
            print(f"  {model}: {count} sessions")

    return 0


def cache_command(args):
    """Manage model cache."""
    cache = get_model_cache()

    if args.action == 'status':
        print_mini_banner()
        print(f"{Colors.BOLD}🗄️  Cache Status{Colors.END}")
        print("=" * 50)

        stats = cache.get_cache_stats()
        print(f"Cache Size: {stats['cache_size']}/{stats['max_cache_size']}")
        print(f"Memory: {stats['total_memory_mb']:.1f}MB / {stats['max_memory_mb']:.1f}MB")
        print(f"Hit Rate: {stats['hit_rate_percent']:.1f}%")

        if stats['cached_models']:
            print(f"\n{Colors.CYAN}Cached Models:{Colors.END}")
            for model in stats['cached_models']:
                status = "✅" if model['is_loaded'] else "⏸️"
                print(f"  {status} {model['model_name']} ({model['model_type']})")

    elif args.action == 'clear':
        cache.clear_cache()
        print(f"{Colors.GREEN}✅ Cache cleared{Colors.END}")

    return 0


# =============================================================================
# VERSION COMMAND
# =============================================================================

def version_command(args):
    """Show version information."""
    print(f"""
{Colors.BOLD}NovaSystem v2.0{Colors.END}
Multi-Agent Problem Solving Framework

{Colors.DIM}Components:
  • Core: DCE, CAE, Domain Experts
  • LLM: Gemini, OpenAI, Anthropic, Ollama
  • Services: Image, Vision, Document, Thinking, Tools
  • Interfaces: CLI, Gradio UI, REST API{Colors.END}
""")
    return 0


# =============================================================================
# ARGUMENT PARSER
# =============================================================================

def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        description="NovaSystem - Multi-Agent Problem-Solving Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick question with streaming
  python -m novasystem ask "What is machine learning?"

  # Interactive chat
  python -m novasystem chat

  # Expert panel analysis
  python -m novasystem experts "Design a REST API" --domains "Backend,Security"

  # Full Nova Process
  python -m novasystem solve "How to scale our system?" --domains "Cloud,DevOps"

  # List available models
  python -m novasystem list-models --detailed

  # Interactive problem-solving mode
  python -m novasystem interactive
        """
    )

    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--version', action='store_true', help='Show version')

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Ask command
    ask_parser = subparsers.add_parser('ask', help='Quick question')
    ask_parser.add_argument('question', help='Question to ask')
    ask_parser.add_argument('--model', '-m', default='gemini-2.5-flash', help='Model')
    ask_parser.add_argument('--system', '-s', help='System instruction')
    ask_parser.add_argument('--stream', action='store_true', default=True)
    ask_parser.add_argument('--no-stream', dest='stream', action='store_false')

    # Chat command
    chat_parser = subparsers.add_parser('chat', help='Interactive chat')
    chat_parser.add_argument('--model', '-m', default='gemini-2.5-flash', help='Model')
    chat_parser.add_argument('--system', '-s', help='System instruction')

    # Experts command
    experts_parser = subparsers.add_parser('experts', help='Expert panel')
    experts_parser.add_argument('problem', help='Problem to analyze')
    experts_parser.add_argument('--domains', '-d', default='Software,Design', help='Domains')
    experts_parser.add_argument('--model', '-m', default='gemini-2.5-flash', help='Model')

    # Solve command
    solve_parser = subparsers.add_parser('solve', help='Full Nova Process')
    solve_parser.add_argument('problem', help='Problem to solve')
    solve_parser.add_argument('--domains', '-d', default='General,Technology', help='Domains')
    solve_parser.add_argument('--max-iterations', '-i', type=int, default=3, help='Max iterations')
    solve_parser.add_argument('--model', '-m', default='gemini-2.5-flash', help='Model')
    solve_parser.add_argument('--output', '-o', choices=['text', 'json'], default='text')
    solve_parser.add_argument('--verbose', '-v', action='store_true')

    # Interactive command
    interactive_parser = subparsers.add_parser('interactive', help='Interactive mode')
    interactive_parser.add_argument('--domains', '-d', default='General', help='Domains')
    interactive_parser.add_argument('--max-iterations', '-i', type=int, default=3)
    interactive_parser.add_argument('--model', '-m', default='gemini-2.5-flash', help='Model')

    # List models command
    list_parser = subparsers.add_parser('list-models', help='List models')
    list_parser.add_argument('--detailed', '-d', action='store_true')

    # Model info command
    info_parser = subparsers.add_parser('model-info', help='Model info')
    info_parser.add_argument('model', help='Model name')

    # Metrics command
    metrics_parser = subparsers.add_parser('metrics', help='Performance metrics')
    metrics_parser.add_argument('--session-id', '-s', help='Session ID')
    metrics_parser.add_argument('--detailed', '-d', action='store_true')

    # Cache command
    cache_parser = subparsers.add_parser('cache', help='Cache management')
    cache_parser.add_argument('action', choices=['status', 'clear'], help='Action')

    return parser


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    setup_logging(parsed_args.verbose)

    if parsed_args.version:
        return version_command(parsed_args)

    if not parsed_args.command:
        parser.print_help()
        return 0

    commands = {
        'ask': ask_command,
        'chat': chat_command,
        'experts': experts_command,
        'solve': solve_command,
        'interactive': interactive_command,
        'list-models': list_models_command,
        'model-info': model_info_command,
        'metrics': metrics_command,
        'cache': cache_command,
    }

    try:
        handler = commands.get(parsed_args.command)
        if handler:
            return handler(parsed_args)
        else:
            parser.print_help()
            return 1

    except KeyboardInterrupt:
        print(f"\n{Colors.DIM}Cancelled.{Colors.END}")
        return 1
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        print(f"{Colors.RED}Error: {str(e)}{Colors.END}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
