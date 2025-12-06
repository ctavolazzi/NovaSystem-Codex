#!/bin/bash
# Nova MVP - Startup Script
# Starts both backend and frontend servers

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║               NOVA MVP - Startup Script                      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check Node
if ! command -v npm &> /dev/null; then
    echo "⚠️  npm not found - web interface will not be available"
    WEB_AVAILABLE=false
else
    WEB_AVAILABLE=true
fi

# Setup backend
echo "📦 Setting up backend..."
cd backend

if [ "${NOVA_USE_SYSTEM_PYTHON:-false}" = true ]; then
    echo "   ⚠️  Using system Python environment (skipping venv setup)"
else
    if [ ! -d "venv" ]; then
        echo "   Creating virtual environment..."
        python3 -m venv venv
    fi

    source venv/bin/activate

    if [ "${NOVA_SKIP_PIP_INSTALL:-false}" = true ]; then
        echo "   ⚠️  NOVA_SKIP_PIP_INSTALL set - skipping dependency installation"
    else
        echo "   Installing dependencies..."
        pip install -q -r requirements.txt
    fi
fi

# Check for API keys
if [ -n "$ANTHROPIC_API_KEY" ]; then
    echo "   ✓ ANTHROPIC_API_KEY found"
elif [ -n "$OPENAI_API_KEY" ]; then
    echo "   ✓ OPENAI_API_KEY found"
else
    echo "   ⚠️  No API keys found - using mock provider"
fi

cd "$SCRIPT_DIR"

echo ""
echo "🚀 Starting backend server on http://localhost:8000..."
# Run from nova-mvp directory so backend is recognized as a package
source backend/venv/bin/activate
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Setup and start frontend if available
if [ "$WEB_AVAILABLE" = true ]; then
    echo ""
    echo "📦 Setting up frontend..."
    cd web

    if [ ! -d "node_modules" ]; then
        echo "   Installing dependencies..."
        npm install --silent
    fi

    echo ""
    echo "🌐 Starting frontend server on http://localhost:3000..."
    npm run dev &
    FRONTEND_PID=$!

    cd ..
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "  Nova MVP is running!"
echo ""
echo "  📡 Backend API:    http://localhost:8000"
echo "  📚 API Docs:       http://localhost:8000/docs"
if [ "$WEB_AVAILABLE" = true ]; then
    echo "  🌐 Web Interface:  http://localhost:3000"
fi
echo ""
echo "  CLI Usage:"
echo "    python cli/nova.py solve \"Your problem\" --domains tech,business"
echo "    python cli/nova.py interactive"
echo ""
echo "  Press Ctrl+C to stop all servers"
echo ""
echo "════════════════════════════════════════════════════════════════"

# Wait for interrupt
cleanup() {
    echo ""
    echo "Shutting down..."
    kill $BACKEND_PID 2>/dev/null || true
    [ "$WEB_AVAILABLE" = true ] && kill $FRONTEND_PID 2>/dev/null || true
    exit 0
}

trap cleanup SIGINT SIGTERM

wait
