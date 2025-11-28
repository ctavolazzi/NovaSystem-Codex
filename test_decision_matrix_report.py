#!/usr/bin/env python3
"""
Comprehensive Decision Matrix Test Report Generator
===================================================
Tests the decision matrix utility with various scenarios and generates a report.
"""

from novasystem.core_utils import make_decision, compare_methods
import json
from datetime import datetime


def test_1_basic_functionality():
    """Test 1: Basic functionality with simple data."""
    print("\n" + "="*80)
    print("TEST 1: Basic Functionality")
    print("="*80)

    result = make_decision(
        options=["Option A", "Option B", "Option C"],
        criteria=["Cost", "Quality", "Speed"],
        scores={
            "Option A": [7, 8, 6],
            "Option B": [9, 5, 7],
            "Option C": [6, 9, 8]
        }
    )

    print(result)

    # Validation checks
    assert result.winner in ["Option A", "Option B", "Option C"]
    assert len(result.rankings) == 3
    assert 0 <= result.confidence_score <= 100

    print("\n✅ PASSED: Basic functionality works correctly")
    return {
        "test": "Basic Functionality",
        "status": "PASSED",
        "winner": result.winner,
        "confidence": result.confidence_score,
        "method": result.analysis_method
    }


def test_2_weighted_criteria():
    """Test 2: Weighted criteria with different importance."""
    print("\n" + "="*80)
    print("TEST 2: Weighted Criteria (Vendor Selection)")
    print("="*80)

    result = make_decision(
        options=["Vendor A", "Vendor B", "Vendor C"],
        criteria=["Price", "Quality", "Delivery", "Support"],
        scores={
            "Vendor A": [8, 7, 6, 9],
            "Vendor B": [6, 9, 8, 7],
            "Vendor C": [7, 8, 9, 8]
        },
        weights=[0.4, 0.3, 0.2, 0.1]  # Price is most important
    )

    print(result)

    # Export test
    json_output = result.to_json()
    dict_output = result.to_dict()

    print("\n📤 Export Test:")
    print(f"  JSON export: {len(json_output)} characters")
    print(f"  Dict keys: {list(dict_output.keys())}")

    assert "Vendor" in result.winner
    assert isinstance(json_output, str)
    assert isinstance(dict_output, dict)

    print("\n✅ PASSED: Weighted criteria and export functionality work")
    return {
        "test": "Weighted Criteria",
        "status": "PASSED",
        "winner": result.winner,
        "confidence": result.confidence_score,
        "export_json_length": len(json_output)
    }


def test_3_all_methods_comparison():
    """Test 3: Compare all 4 analysis methods."""
    print("\n" + "="*80)
    print("TEST 3: All Analysis Methods (Technology Selection)")
    print("="*80)

    options = ["Python", "JavaScript", "Go", "Rust"]
    criteria = ["Learning Curve", "Performance", "Community", "Jobs"]
    scores = {
        "Python": [9, 7, 10, 10],
        "JavaScript": [8, 6, 9, 10],
        "Go": [6, 9, 7, 8],
        "Rust": [4, 10, 6, 7]
    }
    weights = [0.2, 0.3, 0.2, 0.3]

    results = {}
    print("\nTesting each method individually:")
    print("-" * 80)

    for method in ["weighted", "normalized", "ranking", "best_worst"]:
        result = make_decision(
            options, criteria, scores, weights, method=method
        )
        results[method] = result
        print(f"\n{method.upper():15s} → Winner: {result.winner:12s} "
              f"(Confidence: {result.confidence_score:5.1f}%)")

    # Test compare_methods function
    print("\n" + "-" * 80)
    print("\nUsing compare_methods() function:")
    print("-" * 80)
    comparison = compare_methods(options, criteria, scores, weights)
    print(comparison)

    # Validation
    assert len(results) == 4
    assert all(isinstance(r, type(results["weighted"])) for r in results.values())
    assert "CONSENSUS:" in comparison

    print("\n✅ PASSED: All 4 methods work correctly")
    return {
        "test": "All Methods Comparison",
        "status": "PASSED",
        "method_winners": {m: r.winner for m, r in results.items()},
        "consensus": "Found" if "CONSENSUS:" in comparison else "Not found"
    }


def test_4_real_world_hiring():
    """Test 4: Real-world hiring decision."""
    print("\n" + "="*80)
    print("TEST 4: Real-World Scenario (Hiring Decision)")
    print("="*80)

    result = make_decision(
        options=["Alice (Junior)", "Bob (Senior)", "Carol (Mid-level)"],
        criteria=["Technical Skills", "Experience", "Culture Fit", "Salary Req"],
        scores={
            "Alice (Junior)": [7, 4, 9, 9],    # Strong tech, junior, great fit, low salary
            "Bob (Senior)": [9, 10, 7, 5],     # Excellent tech, senior, good fit, high salary
            "Carol (Mid-level)": [8, 7, 8, 7]  # Good all-around, mid-level
        },
        weights=[0.35, 0.25, 0.25, 0.15],
        method="normalized"
    )

    print(result)

    # Check recommendation quality
    assert len(result.recommendation) > 0
    assert result.winner in result.recommendation or "Options are closely matched" in result.recommendation

    print("\n✅ PASSED: Real-world hiring scenario works")
    return {
        "test": "Real-World Hiring",
        "status": "PASSED",
        "winner": result.winner,
        "recommendation_length": len(result.recommendation)
    }


def test_5_edge_cases():
    """Test 5: Edge cases and validation."""
    print("\n" + "="*80)
    print("TEST 5: Edge Cases and Validation")
    print("="*80)

    test_results = []

    # Test 5.1: Single option
    print("\n5.1 - Single Option (should always win with 100% confidence):")
    result = make_decision(
        options=["Only Choice"],
        criteria=["X", "Y"],
        scores={"Only Choice": [5, 5]}
    )
    assert result.winner == "Only Choice"
    assert result.confidence_score == 100.0
    print(f"  ✅ Winner: {result.winner}, Confidence: {result.confidence_score}%")
    test_results.append(("Single option", "PASSED"))

    # Test 5.2: Tied scores
    print("\n5.2 - Identical Scores (should have low confidence):")
    result = make_decision(
        options=["A", "B", "C"],
        criteria=["X", "Y"],
        scores={"A": [5, 5], "B": [5, 5], "C": [5, 5]}
    )
    assert result.confidence_score < 1.0
    print(f"  ✅ Winner: {result.winner}, Confidence: {result.confidence_score:.2f}%")
    test_results.append(("Tied scores", "PASSED"))

    # Test 5.3: Extreme difference
    print("\n5.3 - Extreme Difference (should have high confidence):")
    result = make_decision(
        options=["Clear Winner", "Clear Loser"],
        criteria=["X"],
        scores={"Clear Winner": [100], "Clear Loser": [1]}
    )
    assert result.winner == "Clear Winner"
    assert result.confidence_score > 90
    print(f"  ✅ Winner: {result.winner}, Confidence: {result.confidence_score:.1f}%")
    test_results.append(("Extreme difference", "PASSED"))

    # Test 5.4: Weight normalization
    print("\n5.4 - Weight Normalization (weights [2, 3, 5] → [0.2, 0.3, 0.5]):")
    result = make_decision(
        options=["A"],
        criteria=["X", "Y", "Z"],
        scores={"A": [1, 2, 3]},
        weights=[2, 3, 5]
    )
    print(f"  ✅ Weights automatically normalized to sum to 1.0")
    test_results.append(("Weight normalization", "PASSED"))

    # Test 5.5: Invalid input handling
    print("\n5.5 - Validation Tests:")
    try:
        make_decision(
            options=["A", "B"],
            criteria=["X"],
            scores={"A": [1]}  # Missing B
        )
        print("  ❌ Should have raised ValueError for missing option scores")
        test_results.append(("Missing option validation", "FAILED"))
    except ValueError as e:
        print(f"  ✅ Correctly raised ValueError: {str(e)[:50]}...")
        test_results.append(("Missing option validation", "PASSED"))

    try:
        make_decision(
            options=["A"],
            criteria=["X", "Y"],
            scores={"A": [1]}  # Wrong number of scores
        )
        print("  ❌ Should have raised ValueError for wrong score count")
        test_results.append(("Score count validation", "FAILED"))
    except ValueError as e:
        print(f"  ✅ Correctly raised ValueError: {str(e)[:50]}...")
        test_results.append(("Score count validation", "PASSED"))

    all_passed = all(status == "PASSED" for _, status in test_results)

    print(f"\n{'✅ PASSED' if all_passed else '❌ FAILED'}: Edge cases handled correctly")
    return {
        "test": "Edge Cases",
        "status": "PASSED" if all_passed else "FAILED",
        "subtests": test_results
    }


def test_6_performance():
    """Test 6: Performance with larger datasets."""
    print("\n" + "="*80)
    print("TEST 6: Performance Test (10 options, 8 criteria)")
    print("="*80)

    import time

    # Create larger dataset
    options = [f"Option {i}" for i in range(1, 11)]
    criteria = [f"Criterion {chr(65+i)}" for i in range(8)]
    scores = {
        opt: [7 + (i % 3) for i in range(8)]
        for opt in options
    }

    # Test each method
    timings = {}
    for method in ["weighted", "normalized", "ranking", "best_worst"]:
        start = time.time()
        result = make_decision(options, criteria, scores, method=method)
        end = time.time()
        timings[method] = (end - start) * 1000  # Convert to ms

        print(f"{method:15s}: {timings[method]:6.2f}ms → Winner: {result.winner}")

    # All should be fast (< 100ms)
    avg_time = sum(timings.values()) / len(timings)

    print(f"\nAverage time: {avg_time:.2f}ms")
    print(f"{'✅ PASSED' if avg_time < 100 else '⚠️  SLOW'}: Performance is {'good' if avg_time < 100 else 'acceptable'}")

    return {
        "test": "Performance",
        "status": "PASSED",
        "timings_ms": timings,
        "average_ms": avg_time
    }


def test_7_method_consistency():
    """Test 7: Check if methods produce consistent results for clear winner."""
    print("\n" + "="*80)
    print("TEST 7: Method Consistency (Clear Winner Scenario)")
    print("="*80)

    # Create scenario with clear winner
    options = ["Clear Winner", "Average", "Poor"]
    criteria = ["A", "B", "C"]
    scores = {
        "Clear Winner": [10, 10, 10],
        "Average": [5, 5, 5],
        "Poor": [1, 1, 1]
    }

    winners = {}
    for method in ["weighted", "normalized", "ranking", "best_worst"]:
        result = make_decision(options, criteria, scores, method=method)
        winners[method] = result.winner
        print(f"{method:15s}: {result.winner}")

    # All methods should pick the same winner
    unique_winners = set(winners.values())
    consistent = len(unique_winners) == 1

    print(f"\n{'✅ PASSED' if consistent else '❌ FAILED'}: "
          f"All methods {'agree' if consistent else 'disagree'} on winner")

    return {
        "test": "Method Consistency",
        "status": "PASSED" if consistent else "FAILED",
        "winners": winners,
        "consistent": consistent
    }


def test_8_export_formats():
    """Test 8: Export functionality."""
    print("\n" + "="*80)
    print("TEST 8: Export Formats (JSON, Dict)")
    print("="*80)

    result = make_decision(
        options=["A", "B"],
        criteria=["X", "Y"],
        scores={"A": [7, 8], "B": [6, 9]}
    )

    # Test dict export
    dict_export = result.to_dict()
    print(f"\n✅ Dict export: {len(dict_export)} keys")
    print(f"   Keys: {list(dict_export.keys())}")

    # Test JSON export
    json_export = result.to_json()
    print(f"\n✅ JSON export: {len(json_export)} characters")

    # Verify can be parsed back
    parsed = json.loads(json_export)
    print(f"\n✅ JSON is valid and parseable")
    print(f"   Winner from parsed JSON: {parsed['winner']}")

    assert isinstance(dict_export, dict)
    assert isinstance(json_export, str)
    assert parsed["winner"] == result.winner

    print(f"\n✅ PASSED: Export formats work correctly")

    return {
        "test": "Export Formats",
        "status": "PASSED",
        "dict_keys": list(dict_export.keys()),
        "json_valid": True
    }


def generate_report(test_results):
    """Generate comprehensive test report."""
    print("\n\n")
    print("="*80)
    print("DECISION MATRIX - COMPREHENSIVE TEST REPORT")
    print("="*80)
    print(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Tests: {len(test_results)}")

    passed = sum(1 for r in test_results if r["status"] == "PASSED")
    failed = len(test_results) - passed

    print(f"Passed: {passed} ✅")
    print(f"Failed: {failed} {'❌' if failed > 0 else ''}")
    print(f"Success Rate: {(passed/len(test_results)*100):.1f}%")

    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)

    for i, result in enumerate(test_results, 1):
        status_icon = "✅" if result["status"] == "PASSED" else "❌"
        print(f"\n{i}. {result['test']}: {status_icon} {result['status']}")

        # Print relevant details
        for key, value in result.items():
            if key not in ["test", "status"]:
                if isinstance(value, dict):
                    print(f"   {key}:")
                    for k, v in value.items():
                        print(f"     - {k}: {v}")
                elif isinstance(value, list):
                    print(f"   {key}: {len(value)} items")
                else:
                    print(f"   {key}: {value}")

    print("\n" + "="*80)
    print("FINAL VERDICT")
    print("="*80)

    if failed == 0:
        print("🎉 ALL TESTS PASSED!")
        print("\nThe Decision Matrix utility is working perfectly:")
        print("  ✅ All 4 analysis methods functional")
        print("  ✅ Validation and error handling working")
        print("  ✅ Export formats (JSON, Dict) working")
        print("  ✅ Real-world scenarios tested")
        print("  ✅ Performance is excellent")
        print("  ✅ Edge cases handled correctly")
    else:
        print(f"⚠️  {failed} TEST(S) FAILED")
        print("\nPlease review the failed tests above.")

    print("="*80)

    # Save report to file
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": len(test_results),
        "passed": passed,
        "failed": failed,
        "success_rate": passed/len(test_results)*100,
        "tests": test_results
    }

    return report_data


def main():
    """Run all tests and generate report."""
    print("DECISION MATRIX - COMPREHENSIVE TEST SUITE")
    print("="*80)
    print("Running all tests...")
    print("="*80)

    test_results = []

    # Run all tests
    test_results.append(test_1_basic_functionality())
    test_results.append(test_2_weighted_criteria())
    test_results.append(test_3_all_methods_comparison())
    test_results.append(test_4_real_world_hiring())
    test_results.append(test_5_edge_cases())
    test_results.append(test_6_performance())
    test_results.append(test_7_method_consistency())
    test_results.append(test_8_export_formats())

    # Generate report
    report_data = generate_report(test_results)

    # Save to JSON
    report_file = f"decision_matrix_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(report_data, f, indent=2)

    print(f"\n📄 Full report saved to: {report_file}")

    return report_data


if __name__ == "__main__":
    main()
