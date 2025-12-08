# Changelog

All notable changes to the Nova System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.3.4] - 2025-12-07

### "Clean Sleepy Wizard" - Complete Consolidation Release

#### Major Changes
- **Unified Package Structure**: All functionality consolidated into single `novasystem/` package
- **Removed Duplicate Implementations**: Archived `nova-mvp/`, `NovaSystem-Streamlined/`, and `dev/` to `archive/`
- **Single Source of Truth**: One CLI, one package, one version

#### Added
- **ASCII Animation System** (`novasystem/core/ascii_animation.py`):
  - `play_sleeping_wizard()` - Display animated sleeping wizard
  - `image_to_ascii()` - Convert images to colorized ASCII art
  - `generate_breathing_frames()` - Create subtle motion frames
  - `ASCIIAnimationPlayer` - Terminal animation player with keypress detection
  - `TypewriterMessageBox` - 40 funny loading messages with typewriter effect

- **PixelLab API Integration** (`novasystem/core/pixellab.py`):
  - `generate_wizard_animation()` - Generate pixel art wizard images via API

- **CLI Commands** (added to `novasystem/cli/main.py`):
  - `novasystem sleep` - Display sleeping wizard ASCII animation
    - `--image/-i` - Custom image path
    - `--width/-w` - ASCII width (default: 50)
    - `--fps/-f` - Animation speed (default: 1.5)
    - `--message/-m` - Custom message
  - `novasystem wizard generate` - Generate wizard images via PixelLab API
    - `--prompt/-p` - Custom generation prompt
    - `--frames/-n` - Number of frames
    - `--output/-o` - Output directory
  - `novasystem wizard list` - List available wizard images

#### Changed
- **Package Structure**: Everything now in `novasystem/` - no more `nova-mvp/` or separate implementations
- **CLI**: Unified Typer-based CLI with all features (ask, chat, solve, experts, sleep, wizard, etc.)
- **Imports**: Updated all imports to use `novasystem.core` namespace
- **Image Search**: Improved wizard image auto-detection with multiple search paths

#### Archived
- `archive/nova-mvp-root-YYYYMMDD/` - Original nova-mvp implementation
- `archive/NovaSystem-Streamlined-root-YYYYMMDD/` - Original streamlined implementation
- `archive/dev-root-YYYYMMDD/` - Experimental dev code

#### Migration Notes
If you were using `nova-mvp/cli/nova.py`:
```bash
# Old
python nova-mvp/cli/nova.py sleep

# New
novasystem sleep
```

All functionality is now available through the unified `novasystem` CLI.

---

## [v0.3.3] - 2025-12-07

### ASCII Animation & CLI Enhancement Release

#### Added
- **ASCII Animation System** (`nova-mvp/backend/core/ascii_animation.py`):
  - `image_to_ascii()` - Convert images to colorized ASCII art with ANSI colors
  - `generate_breathing_frames()` - Generate subtle motion frames for animation
  - `ASCIIAnimationPlayer` - Terminal animation player with non-blocking keypress detection
  - `TypewriterMessageBox` - Animated message box with typewriter + backspace effect
  - `play_sleeping_wizard()` - One-liner to run the sleeping wizard animation
  - 40 funny loading messages ("Reticulating splines...", "Consulting the ancient tomes...", etc.)

- **PixelLab API Integration** (`nova-mvp/backend/core/pixellab.py`):
  - `generate_wizard_animation()` - Generate pixel art wizard images via PixelLab API
  - Async HTTP client with proper error handling
  - Frame output to configurable directory

- **CLI Commands**:
  - `nova sleep` - Display sleeping wizard ASCII animation
    - `--image/-i` - Custom image path
    - `--width/-w` - ASCII width (default: 50)
    - `--fps/-f` - Animation speed (default: 1.5)
    - `--message/-m` - Custom message
  - `nova wizard list` - List available wizard images in repo
  - `nova wizard generate` - Generate new wizard images via PixelLab API
    - `--prompt/-p` - Custom generation prompt
    - `--frames/-n` - Number of frames
    - `--output/-o` - Output directory

#### Changed
- Moved `nova-mvp/` from `archive/` to repository root as canonical location
- Added `pillow>=10.0.0` dependency for image processing
- Added `nova-mvp/backend/venv/` to `.gitignore`

#### Fixed
- Non-interactive terminal fallback for `ASCIIAnimationPlayer` (graceful degradation when `termios` unavailable)
- Robust wizard image auto-detection with multiple search paths

---

## [v0.3.0] - 2025-12-07

### Major Consolidation Release

This release consolidates **4 separate implementations** into a single, unified CLI-first package.

### Merged From
- **NovaSystem-Streamlined (v2.0)** - Multi-agent framework with full UI support
- **novasystem CLI (v0.1.1)** - Repository tools, Docker executor, Decision Matrix
- **nova-mvp** - LocalVectorStore, pricing/usage tracking, clean agent patterns
- **dev/* experimental** - Best patterns extracted, rest archived

### Added
- **Unified Package Structure:**
  ```
  novasystem/
  ├── cli/          # CLI commands (primary interface)
  ├── core/         # Agents, process, memory, workflow
  ├── tools/        # Decision Matrix, Docker, repo installer
  ├── utils/        # Vision, docs, image generation services
  ├── api/          # REST API endpoints
  └── ui/           # Web and Gradio interfaces
  ```
- **Tools Module** (`novasystem.tools`):
  - `DecisionMatrix` - Multi-criteria decision analysis
  - `DockerExecutor` - Containerized command execution
  - `RepositoryHandler` - Git repository operations
  - `DocumentationParser` - Documentation extraction
  - `TechnicalDebtManager` - Debt tracking
  - `Nova` - Main orchestrator class
- **Vector Store** (`core/vector_store.py`) - Zero-cost local RAG from nova-mvp
- **Pricing/Usage** (`core/pricing.py`, `core/usage.py`) - Cost tracking from nova-mvp
- **Backwards Compatibility Shims** - Old import paths still work:
  - `novasystem.core_utils` → `novasystem.tools.decision_matrix`
  - `novasystem.parser` → `novasystem.tools.parser`
  - `novasystem.docker` → `novasystem.tools.docker`
  - `novasystem.repository` → `novasystem.tools.repository`
  - `novasystem.nova` → `novasystem.tools.nova`
- **Dual CLI Entry Points:** `novasystem` and `nova` commands

### Changed
- Version: 0.1.1 → 0.3.0 (consolidation release)
- All old implementations moved to `archive/` directory
- Root-level documentation cleaned up (DECISION_MATRIX_*.md → docs/)
- Updated pyproject.toml with comprehensive dependencies

### Archived
- `archive/NovaSystem-Streamlined/` - Original v2.0 source
- `archive/novasystem-v0.1.1-cli/` - Original CLI tool
- `archive/nova-mvp/` - Original FastAPI MVP
- `archive/dev-experimental/` - NS-bytesize, NS-core, NS-lite, mcp-claude, saas
- `archive/streamlined-backup-20250928/` - Historical backup

### Removed
- Duplicate implementations and conflicting package names
- Scattered root-level test files (moved to tests/)
- Orphaned files (package-lock.json, .git-rewrite/)

### Migration Notes
If upgrading from v0.1.1 (CLI tool) or v2.0 (Streamlined):
```bash
pip install -e .  # Reinstall to get new package structure
novasystem --help  # or: nova --help
```

---

## Pre-Consolidation History (from nova-mvp)

The following versions were from the nova-mvp implementation before consolidation.

## [nova-mvp v0.3.0] - 2025-12-06

### Added
- **Long-Term Memory:** Full RAG pipeline with zero-cost local embeddings (`memory.py`)
  - `LocalVectorStore`: JSON-backed vector storage with atomic writes
  - `SimpleEmbedder`: Hash-based 256-dim embeddings (no API calls)
  - Cosine similarity search with configurable thresholds
  - Tag-based filtering for organized retrieval
- **CLI Memory Commands:**
  - `nova remember "text" --tags tag1,tag2` — Store memories with metadata
  - `nova recall "query" --limit 5` — Semantic search
  - `nova memory list` — View all stored memories
  - `nova memory stats` — Usage statistics and tag breakdown
  - `nova memory clear` — Clear with confirmation

### Changed
- Updated `backend/core/__init__.py` to export memory components
- README updated with memory usage examples and architecture docs

### Technical Notes
- Memory persists to `.nova_memory.json` (gitignored)
- Embedder interface allows swapping to GeminiEmbedder later
- Zero external dependencies for basic RAG functionality

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
