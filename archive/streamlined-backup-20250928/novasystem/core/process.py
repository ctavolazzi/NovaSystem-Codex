"""
Nova Process Orchestration.

This module implements the core Nova Process workflow that coordinates
multiple agents to solve complex problems through iterative refinement.
"""

from typing import Dict, List, Any, Optional, AsyncGenerator
import asyncio
import logging
from datetime import datetime
import json

from .agents import BaseAgent, DCEAgent, CAEAgent, DomainExpert, AgentFactory
from .memory import MemoryManager
from ..utils.llm_service import LLMService
from ..utils.metrics import get_metrics_collector, PerformanceMetrics

logger = logging.getLogger(__name__)

class NovaProcess:
    """
    Main orchestrator for the Nova Process.

    Coordinates multiple agents to solve complex problems through structured
    iterative refinement.
    """

    def __init__(self,
                 domains: List[str] = None,
                 model: str = "gpt-5-nano",
                 memory_manager: Optional[MemoryManager] = None,
                 llm_service: Optional[LLMService] = None):
        """
        Initialize the Nova Process.

        Args:
            domains: List of domain expertise areas
            model: LLM model to use
            memory_manager: Optional memory manager for context
            llm_service: Optional LLM service for AI calls
        """
        self.domains = domains or ["General"]
        self.memory_manager = memory_manager or MemoryManager()
        self.llm_service = llm_service or LLMService()
        self.metrics_collector = get_metrics_collector()

        # Use default model from LLM service if not specified
        if model == "gpt-4o":
            self.model = self.llm_service.get_default_model()
        else:
            self.model = model

        # Create agent team with LLM service
        self.agents = AgentFactory.create_agent_team(self.domains, self.model, self.llm_service)
        self.dce = self.agents["dce"]
        self.cae = self.agents["cae"]
        self.domain_experts = {k: v for k, v in self.agents.items()
                              if k.startswith("expert_")}

        # Process state
        self.current_iteration = 0
        self.problem_statement = ""
        self.solution_history = []
        self.is_active = False

    async def solve_problem(self,
                          problem_statement: str,
                          max_iterations: int = 5,
                          stream: bool = False,
                          session_id: str = None):
        """
        Solve a problem using the Nova Process.

        Args:
            problem_statement: The problem to solve
            max_iterations: Maximum number of iterations
            stream: Whether to stream results
            session_id: Optional session ID for metrics tracking

        Returns:
            Final result if not streaming, or AsyncGenerator if streaming
        """
        # Start metrics collection
        if session_id:
            self.metrics_collector.start_session(session_id)
            self.metrics_collector.record_memory_usage()

        try:
            if stream:
                return self._solve_problem_streaming(problem_statement, max_iterations)
            else:
                return await self._solve_problem_sync(problem_statement, max_iterations)
        finally:
            # End metrics collection
            if session_id:
                self.metrics_collector.record_memory_usage()
                metrics = self.metrics_collector.end_session(session_id)
                if metrics:
                    logger.info(f"Session {session_id} completed with metrics: {metrics.to_dict()}")

    async def _solve_problem_sync(self, problem_statement: str, max_iterations: int) -> Dict[str, Any]:
        """Solve problem synchronously (no streaming)."""
        self.problem_statement = problem_statement
        self.current_iteration = 0
        self.solution_history = []
        self.is_active = True

        # Store initial problem
        await self.memory_manager.store_context("problem", problem_statement)

        try:
            # Problem Unpacking Phase
            unpacking_result = await self._problem_unpacking_phase(False)

            # Iterative Refinement Phase
            for iteration in range(max_iterations):
                self.current_iteration = iteration + 1
                iteration_result = await self._iteration_phase(iteration + 1, False)
                self.solution_history.append(iteration_result)

                # Record iteration metrics
                self.metrics_collector.record_iteration()
                self.metrics_collector.record_memory_usage()

                # Check for convergence
                if await self._check_convergence(iteration_result):
                    break

            # Final Synthesis
            final_result = await self._final_synthesis_phase(False)
            return final_result

        except Exception as e:
            logger.error(f"Error in Nova Process: {str(e)}")
            raise
        finally:
            self.is_active = False

    async def _solve_problem_streaming(self, problem_statement: str, max_iterations: int) -> AsyncGenerator[Dict[str, Any], None]:
        """Solve problem with streaming updates."""
        self.problem_statement = problem_statement
        self.current_iteration = 0
        self.solution_history = []
        self.is_active = True

        # Store initial problem
        await self.memory_manager.store_context("problem", problem_statement)

        yield {
            "type": "start",
            "problem": problem_statement,
            "timestamp": datetime.now().isoformat()
        }

        try:
            # Problem Unpacking Phase
            yield {"type": "phase", "phase": "problem_unpacking"}

            unpacking_result = await self._problem_unpacking_phase(True)
            yield {"type": "result", "phase": "problem_unpacking", "result": unpacking_result}

            # Iterative Refinement Phase
            for iteration in range(max_iterations):
                self.current_iteration = iteration + 1

                yield {"type": "iteration", "number": self.current_iteration}

                iteration_result = await self._iteration_phase(iteration + 1, True)
                self.solution_history.append(iteration_result)

                yield {"type": "result", "iteration": self.current_iteration, "result": iteration_result}

                # Check for convergence
                if await self._check_convergence(iteration_result):
                    yield {"type": "convergence", "iteration": self.current_iteration}
                    break

            # Final Synthesis
            yield {"type": "phase", "phase": "final_synthesis"}

            final_result = await self._final_synthesis_phase(True)
            yield {"type": "complete", "result": final_result}

        except Exception as e:
            logger.error(f"Error in Nova Process: {str(e)}")
            yield {"type": "error", "error": str(e)}
        finally:
            self.is_active = False

    async def _problem_unpacking_phase(self, stream: bool = False) -> Dict[str, Any]:
        """Phase 1: Problem Unpacking - Break down the problem."""

        # Get domain expert analysis
        domain_insights = {}
        for domain, expert in self.domain_experts.items():
            insight = await expert.process(
                f"Analyze this problem in detail: {self.problem_statement}"
            )
            domain_insights[domain] = insight

        # DCE synthesis
        dce_summary = await self.dce.process(
            f"Summarize and synthesize these domain insights: {json.dumps(domain_insights)}"
        )

        # CAE critical analysis
        cae_analysis = await self.cae.process(
            f"Critically analyze this problem breakdown: {dce_summary}"
        )

        result = {
            "domain_insights": domain_insights,
            "dce_synthesis": dce_summary,
            "cae_analysis": cae_analysis,
            "phase": "problem_unpacking"
        }

        await self.memory_manager.store_context("problem_unpacking", result)
        return result

    async def _iteration_phase(self, iteration: int, stream: bool = False) -> Dict[str, Any]:
        """Phase 2: Iterative Refinement - Refine solutions."""

        # Get context from previous iterations
        context = await self.memory_manager.get_relevant_context(
            f"iteration {iteration} refinement"
        )

        # Domain experts propose solutions
        expert_solutions = {}
        for domain, expert in self.domain_experts.items():
            solution = await expert.process(
                f"Based on the problem and previous work, propose a solution: {context}"
            )
            expert_solutions[domain] = solution

        # DCE coordination
        dce_coordination = await self.dce.process(
            f"Coordinate these solutions and identify next steps: {json.dumps(expert_solutions)}"
        )

        # CAE critical evaluation
        cae_evaluation = await self.cae.process(
            f"Critically evaluate this iteration: {dce_coordination}"
        )

        result = {
            "iteration": iteration,
            "expert_solutions": expert_solutions,
            "dce_coordination": dce_coordination,
            "cae_evaluation": cae_evaluation,
            "phase": "iteration"
        }

        await self.memory_manager.store_context(f"iteration_{iteration}", result)
        return result

    async def _final_synthesis_phase(self, stream: bool = False) -> Dict[str, Any]:
        """Phase 3: Final Synthesis - Create final solution."""

        # Get all context
        all_context = await self.memory_manager.get_all_context()

        # DCE final synthesis
        final_synthesis = await self.dce.process(
            f"Create a final synthesis of all work: {json.dumps(all_context)}"
        )

        # CAE final validation
        final_validation = await self.cae.process(
            f"Provide final validation and recommendations: {final_synthesis}"
        )

        result = {
            "final_synthesis": final_synthesis,
            "final_validation": final_validation,
            "total_iterations": self.current_iteration,
            "phase": "final_synthesis"
        }

        await self.memory_manager.store_context("final_result", result)
        return result

    async def _check_convergence(self, iteration_result: Dict[str, Any]) -> bool:
        """Check if the process has converged to a solution."""
        # Simple convergence check - can be enhanced
        cae_evaluation = iteration_result.get("cae_evaluation", "")

        # Look for convergence indicators
        convergence_indicators = [
            "solution is complete",
            "no further improvements needed",
            "ready for implementation",
            "converged"
        ]

        return any(indicator in cae_evaluation.lower()
                  for indicator in convergence_indicators)

    def get_status(self) -> Dict[str, Any]:
        """Get current process status."""
        return {
            "is_active": self.is_active,
            "current_iteration": self.current_iteration,
            "total_iterations": len(self.solution_history),
            "problem_statement": self.problem_statement,
            "domains": self.domains,
            "model": self.model
        }

    def get_solution_history(self) -> List[Dict[str, Any]]:
        """Get the history of solution iterations."""
        return self.solution_history.copy()

    def get_performance_metrics(self, session_id: str = None) -> Dict[str, Any]:
        """Get performance metrics for the current or specified session."""
        if session_id:
            return self.metrics_collector.get_session_summary(session_id)
        else:
            return self.metrics_collector.get_performance_summary()

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system performance metrics."""
        return self.metrics_collector.get_system_metrics()
