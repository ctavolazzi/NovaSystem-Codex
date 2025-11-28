from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from novasystem.technical_debt import (
    Severity,
    Status,
    TechnicalDebtItem,
    TechnicalDebtManager,
)


def make_sample_items():
    return [
        TechnicalDebtItem(
            key="logging-side-effects",
            title="Logging configured on import",
            description="CLI configures logging handlers during import time.",
            severity=Severity.HIGH,
            component="cli",
            remediation="Move configuration behind explicit setup function.",
        ),
        TechnicalDebtItem(
            key="unbounded-deps",
            title="Dependencies are unpinned",
            description="Runtime dependencies have broad version ranges.",
            severity=Severity.MEDIUM,
            component="packaging",
            remediation="Add pinned ranges and separate dev dependencies.",
        ),
        TechnicalDebtItem(
            key="sqlite-lifecycle",
            title="SQLite lifecycle is implicit",
            description="Database connections lack lifecycle hooks.",
            severity=Severity.MEDIUM,
            component="database",
            remediation="Add context manager support and explicit close semantics.",
        ),
    ]


def test_prioritized_orders_by_severity():
    manager = TechnicalDebtManager(make_sample_items())

    prioritized_keys = [item.key for item in manager.prioritized()]

    assert prioritized_keys[0] == "logging-side-effects"
    assert prioritized_keys.count("logging-side-effects") == 1
    assert len(prioritized_keys) == 3


def test_add_item_rejects_duplicates():
    manager = TechnicalDebtManager()
    item = TechnicalDebtItem(
        key="duplicate",
        title="Duplicate entry",
        description="Example entry.",
        severity=Severity.LOW,
    )
    manager.add_item(item)

    with pytest.raises(ValueError):
        manager.add_item(item)

    with pytest.raises(TypeError):
        manager.add_item("not-an-item")  # type: ignore[arg-type]


def test_update_status_and_summary():
    manager = TechnicalDebtManager(make_sample_items())

    manager.update_status("logging-side-effects", Status.IN_PROGRESS)
    manager.update_status("unbounded-deps", Status.RESOLVED)

    summary = manager.summary()

    assert summary == {
        Status.OPEN.value: 1,
        Status.IN_PROGRESS.value: 1,
        Status.RESOLVED.value: 1,
    }

    with pytest.raises(TypeError):
        manager.update_status("logging-side-effects", "open")  # type: ignore[arg-type]


def test_filter_by_component_and_backlog_resolution():
    manager = TechnicalDebtManager(make_sample_items())

    database_items = manager.by_component("database")
    assert len(database_items) == 1
    assert database_items[0].key == "sqlite-lifecycle"

    manager.update_status("sqlite-lifecycle", Status.RESOLVED)
    assert manager.by_component("database") == []
    assert len(manager.backlog()) == 2
    assert len(manager.backlog(include_resolved=True)) == 3

    assert manager.by_status(Status.RESOLVED)[0].key == "sqlite-lifecycle"

    removed = manager.remove_item("unbounded-deps")
    assert removed.key == "unbounded-deps"
    assert "unbounded-deps" not in manager
    assert len(manager) == 2


def test_component_index_uses_set_and_updates_with_changes():
    manager = TechnicalDebtManager(make_sample_items())

    assert manager.components() == {"cli", "packaging", "database"}
    assert manager.components(include_resolved=False) == {"cli", "packaging", "database"}

    manager.update_item("sqlite-lifecycle", component="storage")
    assert manager.components() == {"cli", "packaging", "storage"}
    assert manager.by_component("database") == []
    assert [item.key for item in manager.by_component("storage")] == ["sqlite-lifecycle"]

    manager.update_status("sqlite-lifecycle", Status.RESOLVED)
    assert manager.components(include_resolved=False) == {"cli", "packaging"}
    assert manager.components(include_resolved=True) == {"cli", "packaging", "storage"}

    manager.remove_item("unbounded-deps")
    assert manager.components() == {"cli", "storage"}
    assert manager.by_component("packaging") == []


def test_mark_helpers_change_status():
    item = TechnicalDebtItem(
        key="helpers",
        title="Helpers should transition status",
        description="Marker methods should set lifecycle state.",
        severity=Severity.LOW,
    )

    item.mark_in_progress()
    assert item.status is Status.IN_PROGRESS

    item.mark_resolved()
    assert item.status is Status.RESOLVED


def test_item_validation_and_extend_duplicate_detection():
    with pytest.raises(ValueError):
        TechnicalDebtItem(
            key="",
            title="Missing key",
            description="Key must not be empty.",
            severity=Severity.LOW,
        )

    with pytest.raises(TypeError):
        TechnicalDebtItem(
            key="bad-severity",
            title="Invalid severity",
            description="Severity must be an enum value.",
            severity="low",  # type: ignore[arg-type]
        )

    with pytest.raises(ValueError):
        TechnicalDebtItem(
            key="whitespace-key",
            title="   ",
            description="Title cannot be blank.",
            severity=Severity.LOW,
        )

    with pytest.raises(TypeError):
        TechnicalDebtItem(
            key="component-type",
            title="Component must be a string",
            description="Component field type is enforced.",
            severity=Severity.LOW,
            component=123,  # type: ignore[arg-type]
        )

    with pytest.raises(ValueError):
        TechnicalDebtItem(
            key="remediation-blank",
            title="Remediation must not be empty",
            description="Whitespace remediation should be rejected.",
            severity=Severity.LOW,
            remediation="   ",
        )

    manager = TechnicalDebtManager()
    items = make_sample_items()
    manager.extend(items)

    with pytest.raises(ValueError):
        manager.extend(items)

    # ensure extend is atomic when duplicates are detected
    conflicting = items + [
        TechnicalDebtItem(
            key="logging-side-effects",  # duplicate of first item
            title="Duplicate during bulk add",
            description="Should prevent partial writes.",
            severity=Severity.HIGH,
        )
    ]

    with pytest.raises(ValueError):
        manager.extend(conflicting)

    assert len(manager) == len(items)

    fresh_manager = TechnicalDebtManager()
    with pytest.raises(TypeError):
        fresh_manager.extend([items[0], "invalid"])
    assert len(fresh_manager) == 0


def test_update_item_validates_before_mutation():
    manager = TechnicalDebtManager(make_sample_items())

    updated = manager.update_item(
        "logging-side-effects",
        title="Logging configured on import (updated)",
        description="Ensure logging side effects are controlled.",
        severity=Severity.MEDIUM,
        component="cli",
        remediation="Move configuration behind setup().",
    )

    assert updated.title.endswith("(updated)")
    assert updated.description.startswith("Ensure logging")
    assert updated.severity is Severity.MEDIUM
    assert updated.component == "cli"
    assert updated.remediation == "Move configuration behind setup()."

    with pytest.raises(TypeError):
        manager.update_item("logging-side-effects", severity="low")  # type: ignore[arg-type]

    with pytest.raises(ValueError):
        manager.update_item("logging-side-effects", title="   ")

    with pytest.raises(ValueError):
        manager.update_item("logging-side-effects", remediation=" ")

    with pytest.raises(KeyError):
        manager.update_item("unknown", title="new title")


def test_filter_by_severity_respects_resolution():
    manager = TechnicalDebtManager(make_sample_items())

    high = manager.by_severity(Severity.HIGH)
    assert [item.key for item in high] == ["logging-side-effects"]

    manager.update_status("logging-side-effects", Status.RESOLVED)
    assert manager.by_severity(Severity.HIGH) == []
    assert [item.key for item in manager.by_severity(Severity.HIGH, include_resolved=True)] == [
        "logging-side-effects"
    ]

    with pytest.raises(TypeError):
        manager.by_severity("high")  # type: ignore[arg-type]


def test_item_serialization_round_trip_and_validation():
    item = TechnicalDebtItem(
        key="serialize-me",
        title="Serialize and restore",
        description="Items should convert to/from dictionaries.",
        severity=Severity.MEDIUM,
        remediation="Documented remediation",
        status=Status.IN_PROGRESS,
    )

    data = item.to_dict()
    assert data["severity"] == Severity.MEDIUM.value
    assert data["status"] == Status.IN_PROGRESS.value

    restored = TechnicalDebtItem.from_dict(data)
    assert restored.key == item.key
    assert restored.status is Status.IN_PROGRESS
    assert restored.severity is Severity.MEDIUM
    assert restored.remediation == "Documented remediation"

    with pytest.raises(TypeError):
        TechnicalDebtItem.from_dict("not-a-dict")  # type: ignore[arg-type]

    with pytest.raises(KeyError):
        TechnicalDebtItem.from_dict({"title": "missing required"})

    with pytest.raises(ValueError):
        TechnicalDebtItem.from_dict(
            {
                "key": "bad-severity",
                "title": "Invalid severity",
                "description": "Should fail.",
                "severity": "unknown",
            }
        )

    with pytest.raises(ValueError):
        TechnicalDebtItem.from_dict(
            {
                "key": "bad-status",
                "title": "Invalid status",
                "description": "Should fail.",
                "severity": Severity.LOW.value,
                "status": "unknown",
            }
        )


def test_manager_export_and_severity_breakdown():
    manager = TechnicalDebtManager(make_sample_items())

    export = manager.export()
    assert len(export) == len(manager.backlog())
    assert {entry["severity"] for entry in export} == {"high", "medium"}

    breakdown = manager.breakdown_by_severity()
    assert breakdown == {"low": 0, "medium": 2, "high": 1}

    manager.update_status("logging-side-effects", Status.RESOLVED)

    unresolved_export = manager.export()
    assert len(unresolved_export) == 2
    assert {entry["key"] for entry in unresolved_export} == {
        "unbounded-deps",
        "sqlite-lifecycle",
    }

    resolved_included = manager.export(include_resolved=True)
    assert len(resolved_included) == 3

    unresolved_breakdown = manager.breakdown_by_severity()
    assert unresolved_breakdown == {"low": 0, "medium": 2, "high": 0}

    resolved_breakdown = manager.breakdown_by_severity(include_resolved=True)
    assert resolved_breakdown == {"low": 0, "medium": 2, "high": 1}


def test_manager_iteration_includes_resolved_items():
    manager = TechnicalDebtManager(make_sample_items())
    manager.update_status("logging-side-effects", Status.RESOLVED)

    iterated_keys = {item.key for item in manager}

    assert iterated_keys == {"logging-side-effects", "unbounded-deps", "sqlite-lifecycle"}
    assert len(list(manager)) == len(manager)


def test_manager_ingest_round_trip_and_atomic_behavior():
    manager = TechnicalDebtManager(make_sample_items())
    exported = manager.export(include_resolved=True)

    restored = TechnicalDebtManager()
    restored.ingest(exported)

    assert len(restored) == len(manager)
    assert restored.backlog()[0].key in {item["key"] for item in exported}

    with pytest.raises(ValueError):
        restored.ingest(exported)

    with pytest.raises(TypeError):
        restored.ingest([exported[0], "not-a-dict"])  # type: ignore[list-item]

    assert len(restored) == len(exported)
