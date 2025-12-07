#!/usr/bin/env python3
"""Release Candidate Verification Script for Nova MVP v0.2.0

Tests that all persistence layers and integrations work correctly:
1. Traffic Controller (JSON persistence)
2. Usage Ledger (SQLite persistence)
3. Full module integration

Run: python3 verify_release.py
"""

import os
import sys
import time

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test file paths (isolated from production)
TEST_DB = "release_test_usage.db"
TEST_TRAFFIC = "release_test_traffic.json"


def print_header(msg):
    print(f"\n{'=' * 60}")
    print(f"  {msg}")
    print(f"{'=' * 60}")


def print_step(msg):
    print(f"\n🔹 {msg}")


def print_pass(msg):
    print(f"   ✅ PASS: {msg}")


def print_fail(msg):
    print(f"   ❌ FAIL: {msg}")
    return False


def cleanup():
    """Remove test files."""
    for f in [TEST_DB, TEST_TRAFFIC]:
        if os.path.exists(f):
            os.remove(f)


def test_traffic_persistence():
    """Test 1: Traffic Controller JSON Persistence"""
    print_step("Test 1: Traffic Controller Persistence")

    from backend.core.traffic import TrafficController

    # Create controller with test state file
    tc = TrafficController(state_file=TEST_TRAFFIC, persist=True)

    # Simulate some API calls
    tc.check_allowance("gemini-2.5-flash", 100, estimated_output_tokens=500, commit=True)
    tc.check_allowance("gemini-2.5-flash", 200, estimated_output_tokens=300, commit=True)

    # Force save
    tc._save_state()

    if not os.path.exists(TEST_TRAFFIC):
        return print_fail("Traffic state file not created")

    print_pass(f"State file created: {TEST_TRAFFIC}")

    # Create NEW controller (simulates restart)
    tc_new = TrafficController(state_file=TEST_TRAFFIC, persist=True)

    # Check if state was reloaded
    flash_requests = tc_new._requests.get("gemini-2.5-flash", [])
    if len(flash_requests) >= 2:
        print_pass(f"Traffic state persisted and reloaded ({len(flash_requests)} requests)")
        return True
    else:
        return print_fail(f"Traffic state lost on reload (expected 2, got {len(flash_requests)})")


def test_usage_ledger():
    """Test 2: Usage Ledger SQLite Persistence"""
    print_step("Test 2: Usage Ledger Persistence & Analytics")

    from backend.core.usage import UsageLedger, Transaction

    # Create ledger with test database
    ledger = UsageLedger(db_file=TEST_DB)

    if not os.path.exists(TEST_DB):
        return print_fail("Usage database not created")

    print_pass(f"Database created: {TEST_DB}")

    # Log simulated transactions
    t1 = Transaction(
        timestamp=time.time(),
        model="gemini-2.5-flash",
        provider="mock",
        input_tokens=100,
        output_tokens=500,
        estimated_cost=0.0005,
        actual_cost=0.0006,
        context="test"
    )
    t2 = Transaction(
        timestamp=time.time(),
        model="gemini-2.5-flash",
        provider="mock",
        input_tokens=200,
        output_tokens=300,
        estimated_cost=0.0003,
        context="test"
    )
    t3 = Transaction(
        timestamp=time.time(),
        model="gemini-3-pro",
        provider="mock",
        input_tokens=100,
        output_tokens=200,
        estimated_cost=0.0050,
        actual_cost=0.0055,
        context="test"
    )

    ledger.record(t1)
    ledger.record(t2)
    ledger.record(t3)

    # Verify count
    count = ledger.count()
    if count != 3:
        return print_fail(f"Transaction count wrong. Expected 3, got {count}")
    print_pass(f"Recorded {count} transactions")

    # Verify totals
    total = ledger.total_spend()
    expected = 0.0006 + 0.0003 + 0.0055  # actual or estimated
    if abs(total - expected) < 0.0001:
        print_pass(f"Total spend accurate: ${total:.6f}")
    else:
        return print_fail(f"Total spend mismatch. Expected {expected}, got {total}")

    # Verify breakdown
    by_model = ledger.spend_by_model()
    if "gemini-2.5-flash" in by_model and "gemini-3-pro" in by_model:
        print_pass(f"Spend by model: {by_model}")
    else:
        return print_fail(f"Model breakdown missing keys: {by_model}")

    # Verify drift calculation
    drift = ledger.average_drift_pct()
    if drift is not None:
        print_pass(f"Average drift calculated: {drift:.2f}%")
    else:
        return print_fail("Drift calculation returned None")

    # Verify persistence (new ledger instance)
    ledger2 = UsageLedger(db_file=TEST_DB)
    if ledger2.count() == 3:
        print_pass("Ledger data persisted across instances")
        return True
    else:
        return print_fail("Ledger data lost on reload")


def test_module_integration():
    """Test 3: Full Module Integration"""
    print_step("Test 3: Module Integration")

    try:
        from backend.core import (
            get_llm,
            CostEstimator,
            TrafficController,
            UsageLedger,
            NovaProcess,
        )
        print_pass("All core modules imported")
    except ImportError as e:
        return print_fail(f"Import error: {e}")

    # Test LLM factory
    try:
        mock_llm = get_llm("mock")
        if mock_llm.is_available():
            print_pass("MockProvider initialized and available")
        else:
            return print_fail("MockProvider not available")
    except Exception as e:
        return print_fail(f"LLM factory error: {e}")

    # Test cost estimator
    try:
        estimator = CostEstimator()
        estimate = estimator.estimate("gemini-2.5-flash", "Hello world", 1000)
        if estimate.projected_cost > 0:
            print_pass(f"Cost estimation working: ${estimate.projected_cost:.6f}")
        else:
            return print_fail("Cost estimation returned zero")
    except Exception as e:
        return print_fail(f"Cost estimator error: {e}")

    return True


def test_cli_report():
    """Test 4: CLI Report Command"""
    print_step("Test 4: CLI Report Integration")

    try:
        from cli.nova import usage_report, _format_money

        # Test money formatting
        formatted = _format_money(0.001234)
        if "$" in formatted:
            print_pass(f"Money formatting works: {formatted}")
        else:
            return print_fail("Money formatting broken")

        print_pass("CLI report functions importable")
        return True
    except ImportError as e:
        return print_fail(f"CLI import error: {e}")


def run_verification():
    """Run all verification tests."""
    print_header("NOVA MVP v0.2.0 RELEASE VERIFICATION")

    cleanup()

    results = []

    try:
        results.append(("Traffic Persistence", test_traffic_persistence()))
        results.append(("Usage Ledger", test_usage_ledger()))
        results.append(("Module Integration", test_module_integration()))
        results.append(("CLI Report", test_cli_report()))
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        cleanup()
        sys.exit(1)

    # Summary
    print_header("VERIFICATION SUMMARY")

    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {name}")
        if not passed:
            all_passed = False

    cleanup()

    if all_passed:
        print("\n✨ RELEASE CANDIDATE VERIFIED. READY FOR DEPLOY.\n")
        return 0
    else:
        print("\n⚠️  VERIFICATION FAILED. DO NOT RELEASE.\n")
        return 1


if __name__ == "__main__":
    sys.exit(run_verification())
