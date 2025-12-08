#!/usr/bin/env python3
"""
Technical Debt Tracking Demo
============================

Demonstrates NovaSystem's technical debt tracking capabilities:
- Creating and managing technical debt items
- Prioritization based on severity and impact
- Status tracking (backlog, in_progress, resolved)
- Component-based filtering
- Reporting and analytics

Run:
    python examples/technical_debt_tracking_demo.py
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

# Add parent to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from novasystem.tools.technical_debt import (
    TechnicalDebtItem,
    TechnicalDebtManager,
    Severity,
    Status,
)


def create_sample_debt_items() -> List[TechnicalDebtItem]:
    """Create a realistic set of technical debt items."""
    items = [
        TechnicalDebtItem(
            key="TD-001",
            title="Legacy authentication module needs refactoring",
            description="The current authentication module uses deprecated password hashing and needs bcrypt.",
            severity=Severity.HIGH,
            component="auth",
        ),
        TechnicalDebtItem(
            key="TD-002",
            title="Missing unit tests for payment processing",
            description="Payment processing has only 30% test coverage. Critical paths are untested.",
            severity=Severity.HIGH,
            component="payments",
        ),
        TechnicalDebtItem(
            key="TD-003",
            title="Database queries need optimization",
            description="N+1 query issues in product catalog cause slow page loads.",
            severity=Severity.MEDIUM,
            component="database",
        ),
        TechnicalDebtItem(
            key="TD-004",
            title="Update deprecated npm packages",
            description="12 npm packages are outdated, 3 have known vulnerabilities.",
            severity=Severity.HIGH,
            component="frontend",
        ),
        TechnicalDebtItem(
            key="TD-005",
            title="API documentation is outdated",
            description="OpenAPI spec doesn't match current endpoints.",
            severity=Severity.LOW,
            component="api",
        ),
        TechnicalDebtItem(
            key="TD-006",
            title="Logging inconsistencies across services",
            description="Different services use different log formats.",
            severity=Severity.MEDIUM,
            component="infrastructure",
        ),
        TechnicalDebtItem(
            key="TD-007",
            title="Error handling needs standardization",
            description="Inconsistent error responses across API endpoints.",
            severity=Severity.MEDIUM,
            component="api",
        ),
        TechnicalDebtItem(
            key="TD-008",
            title="Remove feature flags for launched features",
            description="15 feature flags for features launched 6+ months ago.",
            severity=Severity.LOW,
            component="core",
        ),
    ]
    return items


def print_header(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f" {title} ".center(70, "="))
    print("=" * 70)


def print_item(item: TechnicalDebtItem, index: int = None):
    """Print a formatted debt item."""
    severity_colors = {
        Severity.HIGH: "\033[93m",      # Yellow
        Severity.MEDIUM: "\033[94m",    # Blue
        Severity.LOW: "\033[92m",       # Green
    }
    status_icons = {
        Status.OPEN: "📋",
        Status.IN_PROGRESS: "🔄",
        Status.RESOLVED: "✅",
    }

    color = severity_colors.get(item.severity, "")
    reset = "\033[0m"
    icon = status_icons.get(item.status, "❓")

    prefix = f"{index}. " if index else ""
    print(f"\n{prefix}{icon} {color}[{item.severity.value.upper()}]{reset} {item.key}: {item.title}")
    print(f"   Component: {item.component or 'N/A'} | Status: {item.status.value}")
    if item.status == Status.RESOLVED:
        print(f"   ✅ Resolved")


def print_table(items: List[TechnicalDebtItem]):
    """Print items in a table format."""
    print("\n┌" + "─" * 10 + "┬" + "─" * 10 + "┬" + "─" * 15 + "┬" + "─" * 15 + "┐")
    print(f"│ {'Key':<8} │ {'Severity':<8} │ {'Component':<13} │ {'Status':<13} │")
    print("├" + "─" * 10 + "┼" + "─" * 10 + "┼" + "─" * 15 + "┼" + "─" * 15 + "┤")

    for item in items:
        severity_colors = {
            Severity.HIGH: "\033[93m",
            Severity.MEDIUM: "\033[94m",
            Severity.LOW: "\033[92m",
        }
        color = severity_colors.get(item.severity, "")
        reset = "\033[0m"
        comp = (item.component or "N/A")[:13]

        print(f"│ {item.key:<8} │ {color}{item.severity.value:<8}{reset} │ {comp:<13} │ {item.status.value:<13} │")

    print("└" + "─" * 10 + "┴" + "─" * 10 + "┴" + "─" * 15 + "┴" + "─" * 15 + "┘")


def main():
    """Run the technical debt tracking demo."""
    print("\n" + "🔧" * 35)
    print("\n  NOVASYSTEM TECHNICAL DEBT TRACKING DEMO\n")
    print("🔧" * 35)

    # Create manager and add items
    manager = TechnicalDebtManager()

    print_header("LOADING TECHNICAL DEBT ITEMS")
    items = create_sample_debt_items()
    manager.extend(items)
    print(f"✅ Loaded {len(items)} technical debt items")

    # Show all items
    print_header("ALL TECHNICAL DEBT ITEMS")
    print_table(list(manager))

    # Show prioritized list
    print_header("PRIORITIZED BY SEVERITY")
    prioritized = manager.prioritized()
    for i, item in enumerate(prioritized, 1):
        print_item(item, i)

    # Filter by component
    print_header("DEBT BY COMPONENT: API")
    api_items = [i for i in manager if i.component == "api"]
    for item in api_items:
        print_item(item)

    # Show severity breakdown
    print_header("SEVERITY BREAKDOWN")
    breakdown = {}
    for item in manager:
        sev = item.severity
        breakdown[sev] = breakdown.get(sev, 0) + 1

    total = sum(breakdown.values()) or 1

    for severity, count in sorted(breakdown.items(), key=lambda x: x[1], reverse=True):
        bar_length = int((count / total) * 30)
        bar = "█" * bar_length
        percentage = (count / total) * 100
        print(f"  {severity.value:>10}: {bar:<30} {count} ({percentage:.0f}%)")

    # Simulate working on items
    print_header("SIMULATING SPRINT WORK")

    # Start working on high severity item
    high_items = [i for i in prioritized if i.severity == Severity.HIGH]
    if high_items:
        item = high_items[0]
        print(f"\n🔄 Starting work on {item.key}: {item.title}")
        item.mark_in_progress()  # Call method on item itself
        print(f"   Status changed to: {item.status.value}")

    # Resolve a low priority item
    low_items = [i for i in prioritized if i.severity == Severity.LOW]
    if low_items:
        item = low_items[0]
        print(f"\n✅ Resolving {item.key}: {item.title}")
        item.mark_resolved()  # Call method on item itself
        print(f"   Status changed to: {item.status.value}")

    # Show item details
    print_header("ITEM DETAILS")
    update_item = next((i for i in manager if i.key == "TD-003"), None)
    if update_item:
        print(f"Key: {update_item.key}")
        print(f"Title: {update_item.title}")
        print(f"Description: {update_item.description[:80]}...")
        print(f"Severity: {update_item.severity.value}")
        print(f"Component: {update_item.component}")

    # Show final status
    print_header("FINAL STATUS SUMMARY")

    open_count = len([i for i in manager if i.status == Status.OPEN])
    in_progress_count = len([i for i in manager if i.status == Status.IN_PROGRESS])
    resolved_count = len([i for i in manager if i.status == Status.RESOLVED])
    high_count = len([i for i in manager if i.severity == Severity.HIGH])
    medium_count = len([i for i in manager if i.severity == Severity.MEDIUM])
    low_count = len([i for i in manager if i.severity == Severity.LOW])

    print(f"""
📊 Technical Debt Summary:
   • Total Items: {len(list(manager))}
   • Open: {open_count}
   • In Progress: {in_progress_count}
   • Resolved: {resolved_count}

🔥 By Severity:
   • High: {high_count}
   • Medium: {medium_count}
   • Low: {low_count}
""")

    # Export capability
    print_header("EXPORT CAPABILITY")
    all_items = list(manager)
    exported = [item.to_dict() for item in all_items]
    print(f"✅ Exported {len(exported)} items")

    # Show components
    print("\n📦 Components with debt:")
    components = set(item.component for item in manager if item.component)
    for comp in sorted(components):
        count = len([i for i in manager if i.component == comp])
        print(f"   • {comp}: {count} item(s)")

    print("\n" + "=" * 70)
    print(" DEMO COMPLETE ".center(70, "="))
    print("=" * 70)
    print("""
✨ This demo showed:
   • Creating and managing technical debt items
   • Prioritization by severity
   • Component-based filtering
   • Status tracking (backlog → in_progress → resolved)
   • Severity breakdown analytics
   • Export capabilities

💡 Use technical debt tracking to:
   • Make informed decisions about what to fix first
   • Track progress on reducing debt
   • Communicate debt status to stakeholders
   • Plan capacity for debt reduction in sprints
""")


if __name__ == "__main__":
    main()
