#!/usr/bin/env python3
"""
Custom agents example for NovaSystem.

This example demonstrates how to create and use custom agents
with the Nova Process.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from novasystem.core.agents import AgentFactory, BaseAgent
from novasystem import NovaProcess, MemoryManager

class CustomDomainExpert(BaseAgent):
    """Custom domain expert for AI/ML problems."""

    def __init__(self, model: str = "gpt-4"):
        role_description = """
        You are an AI/ML Domain Expert specializing in machine learning,
        artificial intelligence, and data science. Your role is to:

        1. **Technical Analysis**: Evaluate ML/AI solutions for technical soundness
        2. **Algorithm Selection**: Recommend appropriate algorithms and models
        3. **Data Considerations**: Analyze data requirements and preprocessing needs
        4. **Performance Optimization**: Suggest optimization strategies
        5. **Best Practices**: Recommend ML engineering best practices

        Always provide specific, actionable recommendations with technical details.
        """
        super().__init__("AI/ML Expert", role_description, model)

    async def process(self, input_text: str, context: str = None) -> str:
        """Process input as AI/ML expert."""
        return f"""
**AI/ML Expert Analysis:**

**Technical Recommendations:**
- Evaluate ML algorithms suitable for: {input_text[:100]}...
- Consider data preprocessing requirements
- Assess model complexity vs. performance trade-offs

**Algorithm Suggestions:**
- Supervised learning: Random Forest, XGBoost, Neural Networks
- Unsupervised learning: Clustering, Dimensionality Reduction
- Deep learning: CNNs, RNNs, Transformers (if applicable)

**Data Considerations:**
- Data quality and quantity requirements
- Feature engineering strategies
- Train/validation/test split recommendations

**Performance Optimization:**
- Model optimization techniques
- Hyperparameter tuning strategies
- Deployment considerations
        """

class CustomCAE(BaseAgent):
    """Custom Critical Analysis Expert for AI/ML projects."""

    def __init__(self, model: str = "gpt-4"):
        role_description = """
        You are a Critical Analysis Expert specializing in AI/ML project evaluation.
        Your role is to:

        1. **Risk Assessment**: Identify potential risks in ML projects
        2. **Bias Detection**: Analyze for potential bias and fairness issues
        3. **Validation**: Ensure proper model validation and testing
        4. **Ethics**: Consider ethical implications of AI solutions
        5. **Scalability**: Evaluate scalability and production readiness

        Focus on critical issues that could impact project success.
        """
        super().__init__("AI/ML CAE", role_description, model)

    async def process(self, input_text: str, context: str = None) -> str:
        """Process input as AI/ML CAE."""
        return f"""
**AI/ML Critical Analysis:**

**Risk Assessment:**
- Data quality risks: {input_text[:100]}...
- Model overfitting potential
- Production deployment challenges

**Bias and Fairness:**
- Potential bias in training data
- Fairness considerations across different groups
- Algorithmic bias mitigation strategies

**Validation Concerns:**
- Model validation methodology
- Cross-validation strategies
- Performance metrics selection

**Ethical Considerations:**
- Privacy implications
- Transparency requirements
- Accountability measures

**Production Readiness:**
- Model monitoring needs
- Performance degradation risks
- Maintenance requirements
        """

async def main():
    """Main custom agents example function."""
    print("🧠 NovaSystem Custom Agents Example")
    print("=" * 50)

    # Create custom agents
    custom_agents = {
        "dce": AgentFactory.create_dce("gpt-4"),
        "cae": CustomCAE("gpt-4"),
        "ai_expert": CustomDomainExpert("gpt-4"),
        "data_expert": AgentFactory.create_domain_expert("Data Science", "gpt-4")
    }

    # Create memory manager
    memory_manager = MemoryManager()

    # Create Nova Process with custom agents
    nova_process = NovaProcess(
        domains=["AI/ML", "Data Science"],
        model="gpt-4",
        memory_manager=memory_manager
    )

    # Replace default agents with custom ones
    nova_process.agents = custom_agents
    nova_process.dce = custom_agents["dce"]
    nova_process.cae = custom_agents["cae"]
    nova_process.domain_experts = {
        "ai_expert": custom_agents["ai_expert"],
        "data_expert": custom_agents["data_expert"]
    }

    # Define the problem
    problem = """
    We need to build a recommendation system for our e-commerce platform that can
    suggest products to users based on their browsing history, purchase history,
    and demographic information. The system should be able to handle cold start
    problems for new users and products, and should be scalable to millions of users.
    """

    print(f"Problem: {problem.strip()}")
    print("\n🤔 Starting Nova Process with custom agents...")
    print("-" * 50)

    # Run the Nova Process
    result = await nova_process.solve_problem(
        problem,
        max_iterations=3,
        stream=False
    )

    # Display results
    print("\n🚀 Nova Process Results")
    print("=" * 50)

    if result:
        # Display final synthesis
        if "final_synthesis" in result:
            print("\n📋 Final Synthesis:")
            print("-" * 20)
            print(result["final_synthesis"])

        # Display final validation
        if "final_validation" in result:
            print("\n✅ Final Validation:")
            print("-" * 20)
            print(result["final_validation"])

        # Display process summary
        if "total_iterations" in result:
            print(f"\n📊 Process Summary:")
            print("-" * 20)
            print(f"Total Iterations: {result['total_iterations']}")
            print(f"Process Phase: {result.get('phase', 'Unknown')}")
    else:
        print("No result available.")

    print("\n🎯 Custom agents example completed!")

if __name__ == "__main__":
    asyncio.run(main())
