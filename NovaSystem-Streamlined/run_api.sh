#!/bin/bash

# NovaSystem API Runner
# Quick script to start the API server

set -e

# Activate environment
source venv/bin/activate

echo "🧠 Starting NovaSystem API Server..."
echo "🚀 API available at http://localhost:8000"
echo "📚 API docs at http://localhost:8000/docs"
echo "Press Ctrl+C to stop"
echo ""

python -m novasystem.api.rest
