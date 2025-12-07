# CLAUDE.md - AI Assistant Guide for NovaSystem

**Last Updated:** 2025-12-07
**Version:** 3.0.0

This document provides comprehensive guidance for AI assistants (like Claude, ChatGPT, etc.) working with the NovaSystem codebase. It explains the project structure, development workflows, coding conventions, and key architectural patterns.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Critical Context](#critical-context)
3. [Repository Structure](#repository-structure)
4. [Core Components](#core-components)
5. [Development Workflow](#development-workflow)
6. [Code Conventions](#code-conventions)
7. [Testing Strategy](#testing-strategy)
8. [Git Workflow](#git-workflow)
9. [Key Architectural Patterns](#key-architectural-patterns)
10. [Dependencies & Setup](#dependencies--setup)
11. [Common Tasks](#common-tasks)
12. [Troubleshooting](#troubleshooting)

---

## Project Overview

**NovaSystem** is a pioneering problem-solving framework that harnesses multiple AI models working together through the "Nova Process." It is NOT artificial general intelligence (AGI) - it's a methodology for augmenting existing frontier language models to organize their output in more useful ways.

### Key Characteristics

- **Status:** ALPHA development stage - experimental research tool
- **License:** GPL-3.0
- **Language:** Python 3.8+
- **Architecture:** CLI-first multi-agent orchestration with parallel processing
- **Latest Version:** v3.0.0 (as of Dec 2025)

### The Nova Process

The Nova Process is a three-phase problem-solving workflow:

1. **UNPACK** - Discussion Continuity Expert (DCE) breaks down the problem
2. **ANALYZE** - Domain experts and Critical Analysis Expert (CAE) analyze in parallel
3. **SYNTHESIZE** - DCE combines all perspectives into a coherent solution

Agents run in parallel where possible using `asyncio.gather()`.

---

## Critical Context

### What AI Assistants MUST Know

1. **Not Production-Ready:** This is an experimental research tool. Never suggest deploying to production.

2. **Development Branch Strategy:**
   - Always develop on branches starting with `claude/`
   - Branch names must match the session ID pattern
   - Never push to main/master without explicit permission

3. **v3.0.0 Consolidation:** As of Dec 2025, the repository was consolidated from 4 separate implementations into one unified package. All code lives in `novasystem/`.

4. **Active Areas:**
   - `novasystem/` - **THE** unified package (CLI-first)
   - `docs/` - Comprehensive documentation
   - `tests/` - Pytest-based test suite

5. **Archived Areas (READ-ONLY):**
   - `archive/` - Contains all previous implementations for reference only
   - See `archive/README.md` for details

---

## Repository Structure

```
NovaSystem-Codex/
├── novasystem/                  # UNIFIED PACKAGE (v3.0.0)
│   ├── __init__.py              # Package entry, lazy loading
│   ├── __main__.py              # python -m novasystem support
│   │
│   ├── cli/                     # CLI Interface (PRIMARY)
│   │   ├── main.py              # Main CLI entry point
│   │   └── session_cli.py       # Session management CLI
│   │
│   ├── core/                    # Core Systems
│   │   ├── agents.py            # DCE, CAE, DomainExpert
│   │   ├── process.py           # NovaProcess orchestrator
│   │   ├── memory.py            # MemoryManager (short/long term)
│   │   ├── vector_store.py      # LocalVectorStore (RAG)
│   │   ├── workflow.py          # Workflow engine
│   │   ├── pricing.py           # Cost estimation
│   │   └── usage.py             # Usage tracking ledger
│   │
│   ├── tools/                   # Utility Tools (from v0.1.1)
│   │   ├── docker.py            # Docker executor
│   │   ├── repository.py        # Git repository manager
│   │   ├── parser.py            # Documentation parser
│   │   ├── technical_debt.py    # Debt tracking
│   │   └── decision_matrix/     # Decision Matrix framework
│   │       ├── decision_matrix.py
│   │       └── decision_matrix_cli.py
│   │
│   ├── api/                     # REST API
│   │   └── rest.py              # FastAPI endpoints
│   │
│   ├── ui/                      # User Interfaces
│   │   ├── web.py               # Flask web interface
│   │   └── gradio.py            # Gradio interface
│   │
│   ├── utils/                   # Utilities
│   │   ├── llm_service.py       # LLM provider abstraction
│   │   ├── rate_limiter.py      # Rate limiting
│   │   ├── vision_service.py    # Vision/image analysis
│   │   ├── document_service.py  # Document processing
│   │   └── image_service.py     # Image generation
│   │
│   ├── config/                  # Configuration
│   │   ├── settings.py          # App settings
│   │   └── models.py            # Model configurations
│   │
│   ├── database/                # Database Layer
│   │   └── models.py            # SQLAlchemy models
│   │
│   ├── session/                 # Session Management
│   │   └── manager.py           # Session persistence
│   │
│   └── mcp/                     # Model Context Protocol
│       └── server.py            # MCP server implementation
│
├── archive/                     # Archived implementations (READ-ONLY)
│   ├── README.md                # Archive documentation
│   ├── NovaSystem-Streamlined/  # Original v2.0
│   ├── novasystem-v0.1.1-cli/   # Original CLI tool
│   ├── nova-mvp/                # Original FastAPI MVP
│   └── dev-experimental/        # NS-bytesize, NS-core, etc.
│
├── docs/                        # Documentation
│   ├── decision_matrix/         # Decision Matrix docs
│   ├── architecture/            # Architecture docs
│   ├── guides/                  # User guides
│   └── implementation/          # Implementation notes
│
├── tests/                       # Test suite (pytest)
├── examples/                    # Example scripts
├── scripts/                     # Utility scripts
├── utils/                       # Dev utilities
│
├── pyproject.toml               # Project configuration
├── README.md                    # User documentation
├── CHANGELOG.md                 # Version history
├── CLAUDE.md                    # This file
└── .gitignore                   # Git ignore patterns
```

---

## Core Components

### 1. CLI Interface (`novasystem/cli/`)

The primary interface for NovaSystem. CLI-first design.

```bash
# Entry points (both work)
novasystem --help
nova --help

# Common commands
nova solve "How can I improve API performance?"
nova remember "Important fact" --tags project,api
nova recall "performance tips"
nova report
```

### 2. Agent System (`novasystem/core/agents.py`)

- **DCEAgent**: Discussion Continuity Expert
  - Handles UNPACK phase (problem breakdown)
  - Handles SYNTHESIZE phase (combining perspectives)

- **CAEAgent**: Critical Analysis Expert
  - Provides critical evaluation
  - Identifies edge cases and risks

- **DomainExpert**: Specialized domain experts
  - Dynamically generated based on problem domain
  - Created via factory pattern

### 3. Process Orchestrator (`novasystem/core/process.py`)

- **NovaProcess**: Main orchestrator
  - Manages three-phase workflow (UNPACK → ANALYZE → SYNTHESIZE)
  - Parallel execution using `asyncio.gather()`
  - Session state tracking via `SessionState` dataclass
  - Streaming support via `solve_streaming()` generator

### 4. Memory Systems (`novasystem/core/`)

- **MemoryManager** (`memory.py`): Short/long-term memory with deque storage
- **LocalVectorStore** (`vector_store.py`): Zero-cost RAG with hash embeddings
  - JSON-backed vector storage
  - Cosine similarity search
  - Tag filtering

### 5. Tools Module (`novasystem/tools/`)

Utility tools merged from the original CLI package:

- **DecisionMatrix**: Multi-criteria decision analysis
- **DockerExecutor**: Run commands in Docker containers
- **RepositoryManager**: Clone and manage Git repos
- **DocParser**: Extract commands from documentation

### 6. Services (`novasystem/utils/`)

- **LLM Service**: Multi-provider abstraction (Claude, OpenAI, Gemini, Ollama)
- **Vision Service**: Image analysis and understanding
- **Document Service**: Document processing and extraction
- **Image Service**: Image generation

---

## Development Workflow

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/ctavolazzi/NovaSystem.git
cd NovaSystem-Codex

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

### Environment Variables

Create a `.env` file in the project root:

```bash
# LLM API Keys
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here  # For Gemini

# Optional
DEFAULT_MODEL=claude-3-5-sonnet-20241022
DEFAULT_TEMPERATURE=0.7
```

**IMPORTANT:** Never commit `.env` files or API keys to the repository.

### Running NovaSystem

```bash
# CLI (primary interface)
novasystem --help
nova solve "Your problem here"

# API server
novasystem-web

# Gradio interface
novasystem-gradio
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=novasystem

# Run specific test file
pytest tests/test_core_functions.py

# Run with verbose output
pytest -v
```

---

## Code Conventions

### Python Style Guide

1. **PEP 8 Compliance:** Follow PEP 8 style guide
2. **Type Hints:** Use type hints for function parameters and return values
3. **Docstrings:** Use Google-style docstrings for classes and functions
4. **Async/Await:** Use async/await for I/O operations (especially LLM calls)

### Example Code Style

```python
"""Module docstring explaining purpose."""

from typing import Any, Dict, List, Optional
import asyncio

from novasystem.core.agents import BaseAgent, AgentResponse


class ExampleAgent(BaseAgent):
    """
    Brief description of the class.

    Longer description with usage example if needed.
    """

    def __init__(self, name: str, llm_provider: Optional[LLMProvider] = None):
        """
        Initialize the agent.

        Args:
            name: The agent's display name
            llm_provider: Optional LLM provider (defaults to auto-detect)
        """
        super().__init__(name, "example", llm_provider)

    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Process input and return a response.

        Args:
            input_data: Dictionary containing 'problem' and optional context

        Returns:
            AgentResponse with the agent's analysis
        """
        problem = input_data.get("problem", "")
        result = await self._call_llm(f"Analyze: {problem}")

        return self._create_response(
            content=result,
            success=True
        )
```

---

## Testing Strategy

### Test Structure

```
tests/
├── test_core_functions.py      # Core utility tests
├── test_decision_matrix.py     # Decision matrix tests
├── test_parser.py              # Parser tests
└── test_*.py                   # Other test modules
```

### Writing Tests

```python
import pytest
from novasystem.tools.decision_matrix import DecisionMatrix


class TestDecisionMatrix:
    """Test suite for DecisionMatrix class."""

    def test_initialization(self):
        """Test DecisionMatrix can be initialized."""
        dm = DecisionMatrix()
        assert dm is not None

    @pytest.mark.asyncio
    async def test_async_operation(self):
        """Test async operations work correctly."""
        result = await some_async_function()
        assert result.success is True
```

### Coverage Goals

- Aim for **>80% coverage** on core modules
- Focus on **critical paths** and **edge cases**

---

## Git Workflow

### Branch Naming Convention

```bash
# Format: claude/<descriptive-name>-<session-id>
claude/add-memory-system-01CRKFhZZr365i9jGn6B53tk
claude/fix-rate-limiting-xyz123abc456
```

### Commit Messages

Follow conventional commit format:

```bash
feat(memory): Add long-term memory system with RAG
fix(traffic): Fix race condition in rate limiter
docs(readme): Update installation instructions
refactor(agents): Improve BaseAgent error handling
test(core): Add tests for NovaProcess
chore(deps): Update dependencies
```

### NEVER

- Push to `main` or `master` directly
- Force push without explicit permission
- Skip tests before committing
- Commit API keys, secrets, or `.env` files

---

## Key Architectural Patterns

### 1. Lazy Loading

Components are lazy-loaded to prevent import-time overhead:

```python
# In novasystem/__init__.py
def __getattr__(name):
    if name == "NovaProcess":
        from .core.process import NovaProcess
        return NovaProcess
    # ...
```

### 2. Factory Pattern

Used for creating agents and LLM providers:

```python
from novasystem import DCEAgent, CAEAgent
from novasystem.utils.llm_service import get_llm

llm = get_llm("claude")  # or "openai", "gemini", "ollama"
```

### 3. Async/Await Pattern

Parallel agent execution:

```python
analysis_tasks = [
    self.cae.process(input),
    *[expert.process(input) for expert in domain_experts]
]
responses = await asyncio.gather(*analysis_tasks)
```

---

## Dependencies & Setup

### Core Dependencies

From `pyproject.toml`:
- **pydantic**: Data validation
- **anthropic, openai, ollama**: LLM providers
- **rich, typer**: CLI interface
- **fastapi, uvicorn**: API server
- **gradio, flask**: UI options
- **sqlalchemy**: Database ORM
- **docker, gitpython**: Tools integration

### Installation

```bash
# Standard install
pip install -e .

# With dev dependencies
pip install -e ".[dev]"
```

---

## Common Tasks

### Adding a New Agent

1. Create agent class in `novasystem/core/agents.py` or new file
2. Inherit from `BaseAgent`
3. Implement `process()` method
4. Add tests in `tests/`

### Adding a CLI Command

1. Edit `novasystem/cli/main.py`
2. Add command using the CLI framework
3. Add help text

### Using Tools

```python
from novasystem.tools import DecisionMatrix, DockerExecutor

# Decision Matrix
dm = DecisionMatrix()
result = dm.compare_methods(["Option A", "Option B"], criteria)

# Docker
executor = DockerExecutor()
output = executor.run_command("pip install package")
```

---

## Troubleshooting

### Import Errors

```bash
# Reinstall in development mode
pip install -e .
```

### Test Discovery Issues

```bash
pytest --collect-only -v
```

### Memory Issues

- Check `.nova_memory.json` exists and is writable
- Use `nova memory stats` to verify

---

## Quick Reference

### Key Files

| File | Purpose |
|------|---------|
| `novasystem/core/process.py` | NovaProcess orchestrator |
| `novasystem/core/agents.py` | Agent implementations |
| `novasystem/cli/main.py` | CLI entry point |
| `novasystem/tools/` | Utility tools |
| `pyproject.toml` | Project configuration |

### Key Commands

```bash
# CLI
nova solve "problem"
nova remember "fact" --tags tag1,tag2
nova recall "query"
nova report

# Development
pytest
pip install -e ".[dev]"
```

---

## For AI Assistants: Best Practices

When working with this codebase:

1. **Always read files before editing**
2. **Follow existing patterns**
3. **Write tests for new code**
4. **Update documentation**
5. **Use type hints**
6. **Async for I/O**
7. **Never commit secrets**
8. **Test before pushing**

---

## Version History

| Version | Date | Key Changes |
|---------|------|-------------|
| 3.0.0 | 2025-12-07 | Major consolidation: merged 4 implementations |
| 0.3.0 | 2025-12-06 | Long-term memory system with RAG |
| 0.2.0 | 2025-12-06 | Financial ledger, traffic control |
| 0.1.0 | 2025-12-06 | Initial MVP release |

---

**End of CLAUDE.md**

*This document should be updated whenever significant architectural changes occur.*
