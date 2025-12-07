# NovaSystem CLI

NovaSystem is a Python 3.8+ toolkit for automating repository setup instructions. It clones a repository (remote or local), scans its documentation for installation commands, runs those commands in an isolated Docker container, and records everything in a SQLite database that you can query from the CLI. The package also ships a few reusable utilities (decision matrices, documentation mapping, and technical-debt helpers) that can be imported directly.

## What it does
- Discover documentation files (README, INSTALL, docs/\*) and extract install commands from fenced or inline code blocks.
- Deduplicate and prioritize commands, then execute them sequentially in an ephemeral Docker container (Ubuntu base with Python/Node toolchain).
- Persist run history (repository metadata, documentation snapshots, commands, outputs) to a local SQLite database for later inspection.
- Provide helper utilities: decision matrix scoring, documentation map generation, and technical-debt backlog structures.
- Bundle thorough tests and reference docs to make the behavior auditable and easy to extend.

## Requirements
- Python 3.8 or newer
- Docker daemon available locally (used for isolated command execution)
- Git client

## Installation
Install from the repository root (recommended for now):
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

If you prefer an isolated dependency install without editable mode:
```bash
pip install .
```

## CLI quickstart
Run `novasystem --help` for full options. Common flows:

```bash
# Analyze and install a remote repo
novasystem install https://github.com/owner/project

# Work on a local repo and mount it into the container
novasystem install /path/to/repo --mount

# Disable auto repo-type detection if you know what you're doing
novasystem install https://github.com/owner/project --no-detect

# Review history
novasystem list-runs --output json
novasystem show-run 3

# Clean up records
novasystem delete-run 3
novasystem cleanup --days 30
```

Command results include a summary, counts of executed commands, per-command exit codes/output, and stored documentation paths. Use `--db-path` to point the CLI at a specific database file and `--output json` for machine-readable results.

## CLI demo (no Docker required)
Run the bundled demo script from the project root to see NovaSystem's command-line flow (test-mode by default). It now guides you through Nova processing and can optionally show Gemini image generation/understanding when a Gemini API key is present:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python novasystem_demo.py
```

The script:
- Builds a tiny throwaway repo with mixed install docs.
- Runs NovaSystem in safe test mode (no Docker) and prints the install summary, stored docs, and command log.
- Shows run history and stored documentation/command records for the demo run.
- Optionally runs a Gemini image generation + vision-understanding segment (auto-enabled when `GEMINI_API_KEY` is set, or by passing `--with-gemini`).
- Writes results to `./novasystem_demo.db` and saves artifacts under `./novasystem_demo_outputs` by default.

Options:
- `python novasystem_demo.py --use-docker` to exercise the real Docker executor (requires a running daemon).
- `python novasystem_demo.py --db-path /tmp/my-demo.db` to isolate demo history.
- `python novasystem_demo.py --keep-repo` to leave the generated demo repo on disk for inspection.
- `python novasystem_demo.py --with-gemini` to force-run the Gemini segment (requires `GEMINI_API_KEY`).
- Gemini tuning: `--gemini-model-gen`, `--gemini-model-vision`, `--gemini-prompt`, `--gemini-vision-prompt`, `--out-dir`.
- Delete `novasystem_demo.db` to reset demo history.

Troubleshooting:
- `ModuleNotFoundError: docker` or `git` → run `pip install -e .` from the repo root to pull dependencies.
- Docker-related errors when using `--use-docker` or the main `novasystem install` command → start the Docker daemon and ensure your user can run `docker ps`.
- `sqlite3.OperationalError` about the database/log location → point `--db-path` (or `NOVASYSTEM_DB_PATH`) and `NOVASYSTEM_LOG_PATH` to a writable directory, or set `NOVASYSTEM_DISABLE_FILE_LOG=1` to disable file logging.
- Empty history after running the demo → confirm you're reading the same DB path you wrote to (defaults to `./novasystem_demo.db`).

## Pixel Lab API module demo
Showcases a doc-to-code flow: it downloads the Pixel Lab LLM-friendly docs and emits a minimal Python client with one method per endpoint.
```bash
python examples/pixellab_module_demo.py \
  --output examples/generated/pixellab_client.py
```
- Uses `https://api.pixellab.ai/v2/llms.txt` by default; pass `--source path/to/llms.txt` to work offline.
- After generation:
  ```python
  from examples.generated.pixellab_client import PixelLabClient
  client = PixelLabClient(api_token="YOUR_TOKEN")
  print(client.get_balance())
  ```

## Gemini image demo (image generation + image understanding)
Gemini functionality is integrated into `novasystem_demo.py` (auto-runs when `GEMINI_API_KEY` is set). There is also a standalone script `gemini_image_demo.py` if you want to run Gemini only.

Setup and run from repo root:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .  # core repo (optional but safe)
pip install google-genai pillow
export GEMINI_API_KEY=your_key_here
python gemini_image_demo.py \
  --prompt "Gemini-themed lab scene with holographic dashboards" \
  --model-gen gemini-2.5-flash-image \
  --model-vision gemini-2.5-flash
```

What happens:
- Calls an image-generation model and saves outputs to `gemini_demo_outputs/`.
- Builds a synthetic PNG locally, sends it with a vision prompt, and saves the textual response to `gemini_demo_outputs/vision_result.txt`.
- Flags: `--model-gen` (e.g., `gemini-3-pro-image-preview`), `--model-vision` (vision-capable text+image model), `--vision-prompt`, `--out-dir`.

Troubleshooting:
- Missing API key → ensure `GEMINI_API_KEY` is set in your shell.
- `ModuleNotFoundError: google.genai` or `PIL` → run `pip install google-genai pillow`.
- `403/permission denied` → verify the key has access to the chosen model; try `gemini-2.5-flash-image` for generation and `gemini-2.5-flash` for vision.
- `404 model not found` → double-check the model name spelling.
- `429 rate limit` → wait/retry or lower request volume.
- Corporate proxies/firewalls → ensure outbound HTTPS to the Gemini endpoint is allowed.

## Library usage
The orchestrator can be used programmatically without the CLI:

```python
from novasystem.nova import Nova

nova = Nova(db_path="novasystem.db", test_mode=True)  # test_mode skips Docker calls
result = nova.process_repository("https://github.com/example/repo", mount_local=False)

print(result["message"])
print("Commands executed:", result.get("commands_executed"))
```

Utility modules are importable on their own:

```python
from novasystem.core_utils import make_decision

decision = make_decision(
    options=["Option A", "Option B", "Option C"],
    criteria=["Cost", "Speed", "Quality"],
    scores={
        "Option A": [7, 8, 6],
        "Option B": [9, 5, 7],
        "Option C": [6, 9, 8],
    },
)

print(decision.winner)
print(decision.comparison_table())
```

Documentation mapping and technical-debt helpers are available at `novasystem.core_utils.generate_doc_map` and `novasystem.technical_debt.*`.

## Data and configuration
- Database: defaults to `novasystem.db` in the working directory. Override with `--db-path` or `NOVASYSTEM_DB_PATH`.
- Logging: console logging is always enabled. A file log at `~/.novasystem.log` is created unless `NOVASYSTEM_DISABLE_FILE_LOG=1` is set; override the path with `NOVASYSTEM_LOG_PATH`.
- Docker: the executor builds/uses `novasystem/runner:latest`, mounts repositories read-only at `/app/repo`, and runs with network isolation (`network_mode="none"` by default). Set `test_mode=True` when instantiating `Nova` if you need to bypass Docker during local tests.
- Cleanup: `novasystem cleanup --days N` purges run records older than N days. Temporary clone directories created for remote repositories are cleaned up automatically.

## Project layout
- `novasystem/` — core package (CLI, orchestrator, Docker executor, parser, database, utilities).
- `tests/` — pytest suite covering the CLI, parser, repository handling, database, decision matrix, and utilities.
- `docs/` — architectural and process documentation for the broader NovaSystem work.
- `assets/`, `examples/`, `reports/`, `work_efforts/` — supporting materials and research notes.
- `NovaSystem-Streamlined` and `NovaSystem-Streamlined-backup-*` — archived experiments and UI prototypes; not used by the current CLI package.

## Development
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pytest
```

Consider setting `NOVASYSTEM_DISABLE_FILE_LOG=1` while iterating locally if you do not want log files in your home directory.

## Status and cautions
NovaSystem v0.1.1 is an alpha research tool. Command extraction is heuristic and may miss or misorder steps; always review the proposed commands before letting them run. Although execution happens inside Docker with limited resources and no network by default, you are responsible for auditing commands from untrusted repositories and for validating any installation outcomes.
