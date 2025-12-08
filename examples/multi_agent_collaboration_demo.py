#!/usr/bin/env python3
"""
Multi-Agent Collaboration Demo
==============================

Demonstrates how multiple NovaSystem agents work together to solve a problem:
- DCE (Discussion Continuity Expert) - Orchestrates and synthesizes
- CAE (Critical Analysis Expert) - Provides critical evaluation
- Domain Experts - Provide specialized knowledge

This demo simulates the Nova Process without requiring actual LLM API calls.

Run:
    python examples/multi_agent_collaboration_demo.py
"""

import asyncio
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add parent to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


# =============================================================================
# Mock Agent System (simulates LLM responses)
# =============================================================================


@dataclass
class AgentResponse:
    """Response from an agent."""
    agent_name: str
    role: str
    content: str
    timestamp: datetime
    thinking_time: float


class MockAgent:
    """Base mock agent for demonstration."""

    def __init__(self, name: str, role: str, expertise: str):
        self.name = name
        self.role = role
        self.expertise = expertise
        self.conversation_history: List[Dict] = []

    async def process(self, problem: str, context: str = "") -> AgentResponse:
        """Simulate processing with realistic delay."""
        start = time.time()
        await asyncio.sleep(0.1)  # Simulate thinking time

        response = self._generate_response(problem, context)
        thinking_time = time.time() - start

        self.conversation_history.append({
            "input": problem,
            "output": response,
            "timestamp": datetime.now()
        })

        return AgentResponse(
            agent_name=self.name,
            role=self.role,
            content=response,
            timestamp=datetime.now(),
            thinking_time=thinking_time
        )

    def _generate_response(self, problem: str, context: str) -> str:
        """Override in subclasses to generate specific responses."""
        return f"[{self.name}] Generic response to: {problem[:50]}..."


class MockDCE(MockAgent):
    """Mock Discussion Continuity Expert."""

    def __init__(self):
        super().__init__(
            name="DCE",
            role="Discussion Continuity Expert",
            expertise="Orchestration and Synthesis"
        )
        self.phase = "unpack"

    def _generate_response(self, problem: str, context: str) -> str:
        if self.phase == "unpack":
            return f"""## Problem Analysis (UNPACK Phase)

### Understanding the Challenge
The problem presented is: "{problem[:100]}..."

### Key Components Identified:
1. **Core Challenge**: Determining the best approach for the given scenario
2. **Constraints**: Time, resources, and technical limitations
3. **Success Criteria**: Measurable outcomes that define success

### Questions for Exploration:
- What are the primary technical requirements?
- What trade-offs are acceptable?
- What is the timeline for implementation?

### Recommended Expert Consultation:
I suggest we consult domain experts in:
- Backend Architecture
- Security
- DevOps

*Proceeding to ANALYZE phase with expert consultations...*
"""
        elif self.phase == "synthesize":
            return f"""## Synthesized Recommendation (SYNTHESIZE Phase)

### Executive Summary
After analyzing input from all experts, here is our consolidated recommendation:

### Primary Recommendation
Based on the collective analysis, we recommend a **microservices architecture**
with the following characteristics:

1. **Architecture**: Event-driven microservices
2. **Technology Stack**: Python/FastAPI for services, PostgreSQL for data
3. **Deployment**: Kubernetes with GitOps workflow

### Implementation Roadmap
| Phase | Duration | Deliverables |
|-------|----------|--------------|
| Phase 1 | 2 weeks | Core services |
| Phase 2 | 2 weeks | Integration |
| Phase 3 | 1 week | Testing & Deployment |

### Risk Mitigation
{context if context else "- Monitor performance metrics continuously"}

### Consensus Score: 87%
All experts agree on the fundamental approach with minor variations in implementation details.

*Decision ready for stakeholder review.*
"""
        return "Processing..."


class MockCAE(MockAgent):
    """Mock Critical Analysis Expert."""

    def __init__(self):
        super().__init__(
            name="CAE",
            role="Critical Analysis Expert",
            expertise="Risk Assessment and Quality Assurance"
        )

    def _generate_response(self, problem: str, context: str) -> str:
        return f"""## Critical Analysis Report

### Risk Assessment 🔍

#### High Priority Concerns:
1. **Scalability Risk** (Medium)
   - Current design may face bottlenecks at 10K concurrent users
   - Mitigation: Implement horizontal scaling from the start

2. **Security Considerations** (High)
   - API endpoints need rate limiting
   - Data encryption at rest and in transit required

3. **Technical Debt Potential** (Low)
   - Clean architecture should prevent accumulation
   - Regular refactoring sprints recommended

### Alternative Approaches Considered:
| Approach | Pros | Cons | Recommendation |
|----------|------|------|----------------|
| Monolith | Simple | Scaling issues | Not recommended |
| Microservices | Scalable | Complexity | ✅ Recommended |
| Serverless | Cost-effective | Cold starts | Consider for specific functions |

### Validation Requirements:
- [ ] Load testing at 2x expected capacity
- [ ] Security penetration testing
- [ ] Code review by senior architect
- [ ] Disaster recovery drill

### Overall Assessment: ✅ PROCEED WITH CAUTION
The proposed approach is sound but requires attention to the identified risks.
"""


class MockDomainExpert(MockAgent):
    """Mock Domain Expert."""

    def __init__(self, domain: str):
        super().__init__(
            name=f"Expert ({domain})",
            role=f"Domain Expert in {domain}",
            expertise=domain
        )
        self.domain = domain

    def _generate_response(self, problem: str, context: str) -> str:
        responses = {
            "Backend Architecture": """## Backend Architecture Recommendations

### Recommended Stack:
- **Framework**: FastAPI (async, modern, fast)
- **Database**: PostgreSQL with async driver (asyncpg)
- **Cache**: Redis for session and query caching
- **Message Queue**: RabbitMQ for async tasks

### Architecture Pattern:
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   API GW    │────▶│   Services  │────▶│  Database   │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │
       ▼                   ▼
┌─────────────┐     ┌─────────────┐
│    Cache    │     │   Queue     │
└─────────────┘     └─────────────┘
```

### Best Practices:
1. Use dependency injection for testability
2. Implement circuit breakers for external calls
3. Design APIs contract-first using OpenAPI
4. Apply CQRS for read-heavy workloads
""",
            "Security": """## Security Recommendations

### Authentication & Authorization:
- **Method**: JWT with refresh tokens
- **Storage**: HTTP-only secure cookies
- **Sessions**: Server-side session validation

### Security Checklist:
✅ Input validation on all endpoints
✅ SQL injection prevention (parameterized queries)
✅ XSS protection (Content Security Policy)
✅ CSRF tokens for state-changing operations
✅ Rate limiting (100 req/min per user)
✅ API key rotation policy

### Compliance Considerations:
- GDPR: Data anonymization for EU users
- SOC2: Audit logging enabled
- PCI-DSS: Not storing card data directly

### Security Headers:
```
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'
```
""",
            "DevOps": """## DevOps & Deployment Strategy

### CI/CD Pipeline:
```
Code Push → Lint → Test → Build → Deploy (Staging) → Deploy (Prod)
    │         │       │       │           │               │
    └─────────┴───────┴───────┴───────────┴───────────────┘
                    Automated with GitHub Actions
```

### Infrastructure:
- **Container**: Docker with multi-stage builds
- **Orchestration**: Kubernetes (EKS/GKE)
- **IaC**: Terraform for all resources
- **Secrets**: HashiCorp Vault

### Monitoring Stack:
| Component | Tool | Purpose |
|-----------|------|---------|
| Metrics | Prometheus | System metrics |
| Logs | Loki | Centralized logging |
| Traces | Jaeger | Distributed tracing |
| Dashboards | Grafana | Visualization |

### SLA Targets:
- Uptime: 99.9%
- Response time: P95 < 200ms
- Recovery time: < 15 minutes
"""
        }
        return responses.get(self.domain, f"Expert analysis for {self.domain}...")


# =============================================================================
# Multi-Agent Orchestrator
# =============================================================================


class NovaProcessSimulator:
    """Simulates the Nova Process multi-agent collaboration."""

    def __init__(self):
        self.dce = MockDCE()
        self.cae = MockCAE()
        self.domain_experts: Dict[str, MockDomainExpert] = {}
        self.conversation_log: List[AgentResponse] = []

    def add_domain_expert(self, domain: str):
        """Add a domain expert to the team."""
        self.domain_experts[domain] = MockDomainExpert(domain)

    async def solve(self, problem: str) -> Dict[str, Any]:
        """Run the full Nova Process on a problem."""
        print("\n" + "=" * 70)
        print(" NOVA PROCESS: MULTI-AGENT COLLABORATION ".center(70, "="))
        print("=" * 70)
        print(f"\n📋 Problem: {problem[:100]}...")

        results = {
            "problem": problem,
            "phases": {},
            "start_time": datetime.now(),
            "agents_consulted": [],
        }

        # Phase 1: UNPACK
        print("\n" + "-" * 50)
        print("🔍 PHASE 1: UNPACK")
        print("-" * 50)

        self.dce.phase = "unpack"
        unpack_response = await self.dce.process(problem)
        self._print_agent_response(unpack_response)
        results["phases"]["unpack"] = unpack_response
        results["agents_consulted"].append(self.dce.name)

        # Phase 2: ANALYZE (parallel expert consultations)
        print("\n" + "-" * 50)
        print("🔬 PHASE 2: ANALYZE (Parallel Expert Consultation)")
        print("-" * 50)

        # Run experts in parallel
        expert_tasks = [
            expert.process(problem, unpack_response.content)
            for expert in self.domain_experts.values()
        ]

        # Add CAE analysis
        expert_tasks.append(self.cae.process(problem, unpack_response.content))

        expert_responses = await asyncio.gather(*expert_tasks)

        results["phases"]["analyze"] = []
        for response in expert_responses:
            self._print_agent_response(response)
            results["phases"]["analyze"].append(response)
            results["agents_consulted"].append(response.agent_name)

        # Phase 3: SYNTHESIZE
        print("\n" + "-" * 50)
        print("✨ PHASE 3: SYNTHESIZE")
        print("-" * 50)

        # Compile expert insights for synthesis
        expert_context = "\n".join([
            f"### {r.agent_name}\n{r.content[:200]}..."
            for r in expert_responses
        ])

        self.dce.phase = "synthesize"
        synthesis_response = await self.dce.process(problem, expert_context)
        self._print_agent_response(synthesis_response)
        results["phases"]["synthesize"] = synthesis_response

        # Summary
        results["end_time"] = datetime.now()
        results["total_time"] = (results["end_time"] - results["start_time"]).total_seconds()

        self._print_summary(results)

        return results

    def _print_agent_response(self, response: AgentResponse):
        """Print a formatted agent response."""
        colors = {
            "DCE": "\033[94m",  # Blue
            "CAE": "\033[93m",  # Yellow
            "Expert": "\033[92m",  # Green
        }

        color = "\033[0m"
        for key, val in colors.items():
            if key in response.agent_name:
                color = val
                break

        reset = "\033[0m"

        print(f"\n{color}{'─' * 50}")
        print(f"🤖 {response.agent_name} ({response.role})")
        print(f"⏱️  Thinking time: {response.thinking_time:.2f}s")
        print(f"{'─' * 50}{reset}")
        print(response.content)

    def _print_summary(self, results: Dict):
        """Print final summary."""
        print("\n" + "=" * 70)
        print(" NOVA PROCESS COMPLETE ".center(70, "="))
        print("=" * 70)
        print(f"""
📊 Session Summary:
   • Total Time: {results['total_time']:.2f}s
   • Agents Consulted: {len(results['agents_consulted'])}
   • Phases Completed: {len(results['phases'])}

🤝 Agent Team:
   {', '.join(results['agents_consulted'])}

✅ Status: Problem analysis complete
   Recommendation ready for stakeholder review.
""")


# =============================================================================
# Main Demo
# =============================================================================


async def main():
    """Run the multi-agent collaboration demo."""
    print("\n" + "🚀" * 35)
    print("\n  NOVASYSTEM MULTI-AGENT COLLABORATION DEMO\n")
    print("🚀" * 35 + "\n")

    # Create the Nova Process simulator
    nova = NovaProcessSimulator()

    # Add domain experts
    nova.add_domain_expert("Backend Architecture")
    nova.add_domain_expert("Security")
    nova.add_domain_expert("DevOps")

    # Define the problem
    problem = """
    We need to design and implement a new API backend for our e-commerce platform.
    The system must handle 10,000 concurrent users, integrate with payment providers,
    maintain PCI compliance, and support real-time inventory updates.
    What architecture and technology stack should we use?
    """

    # Run the Nova Process
    results = await nova.solve(problem)

    # Show conversation log
    print("\n" + "=" * 70)
    print(" CONVERSATION LOG ".center(70, "="))
    print("=" * 70)

    for i, (agent_name, history) in enumerate([
        (nova.dce.name, nova.dce.conversation_history),
        (nova.cae.name, nova.cae.conversation_history),
        *[(e.name, e.conversation_history) for e in nova.domain_experts.values()]
    ]):
        if history:
            print(f"\n📝 {agent_name}: {len(history)} interaction(s)")

    print("\n✨ Demo complete! The Nova Process successfully coordinated multiple")
    print("   AI agents to analyze and solve a complex problem.")


if __name__ == "__main__":
    asyncio.run(main())
