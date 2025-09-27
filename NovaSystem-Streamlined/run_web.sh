#!/bin/bash

# NovaSystem Web Runner
# Quick script to start the web interface

set -e

# Activate environment
source venv/bin/activate

echo "🧠 Starting NovaSystem Web Interface..."
echo "🌐 Open http://localhost:5000 in your browser"
echo "Press Ctrl+C to stop"
echo ""

novasystem-web
