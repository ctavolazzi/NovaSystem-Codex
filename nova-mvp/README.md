# Nova MVP

**Multi-Agent Problem Solving System**

Nova MVP orchestrates multiple AI agents to analyze problems from different perspectives and synthesize comprehensive solutions.

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
│   │   └── process.py      # NovaProcess orchestrator
│   ├── api/
│   │   ├── routes.py       # REST endpoints
│   │   └── websocket.py    # Real-time streaming
│   ├── main.py             # FastAPI entry point
│   └── requirements.txt
├── cli/
│   └── nova.py             # CLI with interactive mode
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
```

### 3. Web Interface

```bash
cd nova-mvp/web

# Install dependencies
npm install

# Start dev server (proxies to backend on :8000)
npm run dev

# Open http://localhost:3000
```

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

Custom domains can be created by passing any string - the system will create a generic expert.

## Design

The web interface features a **command center aesthetic**:
- Dark theme with `#0a0a0f` background
- Cyan accent (`#00ffaa`) for Nova brand
- JetBrains Mono + Sora fonts
- Subtle grid background
- Agent-specific color coding
- Real-time WebSocket updates with animations

## Development

```bash
# Run backend with auto-reload
cd backend && uvicorn main:app --reload

# Run frontend with hot reload
cd web && npm run dev

# Run CLI tests
python cli/nova.py solve "test" --provider mock -v
```

## License

MIT - See LICENSE file in project root.
