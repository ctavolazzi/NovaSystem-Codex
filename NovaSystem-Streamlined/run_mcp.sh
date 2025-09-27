#!/bin/bash

# NovaSystem MCP Server Launch Script

# Activate virtual environment
source venv/bin/activate

# Run the MCP server
python -m novasystem.mcp.server

