"""
Gradio Interface for NovaSystem.

This module provides a simple Gradio-based web interface for the Nova Process.
"""

import gradio as gr
import asyncio
import json
import time
import os
from typing import Dict, Any, List
import logging
from datetime import datetime

from ..core.process import NovaProcess
from ..core.memory import MemoryManager

logger = logging.getLogger(__name__)

class GradioInterface:
    """Gradio interface for NovaSystem."""

    def __init__(self):
        self.current_process = None
        self.session_history = []
        self.performance_metrics = {}
        self.model_performance = {}

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
        if not problem.strip():
            return ("Please enter a problem statement first!", "", "")

        start_time = time.time()
        session_id = f"session_{int(time.time())}"

        try:
            # Parse domains
            domain_list = [d.strip() for d in domains.split(",") if d.strip()]

            # Create Nova Process
            memory_manager = MemoryManager()
            nova_process = NovaProcess(
                domains=domain_list,
                model=model,
                memory_manager=memory_manager
            )

            # Run the process
            result = asyncio.run(nova_process.solve_problem(
                problem,
                max_iterations=max_iterations,
                stream=False
            ))

            # Calculate performance metrics
            end_time = time.time()
            duration = end_time - start_time

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

            # Format the result based on export format
            formatted_result = self._format_result(result, export_format)

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

            return (formatted_result, session_info, performance_info)

        except Exception as e:
            logger.error(f"Error in Nova Process: {str(e)}")
            error_msg = f"Error: {str(e)}\n\nPlease try again with a more specific problem statement."
            return (error_msg, f"Session {session_id} failed", f"Error occurred after {time.time() - start_time:.2f} seconds")

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

            with gr.Tab("🎯 Problem Solver"):
                with gr.Row():
                    with gr.Column(scale=2):
                        problem_input = gr.Textbox(
                            lines=6,
                            placeholder="Describe your problem or challenge in detail. Be specific about context, constraints, and desired outcomes...",
                            label="🧠 Problem Description",
                            info="💡 The more detailed your description, the better our AI experts can help you"
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
                                choices=[
                                    "gpt-4",
                                    "gpt-3.5-turbo",
                                    "claude-3",
                                    "claude-3-haiku",
                                    "claude-3-sonnet",
                                    "ollama:phi3",
                                    "ollama:llama2",
                                    "ollama:gpt-oss:20b",
                                    "ollama:mistral"
                                ],
                                value="gpt-4",
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

        return interface

    def launch(self, share: bool = False, server_name: str = "0.0.0.0", server_port: int = 7860, mcp_server: bool = True):
        """Launch the Gradio interface with optional MCP server."""
        interface = self.create_interface()
        interface.launch(
            share=share,
            server_name=server_name,
            server_port=server_port,
            show_error=True,
            quiet=False,
            mcp_server=mcp_server
        )

def main():
    """Main function to run the Gradio interface."""
    interface = GradioInterface()
    interface.launch()

if __name__ == "__main__":
    main()
