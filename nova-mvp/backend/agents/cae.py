"""Critical Analysis Expert (CAE) Agent.

The CAE is responsible for:
1. Identifying potential issues, risks, and edge cases
2. Playing devil's advocate
3. Ensuring robustness of solutions
4. Highlighting what could go wrong
"""

from typing import Any, Dict
from .base import BaseAgent, AgentResponse


class CAEAgent(BaseAgent):
    """
    Critical Analysis Expert - The skeptic and risk identifier.

    Ensures solutions are robust by:
    - Identifying edge cases
    - Highlighting risks
    - Questioning assumptions
    - Stress-testing proposals
    """

    def __init__(self, llm_provider=None):
        super().__init__(
            name="Critical Analysis Expert",
            agent_type="cae",
            llm_provider=llm_provider
        )

    @property
    def system_prompt(self) -> str:
        return """You are the Critical Analysis Expert (CAE), a rigorous analyst and constructive skeptic.

Your responsibilities:
1. IDENTIFY risks, edge cases, and potential failures
2. QUESTION assumptions that others might take for granted
3. STRESS-TEST proposals and solutions
4. ENSURE robustness and completeness

Communication style:
- Direct but constructive
- Evidence-based concerns
- Always offer mitigation strategies
- Distinguish between critical and minor issues

When analyzing:
- What assumptions are being made?
- What could go wrong?
- What edge cases exist?
- What hasn't been considered?
- How might this fail at scale?
- What are the second-order effects?

Remember: Your role is not to block progress but to make solutions stronger.
Every criticism should come with a constructive suggestion when possible."""

    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Analyze the problem and DCE's framing for risks and issues."""
        problem = input_data.get("problem", "")
        dce_analysis = input_data.get("dce_analysis", "")

        prompt = f"""Provide critical analysis of the following problem and initial framing.

PROBLEM:
{problem}

INITIAL ANALYSIS:
{dce_analysis}

Please provide:
1. **Assumption Check**: What assumptions are being made? Which are risky?
2. **Risk Assessment**: What could go wrong? Rate severity (High/Medium/Low)
3. **Edge Cases**: What unusual scenarios need consideration?
4. **Blind Spots**: What hasn't been adequately addressed?
5. **Scale Considerations**: How might this behave differently at scale?
6. **Mitigation Strategies**: For each major risk, suggest a mitigation

Be constructive - the goal is to strengthen the solution, not block it."""

        try:
            content = await self._call_llm(prompt)
            return self._create_response(
                content=content,
                metadata={"analysis_type": "critical"}
            )
        except Exception as e:
            return self._create_response(
                content="",
                success=False,
                error=str(e)
            )
