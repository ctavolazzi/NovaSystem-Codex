# Changelog

All notable changes to NovaSystem-Codex will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.2] - 2025-11-28

### Added
- **Decision Matrix Utility** - Comprehensive decision-making tool with 4 analysis methods
  - Weighted, Normalized, Ranking, and Best-Worst scoring
  - Confidence scoring (0-100%)
  - Strengths and weaknesses identification per option
  - "Why winner won" explanations
  - Comparison tables for side-by-side analysis
  - Statistical tie warnings for close scores
- **Decision Matrix CLI** - Full command-line interface
  - JSON input/output support
  - Stdin auto-detection (no `-` required)
  - Method comparison mode with consensus detection
  - Example file generator
- **Environment Variables for CLI Logging**
  - `NOVASYSTEM_DISABLE_FILE_LOG` - Disable file logging
  - `NOVASYSTEM_LOG_PATH` - Custom log file location
- **Technical Debt Manager** - Component tracking system

### Fixed
- CLI logging now gracefully falls back to console-only when file logging fails
- Test subprocess calls use `sys.executable` instead of assuming `python` on PATH
- Missing `lib/utils.ts` in modern UI causing build errors

### Changed
- Decision matrix JSON output now rounds numeric values to 2 decimal places
- Strengths/weaknesses hidden when ≤3 criteria to avoid overlap

### Tests
- 70/70 tests passing (100%)
- 29 dedicated decision matrix tests
- All system validation tests now pass cross-platform

---

## [0.1.1] - 2025-09-28

### Added
- Automated repository installation tool
- Docker container execution for isolated command running
- Documentation parsing for installation command extraction
- Command sequencing based on dependencies
- Persistent storage of run data
- Basic CLI interface

### Features
- Automatic repository cloning and analysis
- Command execution in isolated Docker containers
- Command-line interface for easy interaction

---

## [0.1.0] - 2025-09-26

### Added
- Initial NovaSystem implementation
- Nova Process framework for multi-agent problem solving
- DCE (Discussion Continuity Expert) agent
- CAE (Critical Analysis Expert) agent
- Domain Expert agents
- Memory management system
- LLM service with multi-provider support (OpenAI, Anthropic, Ollama)
- CLI, Web, and Gradio interfaces
- Session management
- WebSocket support for real-time updates

---

[0.1.2]: https://github.com/ctavolazzi/NovaSystem-Codex/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/ctavolazzi/NovaSystem-Codex/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/ctavolazzi/NovaSystem-Codex/releases/tag/v0.1.0

