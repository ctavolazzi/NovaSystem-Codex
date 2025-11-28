# GitHub Actions Workflows

This directory contains automated CI/CD workflows for NovaSystem-Codex.

## Workflows

### `test.yml` - Continuous Integration Testing

Runs automatically on:
- Pushes to `main`, `develop`, or any `claude/**` branches
- Pull requests to `main` or `develop`

**Jobs:**

1. **test-main-package** - Tests the core NovaSystem package
   - Runs on Python 3.8, 3.9, 3.10, 3.11
   - Executes all tests in `tests/`
   - Uploads test results as artifacts

2. **test-streamlined** - Tests NovaSystem-Streamlined
   - Runs on Python 3.9, 3.10, 3.11
   - Executes tests in `NovaSystem-Streamlined/tests/`
   - Continues on failure (some tests may fail without API keys)

3. **lint** - Code quality checks
   - Runs black (code formatting)
   - Runs isort (import sorting)
   - Runs flake8 (linting)
   - Continues on failure (informational)

## Viewing Results

- Check the "Actions" tab in GitHub to see workflow runs
- Failed tests will be highlighted in PR checks
- Artifacts contain detailed test output

## Local Testing

Before pushing, run tests locally:

```bash
# Main package
python -m pytest tests/ -v

# NovaSystem-Streamlined
cd NovaSystem-Streamlined
python -m pytest tests/ -v

# Code formatting
black --check novasystem/ tests/
isort --check novasystem/ tests/
```
