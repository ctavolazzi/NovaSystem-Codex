"""Module execution entrypoint for `python -m novasystem.cli`."""

from . import legacy_main

if __name__ == "__main__":
    raise SystemExit(legacy_main())
