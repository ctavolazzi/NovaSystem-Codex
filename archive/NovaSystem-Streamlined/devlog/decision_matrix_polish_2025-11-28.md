# Decision Matrix Polish & v0.1.2 Release

**Date:** November 28, 2025
**Release:** v0.1.2
**Tests:** 70/70 passing (100%)

---

## Summary

Polished the decision matrix utility, fixed test failures, tagged v0.1.2 release, and investigated v3 workflow UI status.

---

## Decision Matrix Improvements

### Polish Fixes Applied

| Fix | Before | After |
|-----|--------|-------|
| **Strength/weakness overlap** | Same values shown for both | Hidden when ≤3 criteria |
| **JSON values** | `7.500000000000001` | `7.5` |
| **Close scores** | No indication | "Statistical tie" warning |
| **CLI stdin** | Required `-` argument | Auto-detects piped input |

### Usage Examples

```python
from novasystem.core_utils import make_decision

result = make_decision(
    options=["Option A", "Option B", "Option C"],
    criteria=["Cost", "Quality", "Speed"],
    scores={
        "Option A": [7, 8, 6],
        "Option B": [9, 5, 7],
        "Option C": [6, 9, 8]
    },
    weights=[0.3, 0.5, 0.2]
)

print(result)
print(result.comparison_table())
```

```bash
# CLI usage - now auto-detects stdin
echo '{"options": ["A","B"], "criteria": ["X","Y"], "scores": {"A":[7,8],"B":[9,5]}}' | \
  python3 -m novasystem.core_utils.decision_matrix_cli --json
```

---

## Test Suite Fixes

### CLI Logging Hardening

```python
# Now respects environment variables:
# NOVASYSTEM_DISABLE_FILE_LOG=1  - Disable file logging
# NOVASYSTEM_LOG_PATH=/path      - Custom log location

# Falls back gracefully if log file isn't writable
```

### Subprocess Fix

```python
# Before: subprocess.run(["python", "-m", "pip", ...])  # Fails if python not on PATH
# After:  subprocess.run([sys.executable, "-m", "pip", ...])  # Always works
```

---

## Release v0.1.2

Tagged with full changelog:

```
git tag -a v0.1.2 -m "v0.1.2: Decision Matrix + Stability Improvements

Features:
- Decision Matrix utility with 4 analysis methods
- CLI interface with stdin auto-detection
- Confidence scoring, strengths/weaknesses, explanations
- Statistical tie warnings

Improvements:
- CLI logging hardening (graceful fallback, env toggles)
- Test subprocess fixes (sys.executable)

Quality:
- 70/70 tests passing (100%)
- Decision matrix: 29 dedicated tests"
```

---

## v3 Workflow UI Status

### Current State
- Card-based agent selection: ✅ Working
- Mock workflow execution: ✅ Simulated
- `WorkflowCanvas` (node-based): ⚠️ Built but unused
- Real backend integration: ❌ Not connected

### Infrastructure Ready
- `WorkflowCanvas.tsx` - 370 lines, full node-based canvas
- `WorkflowProcess.py` - Backend with topological sort
- WebSocket support - Already in codebase

### Next Steps
1. Wire `WorkflowCanvas` to workflow page
2. Connect to real `WorkflowProcess` API
3. Add real-time WebSocket updates

---

## Commits

```
86067ba Add missing lib/utils.ts for cn() function
fa5c612 Fix CLI logging permissions and test subprocess calls
7a3957c Polish decision matrix: fix overlap, round JSON, add tie warning, auto-detect stdin
```

---

## Files Modified

- `novasystem/core_utils/decision_matrix.py`
- `novasystem/core_utils/decision_matrix_cli.py`
- `novasystem/cli.py`
- `tests/test_system_validation.py`
- `NovaSystem-Streamlined/novasystem_modern_ui/src/lib/utils.ts`

---

**Status:** Complete ✅







