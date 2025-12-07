"""
Gradio Interface for NovaSystem.

This module provides a simple Gradio-based web interface for the Nova Process.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (NovaSystem-Codex) or current directory
_env_paths = [
    Path(__file__).parent.parent.parent.parent / ".env",  # NovaSystem-Codex/.env
    Path(__file__).parent.parent.parent / ".env",  # NovaSystem-Streamlined/.env
    Path.cwd() / ".env",  # Current working directory
]
for _env_path in _env_paths:
    if _env_path.exists():
        load_dotenv(_env_path)
        print(f"🔧 [ENV] Loaded environment from: {_env_path}")
        break

import gradio as gr
import asyncio
import json
import time
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

from ..core.process import NovaProcess
from ..core.memory import MemoryManager
from ..utils.llm_service import LLMService

# Configure detailed console logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s',
    datefmt='%H:%M:%S',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Console logging helper with emojis for visibility
def log_event(emoji: str, category: str, message: str, details: dict = None):
    """Log an event with emoji prefix for easy console scanning."""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"{timestamp} | {emoji} [{category}] {message}")
    if details:
        for key, value in details.items():
            print(f"           └─ {key}: {value}")

class GradioInterface:
    """Gradio interface for NovaSystem."""

    def __init__(self, llm_service: Optional[LLMService] = None):
        log_event("🚀", "INIT", "Initializing GradioInterface...")
        
        self.current_process = None
        self.session_history = []
        self.performance_metrics = {}
        self.model_performance = {}
        
        # Share a single LLM service instance so model availability checks are consistent
        log_event("🔌", "INIT", "Creating LLMService instance...")
        self.llm_service = llm_service or LLMService()
        
        available = self.llm_service.get_available_models()
        log_event("✅", "INIT", f"GradioInterface ready!", {
            "available_models": len(available),
            "models": available[:5] if len(available) > 5 else available
        })

    def _validate_model_selection(self, model: str) -> Optional[str]:
        """Ensure the requested model is available before starting a run."""
        log_event("🔍", "VALIDATE", f"Checking model availability: {model}")
        
        if self.llm_service.is_model_available(model):
            log_event("✅", "VALIDATE", f"Model '{model}' is available")
            return None

        available_models = self.llm_service.get_available_models()
        if not available_models:
            log_event("❌", "VALIDATE", "No LLM models available!")
            return (
                "Error: No LLMs are available. Please set OPENAI_API_KEY/ANTHROPIC_API_KEY "
                "or start Ollama with at least one pulled model."
            )

        log_event("⚠️", "VALIDATE", f"Model '{model}' not available", {
            "available": available_models
        })
        return (
            f"Error: The selected model '{model}' is not available.\n\n"
            f"Available models: {', '.join(available_models)}"
        )

    def run_nova_process(self,
                        problem: str,
                        domains: str = "General,Technology,Business",
                        max_iterations: int = 3,
                        model: str = "gpt-4",
                        save_session: bool = False,
                        export_format: str = "text") -> tuple:
        """
        Run the Nova Process with enhanced features and return formatted results.

        Args:
            problem: Problem statement
            domains: Comma-separated list of domains
            max_iterations: Maximum number of iterations
            model: LLM model to use
            save_session: Whether to save session for later reference
            export_format: Format for exporting results (text, json, markdown)

        Returns:
            Tuple of (formatted results, session info, performance metrics)
        """
        print("\n" + "="*80)
        log_event("🎯", "NOVA", "Starting Nova Process run", {
            "problem_length": len(problem),
            "model": model,
            "domains": domains,
            "max_iterations": max_iterations,
            "export_format": export_format
        })
        print("="*80)
        
        if not problem.strip():
            log_event("⚠️", "NOVA", "Empty problem statement - aborting")
            return ("Please enter a problem statement first!", "", "")

        # Fail fast if the selected model cannot be used
        model_error = self._validate_model_selection(model)
        if model_error:
            log_event("❌", "NOVA", "Model validation failed")
            return (model_error, "", "")

        start_time = time.time()
        session_id = f"session_{int(time.time())}"
        log_event("📋", "NOVA", f"Session created: {session_id}")

        try:
            # Parse domains
            domain_list = [d.strip() for d in domains.split(",") if d.strip()]
            log_event("🎓", "NOVA", f"Domains parsed: {domain_list}")

            # Create Nova Process
            log_event("🔧", "NOVA", "Creating NovaProcess instance...")
            memory_manager = MemoryManager()
            nova_process = NovaProcess(
                domains=domain_list,
                model=model,
                memory_manager=memory_manager,
                llm_service=self.llm_service
            )
            log_event("✅", "NOVA", "NovaProcess created successfully")

            # Run the process
            log_event("🚀", "NOVA", "Starting problem solving...")
            result = asyncio.run(nova_process.solve_problem(
                problem,
                max_iterations=max_iterations,
                stream=False
            ))
            log_event("✅", "NOVA", "Problem solving completed!")

            # Calculate performance metrics
            end_time = time.time()
            duration = end_time - start_time
            log_event("⏱️", "NOVA", f"Total processing time: {duration:.2f}s")

            # Track performance
            self.performance_metrics[session_id] = {
                'duration': duration,
                'iterations': max_iterations,
                'domains': len(domain_list),
                'model': model,
                'timestamp': datetime.now().isoformat()
            }

            # Update model performance tracking
            if model not in self.model_performance:
                self.model_performance[model] = {'total_time': 0, 'sessions': 0}
            self.model_performance[model]['total_time'] += duration
            self.model_performance[model]['sessions'] += 1

            # Save session if requested
            session_info = ""
            if save_session:
                session_data = {
                    'session_id': session_id,
                    'problem': problem,
                    'domains': domain_list,
                    'result': result,
                    'timestamp': datetime.now().isoformat(),
                    'duration': duration
                }
                self.session_history.append(session_data)
                session_info = f"Session saved with ID: {session_id}"
                log_event("💾", "NOVA", f"Session saved: {session_id}")

            # Format the result based on export format
            formatted_result = self._format_result(result, export_format)
            log_event("📝", "NOVA", f"Result formatted as: {export_format}")

            # Create performance summary
            avg_model_time = self.model_performance[model]['total_time'] / self.model_performance[model]['sessions']
            performance_info = f"""
Performance Metrics:
• Processing Time: {duration:.2f} seconds
• Model: {model} (avg: {avg_model_time:.2f}s)
• Iterations: {max_iterations}
• Domains: {len(domain_list)}
• Session ID: {session_id}
"""

            print("\n" + "="*80)
            log_event("🎉", "NOVA", "Nova Process run completed successfully!", {
                "session_id": session_id,
                "duration": f"{duration:.2f}s",
                "model": model,
                "result_length": len(str(formatted_result))
            })
            print("="*80 + "\n")

            return (formatted_result, session_info, performance_info)

        except Exception as e:
            duration = time.time() - start_time
            log_event("❌", "NOVA", f"Error in Nova Process!", {
                "error": str(e),
                "duration": f"{duration:.2f}s",
                "session_id": session_id
            })
            logger.exception(f"Error in Nova Process: {str(e)}")
            error_msg = f"Error: {str(e)}\n\nPlease try again with a more specific problem statement."
            return (error_msg, f"Session {session_id} failed", f"Error occurred after {duration:.2f} seconds")

    def _format_result(self, result: Dict[str, Any], format_type: str = "text") -> str:
        """Format the Nova Process result for display in different formats."""
        if not result:
            return "No result available."

        if format_type == "json":
            return json.dumps(result, indent=2)
        elif format_type == "markdown":
            return self._format_markdown(result)
        else:  # text format
            return self._format_text(result)

    def _format_text(self, result: Dict[str, Any]) -> str:
        """Format result as plain text."""
        formatted = []
        formatted.append("## 🚀 Nova Process Results\n")

        # Add final synthesis
        if "final_synthesis" in result:
            formatted.append("### 📋 Final Synthesis")
            formatted.append(result["final_synthesis"])
            formatted.append("")

        # Add final validation
        if "final_validation" in result:
            formatted.append("### ✅ Final Validation")
            formatted.append(result["final_validation"])
            formatted.append("")

        # Add iteration summary
        if "total_iterations" in result:
            formatted.append(f"### 📊 Process Summary")
            formatted.append(f"- Total Iterations: {result['total_iterations']}")
            formatted.append(f"- Process Phase: {result.get('phase', 'Unknown')}")
            formatted.append("")

        return "\n".join(formatted)

    def _format_markdown(self, result: Dict[str, Any]) -> str:
        """Format result as markdown."""
        formatted = []
        formatted.append("# 🚀 Nova Process Results\n")
        formatted.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")

        # Add final synthesis
        if "final_synthesis" in result:
            formatted.append("## 📋 Final Synthesis\n")
            formatted.append(result["final_synthesis"])
            formatted.append("\n")

        # Add final validation
        if "final_validation" in result:
            formatted.append("## ✅ Final Validation\n")
            formatted.append(result["final_validation"])
            formatted.append("\n")

        # Add iteration summary
        if "total_iterations" in result:
            formatted.append("## 📊 Process Summary\n")
            formatted.append(f"- **Total Iterations**: {result['total_iterations']}")
            formatted.append(f"- **Process Phase**: {result.get('phase', 'Unknown')}")
            formatted.append("\n")

        return "\n".join(formatted)

    def get_session_history(self) -> str:
        """Get formatted session history."""
        if not self.session_history:
            return "No sessions saved yet."

        formatted = ["## 📚 Session History\n"]
        for session in self.session_history[-10:]:  # Last 10 sessions
            formatted.append(f"**Session {session['session_id']}** ({session['timestamp'][:10]})")
            formatted.append(f"- Problem: {session['problem'][:100]}...")
            formatted.append(f"- Duration: {session['duration']:.2f}s")
            formatted.append(f"- Domains: {', '.join(session['domains'])}")
            formatted.append("")

        return "\n".join(formatted)

    def get_performance_stats(self) -> str:
        """Get formatted performance statistics."""
        if not self.performance_metrics:
            return "No performance data available yet."

        formatted = ["## 📈 Performance Statistics\n"]

        # Overall stats
        total_sessions = len(self.performance_metrics)
        avg_duration = sum(m['duration'] for m in self.performance_metrics.values()) / total_sessions

        formatted.append(f"**Overall Statistics:**")
        formatted.append(f"- Total Sessions: {total_sessions}")
        formatted.append(f"- Average Duration: {avg_duration:.2f} seconds")
        formatted.append("")

        # Model performance
        formatted.append("**Model Performance:**")
        for model, stats in self.model_performance.items():
            avg_time = stats['total_time'] / stats['sessions']
            formatted.append(f"- {model}: {stats['sessions']} sessions, avg {avg_time:.2f}s")

        return "\n".join(formatted)

    def create_interface(self) -> gr.Blocks:
        """Create the enhanced Gradio interface with advanced features."""
        with gr.Blocks(title="NovaSystem - Advanced AI Problem Solver", theme="soft") as interface:
            gr.Markdown("# 🚀 NovaSystem - Advanced Multi-Agent Problem Solver")
            gr.Markdown("**Transform complex challenges into actionable solutions** with our advanced multi-agent AI system.")

            with gr.Tabs():
                self._build_problem_solver_tab()
                self._build_session_history_tab()
                self._build_performance_tab()
                self._build_system_info_tab()

        return interface

    def _build_problem_solver_tab(self):
        """Problem solver tab components and wiring."""
        model_choices = self.llm_service.get_available_models()
        if not model_choices:
            # Fallback to a static list so the UI still renders, validation will guard execution
            model_choices = [
                "gpt-4",
                "gpt-3.5-turbo",
                "claude-3",
                "claude-3-haiku",
                "claude-3-sonnet",
                "ollama:phi3",
                "ollama:llama2",
                "ollama:gpt-oss:20b",
                "ollama:mistral"
            ]
        default_model = model_choices[0] if model_choices else "gpt-4"

        # Example problems for users to try
        example_problems = [
            ["How can I improve the performance of my Python web application that's experiencing slow response times under heavy load? The app uses Flask, PostgreSQL, and serves about 10,000 requests per hour."],
            ["I'm designing a new mobile app for personal finance management. What features should I prioritize for the MVP, and what's the best tech stack for cross-platform development?"],
            ["Our team is struggling with code review bottlenecks. Reviews take too long and developers are getting blocked. How can we streamline the process while maintaining code quality?"],
            ["I need to explain machine learning concepts to non-technical stakeholders. What analogies and examples work best for explaining neural networks, training data, and model accuracy?"],
            ["What are the key considerations for migrating a monolithic application to microservices? Our current system is a 5-year-old Java application with tight coupling between components."]
        ]

        with gr.Tab("🎯 Problem Solver"):
            with gr.Row():
                with gr.Column(scale=2):
                    problem_input = gr.Textbox(
                        lines=6,
                        placeholder="Describe your problem or challenge in detail. Be specific about context, constraints, and desired outcomes...",
                        label="🧠 Problem Description",
                        info="💡 The more detailed your description, the better our AI experts can help you"
                    )

                    # Add example problems
                    gr.Examples(
                        examples=example_problems,
                        inputs=problem_input,
                        label="📝 Try an Example Problem"
                    )

                    with gr.Row():
                        domains_input = gr.Textbox(
                            value="General,Technology,Business",
                            label="🎯 Expert Domains",
                            info="💡 Comma-separated expertise areas"
                        )
                        iterations_input = gr.Slider(
                            minimum=1,
                            maximum=20,
                            value=3,
                            step=1,
                            label="🔄 Max Iterations",
                            info="💡 More iterations = deeper analysis"
                        )

                    with gr.Row():
                        model_input = gr.Dropdown(
                            choices=model_choices,
                            value=default_model,
                            label="🤖 AI Model",
                            info="💡 Choose your preferred AI model"
                        )
                        export_format = gr.Dropdown(
                            choices=["text", "markdown", "json"],
                            value="text",
                            label="📄 Export Format",
                            info="💡 Choose output format"
                        )

                    with gr.Row():
                        save_session = gr.Checkbox(
                            label="💾 Save Session",
                            value=False,
                            info="💡 Save this session for later reference"
                        )
                        solve_btn = gr.Button("🚀 Solve Problem", variant="primary")

                with gr.Column(scale=1):
                    gr.Markdown("### 🤖 Our AI Expert Team:")
                    gr.Markdown("""
                    - **🧠 DCE (Discussion Continuity Expert)**: Maintains conversation flow and coherence
                    - **🔍 CAE (Critical Analysis Expert)**: Provides rigorous evaluation and identifies potential issues
                    - **🎯 Domain Experts**: Deliver specialized knowledge in your specified expertise areas
                    """)

                    gr.Markdown("### 💡 Pro Tips:")
                    gr.Markdown("""
                    - **Be Specific**: Include context, constraints, and desired outcomes
                    - **Choose Wisely**: Select 2-4 relevant expert domains
                    - **Iterate Deeply**: More iterations = more thorough analysis
                    - **Model Selection**: GPT-4 or Claude-3 for complex problems
                    """)

            with gr.Row():
                results_output = gr.Textbox(
                    lines=25,
                    label="🎯 Nova Process Results",
                    show_copy_button=True,
                    max_lines=50
                )

            with gr.Row():
                session_info = gr.Textbox(
                    lines=2,
                    label="📋 Session Information",
                    show_copy_button=True
                )

            with gr.Row():
                performance_metrics = gr.Textbox(
                    lines=3,
                    label="📊 Performance Metrics",
                    show_copy_button=True
                )

            solve_btn.click(
                fn=self.run_nova_process,
                inputs=[problem_input, domains_input, iterations_input, model_input, save_session, export_format],
                outputs=[results_output, session_info, performance_metrics]
            )

    def _build_session_history_tab(self):
        """Session history tab."""
        with gr.Tab("📚 Session History"):
            history_btn = gr.Button("📖 Load Session History")
            history_output = gr.Textbox(
                lines=20,
                label="📚 Recent Sessions",
                show_copy_button=True
            )
            history_btn.click(
                fn=self.get_session_history,
                outputs=[history_output]
            )

    def _build_performance_tab(self):
        """Performance analytics tab."""
        with gr.Tab("📈 Performance Analytics"):
            stats_btn = gr.Button("📊 Load Performance Statistics")
            stats_output = gr.Textbox(
                lines=20,
                label="📈 Performance Statistics",
                show_copy_button=True
            )
            stats_btn.click(
                fn=self.get_performance_stats,
                outputs=[stats_output]
            )

    def _build_system_info_tab(self):
        """System info/help tab."""
        with gr.Tab("⚙️ System Info"):
            gr.Markdown("### 🔧 System Information")
            gr.Markdown(f"""
            - **Version**: NovaSystem v2.0
            - **Interface**: Advanced Gradio Interface
            - **Features**: Multi-agent AI, Session Management, Performance Tracking
            - **Supported Models**: OpenAI, Anthropic, Ollama
            - **Export Formats**: Text, Markdown, JSON
            - **Session Storage**: In-memory (temporary)
            """)

            gr.Markdown("### 🚀 Quick Start Guide")
            gr.Markdown("""
            1. **Describe your problem** in detail in the Problem Description field
            2. **Select expertise domains** relevant to your challenge
            3. **Choose iteration depth** based on problem complexity
            4. **Select AI model** based on your needs and availability
            5. **Click Solve Problem** and watch our AI experts collaborate!
            """)

    def launch(self, share: bool = False, server_name: str = "0.0.0.0", server_port: int = 7860):
        """Launch the Gradio interface."""
        interface = self.create_interface()
        interface.launch(
            share=share,
            server_name=server_name,
            server_port=server_port,
            show_error=True,
            quiet=False
        )

def main():
    """Main function to run the Gradio interface."""
    interface = GradioInterface()
    interface.launch()

if __name__ == "__main__":
    main()
