"""Module execution entrypoint for `python -m novasystem.cli`."""

from .main import main as typer_main

if __name__ == "__main__":
    raise SystemExit(typer_main())
