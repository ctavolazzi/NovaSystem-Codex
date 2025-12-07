# 🧠 NovaSystem v2.0 - Unified Multi-Agent Problem-Solving Framework

A streamlined, unified implementation of the Nova Process that provides multiple interfaces (CLI, Web, Gradio) for complex problem-solving using specialized AI agents.

## ✨ Features

- **Multi-Agent Architecture**: DCE (Discussion Continuity Expert), CAE (Critical Analysis Expert), and Domain Experts
- **Multiple Interfaces**: CLI, Web, and Gradio interfaces from the same core
- **Real LLM Integration**: OpenAI, Ollama, and other providers with automatic fallback
- **Real-time Updates**: WebSocket support for live progress tracking
- **Memory Management**: Context-aware conversation with memory compression
- **Streamlined Codebase**: Single source of truth, no duplicate implementations
- **Comprehensive Testing**: Full test suite with 12 passing tests

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd NovaSystem-Streamlined

# Install dependencies
pip install -e .

# Set up environment variables (required for real AI responses)
export OPENAI_API_KEY="your-openai-key"
export OLLAMA_HOST="http://localhost:11434"

# Or create a .env file
cp env.template .env
# Edit .env with your API keys
```

### Usage

#### CLI Interface
```bash
# Solve a problem (requires OpenAI API key for real AI responses)
novasystem solve "How can we improve our code review process?"

# Interactive mode
novasystem interactive --domains "Technology,Business"

# With specific options
novasystem solve "Design a scalable auth system" \
  --domains "Security,Architecture" \
  --max-iterations 5 \
  --model gpt-4

# Verbose output
novasystem --verbose solve "Test problem" --max-iterations 1
```

#### Web Interface
```bash
# Start the web interface
novasystem-web

# Open http://localhost:5000 in your browser
```

#### Gradio Interface
```bash
# Start the Gradio interface
novasystem-gradio

# Open http://localhost:7860 in your browser
```

#### API Server
```bash
# Start the API server
python -m novasystem.api.rest

# API will be available at http://localhost:8000
```

## 🏗️ Architecture

```
NovaSystem-Streamlined/
├── src/novasystem/
│   ├── core/           # Core Nova Process logic
│   │   ├── agents.py   # DCE, CAE, Domain Experts
│   │   ├── process.py  # Process orchestration
│   │   └── memory.py   # Context/memory management
│   ├── api/            # API layer
│   │   ├── rest.py     # REST endpoints
│   │   └── websocket.py # Real-time updates
│   ├── ui/             # User interfaces
│   │   ├── web.py      # Web interface
│   │   └── gradio.py   # Gradio interface
│   ├── utils/          # Utilities
│   │   ├── config.py   # Configuration
│   │   └── llm_service.py # LLM integration
│   └── cli.py          # Command line interface
├── tests/              # Test suite
├── docs/               # Documentation
└── examples/           # Usage examples
```

## 🧩 Core Components

### Agents

- **DCE (Discussion Continuity Expert)**: Maintains conversation flow and synthesizes insights
- **CAE (Critical Analysis Expert)**: Provides critical evaluation and identifies issues
- **Domain Experts**: Provide specialized knowledge in specific areas

### Process Flow

1. **Problem Unpacking**: Break down the problem into components
2. **Iterative Refinement**: Multiple rounds of solution development
3. **Final Synthesis**: Create comprehensive solution

### Memory Management

- **Short-term Memory**: Recent conversation context
- **Long-term Memory**: Important insights and decisions
- **Context Retrieval**: Relevant information based on queries

## 🔧 Configuration

### Environment Variables

```bash
# LLM Configuration
OPENAI_API_KEY=your-openai-key
OLLAMA_HOST=http://localhost:11434
DEFAULT_MODEL=gpt-4

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
WEB_HOST=0.0.0.0
WEB_PORT=5000
GRADIO_HOST=0.0.0.0
GRADIO_PORT=7860
```

### Configuration File

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your-openai-key
OLLAMA_HOST=http://localhost:11434
DEFAULT_MODEL=gpt-4
MAX_ITERATIONS=5
DEFAULT_DOMAINS=General,Technology,Business
```

## 📚 Examples

### Basic Problem Solving

```python
from novasystem import NovaProcess
from novasystem.core.memory import MemoryManager

# Create Nova Process
memory_manager = MemoryManager()
nova_process = NovaProcess(
    domains=["Technology", "Business"],
    model="gpt-4",
    memory_manager=memory_manager
)

# Solve a problem (requires OpenAI API key for real AI responses)
result = await nova_process.solve_problem(
    "How can we improve our team's productivity?",
    max_iterations=3
)

print(result)
```

### Streaming Results

```python
# Stream results in real-time
async for update in nova_process.solve_problem(
    "Design a new feature",
    max_iterations=5,
    stream=True
):
    print(f"Update: {update}")
```

### Custom Agents

```python
from novasystem.core.agents import AgentFactory

# Create custom agent team
team = AgentFactory.create_agent_team(
    domains=["AI", "Robotics", "Ethics"],
    model="gpt-4"
)

# Use in Nova Process
nova_process = NovaProcess(agents=team)
```

## 🧪 Testing

```bash
# Run all tests (12 tests currently passing)
python3 -m pytest tests/ -v

# Run with coverage
pytest --cov=novasystem

# Run specific test file
pytest tests/test_core.py -v
```

### Test Results
- ✅ **12/12 tests passing**
- ✅ CLI interface working
- ✅ Programmatic usage working
- ✅ Memory management working
- ✅ Agent creation and factory pattern working
- ✅ Process orchestration working
- ✅ **LLM Integration**: Real AI calls with automatic fallback when API keys not available

## 📖 API Documentation

### REST API Endpoints

- `POST /api/solve` - Start a new problem-solving session
- `GET /api/sessions/{session_id}/status` - Get session status
- `GET /api/sessions/{session_id}/result` - Get session result
- `GET /api/sessions` - List all sessions
- `WebSocket /ws/{session_id}` - Real-time updates

### Example API Usage

```bash
# Start a session
curl -X POST http://localhost:8000/api/solve \
  -H "Content-Type: application/json" \
  -d '{
    "problem": "How can we optimize our database queries?",
    "domains": ["Database", "Performance"],
    "max_iterations": 3
  }'

# Check status
curl http://localhost:8000/api/sessions/{session_id}/status
```

## 🤖 Model Management

NovaSystem now includes intelligent model management with automatic discovery and selection:

### List Available Models
```bash
# List all available models with capabilities
novasystem list-models

# Show detailed capability scores
novasystem list-models --detailed
```

### Get Model Information
```bash
# Get detailed info about a specific model
novasystem model-info phi3
novasystem model-info gpt-oss:20b
```

### Performance Metrics
```bash
# View overall performance metrics
novasystem metrics

# View metrics for specific session
novasystem metrics --session-id abc123

# View detailed metrics with system info
novasystem metrics --detailed --system
```

### Model Cache Management
```bash
# View cache status
novasystem cache status

# Clear model cache
novasystem cache clear

# Preload a model
novasystem cache preload --model phi3

# Get model recommendations
novasystem cache recommend --task-type reasoning
```

### Intelligent Model Selection

The system automatically selects the best model based on:
- **Task Type**: Different agents use models optimized for their role
  - DCE (Discussion Continuity Expert): Reasoning and analysis models
  - CAE (Critical Analysis Expert): Analysis-focused models
  - Domain Experts: General-purpose models with coding capabilities
- **Performance**: Speed vs capability trade-offs
- **Availability**: Automatic fallback from OpenAI to Ollama

### Model Capabilities

Each model is rated on:
- **Reasoning** (0-100): Logical thinking and problem-solving
- **Coding** (0-100): Programming and technical tasks
- **Analysis** (0-100): Critical thinking and evaluation
- **Creativity** (0-100): Creative problem-solving and ideation
- **Speed** (0-100): Response time and efficiency
- **Context Length**: Maximum tokens supported
- **Size**: Model size in GB (affects loading time)

## 🏭 Production Deployment

NovaSystem includes a complete production deployment setup with Docker Compose, monitoring, and security.

### Quick Production Deploy

```bash
# Clone and setup
git clone <repository-url>
cd NovaSystem-Streamlined

# Configure environment
cp env.prod .env.prod
# Edit .env.prod with your settings

# Deploy to production
./deploy.sh deploy
```

### Production Features

- **Docker Compose**: Complete containerized deployment
- **Nginx Load Balancer**: Reverse proxy with SSL support
- **Redis Caching**: High-performance caching and session management
- **Prometheus Monitoring**: Comprehensive metrics collection
- **Grafana Dashboards**: Real-time system visualization
- **Health Checks**: Automatic service monitoring
- **Backup System**: Automated backup and restore
- **Security**: Rate limiting, SSL/TLS, security headers

### Production URLs

- **API Server**: http://localhost:8000
- **Web Interface**: http://localhost:5000
- **Gradio Interface**: http://localhost:7860
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000

### Deployment Commands

```bash
# Deploy to production
./deploy.sh deploy

# Update deployment
./deploy.sh update

# View logs
./deploy.sh logs

# Check status
./deploy.sh status

# Stop services
./deploy.sh stop
```

For detailed production deployment instructions, see [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Based on the original Nova Process methodology
- Built with FastAPI, Gradio, and modern Python practices
- Inspired by multi-agent AI research and collaborative problem-solving

## 🔧 Current Status & Features

### ✅ What's Working
- **Core Framework**: Multi-agent architecture with DCE, CAE, and Domain Experts
- **CLI Interface**: Full command-line interface with solve, interactive, model management, metrics, and cache commands
- **Web Interfaces**: Flask-based web interface and Gradio interface with real LLM integration
- **Memory Management**: Context-aware memory system with short/long-term storage
- **API Server**: REST API server with WebSocket support for real-time updates
- **Testing**: Comprehensive test suite (12/12 tests passing)
- **Programmatic Usage**: Full Python API for integration
- **LLM Integration**: Real AI calls with OpenAI/Ollama support and intelligent fallback
- **Ollama Integration**: Full local LLM support with model discovery and capability detection
- **Intelligent Model Selection**: Automatic model selection based on task type and performance
- **Performance Monitoring**: Comprehensive metrics collection and system monitoring
- **Model Caching**: Intelligent model caching with LRU eviction and memory management
- **Production Ready**: Docker Compose deployment with monitoring, load balancing, and security

### 🆕 New Features in v2.0
- **Performance Metrics**: Real-time performance monitoring with Prometheus integration
- **Model Caching**: Intelligent caching system for faster model loading
- **Web Interfaces**: Modern web UI and interactive Gradio interface
- **Production Deployment**: Complete Docker Compose setup with Nginx, Redis, and monitoring
- **CLI Enhancements**: New commands for metrics, cache management, and system monitoring
- **Large Model Support**: Optimized for 13GB+ models with memory management
- **System Monitoring**: Grafana dashboards and Prometheus metrics
- **Security**: Production-ready security configuration with rate limiting and SSL support

### 🚀 Production Features
- **Docker Deployment**: One-command deployment with `./deploy.sh deploy`
- **Monitoring**: Prometheus metrics and Grafana dashboards
- **Load Balancing**: Nginx reverse proxy with rate limiting
- **Caching**: Redis-based caching and session management
- **Security**: SSL/TLS support, security headers, and access control
- **Backup**: Automated backup and restore functionality
- **Scaling**: Horizontal and vertical scaling support

---

**NovaSystem v2.0** - Streamlined, unified, and ready for complex problem-solving! 🚀
