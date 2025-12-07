#!/usr/bin/env python3
"""
Nova Problem-Solving Demo
=========================

A comprehensive demonstration of how NovaSystem solves complex problems
using the complete Nova Process:

1. UNPACK - Break down the problem with DCE
2. ANALYZE - Get expert perspectives in parallel
3. SYNTHESIZE - Combine insights into actionable solution

Features demonstrated:
- Full Nova Process workflow
- Memory system integration
- Decision matrix for recommendations
- Event-driven logging
- Historical context from journal

Run:
    python examples/nova_problem_solving_demo.py

    # With specific problem
    python examples/nova_problem_solving_demo.py --problem "How do I scale my API?"
"""

import argparse
import asyncio
import json
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add parent to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from novasystem.core.memory import MemoryManager
from novasystem.core.vector_store import LocalVectorStore
from novasystem.domain.events import EventBus, get_event_bus
from novasystem.tools.decision_matrix.decision_matrix import make_decision


# =============================================================================
# Configuration
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
JOURNAL_PATH = DATA_DIR / "nova_problem_solving_journal.json"
MEMORY_PATH = DATA_DIR / "nova_problem_solving_memory.json"


# =============================================================================
# Problem Solver Classes
# =============================================================================


@dataclass
class Insight:
    """An insight from analysis."""
    source: str
    category: str
    content: str
    confidence: float
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class Recommendation:
    """A recommendation from the problem-solving process."""
    title: str
    description: str
    priority: int
    effort: str
    impact: str
    tags: List[str] = field(default_factory=list)


@dataclass
class Solution:
    """Complete solution from Nova Process."""
    problem: str
    insights: List[Insight]
    recommendations: List[Recommendation]
    decision_analysis: Dict[str, Any]
    confidence_score: float
    execution_time: float
    timestamp: datetime = field(default_factory=datetime.now)


class NovaProcessSolver:
    """
    Complete Nova Process problem solver.

    Implements the three-phase approach:
    1. UNPACK - Understand and decompose the problem
    2. ANALYZE - Gather expert perspectives
    3. SYNTHESIZE - Create actionable solution
    """

    def __init__(self):
        self.memory = MemoryManager(max_short_term=50, max_long_term=200)
        self.vector_store = LocalVectorStore(memory_file=MEMORY_PATH, persist=True)
        self.insights: List[Insight] = []
        self.recommendations: List[Recommendation] = []

        # Initialize knowledge base
        self._init_knowledge_base()

    def _init_knowledge_base(self):
        """Initialize vector store with domain knowledge."""
        knowledge = [
            ("API scaling requires horizontal scaling, load balancing, and caching strategies",
             ["scaling", "api", "architecture"]),
            ("Database performance improves with proper indexing, query optimization, and connection pooling",
             ["database", "performance", "optimization"]),
            ("Microservices provide scalability but increase operational complexity",
             ["microservices", "architecture", "tradeoffs"]),
            ("Event-driven architecture enables loose coupling and better scalability",
             ["events", "architecture", "scalability"]),
            ("Caching strategies include CDN, Redis, and application-level caching",
             ["caching", "performance", "infrastructure"]),
            ("Security best practices include authentication, authorization, encryption, and audit logging",
             ["security", "best-practices", "compliance"]),
            ("CI/CD pipelines automate testing, building, and deployment processes",
             ["devops", "automation", "deployment"]),
            ("Monitoring requires metrics, logs, traces, and alerting systems",
             ["observability", "monitoring", "operations"]),
        ]

        for text, tags in knowledge:
            # Only add if not already present (check by searching)
            existing = self.vector_store.recall(text[:30], limit=1, min_score=0.9)
            if not existing:
                self.vector_store.remember(text, tags=tags)

    async def solve(self, problem: str) -> Solution:
        """
        Solve a problem using the full Nova Process.

        Args:
            problem: The problem statement to solve

        Returns:
            Complete Solution with insights, recommendations, and analysis
        """
        start_time = time.time()

        print("\n" + "=" * 70)
        print(" NOVA PROCESS: PROBLEM SOLVING ".center(70, "="))
        print("=" * 70)

        # Store problem in memory
        await self.memory.store_context("current_problem", {
            "statement": problem,
            "started_at": datetime.now().isoformat()
        }, "short_term")

        # Phase 1: UNPACK
        print("\n" + "-" * 50)
        print("🔍 PHASE 1: UNPACK")
        print("-" * 50)
        unpacked = await self._unpack_problem(problem)

        # Phase 2: ANALYZE
        print("\n" + "-" * 50)
        print("🔬 PHASE 2: ANALYZE")
        print("-" * 50)
        analysis = await self._analyze_problem(problem, unpacked)

        # Phase 3: SYNTHESIZE
        print("\n" + "-" * 50)
        print("✨ PHASE 3: SYNTHESIZE")
        print("-" * 50)
        decision_analysis = await self._synthesize_solution(problem, analysis)

        execution_time = time.time() - start_time

        # Create solution
        solution = Solution(
            problem=problem,
            insights=self.insights.copy(),
            recommendations=self.recommendations.copy(),
            decision_analysis=decision_analysis,
            confidence_score=self._calculate_confidence(),
            execution_time=execution_time
        )

        # Store solution
        await self.memory.store_context("final_solution", {
            "problem": problem,
            "confidence": solution.confidence_score,
            "recommendation_count": len(solution.recommendations),
            "timestamp": datetime.now().isoformat()
        }, "long_term")

        # Save to journal
        self._save_to_journal(solution)

        # Print solution
        self._print_solution(solution)

        return solution

    async def _unpack_problem(self, problem: str) -> Dict[str, Any]:
        """
        UNPACK phase: Break down the problem into components.
        """
        print(f"\n📋 Problem Statement:\n   {problem}")

        # Retrieve relevant context from vector store
        relevant_knowledge = self.vector_store.recall(problem, limit=5, min_score=0.1)

        print(f"\n🔎 Found {len(relevant_knowledge)} relevant knowledge items")
        for item, score in relevant_knowledge[:3]:
            print(f"   [{score:.2f}] {item['text'][:60]}...")

        # Identify key components
        components = self._identify_components(problem)
        print(f"\n🧩 Identified Components:")
        for comp in components:
            print(f"   • {comp}")

        # Store unpacked analysis
        unpacked = {
            "original_problem": problem,
            "components": components,
            "relevant_knowledge": [item['text'] for item, _ in relevant_knowledge],
            "complexity_estimate": len(components)
        }

        await self.memory.store_context("unpacked_problem", unpacked, "short_term")

        self.insights.append(Insight(
            source="DCE (Unpack)",
            category="problem_analysis",
            content=f"Problem decomposed into {len(components)} key components",
            confidence=0.85
        ))

        return unpacked

    async def _analyze_problem(self, problem: str, unpacked: Dict) -> Dict[str, Any]:
        """
        ANALYZE phase: Get expert perspectives.
        """
        analyses = {}

        # Architecture Analysis
        print("\n🏗️  Architecture Expert:")
        arch_analysis = self._analyze_architecture(problem, unpacked)
        analyses["architecture"] = arch_analysis
        print(f"   Recommendation: {arch_analysis['recommendation']}")
        print(f"   Confidence: {arch_analysis['confidence']:.0%}")

        self.insights.append(Insight(
            source="Architecture Expert",
            category="architecture",
            content=arch_analysis['recommendation'],
            confidence=arch_analysis['confidence']
        ))

        # Performance Analysis
        print("\n⚡ Performance Expert:")
        perf_analysis = self._analyze_performance(problem, unpacked)
        analyses["performance"] = perf_analysis
        print(f"   Recommendation: {perf_analysis['recommendation']}")
        print(f"   Confidence: {perf_analysis['confidence']:.0%}")

        self.insights.append(Insight(
            source="Performance Expert",
            category="performance",
            content=perf_analysis['recommendation'],
            confidence=perf_analysis['confidence']
        ))

        # Security Analysis
        print("\n🔒 Security Expert:")
        sec_analysis = self._analyze_security(problem, unpacked)
        analyses["security"] = sec_analysis
        print(f"   Recommendation: {sec_analysis['recommendation']}")
        print(f"   Confidence: {sec_analysis['confidence']:.0%}")

        self.insights.append(Insight(
            source="Security Expert",
            category="security",
            content=sec_analysis['recommendation'],
            confidence=sec_analysis['confidence']
        ))

        # Critical Analysis (CAE)
        print("\n⚠️  Critical Analysis Expert:")
        cae_analysis = self._critical_analysis(problem, analyses)
        analyses["critical"] = cae_analysis
        print(f"   Risk Level: {cae_analysis['risk_level']}")
        print(f"   Concerns: {len(cae_analysis['concerns'])}")

        for concern in cae_analysis['concerns'][:2]:
            print(f"   • {concern}")

        self.insights.append(Insight(
            source="CAE",
            category="risk_assessment",
            content=f"Risk level: {cae_analysis['risk_level']}, {len(cae_analysis['concerns'])} concerns identified",
            confidence=0.9
        ))

        await self.memory.store_context("analysis_results", analyses, "short_term")
        return analyses

    async def _synthesize_solution(self, problem: str, analysis: Dict) -> Dict[str, Any]:
        """
        SYNTHESIZE phase: Combine insights into actionable recommendations.
        """
        print("\n📊 Running Decision Matrix Analysis...")

        # Use decision matrix to evaluate approaches
        options = [
            "Incremental Improvement",
            "Major Refactoring",
            "New Architecture"
        ]

        criteria = [
            "Implementation Speed",
            "Long-term Scalability",
            "Risk Level",
            "Resource Requirements",
            "Business Continuity"
        ]

        # Scores based on analysis
        scores = {
            "Incremental Improvement": [9, 5, 9, 8, 10],
            "Major Refactoring": [5, 8, 5, 5, 6],
            "New Architecture": [3, 10, 3, 3, 4],
        }

        weights = [0.15, 0.30, 0.20, 0.15, 0.20]

        decision_result = make_decision(
            options=options,
            criteria=criteria,
            scores=scores,
            weights=weights,
            show_all_methods=True
        )

        winner = decision_result["weighted"]
        print(f"\n🏆 Decision: {winner.winner}")
        print(f"   Confidence: {winner.confidence_score:.1f}%")

        if winner.warnings:
            print(f"   ⚠️  Warnings:")
            for w in winner.warnings:
                print(f"      • {w}")

        # Generate recommendations
        self._generate_recommendations(winner.winner, analysis)

        return {
            "winner": winner.winner,
            "confidence": winner.confidence_score,
            "rankings": winner.rankings,
            "method_comparison": {
                method: {
                    "winner": result.winner,
                    "confidence": result.confidence_score
                }
                for method, result in decision_result.items()
            }
        }

    def _identify_components(self, problem: str) -> List[str]:
        """Identify key components from the problem statement."""
        components = []
        keywords = {
            "scale": "Scalability Requirements",
            "api": "API Design",
            "database": "Data Storage",
            "performance": "Performance Optimization",
            "security": "Security Considerations",
            "user": "User Experience",
            "deploy": "Deployment Strategy",
            "test": "Testing Strategy",
            "monitor": "Monitoring & Observability",
            "cost": "Cost Optimization",
        }

        problem_lower = problem.lower()
        for keyword, component in keywords.items():
            if keyword in problem_lower:
                components.append(component)

        # Always include some basics
        if len(components) < 3:
            components.extend(["Architecture Design", "Implementation Plan", "Risk Assessment"])

        return list(set(components))[:6]  # Limit to 6 components

    def _analyze_architecture(self, problem: str, unpacked: Dict) -> Dict:
        """Generate architecture analysis."""
        if "scale" in problem.lower() or "api" in problem.lower():
            return {
                "recommendation": "Implement horizontal scaling with load balancing",
                "pattern": "Microservices with API Gateway",
                "confidence": 0.82
            }
        return {
            "recommendation": "Review current architecture for optimization opportunities",
            "pattern": "Modular Monolith",
            "confidence": 0.75
        }

    def _analyze_performance(self, problem: str, unpacked: Dict) -> Dict:
        """Generate performance analysis."""
        return {
            "recommendation": "Implement caching layer and optimize database queries",
            "optimizations": ["Redis caching", "Query optimization", "CDN for static assets"],
            "confidence": 0.88
        }

    def _analyze_security(self, problem: str, unpacked: Dict) -> Dict:
        """Generate security analysis."""
        return {
            "recommendation": "Implement defense in depth with authentication, encryption, and monitoring",
            "measures": ["OAuth 2.0", "TLS everywhere", "Rate limiting", "Audit logging"],
            "confidence": 0.91
        }

    def _critical_analysis(self, problem: str, analyses: Dict) -> Dict:
        """Generate critical analysis."""
        concerns = [
            "Implementation complexity may exceed initial estimates",
            "Team may need additional training on new technologies",
            "Migration path needs careful planning to avoid downtime",
            "Monitoring and alerting must be in place before changes",
        ]
        return {
            "risk_level": "Medium",
            "concerns": concerns,
            "mitigation_suggestions": [
                "Start with pilot project",
                "Implement feature flags for gradual rollout",
                "Ensure rollback capability"
            ]
        }

    def _generate_recommendations(self, approach: str, analysis: Dict):
        """Generate specific recommendations based on chosen approach."""
        self.recommendations = [
            Recommendation(
                title="Implement Caching Strategy",
                description="Add Redis caching for frequently accessed data and API responses",
                priority=1,
                effort="Medium",
                impact="High",
                tags=["performance", "infrastructure"]
            ),
            Recommendation(
                title="Optimize Database Queries",
                description="Review and optimize slow queries, add missing indexes",
                priority=2,
                effort="Low",
                impact="High",
                tags=["database", "performance"]
            ),
            Recommendation(
                title="Add Horizontal Scaling",
                description="Configure auto-scaling for API servers based on load",
                priority=3,
                effort="Medium",
                impact="High",
                tags=["scaling", "infrastructure"]
            ),
            Recommendation(
                title="Implement Monitoring",
                description="Set up comprehensive monitoring with Prometheus and Grafana",
                priority=4,
                effort="Medium",
                impact="Medium",
                tags=["observability", "operations"]
            ),
            Recommendation(
                title="Security Hardening",
                description="Implement rate limiting and enhance authentication",
                priority=5,
                effort="Low",
                impact="High",
                tags=["security"]
            ),
        ]

    def _calculate_confidence(self) -> float:
        """Calculate overall solution confidence."""
        if not self.insights:
            return 0.5
        return sum(i.confidence for i in self.insights) / len(self.insights)

    def _save_to_journal(self, solution: Solution):
        """Save solution to journal for historical reference."""
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        journal = []
        if JOURNAL_PATH.exists():
            try:
                with JOURNAL_PATH.open("r") as f:
                    journal = json.load(f)
            except json.JSONDecodeError:
                journal = []

        entry = {
            "timestamp": solution.timestamp.isoformat(),
            "problem": solution.problem[:200],
            "confidence": solution.confidence_score,
            "recommendations": len(solution.recommendations),
            "insights": len(solution.insights),
            "execution_time": solution.execution_time,
            "decision": solution.decision_analysis.get("winner"),
        }
        journal.append(entry)

        with JOURNAL_PATH.open("w") as f:
            json.dump(journal, f, indent=2)

    def _print_solution(self, solution: Solution):
        """Print the complete solution."""
        print("\n" + "=" * 70)
        print(" SOLUTION SUMMARY ".center(70, "="))
        print("=" * 70)

        print(f"""
📋 Problem: {solution.problem[:100]}...

🎯 Recommended Approach: {solution.decision_analysis.get('winner', 'N/A')}
📊 Confidence Score: {solution.confidence_score:.0%}
⏱️  Execution Time: {solution.execution_time:.2f}s
""")

        print("💡 Key Insights:")
        for i, insight in enumerate(solution.insights[:5], 1):
            print(f"   {i}. [{insight.source}] {insight.content}")

        print("\n📝 Recommendations (Priority Order):")
        for rec in solution.recommendations:
            print(f"\n   {rec.priority}. {rec.title}")
            print(f"      {rec.description}")
            print(f"      Effort: {rec.effort} | Impact: {rec.impact}")
            print(f"      Tags: {', '.join(rec.tags)}")

        print("\n🔄 Method Comparison:")
        for method, data in solution.decision_analysis.get("method_comparison", {}).items():
            print(f"   • {method}: {data['winner']} ({data['confidence']:.1f}%)")

        print("\n" + "=" * 70)
        print(" PROBLEM SOLVING COMPLETE ".center(70, "="))
        print("=" * 70)


# =============================================================================
# Main
# =============================================================================


async def main(problem: Optional[str] = None):
    """Run the Nova Problem-Solving demo."""
    print("\n" + "🧠" * 35)
    print("\n  NOVASYSTEM NOVA PROBLEM-SOLVING DEMO\n")
    print("🧠" * 35)

    # Default problem if not provided
    if not problem:
        problem = """
        Our e-commerce API is experiencing slow response times during peak traffic.
        We need to scale the system to handle 10x current load while maintaining
        sub-200ms response times. How should we approach this?
        """

    solver = NovaProcessSolver()
    solution = await solver.solve(problem.strip())

    # Show journal history
    if JOURNAL_PATH.exists():
        print("\n📚 Problem-Solving History:")
        with JOURNAL_PATH.open("r") as f:
            journal = json.load(f)
        for entry in journal[-3:]:
            ts = entry.get("timestamp", "")[:19]
            dec = entry.get("decision", "N/A")
            conf = entry.get("confidence", 0)
            print(f"   {ts} | Decision: {dec} | Confidence: {conf:.0%}")

    print(f"\n💾 Solution saved to: {JOURNAL_PATH}")
    print(f"🧠 Knowledge base: {MEMORY_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nova Problem-Solving Demo")
    parser.add_argument(
        "--problem", "-p",
        type=str,
        help="Problem statement to solve"
    )
    args = parser.parse_args()

    asyncio.run(main(args.problem))
