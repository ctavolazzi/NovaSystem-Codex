#!/usr/bin/env python3
"""
Decision Matrix Examples
========================

This file demonstrates various use cases for the NovaSystem decision matrix utility.

The decision matrix helps you make quantitative decisions by comparing options
against multiple criteria with optional weighting.
"""

from novasystem.core_utils import make_decision, compare_methods


def example_1_basic_usage():
    """Example 1: Basic decision matrix usage."""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic Technology Selection")
    print("=" * 70)

    result = make_decision(
        options=["Python", "JavaScript", "Go"],
        criteria=["Learning Curve", "Performance", "Community Support"],
        scores={
            "Python": [9, 7, 10],  # Easy to learn, good performance, great community
            "JavaScript": [8, 6, 9],  # Easy to learn, ok performance, great community
            "Go": [6, 9, 7],  # Harder to learn, excellent performance, good community
        },
    )

    print(result)


def example_2_weighted_criteria():
    """Example 2: Using weighted criteria."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Weighted Vendor Selection")
    print("=" * 70)

    # Price is most important (40%), then quality (30%), delivery (20%), support (10%)
    result = make_decision(
        options=["Vendor A", "Vendor B", "Vendor C"],
        criteria=["Price", "Quality", "Delivery Time", "Customer Support"],
        scores={
            "Vendor A": [8, 7, 6, 9],  # Good price, ok quality, slow delivery, great support
            "Vendor B": [6, 9, 8, 7],  # Higher price, excellent quality, good delivery, good support
            "Vendor C": [7, 8, 9, 8],  # Medium price, good quality, fast delivery, good support
        },
        weights=[0.4, 0.3, 0.2, 0.1],
    )

    print(result)
    print(f"\n📊 Export as JSON:")
    print(result.to_json())


def example_3_different_methods():
    """Example 3: Comparing different analysis methods."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Comparing Analysis Methods")
    print("=" * 70)

    options = ["Candidate A", "Candidate B", "Candidate C"]
    criteria = ["Technical Skills", "Experience", "Culture Fit", "Cost"]
    scores = {
        "Candidate A": [9, 5, 8, 6],  # Strong technical, junior, good fit, lower cost
        "Candidate B": [7, 9, 9, 4],  # Good technical, senior, great fit, higher cost
        "Candidate C": [8, 7, 7, 7],  # Good all-around, mid-level, ok fit, medium cost
    }
    weights = [0.4, 0.3, 0.2, 0.1]

    # Compare all methods
    comparison = compare_methods(options, criteria, scores, weights)
    print(comparison)

    # Or get individual method results
    print("\n" + "-" * 70)
    print("Individual Method Details:")
    print("-" * 70)

    for method in ["weighted", "normalized", "ranking", "best_worst"]:
        result = make_decision(
            options, criteria, scores, weights, method=method
        )
        print(f"\n{method.upper()} METHOD → Winner: {result.winner} "
              f"(Confidence: {result.confidence_score:.1f}%)")


def example_4_project_prioritization():
    """Example 4: Project prioritization."""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Project Prioritization")
    print("=" * 70)

    result = make_decision(
        options=[
            "Mobile App Redesign",
            "API Performance Optimization",
            "New Feature: AI Chatbot",
            "Technical Debt Cleanup",
        ],
        criteria=[
            "Business Value",
            "Development Effort",  # Lower is better, but we score as inverse
            "Risk",  # Lower is better, but we score as inverse
            "Strategic Alignment",
        ],
        scores={
            "Mobile App Redesign": [8, 4, 6, 7],  # High value, medium effort
            "API Performance Optimization": [7, 7, 8, 6],  # Good value, low effort
            "New Feature: AI Chatbot": [9, 3, 5, 9],  # High value, high effort
            "Technical Debt Cleanup": [6, 6, 9, 5],  # Medium value, medium effort
        },
        weights=[
            0.35,  # Business value: 35%
            0.25,  # Effort: 25%
            0.15,  # Risk: 15%
            0.25,  # Strategic alignment: 25%
        ],
    )

    print(result)


def example_5_feature_comparison():
    """Example 5: Product/Feature comparison."""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Cloud Provider Selection")
    print("=" * 70)

    result = make_decision(
        options=["AWS", "Google Cloud", "Azure", "DigitalOcean"],
        criteria=[
            "Pricing",
            "Services Available",
            "Ease of Use",
            "Documentation",
            "Performance",
        ],
        scores={
            "AWS": [6, 10, 6, 8, 9],  # Expensive, comprehensive, complex
            "Google Cloud": [7, 9, 7, 9, 9],  # Good price, great services
            "Azure": [6, 9, 6, 7, 9],  # Similar to AWS
            "DigitalOcean": [9, 6, 9, 8, 7],  # Cheap, limited, easy
        },
        weights=[0.25, 0.25, 0.20, 0.15, 0.15],
        method="normalized",  # Use normalized method for better comparison
    )

    print(result)


def example_6_all_methods_comparison():
    """Example 6: Get results from all methods at once."""
    print("\n" + "=" * 70)
    print("EXAMPLE 6: All Methods at Once")
    print("=" * 70)

    results = make_decision(
        options=["Option 1", "Option 2", "Option 3"],
        criteria=["Criterion A", "Criterion B", "Criterion C"],
        scores={
            "Option 1": [8, 7, 9],
            "Option 2": [7, 9, 7],
            "Option 3": [9, 8, 6],
        },
        weights=[0.4, 0.3, 0.3],
        show_all_methods=True,  # Returns dict of all method results
    )

    # Results is now a dictionary with all methods
    print("Winners by method:")
    for method_name, result in results.items():
        print(f"  {method_name:15s}: {result.winner}")

    # You can access individual results
    print(f"\nWeighted method details:")
    print(results["weighted"])


def example_7_simple_yes_no_decision():
    """Example 7: Simple binary decision."""
    print("\n" + "=" * 70)
    print("EXAMPLE 7: Should We Build vs Buy?")
    print("=" * 70)

    result = make_decision(
        options=["Build In-House", "Buy Commercial Solution"],
        criteria=[
            "Initial Cost",
            "Long-term Cost",
            "Customization",
            "Time to Market",
            "Maintenance Burden",
        ],
        scores={
            "Build In-House": [3, 8, 10, 4, 3],  # Low initial cost, high long-term
            "Buy Commercial Solution": [7, 7, 6, 9, 8],  # Higher initial, lower long-term
        },
        weights=[0.20, 0.25, 0.20, 0.20, 0.15],
    )

    print(result)


def example_8_career_decision():
    """Example 8: Career/Job offer comparison."""
    print("\n" + "=" * 70)
    print("EXAMPLE 8: Job Offer Comparison")
    print("=" * 70)

    result = make_decision(
        options=["Current Job", "Startup Offer", "Big Tech Offer", "Remote Consulting"],
        criteria=[
            "Salary",
            "Work-Life Balance",
            "Learning Opportunities",
            "Job Security",
            "Impact/Meaningful Work",
        ],
        scores={
            "Current Job": [7, 8, 6, 9, 7],
            "Startup Offer": [6, 5, 9, 4, 9],
            "Big Tech Offer": [10, 6, 7, 8, 6],
            "Remote Consulting": [8, 10, 8, 6, 7],
        },
        weights=[0.25, 0.25, 0.20, 0.15, 0.15],
    )

    print(result)


def example_9_investment_decision():
    """Example 9: Investment comparison."""
    print("\n" + "=" * 70)
    print("EXAMPLE 9: Investment Strategy Comparison")
    print("=" * 70)

    result = make_decision(
        options=[
            "Index Funds",
            "Individual Stocks",
            "Real Estate",
            "Bonds",
        ],
        criteria=[
            "Expected Return",
            "Risk Level (inverse)",
            "Liquidity",
            "Effort Required (inverse)",
            "Diversification",
        ],
        scores={
            "Index Funds": [7, 8, 9, 9, 10],
            "Individual Stocks": [9, 4, 9, 3, 5],
            "Real Estate": [8, 6, 4, 2, 6],
            "Bonds": [5, 9, 8, 9, 7],
        },
        weights=[0.30, 0.25, 0.15, 0.15, 0.15],
    )

    print(result)


def example_10_custom_use_case():
    """Example 10: Template for your custom use case."""
    print("\n" + "=" * 70)
    print("EXAMPLE 10: Template - Customize This!")
    print("=" * 70)

    result = make_decision(
        options=[
            "Your Option 1",
            "Your Option 2",
            "Your Option 3",
        ],
        criteria=[
            "Your Criterion 1",
            "Your Criterion 2",
            "Your Criterion 3",
        ],
        scores={
            "Your Option 1": [8, 7, 9],  # Score each criterion 1-10
            "Your Option 2": [7, 9, 7],
            "Your Option 3": [9, 8, 6],
        },
        weights=[0.4, 0.3, 0.3],  # Optional: weight importance (must sum to 1.0)
        method="weighted",  # weighted, normalized, ranking, or best_worst
    )

    print(result)

    # You can also export for further analysis
    print("\n📤 Exportable formats:")
    print("Python dict:", result.to_dict())
    # print("JSON string:", result.to_json())


def run_all_examples():
    """Run all examples."""
    examples = [
        example_1_basic_usage,
        example_2_weighted_criteria,
        example_3_different_methods,
        example_4_project_prioritization,
        example_5_feature_comparison,
        example_6_all_methods_comparison,
        example_7_simple_yes_no_decision,
        example_8_career_decision,
        example_9_investment_decision,
        example_10_custom_use_case,
    ]

    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n❌ Error in {example.__name__}: {e}")

    print("\n" + "=" * 70)
    print("✅ All examples completed!")
    print("=" * 70)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Run specific example
        example_num = sys.argv[1]
        example_func = globals().get(f"example_{example_num}_" + "_".join(sys.argv[2:]) if len(sys.argv) > 2 else f"example_{example_num}")
        if example_func and callable(example_func):
            example_func()
        else:
            print(f"Example {example_num} not found. Available examples: 1-10")
    else:
        # Run all examples
        run_all_examples()
