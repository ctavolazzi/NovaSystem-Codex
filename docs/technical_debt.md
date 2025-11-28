# Technical Debt Backlog (Current State)

This document tracks the most visible technical debt in the NovaSystem codebase so we can prioritize remediation work. Each item includes the observed issue, associated risk, and suggested next steps.

## Backlog helper

A small `TechnicalDebtManager` utility (see `novasystem/technical_debt.py`) keeps an in-memory backlog of items so new work can be sorted, filtered, and summarized in tests or lightweight scripts. Items validate keys, titles, descriptions, remediation, and enum values at creation time, support safe removal, and expose helpers to list unresolved work by component or severity. Bulk `extend` operations fail fast when duplicates are provided to avoid partial updates. Items can also be updated in-place with validation, serialized to dictionaries for reporting or persistence, and listings can be filtered by status or narrowed to a specific severity for lightweight reporting. Backlog severity breakdowns are available for quick dashboards, and exports respect whether resolved work should be included. Exported dictionaries can be ingested into a new manager with validation so serialized backlogs round-trip without partial writes.

The manager is iterable, so callers can loop directly over all tracked entries (including resolved items) when they need raw access to the backlog without filtering.

Components are indexed in a set for quick discovery and filtering. Use `components()` to retrieve the current component names (optionally excluding resolved items) and `by_component()` for scoped backlog queries.

## High Priority

- **CLI configures logging on import with hard-coded handlers.** `novasystem/cli.py` calls `logging.basicConfig` at module import time and attaches a file handler that writes to `~/.novasystem.log` without checking for path availability or caller preferences. This side effect can break library consumers (e.g., when imported in other applications) and will fail in read-only environments. **Recommendation:** move logging configuration behind a callable that can receive a log path/level, guard file handler creation with directory creation and error handling, and avoid configuring global logging during import. 

## Medium Priority

- **Runtime dependencies are unpinned and include test tooling.** `pyproject.toml` lists broad dependency ranges (e.g., `gitpython`, `docker`) and also pulls `pytest` into the runtime dependency set. This increases the risk of environment drift and bloats installations for end users. **Recommendation:** introduce constrained version ranges, separate dev/test dependencies into an extra or requirements-dev file, and generate a lock file (e.g., via `pip-tools` or Poetry) for reproducible installs.

- **SQLite database path and lifecycle are implicit.** `DatabaseManager` defaults to creating `novasystem.db` in the current working directory and opens the connection eagerly during initialization. Callers receive no hook to close the connection when used as a short-lived helper, which can lead to file descriptor leaks or locked files in long-running sessions. **Recommendation:** allow callers to opt into context management (`__enter__/__exit__`), support configurable data directories, and document when `close()` should be invoked.
