"""Domain Expert Agents.

Domain experts provide specialized knowledge for specific fields.
They are dynamically created based on the problem requirements.
"""

from typing import Any, Dict, List
from .base import BaseAgent, AgentResponse


# Pre-defined domain expertise templates
DOMAIN_TEMPLATES = {
    "technology": {
        "name": "Technology Expert",
        "focus": "software architecture, scalability, technical implementation, DevOps, security",
        "perspective": "technical feasibility and best practices"
    },
    "tech": {  # Alias
        "name": "Technology Expert",
        "focus": "software architecture, scalability, technical implementation, DevOps, security",
        "perspective": "technical feasibility and best practices"
    },
    "business": {
        "name": "Business Strategy Expert",
        "focus": "market analysis, business models, ROI, competitive advantage, go-to-market",
        "perspective": "business viability and strategic value"
    },
    "security": {
        "name": "Security Expert",
        "focus": "threat modeling, vulnerabilities, compliance, data protection, access control",
        "perspective": "security posture and risk mitigation"
    },
    "ux": {
        "name": "User Experience Expert",
        "focus": "user research, usability, accessibility, interaction design, user journeys",
        "perspective": "user needs and experience quality"
    },
    "data": {
        "name": "Data & Analytics Expert",
        "focus": "data architecture, analytics, ML/AI, data governance, insights",
        "perspective": "data-driven decision making"
    },
    "operations": {
        "name": "Operations Expert",
        "focus": "process optimization, resource management, logistics, efficiency",
        "perspective": "operational excellence and efficiency"
    },
    "legal": {
        "name": "Legal & Compliance Expert",
        "focus": "regulatory requirements, contracts, intellectual property, liability",
        "perspective": "legal compliance and risk"
    },
    "finance": {
        "name": "Finance Expert",
        "focus": "budgeting, financial modeling, cost analysis, investment",
        "perspective": "financial viability and resource allocation"
    }
}


class DomainExpert(BaseAgent):
    """
    Domain Expert - Specialized knowledge provider.

    Created dynamically based on the problem domain.
    Provides deep expertise in a specific field.
    """

    def __init__(
        self,
        domain: str,
        name: str = None,
        focus: str = None,
        perspective: str = None,
        llm_provider=None
    ):
        self.domain = domain.lower()

        # Use template if available, otherwise create custom
        template = DOMAIN_TEMPLATES.get(self.domain, {})

        self._name = name or template.get("name", f"{domain.title()} Expert")
        self._focus = focus or template.get("focus", domain)
        self._perspective = perspective or template.get("perspective", f"{domain} considerations")

        super().__init__(
            name=self._name,
            agent_type=f"domain_{self.domain}",
            llm_provider=llm_provider
        )

    @property
    def system_prompt(self) -> str:
        return f"""You are a world-class expert in {self.domain}.

Your Role: Deep Technical Specialist.

Your Goal:

Provide concrete, actionable, and highly technical implementation details.

- Avoid general advice (e.g., "Use a database").

- Propose specific technologies (e.g., "Use PostgreSQL 16 with Partitions").

- Provide architectural patterns or code snippets where relevant.

- Focus ONLY on {self.domain}. Do not try to solve the business or marketing side.

Tone:

- Authoritative and precise.

- Dense with information.

- No fluff."""

    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Provide domain-specific analysis."""
        problem = input_data.get("problem", "")
        dce_analysis = input_data.get("dce_analysis", "")

        prompt = f"""Provide your {self._name} perspective on the following problem.

PROBLEM:
{problem}

PROBLEM BREAKDOWN:
{dce_analysis}

From your domain expertise in {self._focus}, please provide:

1. **Domain Relevance**: How does this problem intersect with your expertise?
2. **Key Insights**: What does your domain knowledge reveal?
3. **Best Practices**: What approaches are recommended in your field?
4. **Opportunities**: What possibilities does your expertise open up?
5. **Domain Risks**: What field-specific concerns should be addressed?
6. **Recommendations**: Your specific advice from a {self.domain} perspective"""

        try:
            content = await self._call_llm(prompt)
            return self._create_response(
                content=content,
                metadata={"domain": self.domain, "focus": self._focus}
            )
        except Exception as e:
            return self._create_response(
                content="",
                success=False,
                error=str(e)
            )


def create_domain_expert(
    domain: str,
    llm_provider=None,
    custom_name: str = None,
    custom_focus: str = None,
    custom_perspective: str = None
) -> DomainExpert:
    """
    Factory function to create domain experts.

    Args:
        domain: The domain/field of expertise
        llm_provider: LLM provider for the agent
        custom_name: Override the default name
        custom_focus: Override the default focus areas
        custom_perspective: Override the default perspective

    Returns:
        A configured DomainExpert instance
    """
    return DomainExpert(
        domain=domain,
        name=custom_name,
        focus=custom_focus,
        perspective=custom_perspective,
        llm_provider=llm_provider
    )


def get_available_domains() -> List[str]:
    """Return list of pre-defined domain templates."""
    return list(DOMAIN_TEMPLATES.keys())
