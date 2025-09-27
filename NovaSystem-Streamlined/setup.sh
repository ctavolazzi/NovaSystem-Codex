#!/bin/bash

# NovaSystem Setup Script
# This script sets up the virtual environment and installs dependencies

set -e  # Exit on any error

echo "🧠 NovaSystem v2.0 Setup"
echo "========================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install the package in development mode
echo "📥 Installing NovaSystem..."
pip install -e .

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To use NovaSystem:"
echo "1. Activate the environment: source venv/bin/activate"
echo "2. Run any of these commands:"
echo "   - novasystem solve 'your problem here'"
echo "   - novasystem-gradio"
echo "   - novasystem-web"
echo "   - python -m novasystem.api.rest"
echo ""
echo "Or use the quick-start script: ./start.sh"
