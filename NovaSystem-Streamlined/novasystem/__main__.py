#!/usr/bin/env python3
"""
NovaSystem CLI Entry Point.

Allows running NovaSystem as a module:
    python -m novasystem solve "Your problem here"
    python -m novasystem interactive
    python -m novasystem list-models
"""

import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())
