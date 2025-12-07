# NovaSystem Development Versions

This directory contains experimental and development versions of NovaSystem, each exploring different architectural approaches and features.

## 📁 Directory Structure

### Production Versions (Outside /dev)

- **`/novasystem/`** - Main package (v0.1.1) - Repository installation automation tool
- **`/NovaSystem-Streamlined/`** - Production framework (v2.0) - Multi-agent problem-solving system

### Experimental Versions (In /dev)

#### 🔹 **NS-core** - Lightweight Core Implementation
**Location:** `dev/NS-core/`
**Status:** Functional
**Purpose:** Minimal FastAPI-based chat implementation

**Features:**
- Async FastAPI backend
- SQLite database with SQLAlchemy ORM
- OpenAI and Ollama LLM integration
- Session management
- Alembic migrations

**When to use:** Reference implementation for minimal NovaSystem setup

**Documentation:** See `/dev/NS-core/readme.md`

---

#### 🔹 **NS-bytesize** - Agent-Based Architecture
**Location:** `dev/NS-bytesize/`
**Status:** Experimental
**Purpose:** Modular agent/bot/hub architecture exploration

**Features:**
- Agent-based design pattern
- Bot and Hub abstractions
- Docker containerization
- Comprehensive test suite
- AutoGen integration experiments

**Structure:**
- `/agents/` - Agent implementations
- `/bots/` - Bot components
- `/hubs/` - Hub orchestration
- `/examples/` - Usage examples
- `/tests/` - Validation and integration tests

**When to use:** Exploring multi-agent coordination patterns

---

#### 🔹 **NS-lite** - UI Experimentation
**Location:** `dev/NS-lite/`
**Status:** Prototype
**Purpose:** User interface experiments and prototypes

**Contains:**
- `gradio_app.py` - Gradio-based UI
- `app.py` - Flask/FastAPI apps
- `mrn-test.py` - Test implementations
- `ns-ollama.py` - Ollama integration tests
- `/templates/` - HTML templates

**When to use:** UI/UX prototyping and rapid testing

---

#### 🔹 **mcp-claude** - Model Context Protocol
**Location:** `dev/mcp-claude/`
**Status:** Functional
**Purpose:** MCP server implementation for Claude integration

**Features:**
- Weather service MCP server example
- OpenWeatherMap API integration
- Claude-compatible context protocol

**Documentation:** See `/dev/mcp-claude/README.md`

**When to use:** Integrating external services via MCP

---

#### 🔹 **saas** - SaaS Framework Exploration
**Location:** `dev/saas/`
**Status:** Experimental
**Purpose:** Exploring SaaS deployment patterns

**Contains:**
- `open-saas/` - Open SaaS framework integration
- SaaS architecture experiments

**When to use:** Exploring commercial deployment patterns

---

#### 🔹 **test_data** - Shared Test Fixtures
**Location:** `dev/test_data/`
**Purpose:** Common test data and fixtures for all dev versions

---

#### 🔹 **utils** - Shared Utilities
**Location:** `dev/utils/`
**Purpose:** Common utility functions shared across dev versions

---

## 🚀 Quick Start Guide

### For Main Package (Production)
```bash
# From project root
pip install -e .
novasystem install https://github.com/user/repo
```

### For NovaSystem-Streamlined (Production)
```bash
cd NovaSystem-Streamlined
pip install -r requirements.txt
cp .env.example .env  # Configure your API keys
python -m novasystem.cli
```

### For Development Versions
```bash
# Example: NS-core
cd dev/NS-core
pip install -r requirements.txt
cp .env.example .env  # If it exists
# See individual README files for specific instructions
```

## 📊 Version Comparison

| Version | Purpose | Status | Production Ready | Main Use Case |
|---------|---------|--------|------------------|---------------|
| `/novasystem/` | Repo installer | Stable | ✅ Yes | Automating repo installation |
| `/NovaSystem-Streamlined/` | Multi-agent framework | Active | ⚠️  Alpha | Problem-solving with AI agents |
| `NS-core` | Minimal implementation | Functional | ❌ No | Learning/reference |
| `NS-bytesize` | Agent architecture | Experimental | ❌ No | Architecture research |
| `NS-lite` | UI prototypes | Prototype | ❌ No | UI/UX exploration |
| `mcp-claude` | MCP integration | Functional | ❌ No | Service integration |
| `saas` | SaaS patterns | Experimental | ❌ No | Commercial exploration |

## 🧪 Testing

Each dev version has its own test suite:

```bash
# Test specific version
cd dev/NS-bytesize
pytest

# Test all dev versions (from /dev)
pytest
```

## 🤝 Contributing

When adding new experimental versions:

1. Create a new directory under `/dev/`
2. Add a descriptive README.md explaining:
   - Purpose and goals
   - Current status
   - How to run/test
   - Key differences from other versions
3. Include `requirements.txt` or `pyproject.toml`
4. Add tests if applicable
5. Update this README with the new version

## 📝 Notes

- **Production use:** Use `/novasystem/` or `/NovaSystem-Streamlined/`
- **Development/Research:** Use versions in `/dev/`
- **API keys required:** Most versions need OpenAI, Anthropic, or Ollama configured
- **Python version:** Most versions require Python 3.8+

## 🔗 Related Documentation

- [Main README](/README.md)
- [NovaSystem-Streamlined README](/NovaSystem-Streamlined/README.md)
- [Architecture docs](/docs/architecture/)
- [API docs](/docs/api/)

---

**Last updated:** 2025-11-28
**Maintained by:** NovaSystem Team
