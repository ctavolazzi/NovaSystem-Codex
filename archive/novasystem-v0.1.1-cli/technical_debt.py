"""Technical debt backlog utilities.

Provides data structures and a small manager abstraction for tracking
technical debt items in codebases. The manager supports basic backlog
operations such as adding new items, enumerating work by severity, and
marking items as resolved.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Iterable, List, Optional, Sequence, Set


_UNSET = object()


class Severity(Enum):
    """Severity levels for technical debt items."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    @property
    def rank(self) -> int:
        """Numeric rank for sorting, higher means more severe."""

        return {Severity.LOW: 1, Severity.MEDIUM: 2, Severity.HIGH: 3}[self]


class Status(Enum):
    """Lifecycle status for technical debt items."""

    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"


@dataclass
class TechnicalDebtItem:
    """Represents a single technical debt item."""

    key: str
    title: str
    description: str
    severity: Severity
    component: Optional[str] = None
    remediation: Optional[str] = None
    status: Status = field(default=Status.OPEN)

    def __post_init__(self) -> None:
        if not isinstance(self.key, str):
            raise TypeError("key must be a string")
        self.key = self.key.strip()
        if not self.key:
            raise ValueError("Technical debt items require a non-empty key")
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("title must be a non-empty string")
        if not isinstance(self.description, str) or not self.description.strip():
            raise ValueError("description must be a non-empty string")
        if not isinstance(self.severity, Severity):
            raise TypeError("severity must be a Severity value")
        if not isinstance(self.status, Status):
            raise TypeError("status must be a Status value")
        if self.component is not None:
            if not isinstance(self.component, str):
                raise TypeError("component must be a string when provided")
            self.component = self.component.strip()
            if not self.component:
                raise ValueError("component must not be empty when provided")
        if self.remediation is not None:
            if not isinstance(self.remediation, str):
                raise TypeError("remediation must be a string when provided")
            self.remediation = self.remediation.strip()
            if not self.remediation:
                raise ValueError("remediation must not be empty when provided")

    def mark_in_progress(self) -> None:
        """Move the item into an in-progress state."""

        self.status = Status.IN_PROGRESS

    def mark_resolved(self) -> None:
        """Mark the item as resolved."""

        self.status = Status.RESOLVED

    def to_dict(self) -> Dict[str, object]:
        """Serialize the item to a plain dictionary suitable for JSON."""

        return {
            "key": self.key,
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "component": self.component,
            "remediation": self.remediation,
            "status": self.status.value,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "TechnicalDebtItem":
        """Create an item from a dictionary that uses enum values as strings."""

        if not isinstance(data, dict):
            raise TypeError("data must be a dict")

        missing = {field for field in ("key", "title", "description", "severity") if field not in data}
        if missing:
            missing_list = ", ".join(sorted(missing))
            raise KeyError(f"Missing required fields: {missing_list}")

        severity_value = data.get("severity")
        try:
            severity = Severity(severity_value)
        except Exception as exc:  # ValueError or TypeError
            raise ValueError("Invalid severity value") from exc

        status_value = data.get("status", Status.OPEN.value)
        try:
            status = Status(status_value)
        except Exception as exc:  # ValueError or TypeError
            raise ValueError("Invalid status value") from exc

        return cls(
            key=data["key"],
            title=data["title"],
            description=data["description"],
            severity=severity,
            component=data.get("component"),
            remediation=data.get("remediation"),
            status=status,
        )


class TechnicalDebtManager:
    """Manage a collection of :class:`TechnicalDebtItem` entries."""

    def __init__(self, items: Optional[Iterable[TechnicalDebtItem]] = None) -> None:
        self._items: Dict[str, TechnicalDebtItem] = {}
        self._components: Set[str] = set()
        if items:
            for item in items:
                self.add_item(item)

    def add_item(self, item: TechnicalDebtItem) -> None:
        """Add a new item to the backlog.

        Raises:
            ValueError: if an item with the same key already exists.
            TypeError: if the object is not a :class:`TechnicalDebtItem`.
        """

        if not isinstance(item, TechnicalDebtItem):
            raise TypeError("item must be a TechnicalDebtItem instance")
        if item.key in self._items:
            raise ValueError(f"Technical debt item with key '{item.key}' already exists")
        self._items[item.key] = item
        if item.component:
            self._components.add(item.component)

    def remove_item(self, key: str) -> TechnicalDebtItem:
        """Remove an item from the backlog and return it.

        Raises:
            KeyError: if the item does not exist.
        """

        try:
            removed = self._items.pop(key)
        except KeyError as exc:
            raise KeyError(f"Unknown technical debt item key '{key}'") from exc

        if removed.component and removed.component not in (
            item.component for item in self._items.values() if item.component
        ):
            self._components.discard(removed.component)

        return removed

    def get_item(self, key: str) -> Optional[TechnicalDebtItem]:
        """Retrieve a single item by its key."""

        return self._items.get(key)

    def backlog(self, include_resolved: bool = False) -> List[TechnicalDebtItem]:
        """Return backlog items, optionally including resolved work."""

        items = self._items.values()
        if include_resolved:
            return list(items)
        return [item for item in items if item.status is not Status.RESOLVED]

    def prioritized(self, include_resolved: bool = False) -> List[TechnicalDebtItem]:
        """Return backlog ordered from highest to lowest severity."""

        items = self.backlog(include_resolved=include_resolved)
        return sorted(items, key=lambda item: item.severity.rank, reverse=True)

    def by_component(self, component: str, include_resolved: bool = False) -> List[TechnicalDebtItem]:
        """Return items scoped to a component name."""

        if component not in self._components:
            return []

        return [
            item
            for item in self.backlog(include_resolved=include_resolved)
            if item.component == component
        ]

    def by_severity(self, severity: Severity, include_resolved: bool = False) -> List[TechnicalDebtItem]:
        """Return items that match a severity level."""

        if not isinstance(severity, Severity):
            raise TypeError("severity must be a Severity value")

        return [
            item
            for item in self.backlog(include_resolved=include_resolved)
            if item.severity is severity
        ]

    def by_status(self, status: Status) -> List[TechnicalDebtItem]:
        """Return items matching a particular status."""

        if not isinstance(status, Status):
            raise TypeError("status must be a Status value")

        return [item for item in self._items.values() if item.status is status]

    def summary(self) -> Dict[str, int]:
        """Summarize counts by status for quick reporting."""

        counts = {status.value: 0 for status in Status}
        for item in self._items.values():
            counts[item.status.value] += 1
        return counts

    def breakdown_by_severity(self, include_resolved: bool = False) -> Dict[str, int]:
        """Count backlog entries by severity, optionally including resolved work."""

        counts = {level.value: 0 for level in Severity}
        for item in self.backlog(include_resolved=include_resolved):
            counts[item.severity.value] += 1
        return counts

    def update_status(self, key: str, status: Status) -> None:
        """Update the status of an existing item.

        Raises:
            KeyError: if the item does not exist.
        """

        if key not in self._items:
            raise KeyError(f"Unknown technical debt item key '{key}'")
        if not isinstance(status, Status):
            raise TypeError("status must be a Status value")
        self._items[key].status = status

    def update_item(
        self,
        key: str,
        *,
        title: object = _UNSET,
        description: object = _UNSET,
        severity: object = _UNSET,
        component: object = _UNSET,
        remediation: object = _UNSET,
        status: object = _UNSET,
    ) -> TechnicalDebtItem:
        """Update fields of an existing item after validating inputs.

        All provided fields are validated before any mutations are applied so
        callers get atomic updates. Returns the updated item for convenience.

        Raises:
            KeyError: if the item does not exist.
            TypeError/ValueError: if a provided field fails validation.
        """

        if key not in self._items:
            raise KeyError(f"Unknown technical debt item key '{key}'")

        item = self._items[key]

        def _validate_required_string(field_name: str, value: object) -> str:
            if not isinstance(value, str):
                raise TypeError(f"{field_name} must be a string")
            stripped = value.strip()
            if not stripped:
                raise ValueError(f"{field_name} must be a non-empty string")
            return stripped

        def _validate_optional_string(field_name: str, value: object) -> Optional[str]:
            if value is None:
                return None
            if not isinstance(value, str):
                raise TypeError(f"{field_name} must be a string when provided")
            stripped = value.strip()
            if not stripped:
                raise ValueError(f"{field_name} must not be empty when provided")
            return stripped

        validated = {}

        if title is not _UNSET:
            validated["title"] = _validate_required_string("title", title)

        if description is not _UNSET:
            validated["description"] = _validate_required_string("description", description)

        if severity is not _UNSET:
            if not isinstance(severity, Severity):
                raise TypeError("severity must be a Severity value")
            validated["severity"] = severity

        if component is not _UNSET:
            validated["component"] = _validate_optional_string("component", component)

        if remediation is not _UNSET:
            validated["remediation"] = _validate_optional_string("remediation", remediation)

        if status is not _UNSET:
            if not isinstance(status, Status):
                raise TypeError("status must be a Status value")
            validated["status"] = status

        for field_name, value in validated.items():
            if field_name == "component":
                old_component = item.component
                new_component = value
                if old_component != new_component:
                    if old_component and not any(
                        other_item.component == old_component
                        for other_item in self._items.values()
                        if other_item.key != key
                    ):
                        self._components.discard(old_component)
                    if new_component:
                        self._components.add(new_component)
            setattr(item, field_name, value)

        return item

    def extend(self, items: Sequence[TechnicalDebtItem]) -> None:
        """Add multiple items to the backlog."""

        validated_items: List[TechnicalDebtItem] = []
        for item in items:
            if not isinstance(item, TechnicalDebtItem):
                raise TypeError("all items must be TechnicalDebtItem instances")
            validated_items.append(item)

        keys = [item.key for item in validated_items]
        self._validate_new_keys(keys)

        for item in validated_items:
            self.add_item(item)

    def export(self, include_resolved: bool = False) -> List[Dict[str, object]]:
        """Return a serialized view of the backlog for persistence or reporting."""

        return [item.to_dict() for item in self.backlog(include_resolved=include_resolved)]

    def ingest(self, serialized_items: Sequence[Dict[str, object]]) -> None:
        """Load serialized items, validating before mutating the backlog."""

        validated_items: List[TechnicalDebtItem] = []
        for raw in serialized_items:
            if not isinstance(raw, dict):
                raise TypeError("serialized items must be dictionaries")
            validated_items.append(TechnicalDebtItem.from_dict(raw))

        keys = [item.key for item in validated_items]
        self._validate_new_keys(keys)

        for item in validated_items:
            self.add_item(item)

    def components(self, include_resolved: bool = True) -> Set[str]:
        """Return a set of components currently represented in the manager."""

        if include_resolved:
            return set(self._components)

        return {item.component for item in self.backlog(include_resolved=False) if item.component}

    def _validate_new_keys(self, keys: Sequence[str]) -> None:
        """Ensure new keys are unique and not already present."""

        seen: set[str] = set()
        duplicate_keys: set[str] = set()
        for key in keys:
            if key in seen:
                duplicate_keys.add(key)
            else:
                seen.add(key)

        if duplicate_keys:
            duplicate_list = ", ".join(sorted(duplicate_keys))
            raise ValueError(f"Duplicate keys in provided items: {duplicate_list}")

        existing_conflicts = [key for key in keys if key in self._items]
        if existing_conflicts:
            conflict_list = ", ".join(sorted(existing_conflicts))
            raise ValueError(f"Items already exist for keys: {conflict_list}")

    def __contains__(self, key: object) -> bool:
        return key in self._items

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        """Iterate over all tracked items, including resolved entries."""

        return iter(self._items.values())
