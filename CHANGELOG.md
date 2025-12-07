# Changelog

All notable changes to the Nova System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.2.1] - 2025-12-06

### Security
- **Race Condition Fix:** Atomic write + merge strategy for `TrafficController`
  - Write to temp file, then `os.replace()` (prevents corruption on crash)
  - Merge existing disk state with in-memory state (prevents data loss)
- **Budget Circuit Breaker:** New `BudgetExceededError` exception
  - `check_budget()` method validates spend before API calls
  - Default limits: $2/hour, $10/day (configurable per instance)
  - `budget_status()` returns current spend vs limits

### Added
- **Security Probe:** `security_probe.py` vulnerability scanner
  - Tests corruption resilience, race conditions, SQL injection, PII leakage
- **API Miner:** `mine_apis.py` stress test tool
  - Embedded 35 API catalog across 5 categories
  - Tests Traffic Control, Budget, and Ledger under load
  - Supports `--dry-run`, `--provider`, `--categories` flags

### Fixed
- `UsageLedger.summary()` key access in CLI report

## [v0.2.0] - 2025-12-06

### Added
- **Financial Ledger:** SQLite-backed tracking of all LLM transactions (`usage.py`)
  - Records estimated vs actual costs for drift analysis
  - Breakdowns by model and provider
  - Queryable transaction history
- **Traffic Control:** Persistent rate limiting to prevent 429 errors (`traffic.py`)
  - Sliding window RPM/TPM tracking
  - JSON persistence survives restarts
  - Per-model limit configuration
- **CLI Dashboard:** New `report` command to view spend and drift analytics
  - `nova report` shows totals, top model, drift %, recent transactions
  - Supports `--db` for custom database and `--limit` for row count
- **Cost Estimation:** Pre-flight checks (`pricing.py`) before execution
  - Gemini model pricing tiers
  - Token estimation heuristic (4 chars ≈ 1 token)
- **Memory Stub:** Abstract `VectorStore` interface for future RAG support

### Changed
- Refactored `llm.py` to integrate usage tracking automatically
- All LLM providers now record transactions after API calls
- Claude/OpenAI providers extract actual token counts from responses

### Fixed
- Rate limit state no longer lost on server restart
- Cost tracking now uses actual tokens when available (not just estimates)

## [v0.1.0] - 2025-12-06

### Added
- Initial Nova MVP release
- Multi-agent problem solving (DCE, CAE, Domain Experts)
- CLI interface with interactive mode
- FastAPI backend with WebSocket support
- Svelte web frontend
- Support for Claude, OpenAI, and Mock providers
