#!/bin/bash

# NovaSystem Quick Start Script
# This script activates the environment and provides options to run NovaSystem

set -e  # Exit on any error

echo "🧠 NovaSystem v2.0 Quick Start"
echo "==============================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Run ./setup.sh first."
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if package is installed
if ! command -v novasystem &> /dev/null; then
    echo "❌ NovaSystem not installed. Run ./setup.sh first."
    exit 1
fi

echo "✅ Environment ready!"
echo ""
echo "Choose how to run NovaSystem:"
echo ""
echo "1) CLI - Solve a problem via command line"
echo "2) Gradio - Web interface (easiest)"
echo "3) Web - Flask web interface"
echo "4) API - FastAPI server"
echo "5) Interactive - Interactive CLI mode"
echo "6) Test - Run tests"
echo "7) Exit"
echo ""

read -p "Enter your choice (1-7): " choice

case $choice in
    1)
        echo ""
        read -p "Enter your problem: " problem
        echo "🤔 Solving: $problem"
        echo ""
        novasystem solve "$problem"
        ;;
    2)
        echo "🌐 Starting Gradio interface..."
        echo "Open http://localhost:7860 in your browser"
        novasystem-gradio
        ;;
    3)
        echo "🌐 Starting Web interface..."
        echo "Open http://localhost:5000 in your browser"
        novasystem-web
        ;;
    4)
        echo "🚀 Starting API server..."
        echo "API available at http://localhost:8000"
        echo "Docs at http://localhost:8000/docs"
        python -m novasystem.api.rest
        ;;
    5)
        echo "💬 Starting interactive mode..."
        novasystem interactive
        ;;
    6)
        echo "🧪 Running tests..."
        pytest tests/ -v
        ;;
    7)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac
