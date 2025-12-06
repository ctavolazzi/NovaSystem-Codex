#!/usr/bin/env python3
"""Security Probe for Nova MVP v0.2.0

Tests for vulnerabilities:
1. State File Corruption resilience
2. Race Condition / Last Writer Wins
3. SQL Injection resistance
4. PII/Sensitive Data Leakage

Run: python3 security_probe.py
"""

import os
import sys
import json
import sqlite3
import time

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test file paths (isolated from production)
TEST_STATE = "probe_traffic.json"
TEST_DB = "probe_usage.db"


def print_header(msg):
    print(f"\n🔎 PROBE: {msg}")


def print_result(status, msg):
    colors = {"PASS": "\033[92m", "FAIL": "\033[91m", "WARN": "\033[93m"}
    color = colors.get(status, "\033[0m")
    reset = "\033[0m"
    print(f"   {color}[{status}]{reset} {msg}")


def cleanup():
    for f in [TEST_STATE, TEST_DB, f"{TEST_STATE}.tmp"]:
        if os.path.exists(f):
            os.remove(f)


def probe_corruption_resilience():
    """
    VULNERABILITY: State File Corruption
    Scenario: Power goes out while writing JSON, leaving a half-written file.
    Goal: The app should start with a fresh state, not crash.
    """
    print_header("Testing Resilience to Corrupted State Files")
    
    from backend.core.traffic import TrafficController
    
    # 1. Create a corrupted JSON file (half-written)
    with open(TEST_STATE, "w") as f:
        f.write('{"window_seconds": 60, "requests": {"model": [[123456.7, 100')  # Truncated
    
    try:
        # 2. Attempt to initialize the controller with corrupted file
        tc = TrafficController(state_file=TEST_STATE, persist=True)
        # If we get here, it recovered
        print_result("PASS", "TrafficController recovered from corrupted JSON (started fresh).")
        return True
    except json.JSONDecodeError as e:
        print_result("FAIL", f"CRASHED! JSONDecodeError: {e}")
        return False
    except Exception as e:
        print_result("FAIL", f"CRASHED! Unexpected error: {e}")
        return False


def probe_race_condition():
    """
    VULNERABILITY: Race Condition / Last Writer Wins
    Scenario: Two CLI instances run at once.
    Goal: Identify if data is overwritten.
    """
    print_header("Testing Concurrency / Race Conditions")
    
    cleanup()
    
    from backend.core.traffic import TrafficController
    
    # Instance A loads state (empty)
    tc_A = TrafficController(state_file=TEST_STATE, persist=True)
    
    # Instance B loads state (empty) - simulates second process
    tc_B = TrafficController(state_file=TEST_STATE, persist=True)
    
    # A logs a request
    tc_A.check_allowance("test-model", 100, estimated_output_tokens=500, commit=True)
    
    # B logs a request
    tc_B.check_allowance("test-model", 200, estimated_output_tokens=300, commit=True)
    
    # A saves (writes its state)
    tc_A._save_state()
    
    # B saves (writes its state) - DOES IT OVERWRITE A?
    tc_B._save_state()
    
    # Reload to see what survived
    tc_final = TrafficController(state_file=TEST_STATE, persist=True)
    requests = tc_final._requests.get("test-model", [])
    count = len(requests)
    
    if count == 2:
        print_result("PASS", "Both requests survived (Merging logic exists).")
        return True
    else:
        print_result("FAIL", f"Data Loss! Expected 2 requests, found {count}. (Last Writer Won).")
        return False


def probe_sql_injection():
    """
    VULNERABILITY: SQL Injection
    Scenario: A malicious context string attempts to drop the table.
    Goal: Ensure parameterized queries are used.
    """
    print_header("Testing SQL Injection in Usage Ledger")
    
    cleanup()
    
    from backend.core.usage import UsageLedger, Transaction
    
    ledger = UsageLedger(db_file=TEST_DB)
    
    # The payload: Try to terminate the string and drop the table
    evil_context = "test'); DROP TABLE transactions; --"
    
    t = Transaction(
        timestamp=time.time(),
        model="test-model",
        provider="test",
        input_tokens=100,
        output_tokens=100,
        estimated_cost=0.10,
        context=evil_context
    )
    ledger.record(t)
    
    # Check if table still exists
    try:
        with sqlite3.connect(TEST_DB) as conn:
            result = conn.execute("SELECT count(*) FROM transactions").fetchone()[0]
        if result >= 1:
            print_result("PASS", f"Table survived injection attempt ({result} row(s)).")
            return True
        else:
            print_result("FAIL", "Table exists but no data - possible injection issue.")
            return False
    except sqlite3.OperationalError as e:
        print_result("FAIL", f"Table was deleted or corrupted! Error: {e}")
        return False


def probe_pii_leak():
    """
    VULNERABILITY: Cleartext PII Logging
    Scenario: User puts a password or secret in the 'context'.
    Goal: Warn that the DB stores this in plain text.
    """
    print_header("Testing PII / Sensitive Data Leakage")
    
    cleanup()
    
    from backend.core.usage import UsageLedger, Transaction
    
    ledger = UsageLedger(db_file=TEST_DB)
    secret = "MySuperSecretPassword123"
    
    t = Transaction(
        timestamp=time.time(),
        model="test-model",
        provider="test",
        input_tokens=100,
        output_tokens=100,
        estimated_cost=0.10,
        context=f"auth_check:{secret}"
    )
    ledger.record(t)
    
    # Simulate an attacker reading the DB file
    with open(TEST_DB, "rb") as f:
        content = f.read()
        if secret.encode() in content:
            print_result("WARN", "Sensitive data found in CLEARTEXT in .db file.")
            print_result("WARN", "→ Never store secrets/PII in the context field!")
            return None  # Warning, not pass/fail
        else:
            print_result("PASS", "Sensitive data not found in cleartext (unexpected).")
            return True


def probe_budget_limit():
    """
    VULNERABILITY: Open Wallet / No Budget Cap
    Scenario: Runaway process drains API budget.
    Goal: Check if budget limits exist.
    """
    print_header("Testing Budget Limit / Circuit Breaker")
    
    from backend.core.usage import UsageLedger
    
    # Check if budget enforcement exists
    ledger = UsageLedger.__dict__
    has_budget_check = any('budget' in str(v).lower() for v in ledger.values())
    
    if has_budget_check:
        print_result("PASS", "Budget enforcement logic detected.")
        return True
    else:
        print_result("WARN", "No budget cap implemented - runaway costs possible.")
        print_result("WARN", "→ Consider adding a daily spend limit.")
        return None


def run_probes():
    """Run all security probes."""
    print("=" * 60)
    print("  🛑 NOVA v0.2.0 SECURITY PROBE")
    print("=" * 60)
    
    cleanup()
    
    results = []
    
    try:
        results.append(("Corruption Resilience", probe_corruption_resilience()))
        cleanup()
        results.append(("Race Conditions", probe_race_condition()))
        cleanup()
        results.append(("SQL Injection", probe_sql_injection()))
        cleanup()
        results.append(("PII Leakage", probe_pii_leak()))
        cleanup()
        results.append(("Budget Limits", probe_budget_limit()))
    except Exception as e:
        print(f"\n❌ PROBE ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cleanup()
    
    # Summary
    print("\n" + "=" * 60)
    print("  VULNERABILITY SUMMARY")
    print("=" * 60)
    
    for name, result in results:
        if result is True:
            status = "✅ SECURE"
        elif result is False:
            status = "🔴 VULNERABLE"
        else:
            status = "⚠️  WARNING"
        print(f"  {status}: {name}")
    
    critical_fails = sum(1 for _, r in results if r is False)
    if critical_fails > 0:
        print(f"\n⚠️  {critical_fails} CRITICAL VULNERABILITY(S) FOUND")
        return 1
    else:
        print("\n✅ No critical vulnerabilities detected.")
        return 0


if __name__ == "__main__":
    sys.exit(run_probes())
