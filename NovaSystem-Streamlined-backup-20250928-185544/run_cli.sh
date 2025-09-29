#!/bin/bash

# NovaSystem CLI Runner
# Quick script to run CLI commands

set -e

# Activate environment
source venv/bin/activate

# Run the command passed as arguments
novasystem "$@"
