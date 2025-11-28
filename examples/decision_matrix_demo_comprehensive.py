#!/usr/bin/env python3
"""
Decision Matrix - Comprehensive Feature Demonstration

This script demonstrates ALL features of the decision matrix utility including:
- Basic decision making
- All 4 analysis methods
- Enhanced v2.0 features (strengths, weaknesses, why winner won)
- Comparison table
- Top-N filtering
- Method comparison
- Export capabilities
- Real-world scenario

Run: python examples/decision_matrix_demo_comprehensive.py
"""

from novasystem.core_utils import make_decision, compare_methods
import json


def demo_basic_usage():
    """Demo 1: Basic usage with all v2.0 features"""
    print("=" * 80)
    print("DEMO 1: BASIC USAGE WITH v2.0 FEATURES")
    print("=" * 80)
    print("\nScenario: Choosing a cloud platform for a new project\n")

    result = make_decision(
        options=["AWS", "Google Cloud", "Azure", "DigitalOcean"],
        criteria=["Cost", "Features", "Ease of Use", "Support", "Performance"],
        scores={
            "AWS": [6, 10, 6, 8, 9],
            "Google Cloud": [7, 9, 9, 9, 9],
            "Azure": [6, 9, 6, 7, 9],
            "DigitalOcean": [9, 6, 9, 7, 7]
        },
        weights=[0.25, 0.25, 0.20, 0.15, 0.15]
    )

    print(result)
    print("\n" + "=" * 80)
    print()


def demo_comparison_table():
    """Demo 2: Comparison table view"""
    print("=" * 80)
    print("DEMO 2: COMPARISON TABLE")
    print("=" * 80)
    print("\nSame scenario, but showing side-by-side comparison:\n")

    result = make_decision(
        options=["AWS", "Google Cloud", "Azure", "DigitalOcean"],
        criteria=["Cost", "Features", "Ease of Use", "Support", "Performance"],
        scores={
            "AWS": [6, 10, 6, 8, 9],
            "Google Cloud": [7, 9, 9, 9, 9],
            "Azure": [6, 9, 6, 7, 9],
            "DigitalOcean": [9, 6, 9, 7, 7]
        },
        weights=[0.25, 0.25, 0.20, 0.15, 0.15]
    )

    print(result.comparison_table())
    print("\n" + "=" * 80)
    print()


def demo_top_n_filtering():
    """Demo 3: Top-N filtering for large option sets"""
    print("=" * 80)
    print("DEMO 3: TOP-N FILTERING")
    print("=" * 80)
    print("\nScenario: Comparing 10 programming languages, show only top 3\n")

    result = make_decision(
        options=[
            "Python", "JavaScript", "Java", "C++", "Go",
            "Rust", "TypeScript", "PHP", "Ruby", "Swift"
        ],
        criteria=["Learning Curve", "Performance", "Community", "Jobs", "Tooling"],
        scores={
            "Python": [9, 7, 10, 10, 9],
            "JavaScript": [8, 6, 9, 10, 8],
            "Java": [6, 8, 9, 9, 9],
            "C++": [3, 10, 8, 7, 7],
            "Go": [7, 9, 7, 8, 8],
            "Rust": [4, 10, 6, 7, 8],
            "TypeScript": [7, 6, 8, 9, 9],
            "PHP": [7, 5, 8, 7, 7],
            "Ruby": [8, 5, 7, 6, 7],
            "Swift": [7, 8, 6, 7, 8]
        },
        weights=[0.2, 0.25, 0.2, 0.25, 0.1],
        top_n=3  # Only show top 3
    )

    print(result)
    print("\n" + "=" * 80)
    print()


def demo_method_comparison():
    """Demo 4: Compare all 4 analysis methods"""
    print("=" * 80)
    print("DEMO 4: METHOD COMPARISON")
    print("=" * 80)
    print("\nScenario: Hiring decision - see consensus across all methods\n")

    comparison = compare_methods(
        options=["Alice (Junior)", "Bob (Senior)", "Carol (Mid-level)"],
        criteria=["Technical Skills", "Experience", "Culture Fit", "Salary Budget"],
        scores={
            "Alice (Junior)": [7, 4, 9, 9],
            "Bob (Senior)": [9, 10, 7, 5],
            "Carol (Mid-level)": [8, 7, 8, 7]
        },
        weights=[0.35, 0.25, 0.25, 0.15]
    )

    print(comparison)
    print("\n" + "=" * 80)
    print()


def demo_export_capabilities():
    """Demo 5: Export to JSON and Dict"""
    print("=" * 80)
    print("DEMO 5: EXPORT CAPABILITIES")
    print("=" * 80)
    print("\nExporting decision results for integration with other systems\n")

    result = make_decision(
        options=["Option A", "Option B", "Option C"],
        criteria=["Cost", "Quality", "Speed"],
        scores={
            "Option A": [7, 8, 6],
            "Option B": [9, 5, 7],
            "Option C": [6, 9, 8]
        },
        weights=[0.3, 0.5, 0.2]
    )

    # Export as dict
    dict_export = result.to_dict()
    print("📦 DICT EXPORT:")
    print(f"   Keys: {list(dict_export.keys())}")
    print(f"   Winner: {dict_export['winner']}")
    print(f"   Confidence: {dict_export['confidence_score']}%")
    print(f"   Top 3: {dict_export['rankings'][:3]}")

    # Export as JSON
    json_export = result.to_json()
    print(f"\n📄 JSON EXPORT:")
    print(f"   Size: {len(json_export)} characters")
    print(f"   Valid JSON: {isinstance(json.loads(json_export), dict)}")

    # Show sample of JSON
    print(f"\n   Sample (first 200 chars):")
    print(f"   {json_export[:200]}...")

    print("\n" + "=" * 80)
    print()


def demo_all_methods():
    """Demo 6: Get results from all methods at once"""
    print("=" * 80)
    print("DEMO 6: ALL METHODS AT ONCE")
    print("=" * 80)
    print("\nRunning all 4 methods and showing each winner\n")

    results = make_decision(
        options=["Vendor A", "Vendor B", "Vendor C"],
        criteria=["Price", "Quality", "Delivery", "Support"],
        scores={
            "Vendor A": [8, 7, 6, 9],
            "Vendor B": [6, 9, 8, 7],
            "Vendor C": [7, 8, 9, 8]
        },
        weights=[0.4, 0.3, 0.2, 0.1],
        show_all_methods=True
    )

    print("Results by Method:")
    print("-" * 80)
    for method, result in results.items():
        print(f"{method.upper():15s} → Winner: {result.winner:12s} "
              f"(Confidence: {result.confidence_score:5.1f}%)")

    print("\n" + "=" * 80)
    print()


def demo_feature_highlights():
    """Demo 7: Highlight all v2.0 features"""
    print("=" * 80)
    print("DEMO 7: v2.0 FEATURE HIGHLIGHTS")
    print("=" * 80)
    print("\nShowcasing: Strengths, Weaknesses, Why Winner Won\n")

    result = make_decision(
        options=["Product A", "Product B", "Product C"],
        criteria=["Innovation", "Reliability", "Price", "Support", "Ease of Use"],
        scores={
            "Product A": [10, 8, 5, 7, 8],  # Innovative but expensive
            "Product B": [6, 10, 9, 9, 7],  # Reliable and affordable
            "Product C": [7, 7, 7, 7, 10]   # Very easy to use
        },
        weights=[0.25, 0.25, 0.20, 0.15, 0.15]
    )

    print(f"🏆 WINNER: {result.winner}")
    print(f"   Confidence: {result.confidence_score}%")

    print(f"\n✨ WHY {result.winner.upper()} WON:")
    print(f"   {result.why_winner_won}")

    print(f"\n💪 STRENGTHS of {result.winner}:")
    for criterion, score in result.strengths[result.winner][:3]:
        print(f"   - {criterion}: {score:.2f}")

    print(f"\n⚠️  WEAKNESSES of {result.winner}:")
    for criterion, score in result.weaknesses[result.winner][:3]:
        print(f"   - {criterion}: {score:.2f}")

    print("\n📊 RECOMMENDATION:")
    print(f"   {result.recommendation}")

    print("\n" + "=" * 80)
    print()


def main():
    """Run all demos"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  DECISION MATRIX - COMPREHENSIVE FEATURE DEMONSTRATION".center(78) + "║")
    print("║" + "  Version 2.0 with All Enhancements".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")

    # Run all demos
    demo_basic_usage()
    input("Press Enter to continue to Demo 2...")

    demo_comparison_table()
    input("Press Enter to continue to Demo 3...")

    demo_top_n_filtering()
    input("Press Enter to continue to Demo 4...")

    demo_method_comparison()
    input("Press Enter to continue to Demo 5...")

    demo_export_capabilities()
    input("Press Enter to continue to Demo 6...")

    demo_all_methods()
    input("Press Enter to continue to Demo 7...")

    demo_feature_highlights()

    # Final summary
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  DEMONSTRATION COMPLETE".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("║" + "  Features Demonstrated:".ljust(78) + "║")
    print("║" + "    ✓ Basic decision making with v2.0 enhancements".ljust(78) + "║")
    print("║" + "    ✓ Comparison table view".ljust(78) + "║")
    print("║" + "    ✓ Top-N filtering".ljust(78) + "║")
    print("║" + "    ✓ Method comparison with consensus".ljust(78) + "║")
    print("║" + "    ✓ Export to JSON and Dict".ljust(78) + "║")
    print("║" + "    ✓ All 4 methods at once".ljust(78) + "║")
    print("║" + "    ✓ Strengths, weaknesses, and explanations".ljust(78) + "║")
    print("║" + " " * 78 + "║")
    print("║" + "  Status: ✅ All features working perfectly!".ljust(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")

    print("For more information:")
    print("  - User Guide: DECISION_MATRIX_README.md")
    print("  - Quick Reference: DECISION_MATRIX_QUICK_REFERENCE.md")
    print("  - CLI Guide: DECISION_MATRIX_CLI.md")
    print("  - Test Report: DECISION_MATRIX_TEST_REPORT.md")
    print("  - Enhancements: DECISION_MATRIX_ENHANCEMENTS.md")
    print("  - Summary: DECISION_MATRIX_SUMMARY.md")
    print()


if __name__ == "__main__":
    main()
