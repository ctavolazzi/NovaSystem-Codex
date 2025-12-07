"""
Nova Process Orchestration.

Coordinates multiple agents to solve complex problems through iterative refinement.
"""

from typing import Dict, List, Any, Optional, AsyncGenerator
import asyncio
import logging
import json
from datetime import datetime

from .agents import AgentFactory, BaseAgent
from .memory import MemoryManager
from ..utils.llm_service import LLMService
from ..utils.metrics import get_metrics_collector
from ..config.models import get_default_model

logger = logging.getLogger(__name__)


# Convergence indicators
CONVERGENCE_INDICATORS = [
    "solution is complete",
    "no further improvements needed",
    "ready for implementation",
    "converged",
]


class NovaProcess:
    """
    Main orchestrator for the Nova Process.

    Coordinates multiple agents to solve complex problems through structured
    iterative refinement.
    """

    def __init__(
        self,
        domains: List[str] = None,
        model: Optional[str] = None,
        memory_manager: Optional[MemoryManager] = None,
        llm_service: Optional[LLMService] = None
    ):
        """
        Initialize the Nova Process.

        Args:
            domains: List of domain expertise areas
            model: LLM model to use
            memory_manager: Optional memory manager for context
            llm_service: Optional LLM service for AI calls
        """
        self.domains = domains or ["General"]
        self.model = model or get_default_model()
        self.memory_manager = memory_manager or MemoryManager()
        self.llm_service = llm_service or LLMService()
        self.metrics_collector = get_metrics_collector()

        # Create agent team
        self.agents = AgentFactory.create_agent_team(self.domains, self.model, self.llm_service)
        self.dce = self.agents["dce"]
        self.cae = self.agents["cae"]
        self.domain_experts = {k: v for k, v in self.agents.items() if k.startswith("expert_")}

        # Process state
        self.current_iteration = 0
        self.problem_statement = ""
        self.solution_history: List[Dict[str, Any]] = []
        self.is_active = False

    async def solve_problem(
        self,
        problem_statement: str,
        max_iterations: int = 5,
        stream: bool = False,
        session_id: str = None
    ):
        """
        Solve a problem using the Nova Process.

        Args:
            problem_statement: The problem to solve
            max_iterations: Maximum number of iterations
            stream: Whether to stream results
            session_id: Optional session ID for metrics tracking

        Returns:
            Final result dict if not streaming, or AsyncGenerator if streaming
        """
        if session_id:
            self.metrics_collector.start_session(session_id)
            self.metrics_collector.record_memory_usage()

        try:
            if stream:
                return self._solve_streaming(problem_statement, max_iterations)
            return await self._solve_sync(problem_statement, max_iterations)
        finally:
            if session_id:
                self.metrics_collector.record_memory_usage()
                metrics = self.metrics_collector.end_session(session_id)
                if metrics:
                    logger.info(f"Session {session_id} completed: {metrics.to_dict()}")

    async def _solve_sync(self, problem: str, max_iterations: int) -> Dict[str, Any]:
        """Solve problem synchronously."""
        self._init_solve(problem)

        try:
            # Phase 1: Problem Unpacking
            unpacking = await self._problem_unpacking_phase()

            # Phase 2: Iterative Refinement
            for i in range(max_iterations):
                self.current_iteration = i + 1
                result = await self._iteration_phase(i + 1)
                self.solution_history.append(result)

                self.metrics_collector.record_iteration()
                self.metrics_collector.record_memory_usage()

                if self._check_convergence(result):
                    break

            # Phase 3: Final Synthesis
            return await self._final_synthesis_phase()

        except Exception as e:
            logger.error(f"Error in Nova Process: {e}")
            raise
        finally:
            self.is_active = False

    async def _solve_streaming(self, problem: str, max_iterations: int) -> AsyncGenerator[Dict[str, Any], None]:
        """Solve problem with streaming updates."""
        self._init_solve(problem)

        yield {"type": "start", "problem": problem, "timestamp": datetime.now().isoformat()}

        try:
            # Phase 1
            yield {"type": "phase", "phase": "problem_unpacking"}
            unpacking = await self._problem_unpacking_phase()
            yield {"type": "result", "phase": "problem_unpacking", "result": unpacking}

            # Phase 2
            for i in range(max_iterations):
                self.current_iteration = i + 1
                yield {"type": "iteration", "number": self.current_iteration}

                result = await self._iteration_phase(i + 1)
                self.solution_history.append(result)
                yield {"type": "result", "iteration": self.current_iteration, "result": result}

                if self._check_convergence(result):
                    yield {"type": "convergence", "iteration": self.current_iteration}
                    break

            # Phase 3
            yield {"type": "phase", "phase": "final_synthesis"}
            final = await self._final_synthesis_phase()
            yield {"type": "complete", "result": final}

        except Exception as e:
            logger.error(f"Error in Nova Process: {e}")
            yield {"type": "error", "error": str(e)}
        finally:
            self.is_active = False

    def _init_solve(self, problem: str):
        """Initialize solve state."""
        self.problem_statement = problem
        self.current_iteration = 0
        self.solution_history = []
        self.is_active = True

    async def _problem_unpacking_phase(self) -> Dict[str, Any]:
        """Phase 1: Break down the problem."""
        # Store problem
        await self.memory_manager.store_context("problem", self.problem_statement)

        # Get domain expert analysis
        domain_insights = {}
        for domain, expert in self.domain_experts.items():
            insight = await expert.process(f"Analyze this problem in detail: {self.problem_statement}")
            domain_insights[domain] = insight

        # DCE synthesis
        dce_summary = await self.dce.process(
            f"Summarize and synthesize these domain insights: {json.dumps(domain_insights)}"
        )

        # CAE critical analysis
        cae_analysis = await self.cae.process(f"Critically analyze this breakdown: {dce_summary}")

        result = {
            "domain_insights": domain_insights,
            "dce_synthesis": dce_summary,
            "cae_analysis": cae_analysis,
            "phase": "problem_unpacking"
        }

        await self.memory_manager.store_context("problem_unpacking", result)
        return result

    async def _iteration_phase(self, iteration: int) -> Dict[str, Any]:
        """Phase 2: Iterative refinement."""
        context = await self.memory_manager.get_relevant_context(f"iteration {iteration} refinement")

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

        # CAE evaluation
        cae_evaluation = await self.cae.process(f"Critically evaluate this iteration: {dce_coordination}")

        result = {
            "iteration": iteration,
            "expert_solutions": expert_solutions,
            "dce_coordination": dce_coordination,
            "cae_evaluation": cae_evaluation,
            "phase": "iteration"
        }

        await self.memory_manager.store_context(f"iteration_{iteration}", result)
        return result

    async def _final_synthesis_phase(self) -> Dict[str, Any]:
        """Phase 3: Create final solution."""
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

    def _check_convergence(self, iteration_result: Dict[str, Any]) -> bool:
        """Check if the process has converged."""
        cae_evaluation = iteration_result.get("cae_evaluation", "").lower()
        return any(indicator in cae_evaluation for indicator in CONVERGENCE_INDICATORS)

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
        """Get performance metrics."""
        if session_id:
            return self.metrics_collector.get_session_summary(session_id)
        return self.metrics_collector.get_performance_summary()

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system performance metrics."""
        return self.metrics_collector.get_system_metrics()
