"""
Command Line Interface for NovaSystem.

This module provides a CLI for interacting with the Nova Process.
"""

import argparse
import asyncio
import sys
import json
import logging
import uuid
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

# ANSI colors for terminal
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def print_banner():
    """Print the NovaSystem banner."""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🧠 NovaSystem v2.0                        ║
    ║              Multi-Agent Problem-Solving Framework           ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def format_result(result: dict) -> str:
    """Format the Nova Process result for CLI display."""
    if not result:
        return "No result available."

    formatted = []
    formatted.append("🚀 Nova Process Results")
    formatted.append("=" * 50)

    # Add final synthesis
    if "final_synthesis" in result:
        formatted.append("\n📋 Final Synthesis:")
        formatted.append("-" * 20)
        formatted.append(result["final_synthesis"])

    # Add final validation
    if "final_validation" in result:
        formatted.append("\n✅ Final Validation:")
        formatted.append("-" * 20)
        formatted.append(result["final_validation"])

    # Add iteration summary
    if "total_iterations" in result:
        formatted.append(f"\n📊 Process Summary:")
        formatted.append("-" * 20)
        formatted.append(f"Total Iterations: {result['total_iterations']}")
        formatted.append(f"Process Phase: {result.get('phase', 'Unknown')}")

    return "\n".join(formatted)

async def run_nova_process(problem: str,
                          domains: List[str],
                          max_iterations: int,
                          model: str,
                          output_format: str,
                          verbose: bool) -> dict:
    """Run the Nova Process."""
    try:
        # Create Nova Process
        memory_manager = MemoryManager()
        nova_process = NovaProcess(
            domains=domains,
            model=model,
            memory_manager=memory_manager
        )

        if verbose:
            print(f"Starting Nova Process with domains: {', '.join(domains)}")
            print(f"Using model: {model}")
            print(f"Max iterations: {max_iterations}")
            print()

        # Generate session ID for metrics tracking
        session_id = str(uuid.uuid4())

        if verbose:
            print(f"Session ID: {session_id}")
            print()

        # Run the process with streaming
        print("🚀 Starting Nova Process...")
        print(f"📋 Problem: {problem}")
        print(f"🧠 Model: {model}")
        print(f"🔄 Max Iterations: {max_iterations}")
        print(f"🆔 Session ID: {session_id}")
        print("\n" + "="*60)

        result = await nova_process.solve_problem(
            problem,
            max_iterations=max_iterations,
            stream=True,  # Enable streaming
            session_id=session_id
        )

        # Handle streaming results
        if hasattr(result, '__aiter__'):
            print("🧠 NovaSystem is working on your problem...\n")
            final_result = None

            async for update in result:
                if isinstance(update, dict):
                    if 'iteration' in update:
                        print(f"\n🔄 Iteration {update['iteration']}:")
                        print("-" * 40)

                    if 'agent' in update and 'response' in update:
                        agent_name = update['agent']
                        response = update['response']
                        print(f"\n🤖 {agent_name}:")
                        print(f"{response}\n")

                    if 'final_synthesis' in update:
                        print("\n" + "="*60)
                        print("🎯 FINAL SYNTHESIS")
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
    """Handle the solve command."""
    print_banner()

    # Parse domains
    domains = [d.strip() for d in args.domains.split(",") if d.strip()]

    # Run the process
    try:
        result = asyncio.run(run_nova_process(
            problem=args.problem,
            domains=domains,
            max_iterations=args.max_iterations,
            model=args.model,
            output_format=args.output,
            verbose=args.verbose
        ))

        # Output result
        if args.output == "json":
            print(json.dumps(result, indent=2))
        else:
            print(format_result(result))

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def interactive_command(args):
    """Handle the interactive command."""
    print_banner()
    print("🧠 NovaSystem Interactive Mode")
    print("Type 'quit' to exit, 'help' for commands")
    print()

    # Initialize Nova Process
    memory_manager = MemoryManager()
    nova_process = NovaProcess(
        domains=args.domains.split(",") if args.domains else ["General"],
        model=args.model,
        memory_manager=memory_manager
    )

    while True:
        try:
            problem = input("Enter your problem: ").strip()

            if problem.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! 👋")
                break

            if problem.lower() == 'help':
                print("Commands:")
                print("  help - Show this help")
                print("  quit/exit/q - Exit the program")
                print("  status - Show current process status")
                print("  history - Show solution history")
                continue

            if problem.lower() == 'status':
                status = nova_process.get_status()
                print(f"Status: {json.dumps(status, indent=2)}")
                continue

            if problem.lower() == 'history':
                history = nova_process.get_solution_history()
                print(f"History: {json.dumps(history, indent=2)}")
                continue

            if not problem:
                print("Please enter a problem statement.")
                continue

            print("\n🤔 Thinking...")
            result = asyncio.run(nova_process.solve_problem(
                problem,
                max_iterations=args.max_iterations,
                stream=False
            ))

            print("\n" + format_result(result))
            print("\n" + "="*60 + "\n")

        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

def list_models_command(args):
    """Handle the list-models command."""
    print_banner()

    try:
        # Create LLM service
        llm_service = LLMService()

        # Get available models
        models = llm_service.get_available_models()

        if not models:
            print("❌ No models available")
            print("\nTo use models:")
            print("1. Set OPENAI_API_KEY for OpenAI models")
            print("2. Install and run Ollama for local models")
            print("3. Run 'ollama pull <model>' to download models")
            return

        print("🤖 Available Models:")
        print("=" * 50)

        for i, model in enumerate(models, 1):
            clean_name = model.replace("ollama:", "")
            caps = llm_service.get_model_capabilities(model)

            print(f"\n{i}. {clean_name}")
            print(f"   Type: {caps.get('type', 'unknown').upper()}")
            print(f"   Description: {caps.get('description', 'No description')}")

            if args.detailed:
                print(f"   Capabilities:")
                print(f"     Reasoning: {caps.get('reasoning', 0)}/100")
                print(f"     Coding: {caps.get('coding', 0)}/100")
                print(f"     Analysis: {caps.get('analysis', 0)}/100")
                print(f"     Creativity: {caps.get('creativity', 0)}/100")
                print(f"     Speed: {caps.get('speed', 0)}/100")
                print(f"     Context: {caps.get('context_length', 0):,} tokens")

        # Show best models for different tasks
        print(f"\n🎯 Best Models for Different Tasks:")
        print("-" * 40)

        tasks = ["reasoning", "coding", "analysis", "creativity", "dce", "cae", "domain"]
        for task in tasks:
            best_model = llm_service.get_best_model_for_task(task, models)
            clean_name = best_model.replace("ollama:", "")
            print(f"  {task.upper():<12}: {clean_name}")

        print(f"\n💡 Current default model: {llm_service.get_default_model().replace('ollama:', '')}")

    except Exception as e:
        print(f"Error: {str(e)}")

def model_info_command(args):
    """Handle the model-info command."""
    print_banner()

    try:
        # Create LLM service
        llm_service = LLMService()

        # Add ollama: prefix if not present
        model_name = args.model
        if not model_name.startswith("ollama:") and not model_name.startswith("gpt") and not model_name.startswith("claude"):
            model_name = f"ollama:{model_name}"

        # Get model info
        info = llm_service.get_model_info(model_name)
        print(f"🔍 Model Information:")
        print("=" * 50)
        print(info)

    except Exception as e:
        print(f"Error: {str(e)}")


def ask_command(args):
    """Handle the ask command - quick single question."""
    print(f"\n{Colors.BOLD}🧠 NovaSystem Quick Ask{Colors.END}\n")

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
                return

        messages = [
            {"role": "system", "content": args.system or "You are a helpful assistant. Be concise and direct."},
            {"role": "user", "content": args.question}
        ]

        print(f"{Colors.CYAN}📤 Question:{Colors.END} {args.question}")
        print(f"{Colors.CYAN}🤖 Model:{Colors.END} {model}\n")

        if args.stream:
            print(f"{Colors.GREEN}📥 Answer:{Colors.END} ", end="", flush=True)
            response_text = []

            async def stream_response():
                async for chunk in llm_service.stream_completion(messages, model=model):
                    print(chunk, end="", flush=True)
                    response_text.append(chunk)

            asyncio.run(stream_response())
            print("\n")
        else:
            print(f"{Colors.GREEN}📥 Answer:{Colors.END}")
            response = asyncio.run(llm_service.get_completion(messages, model=model))
            print(response)
            print()

    except Exception as e:
        print(f"{Colors.RED}❌ Error: {str(e)}{Colors.END}")


def chat_command(args):
    """Handle the chat command - interactive streaming chat."""
    print_banner()
    print(f"{Colors.BOLD}💬 NovaSystem Interactive Chat{Colors.END}")
    print(f"Type 'quit' to exit, 'clear' to reset history")
    print(f"Model: {args.model}")
    print()

    try:
        llm_service = LLMService()
        model = args.model

        # Validate model
        if not llm_service.is_model_available(model):
            available = llm_service.get_available_models()
            if available:
                model = available[0]
                print(f"{Colors.YELLOW}⚠️  Using {model} (requested model not available){Colors.END}\n")
            else:
                print(f"{Colors.RED}❌ No models available{Colors.END}")
                return

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

    except Exception as e:
        print(f"{Colors.RED}❌ Error: {str(e)}{Colors.END}")


def experts_command(args):
    """Handle the experts command - stream expert analysis."""
    print_banner()
    print(f"{Colors.BOLD}🎭 NovaSystem Expert Panel{Colors.END}\n")

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
                return

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

        # Phase 1: DCE
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

        # Phase 3: CAE
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

    except Exception as e:
        print(f"{Colors.RED}❌ Error: {str(e)}{Colors.END}")

def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        description="NovaSystem - Multi-Agent Problem-Solving Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick question (streaming)
  python -m novasystem ask "What is the best way to learn Python?"

  # Interactive chat
  python -m novasystem chat --model gemini-2.5-flash

  # Expert panel analysis
  python -m novasystem experts "Design a scalable API" --domains "Backend,Security"

  # Full Nova Process
  python -m novasystem solve "How can we improve code reviews?" --domains "Engineering,Process"

  # List available models
  python -m novasystem list-models --detailed

  # Interactive mode
  python -m novasystem interactive
        """
    )

    # Global options
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--version', action='version', version='NovaSystem 2.0.0')

    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Solve command
    solve_parser = subparsers.add_parser('solve', help='Solve a problem using Nova Process')
    solve_parser.add_argument('problem', help='Problem statement to solve')
    solve_parser.add_argument('--domains', '-d', default='General,Technology,Business',
                            help='Comma-separated list of expert domains (default: General,Technology,Business)')
    solve_parser.add_argument('--max-iterations', '-i', type=int, default=3,
                            help='Maximum number of iterations (default: 3)')
    solve_parser.add_argument('--model', '-m', default='gpt-4o',
                            help='AI model to use (default: gpt-4o)')
    solve_parser.add_argument('--output', '-o', choices=['text', 'json'], default='text',
                            help='Output format (default: text)')
    solve_parser.add_argument('--verbose', '-v', action='store_true',
                            help='Enable verbose output with streaming')

    # Interactive command
    interactive_parser = subparsers.add_parser('interactive', help='Start interactive mode')
    interactive_parser.add_argument('--domains', '-d', default='General',
                                  help='Comma-separated list of expert domains (default: General)')
    interactive_parser.add_argument('--max-iterations', '-i', type=int, default=3,
                                  help='Maximum number of iterations (default: 3)')
    interactive_parser.add_argument('--model', '-m', default='gpt-4',
                                  help='AI model to use (default: gpt-4)')

    # List models command
    list_models_parser = subparsers.add_parser('list-models', help='List available models and their capabilities')
    list_models_parser.add_argument('--detailed', '-d', action='store_true',
                                   help='Show detailed capability scores')

    # Model info command
    model_info_parser = subparsers.add_parser('model-info', help='Get detailed information about a specific model')
    model_info_parser.add_argument('model', help='Model name to get info for')

    # Ask command - quick single question
    ask_parser = subparsers.add_parser('ask', help='Quick single question (no full Nova Process)')
    ask_parser.add_argument('question', help='Question to ask')
    ask_parser.add_argument('--model', '-m', default='gemini-2.5-flash',
                           help='AI model to use (default: gemini-2.5-flash)')
    ask_parser.add_argument('--system', '-s', help='Custom system instruction')
    ask_parser.add_argument('--stream', action='store_true', default=True,
                           help='Stream the response (default: True)')
    ask_parser.add_argument('--no-stream', dest='stream', action='store_false',
                           help='Disable streaming')

    # Chat command - interactive streaming chat
    chat_parser = subparsers.add_parser('chat', help='Interactive streaming chat')
    chat_parser.add_argument('--model', '-m', default='gemini-2.5-flash',
                            help='AI model to use (default: gemini-2.5-flash)')
    chat_parser.add_argument('--system', '-s', help='Custom system instruction')

    # Experts command - expert panel analysis
    experts_parser = subparsers.add_parser('experts', help='Run expert panel analysis')
    experts_parser.add_argument('problem', help='Problem to analyze')
    experts_parser.add_argument('--domains', '-d', default='Software Engineering,System Design',
                               help='Comma-separated expert domains')
    experts_parser.add_argument('--model', '-m', default='gemini-2.5-flash',
                               help='AI model to use (default: gemini-2.5-flash)')

    # Metrics command
    metrics_parser = subparsers.add_parser('metrics', help='Display performance metrics')
    metrics_parser.add_argument('--session-id', '-s', help='Show metrics for specific session ID')
    metrics_parser.add_argument('--detailed', '-d', action='store_true', help='Show detailed metrics')
    metrics_parser.add_argument('--system', action='store_true', help='Include system metrics')

    # Cache command
    cache_parser = subparsers.add_parser('cache', help='Manage model cache')
    cache_parser.add_argument('action', choices=['status', 'clear', 'preload', 'recommend'],
                             help='Cache action to perform')
    cache_parser.add_argument('--model', '-m', help='Model name (for preload action)')
    cache_parser.add_argument('--model-type', '-t', choices=['ollama', 'openai'],
                             default='ollama', help='Model type (for preload action)')
    cache_parser.add_argument('--task-type', help='Task type for recommendations (reasoning, coding, analysis, etc.)')

    return parser

def metrics_command(args):
    """Display performance metrics."""
    print("📊 NovaSystem Performance Metrics")
    print("=" * 50)

    metrics_collector = get_metrics_collector()

    if args.session_id:
        # Show specific session metrics
        session_metrics = metrics_collector.get_session_summary(args.session_id)
        if not session_metrics:
            print(f"❌ No metrics found for session: {args.session_id}")
            return

        print(f"Session ID: {session_metrics['session_id']}")
        print(f"Total Sessions: {session_metrics['total_sessions']}")
        print(f"Total Time: {session_metrics['total_time']:.2f}s")
        print(f"Average LLM Response Time: {session_metrics['average_llm_response_time']:.2f}s")
        print(f"Total Tokens Generated: {session_metrics['total_tokens_generated']}")
        print(f"Total Iterations: {session_metrics['total_iterations']}")
        print(f"Models Used: {', '.join(session_metrics['models_used'])}")

        if args.detailed and session_metrics['last_session']:
            print("\n📋 Last Session Details:")
            last_session = session_metrics['last_session']
            print(f"  Total Time: {last_session['timing']['total_time']:.2f}s")
            print(f"  LLM Response Time: {last_session['timing']['llm_response_time']:.2f}s")
            print(f"  Peak Memory: {last_session['memory']['peak_memory_mb']:.2f}MB")
            print(f"  Model: {last_session['model']['model_used']}")
            print(f"  Tokens Generated: {last_session['model']['tokens_generated']}")
            print(f"  Iterations: {last_session['process']['iterations_completed']}")

    else:
        # Show overall performance summary
        summary = metrics_collector.get_performance_summary()

        if 'message' in summary:
            print(f"ℹ️  {summary['message']}")
            return

        print(f"Total Sessions: {summary['total_sessions']}")
        print(f"Recent Sessions: {summary['recent_sessions']}")
        print(f"Average Total Time: {summary['average_total_time']:.2f}s")
        print(f"Average LLM Response Time: {summary['average_llm_response_time']:.2f}s")
        print(f"Average Peak Memory: {summary['average_peak_memory_mb']:.2f}MB")

        print("\n🤖 Model Usage:")
        for model, count in summary['model_usage'].items():
            print(f"  {model}: {count} sessions")

        if args.system:
            print("\n💻 System Metrics:")
            system_metrics = summary['system_metrics']
            if system_metrics['cpu_percent']:
                avg_cpu = sum(system_metrics['cpu_percent']) / len(system_metrics['cpu_percent'])
                print(f"  Average CPU: {avg_cpu:.1f}%")
            if system_metrics['memory_percent']:
                avg_memory = sum(system_metrics['memory_percent']) / len(system_metrics['memory_percent'])
                print(f"  Average Memory: {avg_memory:.1f}%")

    print()

def cache_command(args):
    """Manage model cache."""
    cache = get_model_cache()

    if args.action == 'status':
        print("🗄️  Model Cache Status")
        print("=" * 50)

        stats = cache.get_cache_stats()
        print(f"Cache Size: {stats['cache_size']}/{stats['max_cache_size']}")
        print(f"Loaded Models: {stats['loaded_models']}")
        print(f"Memory Usage: {stats['total_memory_mb']:.1f}MB / {stats['max_memory_mb']:.1f}MB")
        print(f"Hit Rate: {stats['hit_rate_percent']:.1f}%")
        print(f"Cache Hits: {stats['cache_hits']}")
        print(f"Cache Misses: {stats['cache_misses']}")
        print(f"Models Loaded: {stats['models_loaded']}")
        print(f"Average Load Time: {stats['average_load_time']:.2f}s")

        if stats['cached_models']:
            print("\n📋 Cached Models:")
            for model in stats['cached_models']:
                status = "✅ Loaded" if model['is_loaded'] else "⏸️  Unloaded"
                print(f"  {model['model_name']} ({model['model_type']}) - {status}")
                print(f"    Last Used: {model['last_used']}")
                print(f"    Access Count: {model['access_count']}")
                print(f"    Memory: {model['memory_usage_mb']:.1f}MB")
                print()

    elif args.action == 'clear':
        print("🗑️  Clearing model cache...")
        cache.clear_cache()
        print("✅ Cache cleared successfully")

    elif args.action == 'preload':
        if not args.model:
            print("❌ Model name required for preload action")
            return

        print(f"🔄 Preloading model: {args.model}")
        try:
            success = asyncio.run(cache.preload_model(args.model, args.model_type or "ollama"))
            if success:
                print(f"✅ Model {args.model} preloaded successfully")
            else:
                print(f"❌ Failed to preload model {args.model}")
        except Exception as e:
            print(f"❌ Error preloading model: {e}")

    elif args.action == 'recommend':
        print("💡 Recommended Models")
        print("=" * 50)

        task_type = args.task_type or "general"
        recommended = cache.get_recommended_models(task_type)

        if recommended:
            print(f"For {task_type} tasks:")
            for i, model in enumerate(recommended, 1):
                print(f"  {i}. {model}")
        else:
            print("No recommendations available yet. Run some tasks to build cache history.")

    else:
        print("❌ Unknown cache action. Use: status, clear, preload, or recommend")

def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    # Setup logging
    setup_logging(parsed_args.verbose)

    if not parsed_args.command:
        parser.print_help()
        return 0

    try:
        if parsed_args.command == 'solve':
            solve_command(parsed_args)
        elif parsed_args.command == 'interactive':
            interactive_command(parsed_args)
        elif parsed_args.command == 'list-models':
            list_models_command(parsed_args)
        elif parsed_args.command == 'model-info':
            model_info_command(parsed_args)
        elif parsed_args.command == 'ask':
            ask_command(parsed_args)
        elif parsed_args.command == 'chat':
            chat_command(parsed_args)
        elif parsed_args.command == 'experts':
            experts_command(parsed_args)
        elif parsed_args.command == 'metrics':
            metrics_command(parsed_args)
        elif parsed_args.command == 'cache':
            cache_command(parsed_args)
        else:
            parser.print_help()
            return 1

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
