# NovaSystem Architecture Analysis

**Version:** v0.3.4 ("Clean Sleepy Wizard")
**Analysis Date:** 2025-12-21
**Status:** ALPHA (Experimental Research Tool)

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Architecture Overview](#system-architecture-overview)
3. [Core Components Deep Dive](#core-components-deep-dive)
4. [Data Flow & Interactions](#data-flow--interactions)
5. [Critical Issues & Risks](#critical-issues--risks)
6. [Test Coverage Analysis](#test-coverage-analysis)
7. [Technical Debt Inventory](#technical-debt-inventory)
8. [High-Impact Improvement Recommendations](#high-impact-improvement-recommendations)

---

## Executive Summary

NovaSystem is a multi-agent AI problem-solving framework that orchestrates multiple AI agents through the "Nova Process" - a three-phase methodology (UNPACK → ANALYZE → SYNTHESIZE). The system is CLI-first with support for REST API, WebSocket, and Gradio interfaces.

### Key Metrics

| Metric | Value |
|--------|-------|
| Total Source Lines | ~22,618 |
| Total Test Lines | ~6,895 |
| Test-to-Code Ratio | ~30% |
| Files > 500 lines | 17 |
| Critical Issues | 12 |
| High Priority Issues | 18 |
| Untested Modules | ~40% |

### Overall Risk Assessment: MEDIUM-HIGH

The system demonstrates good architectural patterns but contains critical issues in:
- Data consistency (memory index divergence)
- Thread safety (race conditions in vector store)
- Error handling (unhandled exceptions, silent failures)
- Test coverage (40% of code untested)

---

## System Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACES                               │
├─────────────┬─────────────┬──────────────┬─────────────────────────┤
│   CLI       │   REST API  │  WebSocket   │   Gradio/Web UI         │
│ (Typer)     │  (FastAPI)  │ (Real-time)  │   (Flask/Gradio)        │
└──────┬──────┴──────┬──────┴──────┬───────┴──────────┬──────────────┘
       │             │             │                  │
       ▼             ▼             ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      CORE ORCHESTRATION                              │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    NovaProcess                               │   │
│  │  ┌─────────┐    ┌─────────┐    ┌──────────────────────┐    │   │
│  │  │ UNPACK  │───▶│ ANALYZE │───▶│ SYNTHESIZE           │    │   │
│  │  │ Phase 1 │    │ Phase 2 │    │ Phase 3              │    │   │
│  │  └─────────┘    │(Iterate)│    └──────────────────────┘    │   │
│  │                 └─────────┘                                 │   │
│  └─────────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────────┘
                             │
       ┌─────────────────────┼─────────────────────┐
       ▼                     ▼                     ▼
┌─────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AGENTS    │    │     MEMORY      │    │   LLM SERVICE   │
│ ┌─────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │   DCE   │ │    │ │Short-Term   │ │    │ │  OpenAI     │ │
│ ├─────────┤ │    │ │(deque:10)   │ │    │ ├─────────────┤ │
│ │   CAE   │ │    │ ├─────────────┤ │    │ │  Anthropic  │ │
│ ├─────────┤ │    │ │Long-Term    │ │    │ ├─────────────┤ │
│ │ Domain  │ │    │ │(deque:100)  │ │    │ │  Gemini     │ │
│ │ Experts │ │    │ ├─────────────┤ │    │ ├─────────────┤ │
│ └─────────┘ │    │ │VectorStore  │ │    │ │  Ollama     │ │
└─────────────┘    │ │(JSON file)  │ │    │ └─────────────┘ │
                   │ └─────────────┘ │    └─────────────────┘
                   └─────────────────┘
```

### Directory Structure

```
novasystem/
├── cli/                 # CLI Interface (Typer)
│   ├── main.py          # 1,188 lines - Command definitions
│   └── session_cli.py   # 149 lines - Session management
├── core/                # Core Systems
│   ├── agents.py        # 383 lines - DCE, CAE, DomainExpert
│   ├── process.py       # 292 lines - NovaProcess orchestrator
│   ├── memory.py        # 221 lines - MemoryManager
│   ├── vector_store.py  # 446 lines - LocalVectorStore (RAG)
│   ├── workflow.py      # 191 lines - Workflow engine
│   ├── pricing.py       # 85 lines - Cost estimation
│   └── usage.py         # 352 lines - Usage tracking
├── tools/               # Utility Tools
│   ├── docker.py        # 606 lines - Docker executor
│   ├── repository.py    # Repository management
│   ├── parser.py        # 588 lines - Doc parser
│   ├── technical_debt.py# Debt tracking
│   └── decision_matrix/ # Decision analysis
├── utils/               # Services
│   ├── llm_service.py   # 528 lines - Multi-provider LLM
│   ├── rate_limiter.py  # 504 lines - Rate limiting
│   ├── vision_service.py# 633 lines - Vision/image
│   └── document_service.py # 668 lines - Document processing
├── api/                 # REST API
│   ├── rest.py          # 514 lines - FastAPI endpoints
│   └── websocket.py     # WebSocket manager
├── ui/                  # User Interfaces
│   ├── web.py           # 462 lines - Flask interface
│   └── gradio.py        # 731 lines - Gradio interface
├── config/              # Configuration
│   ├── settings.py      # App settings
│   └── models.py        # Model configurations
├── database/            # Database Layer
│   └── models.py        # SQLAlchemy ORM
└── session/             # Session Management
    └── manager.py       # Session persistence
```

---

## Core Components Deep Dive

### 1. Agent System (`novasystem/core/agents.py`)

**Architecture:**
```
BaseAgent (abstract)
  ├── DCEAgent (Discussion Continuity Expert)
  ├── CAEAgent (Critical Analysis Expert)
  └── DomainExpert (specialized domain agent)
AgentFactory (static factory pattern)
```

**Key Classes:**

| Class | Purpose | Lines |
|-------|---------|-------|
| `BaseAgent` | Abstract base with LLM integration | 1-160 |
| `DCEAgent` | Coordinates flow, synthesizes insights | 161-230 |
| `CAEAgent` | Critical evaluation, identifies risks | 231-270 |
| `DomainExpert` | Domain-specific expertise | 271-310 |
| `AgentFactory` | Factory for agent creation | 311-383 |

**Key Methods:**

```python
class BaseAgent:
    async def process(input_text: str) -> str     # Main processing
    async def process_stream(input_text: str)     # Streaming variant
    async def _call_llm(prompt: str) -> str       # LLM invocation
    def add_to_history(role: str, content: str)   # Conversation tracking
```

**Issues:**
- Line 145-147: Conversation history race condition in concurrent execution
- Line 116-118: Model fallback doesn't update `self.model`
- Line 172: Unsafe string parsing for agent colors
- Line 94-96: Fixed 5-message conversation window (may lose context)

---

### 2. NovaProcess Orchestrator (`novasystem/core/process.py`)

**Three-Phase Architecture:**

```
Phase 1: UNPACK (_problem_unpacking_phase)
  ├─ Store problem in memory
  ├─ Domain expert analysis (parallel)
  ├─ DCE synthesis of insights
  └─ CAE critical evaluation

Phase 2: ITERATE (_iteration_phase) [max 5 iterations]
  ├─ Get relevant context from memory
  ├─ Domain expert solutions (parallel)
  ├─ DCE coordination
  ├─ CAE evaluation
  └─ Convergence check

Phase 3: SYNTHESIZE (_final_synthesis_phase)
  ├─ Get all context from memory
  ├─ DCE final synthesis
  ├─ CAE final validation
  └─ Return complete result
```

**Key Methods:**

```python
class NovaProcess:
    async def solve_problem(problem, max_iterations, stream, session_id)
    async def _solve_sync(problem, max_iterations) -> Dict
    async def _solve_streaming(problem, max_iterations) -> AsyncGenerator
    async def _problem_unpacking_phase() -> Dict
    async def _iteration_phase(iteration: int) -> Dict
    async def _final_synthesis_phase() -> Dict
    def _check_convergence(result: Dict) -> bool
```

**Issues:**
- Lines 192, 222, 245: `json.dumps()` without error handling (crash on non-serializable)
- Lines 263-266: Brittle convergence detection (substring matching)
- Lines 241-245: Uncontrolled context size (could exceed LLM token limit)
- Lines 68-71: Process state not thread-safe

---

### 3. Memory System (`novasystem/core/memory.py`)

**Dual-Tier Architecture:**

```
MemoryManager
├── short_term_memory: deque(maxlen=10)  # Recent context
├── long_term_memory: deque(maxlen=100)  # Important items
└── context_index: Dict[key → entry]      # Quick lookup
```

**Key Methods:**

```python
class MemoryManager:
    async def store_context(key, data, memory_type)
    async def get_context(key) -> Optional[Any]
    async def get_relevant_context(query, limit) -> str
    async def get_all_context() -> Dict
    async def compress_memory()
    def _is_relevant(data, query) -> bool
    def _is_important(entry) -> bool
```

**CRITICAL BUG - Context Index Divergence (Lines 32-58):**

When deque reaches maxlen, oldest item is auto-discarded by deque but `context_index` retains stale reference:

```python
# BUG: After 10 items, deque auto-removes oldest but index keeps reference
self.short_term_memory.append(memory_entry)  # Deque auto-removes oldest
self.context_index[key] = memory_entry       # Index never cleaned!
```

**Impact:** Stale data returned, memory leaks, inconsistent state.

---

### 4. Vector Store (`novasystem/core/vector_store.py`)

**Architecture:**

```
Embedder (abstract)
  └─ SimpleEmbedder (hash-based, zero API cost)

VectorStore (abstract)
  └─ LocalVectorStore (JSON-backed)
    ├── embedding: SimpleEmbedder (256-dim)
    ├── documents: Dict[id → MemoryDocument]
    ├── lock: threading.Lock
    └── persistence: .nova_memory.json
```

**Key Methods:**

```python
class LocalVectorStore:
    def add(text, tags, metadata) -> str
    def search(query, limit, min_score, tags) -> List[MemoryDocument]
    def embed_text(text) -> List[float]
    def _save_locked()
    def _load()
```

**Issues:**
- Lines 102-124: Hash collision in embeddings (~40-50% collision rate)
- Lines 369-408: Race condition in atomic writes (read-modify-write gap)
- Lines 411-420: Global singleton not thread-safe
- Line 386: Lock not held during merge operation

---

### 5. LLM Service (`novasystem/utils/llm_service.py`)

**Multi-Provider Architecture:**

```
LLMService
├── openai_client: AsyncOpenAI
├── anthropic_client: AsyncAnthropic
├── gemini_client: AsyncOpenAI (compatible)
├── ollama_client: AsyncClient
├── metrics_collector
├── model_cache
└── session_manager
```

**Key Methods:**

```python
class LLMService:
    async def get_completion(messages, model, temperature, max_tokens) -> str
    async def stream_completion(messages, model, temperature) -> AsyncGenerator
    def get_available_models() -> List[str]
    def is_model_available(model) -> bool
    def get_best_model_for_task(task_type, available, prioritize_speed)
```

**Issues:**
- Lines 283-285: Exception swallowing (returns error string instead of raising)
- Lines 489, 510: Loose token counting (word count ≠ tokens)
- Lines 450-481: Anthropic message conversion loses context for multi-turn
- Line 497-527: Session recording not thread-safe

---

## Data Flow & Interactions

### Problem Solving Flow

```
User Input: "How do we scale our API?"
        │
        ▼
┌─────────────────────────────────────┐
│          CLI/API/UI                 │
│ Receives problem, creates session   │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│         NovaProcess                 │
│ ┌─────────────────────────────────┐ │
│ │ 1. store_context("problem", p)  │ │
│ │                                 │ │
│ │ 2. UNPACK PHASE                 │ │
│ │    ├─ expert_1.process(p)       │ │◄──┐
│ │    ├─ expert_2.process(p)       │ │   │ asyncio.gather()
│ │    └─ expert_n.process(p)       │ │◄──┘
│ │    ├─ dce.process(insights)     │ │
│ │    └─ cae.process(synthesis)    │ │
│ │                                 │ │
│ │ 3. ITERATE PHASE (x5 max)       │ │
│ │    ├─ get_relevant_context()    │ │
│ │    ├─ experts propose solutions │ │
│ │    ├─ dce coordinates           │ │
│ │    ├─ cae evaluates             │ │
│ │    └─ check_convergence()       │ │
│ │                                 │ │
│ │ 4. SYNTHESIZE PHASE             │ │
│ │    ├─ get_all_context()         │ │
│ │    ├─ dce final synthesis       │ │
│ │    └─ cae final validation      │ │
│ └─────────────────────────────────┘ │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│        Final Result                 │
│ {                                   │
│   "final_synthesis": "...",         │
│   "final_validation": "...",        │
│   "total_iterations": 3             │
│ }                                   │
└─────────────────────────────────────┘
```

### Memory Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     MEMORY MANAGER                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  store_context("problem", data)                                 │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────────┐    ┌──────────────────────────────┐      │
│  │ short_term_memory│    │ context_index                │      │
│  │ deque(maxlen=10) │    │ {"problem": {data, ts}}      │      │
│  │ [entry_1, ...]   │    │                              │      │
│  └──────────────────┘    └──────────────────────────────┘      │
│         │                                                       │
│         │ (when full, oldest auto-removed)                      │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────────┐                                          │
│  │ compress_memory()│ → moves "important" to long_term         │
│  └──────────────────┘                                          │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────────┐                                          │
│  │ long_term_memory │                                          │
│  │ deque(maxlen=100)│                                          │
│  └──────────────────┘                                          │
│                                                                 │
│  get_relevant_context("query")                                  │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────────┐                                          │
│  │ _is_relevant()   │ → substring matching (weak)              │
│  │ search both tiers│                                          │
│  └──────────────────┘                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Critical Issues & Risks

### Severity Definitions

| Level | Definition |
|-------|------------|
| **CRITICAL** | Data loss, corruption, or security vulnerability |
| **HIGH** | Significant functionality broken, production blocker |
| **MEDIUM** | Degraded performance or reliability |
| **LOW** | Code quality, minor issues |

### Critical Issues (12)

| # | Component | Issue | Location | Impact |
|---|-----------|-------|----------|--------|
| 1 | Memory | Context index divergence | memory.py:32-58 | Data corruption, stale returns |
| 2 | Memory | Dangerous compression | memory.py:151-168 | O(n²), silent data loss |
| 3 | VectorStore | Hash collision (~50%) | vector_store.py:102-124 | Poor similarity search |
| 4 | VectorStore | Race condition saves | vector_store.py:369-408 | Lost writes |
| 5 | VectorStore | Lock scope issue | vector_store.py:386 | Thread safety broken |
| 6 | Process | JSON serialization | process.py:192,222,245 | Crash on non-serializable |
| 7 | Agents | History race condition | agents.py:145-147 | Corrupted conversation |
| 8 | LLMService | Exception swallowing | llm_service.py:283-285 | Hidden errors |
| 9 | REST API | In-memory sessions | rest.py:50-52 | Data loss on restart |
| 10 | Tools | eval() usage | tools_service.py:530 | Code injection risk |
| 11 | Docker | Weak command validation | docker.py:430-457 | Command bypass |
| 12 | Interactive | Bare except clauses | interactive.py:100,335,462... | Suppressed errors |

### High Priority Issues (18)

| # | Component | Issue | Location |
|---|-----------|-------|----------|
| 1 | Process | Brittle convergence | process.py:263-266 |
| 2 | Process | Uncontrolled context | process.py:241-245 |
| 3 | Agents | Model fallback bug | agents.py:116-118 |
| 4 | Agents | Streaming output pollution | agents.py:174-191 |
| 5 | Memory | Weak relevance detection | memory.py:132-149 |
| 6 | VectorStore | Dimension mismatch | vector_store.py:330-345 |
| 7 | VectorStore | Singleton race | vector_store.py:411-420 |
| 8 | CLI | Global state unsafe | cli/main.py:133 |
| 9 | CLI | Multiple asyncio.run() | cli/main.py:354,375,497... |
| 10 | REST API | CORS misconfiguration | rest.py:211-218 |
| 11 | Web UI | Threading issues | web.py:373-377 |
| 12 | Gradio | Blocking asyncio.run() | gradio.py:163,306... |
| 13 | LLMService | Loose token counting | llm_service.py:489,510 |
| 14 | Repository | Path traversal risk | repository.py:216-223 |
| 15 | Repository | No rate limiting | repository.py:112-134 |
| 16 | Nova Tool | No rollback on failure | nova.py:160-206 |
| 17 | Parser | Regex fragility | parser.py:158-159 |
| 18 | WebSocket | No authentication | websocket.py |

---

## Test Coverage Analysis

### Coverage by Module

| Module | Lines | Tests | Coverage | Status |
|--------|-------|-------|----------|--------|
| core/memory.py | 221 | 227 | ~95% | ✅ Excellent |
| core/vector_store.py | 446 | 346 | ~85% | ✅ Good |
| tools/decision_matrix.py | 808 | 431 | ~80% | ✅ Good |
| core/agents.py | 383 | 385 | ~75% | ✅ Good |
| tools/parser.py | 588 | 50 | ~30% | ⚠️ Partial |
| cli/main.py | 1,188 | minimal | ~5% | ❌ Critical gap |
| **utils/llm_service.py** | **528** | **0** | **0%** | ❌ **Untested** |
| **utils/rate_limiter.py** | **504** | **0** | **0%** | ❌ **Untested** |
| **api/rest.py** | **514** | **0** | **0%** | ❌ **Untested** |
| **utils/vision_service.py** | **633** | **0** | **0%** | ❌ **Untested** |
| **utils/document_service.py** | **668** | **0** | **0%** | ❌ **Untested** |
| ui/web.py | 462 | 0 | 0% | ❌ Untested |
| ui/gradio.py | 731 | 0 | 0% | ❌ Untested |

### Critical Untested Paths

1. **LLM Provider Fallback** (528 lines)
   - API key validation
   - Provider switching logic
   - Streaming implementation
   - Error recovery

2. **Rate Limiter** (504 lines)
   - RPM/TPM/RPD enforcement
   - Exponential backoff
   - Batch processing
   - Queue overflow

3. **REST API** (514 lines)
   - Session lifecycle
   - Request validation
   - WebSocket upgrade
   - Background tasks

4. **NovaProcess Convergence** (292 lines)
   - Iteration termination
   - State transitions
   - Memory consistency

---

## Technical Debt Inventory

### Code Smells Summary

| Category | Count | Severity |
|----------|-------|----------|
| Bare `except:` clauses | 7 | HIGH |
| Long methods (>50 lines) | 11 | MEDIUM |
| Oversized files (>500 lines) | 17 | MEDIUM |
| Deep nesting (>6 levels) | 2 | MEDIUM |
| Missing type hints | 12+ | LOW |
| Unused imports | 9 | LOW |
| Missing docstrings | 11 | LOW |
| Excessive print statements | 291 | MEDIUM |
| Generic exception handling | 20+ | MEDIUM |
| Global mutable state | 8+ | MEDIUM |

### Top Offenders by File Size

| File | Lines | Should Be |
|------|-------|-----------|
| cli/main.py | 1,188 | Split into submodules |
| interactive.py | 851 | Split UI/logic |
| decision_matrix.py | 808 | OK (single purpose) |
| ui/gradio.py | 731 | Split components |
| domain/pipeline.py | 683 | Extract strategies |

### Deprecated/Legacy Code

- `tools/legacy_database.py` (504 lines) - Should be migrated
- `database/__init__.py` - Wildcard imports (`from .models import *`)

---

## High-Impact Improvement Recommendations

Based on the comprehensive analysis, here are the **4 highest-impact improvements** that would significantly improve the codebase:

### 1. Fix Memory Index Divergence (CRITICAL - Data Integrity)

**Problem:** When `short_term_memory` deque reaches maxlen and auto-removes oldest item, `context_index` retains stale reference, causing data corruption.

**Location:** `novasystem/core/memory.py:32-58`

**Current Code:**
```python
self.short_term_memory.append(memory_entry)  # Auto-removes oldest
self.context_index[key] = memory_entry       # Never cleaned!
```

**Fix:**
```python
async def store_context(self, key: str, data: Any, memory_type: str = "short_term") -> None:
    target = self.short_term_memory if memory_type == "short_term" else self.long_term_memory

    # Clean index before adding if deque is full
    if len(target) >= target.maxlen:
        oldest = target[0]
        oldest_key = oldest.get("key")
        if oldest_key in self.context_index:
            del self.context_index[oldest_key]

    memory_entry = {...}
    target.append(memory_entry)
    self.context_index[key] = memory_entry
```

**Impact:**
- Fixes silent data corruption
- Prevents memory leaks
- Ensures consistent state

**Effort:** 2-4 hours

---

### 2. Add LLM Service Unit Tests (CRITICAL - Reliability)

**Problem:** The most critical component (LLMService, 528 lines) has 0% test coverage. All LLM calls go through this module.

**Location:** `novasystem/utils/llm_service.py`

**What to Test:**
```python
# test_llm_service.py (new file)

class TestLLMService:
    async def test_provider_initialization()
    async def test_model_availability_check()
    async def test_openai_completion()
    async def test_anthropic_completion()
    async def test_gemini_completion()
    async def test_ollama_completion()
    async def test_fallback_when_model_unavailable()
    async def test_streaming_completion()
    async def test_error_handling_on_api_failure()
    async def test_message_format_conversion()
    async def test_token_counting_accuracy()
    async def test_session_recording()
```

**Impact:**
- Catches provider integration bugs before production
- Validates fallback logic works correctly
- Ensures error handling is robust

**Effort:** 16-24 hours

---

### 3. Fix Convergence Detection Logic (HIGH - Correctness)

**Problem:** Current convergence detection uses naive substring matching that can produce false positives/negatives.

**Location:** `novasystem/core/process.py:263-266`

**Current Code:**
```python
def _check_convergence(self, iteration_result: Dict[str, Any]) -> bool:
    cae_evaluation = iteration_result.get("cae_evaluation", "").lower()
    return any(indicator in cae_evaluation for indicator in CONVERGENCE_INDICATORS)
```

**Problem Examples:**
- "The solution is **not** complete" → matches "solution is complete" → FALSE POSITIVE
- "While the solution is complete in structure, further improvements needed" → matches → FALSE POSITIVE

**Fix:**
```python
CONVERGENCE_INDICATORS = ["solution is complete", "ready for implementation", "converged"]
NEGATIVE_INDICATORS = ["needs work", "incomplete", "improvements needed", "not ready"]

def _check_convergence(self, iteration_result: Dict[str, Any]) -> bool:
    cae_evaluation = iteration_result.get("cae_evaluation", "").lower()

    # Negative indicators override positive
    if any(neg in cae_evaluation for neg in NEGATIVE_INDICATORS):
        return False

    # Require at least one positive indicator
    positive_count = sum(1 for pos in CONVERGENCE_INDICATORS if pos in cae_evaluation)

    # Also check expert consensus
    expert_solutions = iteration_result.get("expert_solutions", {})
    all_experts_contributed = len(expert_solutions) == len(self.domain_experts)

    return positive_count >= 1 and all_experts_contributed
```

**Impact:**
- Prevents premature termination (false positives)
- Prevents unnecessary iterations (false negatives)
- Improves solution quality

**Effort:** 4-8 hours

---

### 4. Consolidate Async Patterns (MEDIUM - Stability)

**Problem:** Multiple `asyncio.run()` calls in CLI create/destroy event loops repeatedly, causing inefficiency and potential race conditions. Also, Gradio/Web UI block with synchronous asyncio.run().

**Locations:**
- `cli/main.py:354, 375, 497, 586, 602...` (9+ occurrences)
- `ui/gradio.py:163, 306...`
- `ui/web.py:373-377`

**Current Pattern:**
```python
# Called multiple times in same command
asyncio.run(llm.get_completion(messages))
asyncio.run(stream())  # Creates another event loop!
```

**Fix - Create Async Runner Utility:**
```python
# novasystem/utils/async_runner.py (new file)

import asyncio
from typing import Coroutine, TypeVar
import threading

T = TypeVar('T')
_loop_lock = threading.Lock()
_loop: asyncio.AbstractEventLoop = None

def get_event_loop() -> asyncio.AbstractEventLoop:
    """Get or create a singleton event loop."""
    global _loop
    if _loop is None or _loop.is_closed():
        with _loop_lock:
            if _loop is None or _loop.is_closed():
                _loop = asyncio.new_event_loop()
    return _loop

def run_async(coro: Coroutine[Any, Any, T]) -> T:
    """Run coroutine in the singleton event loop."""
    loop = get_event_loop()
    if loop.is_running():
        # Already in async context, use nest_asyncio or thread pool
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as pool:
            future = pool.submit(asyncio.run, coro)
            return future.result(timeout=300)
    return loop.run_until_complete(coro)
```

**Then update CLI:**
```python
from novasystem.utils.async_runner import run_async

# Replace: asyncio.run(llm.get_completion(messages))
# With:
response = run_async(llm.get_completion(messages))
```

**Impact:**
- Single event loop per session
- No race conditions from multiple loops
- Better resource management
- Works in both sync and async contexts

**Effort:** 8-16 hours

---

## Summary: Improvement Roadmap

| Priority | Improvement | Impact | Effort | Risk Reduction |
|----------|-------------|--------|--------|----------------|
| 1 | Fix Memory Index Divergence | Data integrity | 2-4h | CRITICAL |
| 2 | Add LLM Service Tests | Reliability | 16-24h | CRITICAL |
| 3 | Fix Convergence Detection | Correctness | 4-8h | HIGH |
| 4 | Consolidate Async Patterns | Stability | 8-16h | MEDIUM |

**Total Estimated Effort:** 30-52 hours

**Expected Outcomes:**
- Eliminate data corruption bugs
- 70%+ test coverage on critical paths
- Correct convergence behavior
- Stable async execution across all interfaces

---

## Appendix: Quick Reference

### Key Files by Purpose

| Purpose | File |
|---------|------|
| CLI Entry | `cli/main.py` |
| Process Orchestration | `core/process.py` |
| Agent Definitions | `core/agents.py` |
| Memory Management | `core/memory.py` |
| Vector Search | `core/vector_store.py` |
| LLM Integration | `utils/llm_service.py` |
| REST API | `api/rest.py` |
| Configuration | `config/settings.py` |

### Key Commands

```bash
# CLI
nova solve "problem"
nova ask "question"
nova chat
nova status

# Development
pytest
pytest --cov=novasystem
pip install -e ".[dev]"
```

---

*This document should be updated when significant changes are made to the architecture.*
