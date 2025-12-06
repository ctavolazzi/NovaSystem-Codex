# Nova MVP

**Multi-Agent Problem Solving System with Financial Observability**

Nova MVP orchestrates multiple AI agents to analyze problems from different perspectives and synthesize comprehensive solutions. Version 0.2.0 adds full cost tracking and rate limit protection.

## 🚀 Features (v0.2.0)

- **Multi-Provider Support:** Seamlessly switch between Claude, OpenAI, and Mock providers
- **🛡️ Traffic Control:** Automatic rate limiting (RPM/TPM) that survives restarts—prevents 429 errors
- **💰 Financial Ledger:** SQLite-backed tracking of every token and cent spent
- **📊 Analytics Dashboard:** Built-in CLI `report` command to view spend, drift, and usage by model
- **📋 Pre-flight Checks:** Cost estimation before running expensive queries
- **🔄 Smart Architecture:** Modular "System of Systems" design for observability

## Architecture

```
nova-mvp/
├── backend/                # FastAPI Python Backend
│   ├── agents/             # Agent implementations
│   │   ├── base.py         # BaseAgent abstract class
│   │   ├── dce.py          # Discussion Continuity Expert
│   │   ├── cae.py          # Critical Analysis Expert
│   │   └── domain.py       # Domain Expert factory
│   ├── core/
│   │   ├── llm.py          # LLM providers (Claude/OpenAI/Mock)
│   │   ├── process.py      # NovaProcess orchestrator
│   │   ├── traffic.py      # Rate limiting (JSON persistence)   ← NEW
│   │   ├── pricing.py      # Cost estimation                    ← NEW
│   │   ├── usage.py        # Financial ledger (SQLite)          ← NEW
│   │   └── memory.py       # VectorStore stub for RAG           ← NEW
│   ├── api/
│   │   ├── routes.py       # REST endpoints
│   │   └── websocket.py    # Real-time streaming
│   ├── main.py             # FastAPI entry point
│   └── requirements.txt
├── cli/
│   └── nova.py             # CLI with interactive mode + report
└── web/                    # Svelte Frontend
    ├── src/
    │   ├── App.svelte
    │   └── components/
    └── package.json
```

## Quick Start

### 1. Backend Setup

```bash
cd nova-mvp/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set API key (optional - falls back to mock provider)
export ANTHROPIC_API_KEY="your-key"  # or OPENAI_API_KEY

# Start server
uvicorn main:app --reload --port 8000
```

### 2. CLI Usage

```bash
cd nova-mvp

# Solve a problem
python cli/nova.py solve "How do we scale our API?" --domains tech,security

# Verbose output (shows full agent responses)
python cli/nova.py solve "What's our GTM strategy?" --domains business,ux -v

# Interactive mode
python cli/nova.py interactive

# 📊 NEW: View usage report
python cli/nova.py report
```

### 3. Financial Report (New in v0.2.0)

View your usage costs, drift estimates, and top models:

```bash
python cli/nova.py report

# Output:
# Usage Ledger Report
# Database: /path/to/.nova_usage.db
#
# Totals
#   Spend: $0.004200
#   Estimated: $0.003800
#   Transactions: 15
#
# Top Model by Spend
#   gemini-2.5-flash → $0.003500
#
# Average Drift (actual vs. estimate)
#   +10.53%
#
# Last 5 Transactions
#   2025-12-06 15:30:00 | claude/claude-sonnet-4 | est $0.001 | ...

# Options:
python cli/nova.py report --limit 20      # Show more transactions
python cli/nova.py report --db custom.db  # Use custom database
```

### 4. Web Interface

```bash
cd nova-mvp/web

# Install dependencies
npm install

# Start dev server (proxies to backend on :8000)
npm run dev

# Open http://localhost:3000
```

## 🏗️ System Architecture (v0.2.0)

Nova follows a modular "System of Systems" approach:

| Module | Role | Persistence |
|--------|------|-------------|
| `traffic.py` | Rate limiting (RPM/TPM sliding window) | JSON |
| `pricing.py` | Cost estimation before execution | — |
| `usage.py` | Financial ledger for all transactions | SQLite |
| `llm.py` | Coordinates providers, records usage | — |
| `memory.py` | VectorStore stub for future RAG | — |

### Data Files

Nova creates these files automatically:

| File | Purpose | Location |
|------|---------|----------|
| `.nova_usage.db` | Transaction history | Working directory |
| `.nova_traffic_state.json` | Rate limit windows | Working directory |

Both files are gitignored and should not be committed.

## Agents

| Agent | Role | Phase |
|-------|------|-------|
| **DCE** (Discussion Continuity Expert) | Unpacks problems, synthesizes solutions | 1 & 3 |
| **CAE** (Critical Analysis Expert) | Identifies risks, edge cases, blind spots | 2 |
| **Domain Experts** | Specialized knowledge (Tech, Business, Security, UX, etc.) | 2 |

## Three-Phase Process

1. **UNPACK** - DCE analyzes the problem, identifies components, stakeholders, constraints
2. **ANALYZE** - Domain experts and CAE analyze in parallel using `asyncio.gather()`
3. **SYNTHESIZE** - DCE combines all perspectives into actionable recommendations

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/solve` | POST | Async solve - returns immediately with session_id |
| `/api/solve/sync` | POST | Sync solve - waits for full result |
| `/api/sessions/{id}` | GET | Get session status and results |
| `/api/sessions` | GET | List recent sessions |
| `/api/ws/{id}` | WebSocket | Real-time streaming updates |
| `/api/health` | GET | Health check |
| `/api/providers` | GET | List available LLM providers |
| `/api/check-status` | POST | Pre-flight cost + rate limit check ← NEW |

### Example Request

```bash
curl -X POST http://localhost:8000/api/solve/sync \
  -H "Content-Type: application/json" \
  -d '{
    "problem": "How should we handle user authentication?",
    "domains": ["technology", "security"],
    "provider": "auto"
  }'
```

### Pre-flight Check (New in v0.2.0)

```bash
curl -X POST http://localhost:8000/api/check-status \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing",
    "model": "gemini-2.5-flash"
  }'

# Response:
# {
#   "cost_estimate": {"input_tokens": 6, "projected_cost": 0.000024},
#   "rate_limit_status": "ok",
#   "retry_after": 0.0
# }
```

## LLM Providers

| Provider | Model | API Key |
|----------|-------|---------|
| Claude | claude-sonnet-4-20250514 | `ANTHROPIC_API_KEY` |
| OpenAI | gpt-4o | `OPENAI_API_KEY` |
| Mock | mock-v1 | None (always available) |

The `auto` provider tries Claude first, then OpenAI, then falls back to Mock.

## Domain Experts

Pre-defined domains:
- `technology` / `tech` - Software architecture, scalability, DevOps
- `business` - Strategy, market analysis, ROI
- `security` - Threat modeling, compliance, data protection
- `ux` - User research, usability, accessibility
- `data` - Analytics, ML/AI, data governance
- `operations` - Process optimization, logistics
- `legal` - Regulatory compliance, contracts
- `finance` - Budgeting, financial modeling

Custom domains can be created by passing any string.

## Configuration

Create a `.env` file in the `nova-mvp/` directory:

```ini
# LLM API Keys (at least one recommended)
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Default provider: auto, claude, openai, mock
NOVA_LLM_PROVIDER=auto

# Server settings
NOVA_API_HOST=0.0.0.0
NOVA_API_PORT=8000

# Debug mode
NOVA_DEBUG=false
```

## Development

```bash
# Run backend with auto-reload
cd backend && uvicorn main:app --reload

# Run frontend with hot reload
cd web && npm run dev

# Run CLI tests
python cli/nova.py solve "test" --provider mock -v

# Run release verification
python verify_release.py
```

## Offline / Restricted Environments

The `start.sh` helper can skip virtualenv setup when internet access is blocked:

```bash
# Use system Python packages
NOVA_USE_SYSTEM_PYTHON=true ./start.sh

# Skip pip installs (assumes deps present)
NOVA_SKIP_PIP_INSTALL=true ./start.sh
```

## License

MIT - See LICENSE file in project root.
