"""Discussion Continuity Expert (DCE) Agent.

The DCE is responsible for:
1. Unpacking the problem statement
2. Identifying key components and stakeholders
3. Framing the discussion for other agents
4. Synthesizing final responses
"""

from typing import Any, Dict
from .base import BaseAgent, AgentResponse


class DCEAgent(BaseAgent):
    """
    Discussion Continuity Expert - The facilitator and synthesizer.

    Phase 1 (Unpack): Break down the problem into components
    Phase 3 (Synthesize): Combine all agent responses into coherent output
    """

    def __init__(self, llm_provider=None):
        super().__init__(
            name="Discussion Continuity Expert",
            agent_type="dce",
            llm_provider=llm_provider
        )

    @property
    def system_prompt(self) -> str:
        return """You are the Discussion Continuity Expert (DCE), a skilled facilitator and synthesizer.

Your responsibilities:
1. UNPACK problems into clear, actionable components
2. IDENTIFY key stakeholders, constraints, and success criteria
3. FRAME questions to guide domain experts
4. SYNTHESIZE diverse perspectives into coherent recommendations

Communication style:
- Clear and structured
- Use bullet points and headers for organization
- Ask clarifying questions when needed
- Bridge different viewpoints constructively

When unpacking a problem:
- What is the core challenge?
- Who are the stakeholders?
- What constraints exist?
- What does success look like?
- What questions need expert input?

When synthesizing:
- Acknowledge all perspectives
- Highlight areas of agreement
- Address conflicts constructively
- Provide actionable next steps"""

    @property
    def synthesis_system_prompt(self) -> str:
        return """You are the Discussion Continuity Expert (DCE).

Your Role: The Architect and Decision Maker.

Your Input:

1. Technical proposals from Domain Experts (The Thesis).

2. Risk assessments from the CAE (The Antithesis).

Your Goal:

Create a SYNTHESIS. Do not just summarize what the others said.

- Resolve the conflicts. If the Tech Expert says "Speed" and CAE says "Security," propose the specific compromise (e.g., "Fast release cycle but with automated compliance scanning").

- Create a unified, step-by-step solution.

- Be decisive.

Structure your response:

1. The Core Solution (The "One Way" forward).

2. Key Trade-offs (Acknowledging the CAE's valid points).

3. Implementation Plan (Steps to execute)."""

    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Process the problem - either unpack or synthesize based on phase."""
        problem = input_data.get("problem", "")
        phase = input_data.get("phase", "unpack")

        if phase == "unpack":
            return await self._unpack(problem)
        elif phase == "synthesize":
            agent_responses = input_data.get("agent_responses", [])
            return await self._synthesize(problem, agent_responses)
        else:
            return self._create_response(
                content="Unknown phase",
                success=False,
                error=f"Unknown phase: {phase}"
            )

    async def _unpack(self, problem: str) -> AgentResponse:
        """Unpack the problem into components."""
        prompt = f"""Please unpack the following problem/question:

PROBLEM:
{problem}

Provide a structured analysis with:
1. **Core Challenge**: What is the fundamental issue?
2. **Key Components**: Break down the problem
3. **Stakeholders**: Who is affected?
4. **Constraints**: What limitations exist?
5. **Success Criteria**: How will we know the solution works?
6. **Questions for Experts**: What do we need domain expertise on?"""

        try:
            content = await self._call_llm(prompt)
            return self._create_response(
                content=content,
                metadata={"phase": "unpack"}
            )
        except Exception as e:
            return self._create_response(
                content="",
                success=False,
                error=str(e)
            )

    async def _synthesize(
        self,
        problem: str,
        agent_responses: list
    ) -> AgentResponse:
        """Synthesize all agent responses into a coherent recommendation."""
        responses_text = "\n\n".join([
            f"**{r.agent_name}**:\n{r.content}"
            for r in agent_responses
        ])

        user_prompt = f"""Synthesize the following expert analyses into a coherent recommendation.

ORIGINAL PROBLEM:
{problem}

EXPERT ANALYSES:
{responses_text}

Please provide:
1. **Summary**: Key insights from all experts
2. **Consensus Points**: Where experts agree
3. **Divergent Views**: Where perspectives differ (and why both may be valid)
4. **Recommended Approach**: Your synthesized recommendation
5. **Next Steps**: Concrete actions to take
6. **Open Questions**: What still needs investigation"""

        try:
            # Use synthesis prompt instead of default system prompt
            if self.llm is None:
                content = f"[{self.name}] LLM not configured - mock response for synthesis"
            else:
                content = await self.llm.chat(
                    system_prompt=self.synthesis_system_prompt,
                    user_message=user_prompt
                )

            return self._create_response(
                content=content,
                metadata={"phase": "synthesize", "sources": len(agent_responses)}
            )
        except Exception as e:
            return self._create_response(
                content="",
                success=False,
                error=str(e)
            )
