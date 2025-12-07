# CLAUDE.md - AI Assistant Guide for NovaSystem

**Last Updated:** 2025-12-07
**Version:** 0.3.0

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
- **Architecture:** Multi-agent orchestration with parallel processing
- **Latest Version:** v0.3.0 (as of Dec 2025)

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

3. **Current Active Areas:**
   - `nova-mvp/` - Current MVP implementation with FastAPI backend
   - `novasystem/` - CLI tool and core utilities package
   - `docs/` - Comprehensive documentation
   - `tests/` - Pytest-based test suite

4. **Archived/Backup Areas (READ-ONLY):**
   - `NovaSystem-Streamlined-backup-20250928-185544/` - Historical backup
   - `NovaSystem-Streamlined/` - Alternative implementation
   - `dev/` - Experimental implementations (NS-bytesize, NS-core, NS-lite, mcp-claude)

---

## Repository Structure

```
NovaSystem-Codex/
├── nova-mvp/                    # PRIMARY: Current MVP implementation
│   ├── backend/                 # FastAPI backend
│   │   ├── agents/              # Agent implementations (DCE, CAE, Domain Experts)
│   │   │   ├── base.py          # BaseAgent abstract class
│   │   │   ├── dce.py           # Discussion Continuity Expert
│   │   │   ├── cae.py           # Critical Analysis Expert
│   │   │   └── domain.py        # Domain Expert factory
│   │   ├── api/                 # REST API and WebSocket routes
│   │   ├── core/                # Core systems
│   │   │   ├── process.py       # NovaProcess orchestrator
│   │   │   ├── llm.py           # LLM provider abstraction
│   │   │   ├── memory.py        # Long-term memory (RAG)
│   │   │   ├── traffic.py       # Rate limiting
│   │   │   ├── usage.py         # Cost tracking ledger
│   │   │   └── pricing.py       # Cost estimation
│   │   └── main.py              # FastAPI app entry point
│   ├── cli/                     # CLI interface
│   │   └── nova.py              # Command-line tool
│   └── web/                     # Frontend (future Svelte implementation)
│
├── novasystem/                  # CLI tool package
│   ├── cli.py                   # Main CLI entry point
│   ├── core_utils/              # Decision matrix and utilities
│   │   ├── decision_matrix.py   # Decision-making framework
│   │   └── decision_matrix_cli.py
│   ├── parser.py                # Documentation parser
│   ├── docker.py                # Docker integration
│   ├── repository.py            # Repository handling
│   └── database.py              # SQLite database
│
├── tests/                       # Test suite (pytest)
│   ├── test_core_*.py           # Core functionality tests
│   ├── test_decision_matrix.py  # Decision matrix tests
│   └── test_*.py                # Various test modules
│
├── docs/                        # Documentation
│   ├── implementation/          # Implementation guides
│   │   └── CODEBASE_CONTEXT.md  # Historical codebase context
│   ├── architecture/            # Architecture documentation
│   ├── guides/                  # User guides
│   └── testing_guide.md         # Testing best practices
│
├── examples/                    # Example scripts and usage
├── scripts/                     # Utility scripts
├── utils/                       # Utility tools
│   ├── dev_tools/               # Development utilities
│   └── maintenance/             # Maintenance scripts
│
├── dev/                         # Experimental implementations (READ-ONLY)
│   ├── NS-bytesize/             # Lightweight FastAPI implementation
│   ├── NS-core/                 # Async FastAPI with SQLAlchemy
│   ├── NS-lite/                 # Simplified implementations
│   └── mcp-claude/              # Model Context Protocol integration
│
├── pyproject.toml               # Project configuration
├── README.md                    # User-facing documentation
├── CHANGELOG.md                 # Version history
└── .gitignore                   # Git ignore patterns
```

---

## Core Components

### 1. Nova MVP Backend (`nova-mvp/backend/`)

The current implementation of the Nova Process.

#### Agent System (`agents/`)

- **BaseAgent** (`base.py`): Abstract base class for all agents
  - Defines `system_prompt` property (abstract)
  - Defines `process(input_data)` method (abstract)
  - Provides `_call_llm()` helper for LLM interaction
  - Returns structured `AgentResponse` objects

- **DCEAgent** (`dce.py`): Discussion Continuity Expert
  - Handles UNPACK phase (problem breakdown)
  - Handles SYNTHESIZE phase (combining perspectives)

- **CAEAgent** (`cae.py`): Critical Analysis Expert
  - Provides critical evaluation
  - Identifies edge cases and risks

- **DomainExpert** (`domain.py`): Specialized domain experts
  - Created via `create_domain_expert(domain, llm_provider)`
  - Dynamically generated system prompts based on domain

#### Core Systems (`core/`)

- **NovaProcess** (`process.py`): Main orchestrator
  - Manages three-phase workflow (UNPACK → ANALYZE → SYNTHESIZE)
  - Parallel execution using `asyncio.gather()`
  - Session state tracking via `SessionState` dataclass
  - Streaming support via `solve_streaming()` generator
  - Phase change callbacks for real-time updates

- **LLM Providers** (`llm.py`): Multi-provider abstraction
  - `LLMProvider` abstract base class
  - `ClaudeProvider`, `OpenAIProvider`, `MockProvider`
  - `get_llm(provider_name)` factory function
  - Automatic usage tracking integration

- **Long-Term Memory** (`memory.py`): RAG implementation
  - `LocalVectorStore`: JSON-backed vector storage
  - `SimpleEmbedder`: Hash-based embeddings (no API costs)
  - Cosine similarity search with tag filtering
  - Thread-safe operations with atomic writes
  - CLI commands: `nova remember`, `nova recall`, `nova memory list/stats/clear`

- **Traffic Control** (`traffic.py`): Rate limiting
  - Persistent sliding window RPM/TPM tracking
  - JSON state survives restarts
  - Per-model limit configuration

- **Usage Tracking** (`usage.py`): Cost tracking
  - SQLite-backed transaction ledger
  - Estimated vs actual cost tracking
  - Model and provider breakdowns
  - CLI command: `nova report`

- **Pricing** (`pricing.py`): Cost estimation
  - Pre-flight cost checks
  - Model-specific pricing tiers
  - Token estimation (4 chars ≈ 1 token)

### 2. NovaSystem CLI (`novasystem/`)

A separate CLI tool for repository management and utilities.

- **Purpose:** Repository installation, Docker management, documentation parsing
- **Entry Point:** `novasystem` command (defined in `pyproject.toml`)
- **Key Features:**
  - Repository cloning and analysis
  - Documentation parsing to extract installation commands
  - Command execution in isolated Docker containers
  - Decision matrix framework for problem-solving
  - Technical debt management

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

# Install nova-mvp dependencies (if working on MVP)
cd nova-mvp
pip install -r requirements.txt  # If exists
```

### Environment Variables

Create a `.env` file in the project root:

```bash
# LLM API Keys
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Database (optional)
DATABASE_URL=sqlite:///./novasystem.db

# Nova MVP
DEFAULT_MODEL=claude-3-5-sonnet-20241022
DEFAULT_TEMPERATURE=0.7
```

**IMPORTANT:** Never commit `.env` files or API keys to the repository.

### Running the Nova MVP

```bash
# Run the FastAPI backend
cd nova-mvp
python -m uvicorn backend.main:app --reload

# Or use the CLI
python cli/nova.py solve "How can I improve API performance?"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=novasystem --cov=nova-mvp

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

    @property
    def system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        return "You are a helpful assistant."

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

### File Organization

- **One class per file** (exceptions for closely related classes)
- **Group imports:** stdlib, third-party, local (separated by blank lines)
- **Constants at module level** in UPPER_CASE
- **Private methods** prefixed with `_`
- **Abstract classes** inherit from `ABC` and use `@abstractmethod`

### Error Handling

```python
# Good: Specific exception handling
try:
    result = await self.llm.chat(prompt)
except RateLimitError as e:
    return self._create_response("", success=False, error=f"Rate limit: {e}")
except Exception as e:
    return self._create_response("", success=False, error=str(e))

# Bad: Bare except
try:
    result = await self.llm.chat(prompt)
except:  # Don't do this
    pass
```

---

## Testing Strategy

### Test Structure

NovaSystem uses pytest with the following organization:

```
tests/
├── test_core_functions.py      # Core utility tests
├── test_decision_matrix.py     # Decision matrix tests
├── test_parser.py              # Parser tests
├── test_novasystem_pytest.py   # Integration tests
└── test_*.py                   # Other test modules
```

### Test Configuration

From `pyproject.toml`:
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
```

### Writing Tests

```python
import pytest
from novasystem.core_utils.decision_matrix import DecisionMatrix


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

    def test_error_handling(self):
        """Test proper error handling."""
        with pytest.raises(ValueError):
            invalid_operation()
```

### Test Markers

```python
@pytest.mark.unit          # Unit tests
@pytest.mark.integration   # Integration tests
@pytest.mark.slow          # Slow-running tests
@pytest.mark.asyncio       # Async tests
```

Run specific test types:
```bash
pytest -m "unit"           # Only unit tests
pytest -m "not slow"       # Skip slow tests
```

### Coverage Goals

- Aim for **>80% coverage** on core modules
- Focus on **critical paths** and **edge cases**
- Use `pytest --cov=module` to check coverage
- Don't sacrifice test quality for coverage metrics

---

## Git Workflow

### Branch Naming Convention

**CRITICAL:** When working on behalf of a user session:

```bash
# Format: claude/<descriptive-name>-<session-id>
claude/add-memory-system-01CRKFhZZr365i9jGn6B53tk
claude/fix-rate-limiting-xyz123abc456
```

- Prefix: `claude/` (required for automated sessions)
- Description: Kebab-case description
- Session ID: Appended at the end

### Commit Messages

Follow conventional commit format:

```bash
# Format: <type>(<scope>): <subject>

feat(memory): Add long-term memory system with RAG
fix(traffic): Fix race condition in rate limiter
docs(readme): Update installation instructions
refactor(agents): Improve BaseAgent error handling
test(core): Add tests for NovaProcess
chore(deps): Update dependencies
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

### Creating Commits

```bash
# Check status
git status

# Stage files
git add <files>

# Commit with clear message
git commit -m "feat(memory): Add vector store with cosine similarity"

# Push to branch
git push -u origin claude/feature-name-session-id
```

### Pull Request Process

1. **Create feature branch** from main
2. **Make changes** with clear commits
3. **Run tests** locally (`pytest`)
4. **Push to remote** branch
5. **Create PR** with description of changes
6. **Include test plan** in PR description

### NEVER

- Push to `main` or `master` directly
- Force push (`--force`) without explicit permission
- Skip tests before committing
- Commit API keys, secrets, or `.env` files

---

## Key Architectural Patterns

### 1. Abstract Base Classes

The codebase uses ABC (Abstract Base Classes) extensively:

```python
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    @property
    @abstractmethod
    def system_prompt(self) -> str:
        pass

    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        pass
```

### 2. Factory Pattern

Used for creating LLM providers and domain experts:

```python
# LLM provider factory
def get_llm(provider: str = "auto") -> LLMProvider:
    if provider == "claude":
        return ClaudeProvider()
    elif provider == "openai":
        return OpenAIProvider()
    # ...

# Domain expert factory
def create_domain_expert(domain: str, llm_provider=None) -> DomainExpert:
    return DomainExpert(domain=domain, llm_provider=llm_provider)
```

### 3. Dataclasses for State

Dataclasses are used for structured data:

```python
from dataclasses import dataclass, field

@dataclass
class SessionState:
    session_id: str
    problem: str
    phase: ProcessPhase = ProcessPhase.PENDING
    unpack_result: Optional[AgentResponse] = None
    analysis_results: List[AgentResponse] = field(default_factory=list)
```

### 4. Async/Await Pattern

Async operations for parallel execution:

```python
# Parallel agent execution
analysis_tasks = [
    self.cae.process(analysis_input),
    *[expert.process(analysis_input) for expert in domain_experts]
]

analysis_responses = await asyncio.gather(*analysis_tasks, return_exceptions=True)
```

### 5. Singleton Pattern (Memory Store)

Global memory store instance:

```python
_memory_store: Optional[LocalVectorStore] = None

def get_memory_store(memory_file: str | None = None) -> LocalVectorStore:
    global _memory_store
    if _memory_store is None:
        _memory_store = LocalVectorStore(memory_file=memory_file)
    return _memory_store
```

### 6. Thread Safety

Thread-safe operations with locks:

```python
import threading

class LocalVectorStore:
    def __init__(self):
        self._lock = threading.Lock()
        self._documents = {}

    def add_document(self, text: str, metadata: Dict[str, Any]) -> str:
        with self._lock:
            # Critical section
            self._documents[doc_id] = document
            self._save_locked()
```

---

## Dependencies & Setup

### Core Dependencies

From `pyproject.toml`:

```toml
[project]
name = "novasystem"
version = "0.1.1"
requires-python = ">=3.8"
dependencies = [
    "pytest>=7.0.0",
    "gitpython",
    "docker",
    "tqdm",
    "requests",
]
```

### Nova MVP Dependencies

The nova-mvp package typically requires:

- **FastAPI:** Web framework
- **uvicorn:** ASGI server
- **anthropic:** Claude API client
- **openai:** OpenAI API client
- **httpx:** Async HTTP client
- **pydantic:** Data validation
- **python-dotenv:** Environment variable management

### Installation

```bash
# Install novasystem CLI tool
pip install -e .

# Install with dev dependencies (if specified)
pip install -e ".[dev]"
```

---

## Common Tasks

### Adding a New Agent

1. **Create agent file** in `nova-mvp/backend/agents/`
2. **Inherit from BaseAgent**
3. **Implement required methods:**
   - `system_prompt` property
   - `process(input_data)` method
4. **Export in `__init__.py`**
5. **Add tests** in `tests/`

Example:

```python
# nova-mvp/backend/agents/my_agent.py
from .base import BaseAgent, AgentResponse

class MyAgent(BaseAgent):
    def __init__(self, llm_provider=None):
        super().__init__("MyAgent", "custom", llm_provider)

    @property
    def system_prompt(self) -> str:
        return "You are a specialized agent that..."

    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        problem = input_data.get("problem", "")
        result = await self._call_llm(problem)
        return self._create_response(result)
```

### Adding a CLI Command

1. **Edit `nova-mvp/cli/nova.py`** or **`novasystem/cli.py`**
2. **Add subcommand** to argparse
3. **Implement handler function**
4. **Add help text**

### Updating Documentation

1. **Edit relevant `.md` file** in `docs/` or root
2. **Follow markdown style** (clear headings, code blocks)
3. **Update CHANGELOG.md** for significant changes
4. **Update this CLAUDE.md** if architecture changes

---

## Troubleshooting

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'novasystem'`

**Solution:**
```bash
# Install in development mode
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Test Discovery Issues

**Problem:** pytest doesn't find tests

**Solution:**
```bash
# Check test discovery
pytest --collect-only -v

# Ensure tests are in tests/ directory
# Ensure test files start with test_
# Ensure test classes start with Test
```

### Async Test Failures

**Problem:** Async tests failing with `RuntimeError`

**Solution:**
```bash
# Install pytest-asyncio
pip install pytest-asyncio

# Mark tests with @pytest.mark.asyncio
```

### Memory Persistence Issues

**Problem:** Memory not persisting between runs

**Solution:**
- Check `.nova_memory.json` exists and is writable
- Check file permissions
- Check for errors in console output
- Use `nova memory stats` to verify

### Rate Limiting

**Problem:** API rate limit errors

**Solution:**
- Check `.nova_traffic_state.json` for current limits
- Wait for rate limit window to reset
- Adjust limits in `traffic.py` if needed
- Use `MockProvider` for testing

---

## Quick Reference

### Key Files

| File | Purpose |
|------|---------|
| `nova-mvp/backend/core/process.py` | Main NovaProcess orchestrator |
| `nova-mvp/backend/agents/base.py` | BaseAgent abstract class |
| `nova-mvp/backend/core/llm.py` | LLM provider abstraction |
| `nova-mvp/backend/core/memory.py` | Long-term memory system |
| `novasystem/cli.py` | NovaSystem CLI tool |
| `pyproject.toml` | Project configuration |
| `CHANGELOG.md` | Version history |

### Key Commands

```bash
# Testing
pytest                                  # Run all tests
pytest -v                               # Verbose output
pytest --cov=novasystem                 # With coverage

# Nova MVP CLI
python nova-mvp/cli/nova.py solve "..."  # Solve a problem
python nova-mvp/cli/nova.py report       # Usage report

# Memory commands
python nova-mvp/cli/nova.py remember "..." --tags tag1,tag2
python nova-mvp/cli/nova.py recall "..."
python nova-mvp/cli/nova.py memory list
python nova-mvp/cli/nova.py memory stats

# NovaSystem CLI
novasystem install https://github.com/user/repo
novasystem list-runs
```

### Important Patterns

```python
# Creating an agent
class MyAgent(BaseAgent):
    @property
    def system_prompt(self) -> str: ...
    async def process(self, input_data) -> AgentResponse: ...

# Running NovaProcess
process = NovaProcess(llm_provider=get_llm("claude"))
result = await process.solve(problem="...", domains=["tech", "business"])

# Using memory
memory = get_memory_store()
memory.remember("Important fact", tags=["project"])
results = memory.recall("query about fact", limit=5)

# LLM provider
llm = get_llm("claude")  # or "openai", "mock", "auto"
response = await llm.chat(system_prompt="...", user_message="...")
```

---

## For AI Assistants: Best Practices

When working with this codebase as an AI assistant:

1. **Always read files before editing** - Never propose changes to code you haven't seen
2. **Follow existing patterns** - Match the style and structure of existing code
3. **Write tests for new code** - Add tests in `tests/` for new functionality
4. **Update documentation** - Keep docs in sync with code changes
5. **Use type hints** - Add type annotations to all new functions
6. **Async for I/O** - Use async/await for LLM calls and file operations
7. **Thread safety** - Use locks when modifying shared state
8. **Error handling** - Always handle exceptions gracefully
9. **Don't commit secrets** - Never commit API keys or `.env` files
10. **Test before pushing** - Run pytest before committing
11. **Clear commit messages** - Follow conventional commit format
12. **Ask when uncertain** - If architecture is unclear, ask before implementing

---

## Additional Resources

- **Main README:** `README.md` - User-facing documentation
- **Changelog:** `CHANGELOG.md` - Version history and changes
- **Testing Guide:** `docs/testing_guide.md` - Comprehensive testing documentation
- **Standardization Guide:** `docs/standardization.md` - Project structure standards
- **Codebase Context:** `docs/implementation/CODEBASE_CONTEXT.md` - Historical context

---

## Version History

| Version | Date | Key Changes |
|---------|------|-------------|
| 0.3.0 | 2025-12-06 | Long-term memory system with RAG |
| 0.2.1 | 2025-12-06 | Race condition fixes, budget controls |
| 0.2.0 | 2025-12-06 | Financial ledger, traffic control, CLI dashboard |
| 0.1.0 | 2025-12-06 | Initial MVP release |

---

**End of CLAUDE.md**

*This document should be updated whenever significant architectural changes occur.*
