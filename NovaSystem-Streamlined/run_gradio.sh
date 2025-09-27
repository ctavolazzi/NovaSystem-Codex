#!/bin/bash

# NovaSystem Gradio Runner
# Quick script to start the Gradio interface

set -e

# Activate environment
source venv/bin/activate

echo "🧠 Starting NovaSystem Gradio Interface..."
echo "🌐 Open http://localhost:7860 in your browser"
echo "Press Ctrl+C to stop"
echo ""

novasystem-gradio
