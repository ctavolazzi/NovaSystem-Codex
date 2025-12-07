# NovaSystem Archive

This directory contains archived implementations that were consolidated into the unified `novasystem` package (v3.0.0).

## Contents

| Directory | Original Version | Description |
|-----------|-----------------|-------------|
| `NovaSystem-Streamlined/` | v2.0.0 | Full multi-agent framework with Web/Gradio UI |
| `novasystem-v0.1.1-cli/` | v0.1.1 | Repository installer, Docker, Decision Matrix |
| `nova-mvp/` | v0.1.0 | FastAPI backend with agent orchestration |
| `dev-experimental/` | N/A | Experimental versions (NS-bytesize, NS-core, etc.) |
| `streamlined-backup-20250928/` | N/A | Historical backup |

## Why Archived?

These implementations were consolidated to solve:
1. **Namespace conflicts** - Multiple packages named "novasystem"
2. **Feature fragmentation** - Unique features spread across implementations
3. **Maintenance burden** - 4+ codebases to maintain

## What Was Preserved?

The following unique features were merged into the main package:

### From novasystem-v0.1.1-cli
- Decision Matrix framework (`novasystem.tools.decision_matrix`)
- Docker executor (`novasystem.tools.docker`)
- Repository manager (`novasystem.tools.repository`)
- Documentation parser (`novasystem.tools.parser`)

### From nova-mvp
- LocalVectorStore for zero-cost RAG (`novasystem.core.vector_store`)
- Pricing module (`novasystem.core.pricing`)
- Usage tracking (`novasystem.core.usage`)

### From NovaSystem-Streamlined
- Full agent system (`novasystem.core.agents`)
- Process orchestration (`novasystem.core.process`)
- Web and Gradio UIs (`novasystem.ui`)
- Session management (`novasystem.session`)
- MCP integration (`novasystem.mcp`)

## Using Archived Code

If you need to reference the original implementations:

```python
# These are READ-ONLY references
# Import from archive/ for historical reference only
# Use the main novasystem package for actual functionality
```

## Date Archived
2025-12-07

## Archived By
Consolidation effort to create unified CLI-first NovaSystem v3.0.0
