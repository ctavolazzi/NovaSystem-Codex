#!/usr/bin/env python3
"""
Streaming Experts Demo for NovaSystem.

Demonstrates expert-by-expert, token-by-token streaming:
- DCE (Discussion Continuity Expert) streams first
- CAE (Critical Analysis Expert) streams second
- Domain Experts stream based on the problem domains

Each expert's response streams to the console in real-time,
with color-coded output for easy identification.

Usage:
    python streaming_experts_demo.py
    python streaming_experts_demo.py --problem "Your problem here"
    python streaming_experts_demo.py --domains "AI,Security,Performance"
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, AsyncGenerator

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from novasystem.core.agents import (
    AgentFactory,
    BaseAgent,
    DCEAgent,
    CAEAgent,
    DomainExpert,
    Colors,
    AGENT_COLORS
)
from novasystem.utils.llm_service import LLMService


class StreamingNovaProcess:
    """
    Streaming Nova Process that runs experts sequentially,
    streaming each response token by token.
    """

    def __init__(self, domains: List[str] = None, model: str = None):
        """
        Initialize the streaming Nova Process.

        Args:
            domains: List of domain expertise areas
            model: LLM model to use
        """
        self.domains = domains or ["General Problem Solving"]
        self.model = model

        print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}🚀 Initializing Streaming Nova Process{Colors.END}")
        print(f"{'='*70}")

        # Initialize shared LLM service
        self.llm_service = LLMService()

        # Create agents
        self.dce = AgentFactory.create_dce(model=model, llm_service=self.llm_service)
        self.cae = AgentFactory.create_cae(model=model, llm_service=self.llm_service)
        self.domain_experts = [
            AgentFactory.create_domain_expert(domain, model=model, llm_service=self.llm_service)
            for domain in self.domains
        ]

        print(f"\n✅ Created {2 + len(self.domain_experts)} experts:")
        print(f"   • DCE (Discussion Continuity Expert)")
        print(f"   • CAE (Critical Analysis Expert)")
        for domain in self.domains:
            print(f"   • Domain Expert ({domain})")
        print()

    async def run(self, problem: str) -> dict:
        """
        Run the Nova Process with streaming output.

        Each expert streams their response in real-time.

        Args:
            problem: The problem to solve

        Returns:
            Dictionary with all expert responses
        """
        print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}📋 PROBLEM{Colors.END}")
        print(f"{'='*70}")
        print(f"{problem}\n")
        print(f"{Colors.BOLD}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}🎭 EXPERT ANALYSIS (Streaming){Colors.END}")
        print(f"{'='*70}\n")

        results = {
            "problem": problem,
            "timestamp": datetime.now().isoformat(),
            "experts": {}
        }

        accumulated_context = f"Problem: {problem}\n\n"

        # Phase 1: DCE initial analysis
        print(f"\n{Colors.CYAN}Phase 1: Initial Analysis by DCE{Colors.END}\n")
        dce_response = await self._stream_agent(
            self.dce,
            f"Analyze this problem and provide an initial assessment:\n\n{problem}",
            context=None
        )
        results["experts"]["dce_initial"] = dce_response
        accumulated_context += f"DCE Analysis:\n{dce_response}\n\n"

        # Phase 2: Domain Experts provide insights
        print(f"\n{Colors.GREEN}Phase 2: Domain Expert Insights{Colors.END}\n")
        for expert in self.domain_experts:
            expert_response = await self._stream_agent(
                expert,
                f"Provide your specialized perspective on this problem:\n\n{problem}",
                context=accumulated_context
            )
            results["experts"][expert.domain] = expert_response
            accumulated_context += f"{expert.name} Analysis:\n{expert_response}\n\n"

        # Phase 3: CAE critical analysis
        print(f"\n{Colors.YELLOW}Phase 3: Critical Analysis by CAE{Colors.END}\n")
        cae_response = await self._stream_agent(
            self.cae,
            "Review all the insights provided and identify potential issues, risks, or alternative approaches.",
            context=accumulated_context
        )
        results["experts"]["cae"] = cae_response
        accumulated_context += f"CAE Analysis:\n{cae_response}\n\n"

        # Phase 4: DCE synthesis
        print(f"\n{Colors.CYAN}Phase 4: Synthesis by DCE{Colors.END}\n")
        synthesis_response = await self._stream_agent(
            self.dce,
            "Synthesize all the insights and provide a final comprehensive response.",
            context=accumulated_context
        )
        results["experts"]["dce_synthesis"] = synthesis_response

        # Final summary
        print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}✨ NOVA PROCESS COMPLETE{Colors.END}")
        print(f"{'='*70}")
        print(f"\n📊 Summary:")
        print(f"   • Experts consulted: {len(results['experts'])}")
        print(f"   • Total response length: {sum(len(v) for v in results['experts'].values())} characters")
        print(f"   • Timestamp: {results['timestamp']}")
        print()

        return results

    async def _stream_agent(
        self,
        agent: BaseAgent,
        task: str,
        context: str = None
    ) -> str:
        """Stream an agent's response and collect the full text."""
        full_response = []
        async for chunk in agent.process_stream(task, context):
            full_response.append(chunk)
        return "".join(full_response)


async def demo_basic():
    """Basic demo with a simple problem."""
    process = StreamingNovaProcess(
        domains=["Software Engineering", "System Design"]
    )

    await process.run(
        "Design a scalable real-time notification system that can handle "
        "millions of concurrent users with low latency requirements."
    )


async def demo_custom(problem: str, domains: List[str]):
    """Demo with custom problem and domains."""
    process = StreamingNovaProcess(domains=domains)
    await process.run(problem)


async def demo_single_expert():
    """Demo showing just one expert streaming."""
    print(f"\n{Colors.BOLD}Single Expert Streaming Demo{Colors.END}\n")

    llm_service = LLMService()
    expert = DomainExpert("AI/ML", llm_service=llm_service)

    print("Streaming response from Domain Expert (AI/ML)...\n")

    async for chunk in expert.process_stream(
        "Explain the key considerations for deploying a machine learning model in production.",
        context="This is for a web application serving 100k users daily."
    ):
        pass  # The streaming already prints to console

    print("\n✅ Streaming complete!")


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Streaming Experts Demo")
    parser.add_argument(
        "--problem",
        type=str,
        help="Problem to solve"
    )
    parser.add_argument(
        "--domains",
        type=str,
        default="Software Engineering,System Design",
        help="Comma-separated list of domain expertise"
    )
    parser.add_argument(
        "--demo",
        choices=["basic", "single"],
        default="basic",
        help="Demo type to run"
    )

    args = parser.parse_args()

    # Check API key
    if not os.getenv("GEMINI_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: No API keys found. Set GEMINI_API_KEY or OPENAI_API_KEY")
        print("   The demo may fail or use local models only.\n")

    if args.demo == "single":
        await demo_single_expert()
    elif args.problem:
        domains = [d.strip() for d in args.domains.split(",")]
        await demo_custom(args.problem, domains)
    else:
        await demo_basic()


if __name__ == "__main__":
    asyncio.run(main())
