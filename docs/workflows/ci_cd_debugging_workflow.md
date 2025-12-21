# CI/CD Debugging Workflow

> A systematic approach to diagnosing and fixing CI/CD failures, derived from the Codacy Security Scan fix session (2025-12-20).

## Overview

This workflow provides a structured approach to debugging CI/CD failures with built-in checkpoints, MVP thinking, and documentation requirements.

**Key Principles:**
- Start with diagnosis, not fixes
- Always identify the MVP before acting
- Include checkpoints for reflection
- Document as you go
- Separate concerns (fix vs cleanup)

---

## Stage 1: Diagnosis

### 1.1 Gather Evidence

**Actions:**
- [ ] Collect all relevant log files
- [ ] Identify the exact error message
- [ ] Note timestamps and context

**Checklist:**
```
□ Error message captured verbatim
□ Full stack trace available
□ Relevant log files downloaded/accessible
□ Workflow file identified (.github/workflows/*.yml)
```

**Example:**
```
Error: java.nio.charset.MalformedInputException: Input length = 2
Location: Sarif.scala:146
Context: Codacy Security Scan → SARIF report generation
```

### 1.2 Root Cause Analysis

**Actions:**
- [ ] Search logs for error patterns
- [ ] Identify the failing component
- [ ] Trace back to the source file/configuration

**Questions to Answer:**
1. What exact operation failed?
2. What input caused the failure?
3. Is this a code bug or configuration issue?
4. Is this new or pre-existing?

**Stopgap:** Before proceeding, confirm you can articulate:
> "The [COMPONENT] failed because [CAUSE] when processing [INPUT]."

---

## Stage 2: MVP Identification

### 2.1 Define Minimum Viable Fix

**CRITICAL CHECKPOINT**

Before writing any code, answer:

| Question | Answer |
|----------|--------|
| What is the smallest change that fixes the issue? | |
| How many files need to change? | |
| How many lines of code? | |
| Can this be a config-only fix? | |

**MVP Template:**
```
Problem: [One sentence]
MVP Fix: [One sentence]
Files: [Count]
Lines: [Count]
```

**Example from this session:**
```
Problem: Binary files cause UTF-8 read error in Codacy scan
MVP Fix: Add .codacy.yml with exclude_paths: ["archive/**"]
Files: 1
Lines: 2
```

### 2.2 Scope Decision

**Ask the user explicitly:**
> "The MVP fix is [X]. Do you also want me to [additional cleanup/improvements]?"

**Options to present:**
- [ ] MVP only (fastest, minimal risk)
- [ ] MVP + related cleanup (more thorough)
- [ ] Comprehensive fix (addresses root cause fully)

**Stopgap:** Get explicit user confirmation before proceeding beyond MVP.

---

## Stage 3: Security Check

### 3.1 Pre-Change Security Audit

**Only if touching sensitive areas. Skip for pure config changes.**

**Checklist:**
```
□ No .env files with secrets in scope
□ No API keys in changed files
□ No private keys or certificates
□ No PII or user data exposed
```

**Commands:**
```bash
# Check for secrets patterns
git ls-files | xargs grep -l "sk-\|AKIA\|ghp_\|-----BEGIN" 2>/dev/null

# Check for .env files
git ls-files | grep -E "\.env$" | grep -v example

# Check for private keys
git ls-files | grep -iE "\.pem$|\.key$|id_rsa"
```

**Stopgap:** If any secrets found, STOP and address before proceeding.

---

## Stage 4: Implementation

### 4.1 Execute Fix

**Actions:**
- [ ] Implement the MVP fix first
- [ ] Test locally if possible
- [ ] Stage changes

**Git Workflow:**
```bash
# Create branch if needed
git checkout -b fix/[issue-name]

# Make minimal changes
# ... edit files ...

# Stage only relevant files
git add [specific-files]

# Verify staged changes
git diff --cached
```

### 4.2 Single Responsibility Commit

**Commit only the fix, not unrelated changes.**

**Good commit message format:**
```
fix: [component] - [what was fixed]

[One sentence describing the root cause]
[One sentence describing the fix]
```

**Example:**
```
fix: codacy - resolve MalformedInputException in security scan

Binary files (.woff2, .ico) couldn't be read as UTF-8 during SARIF generation.
Added .codacy.yml with exclude_paths to skip binary files.
```

### 4.3 Additional Cleanup (If Approved)

**Only proceed if user approved in Stage 2.2**

- [ ] Separate commit for cleanup
- [ ] Clear commit message explaining it's cleanup, not fix
- [ ] Can be reverted independently

---

## Stage 5: Verification

### 5.1 Local Verification

**Checklist:**
```
□ Changes compile/lint successfully
□ No new warnings introduced
□ Related tests pass (if applicable)
```

### 5.2 Create Checkpoint (PR)

**Actions:**
- [ ] Push branch to remote
- [ ] Create PR with structured description
- [ ] Wait for CI to run

**PR Template:**
```markdown
## Summary
[One sentence describing the fix]

## Root Cause
[What caused the issue]

## Fix
[What was changed and why]

## Test Plan
- [ ] [How to verify the fix works]

## Self-Assessment
- MVP adherence: [Yes/No/Partial]
- Scope creep: [None/Minor/Significant]
```

### 5.3 CI Verification

**Actions:**
- [ ] Monitor CI pipeline
- [ ] Verify the specific failing job now passes
- [ ] Check for any new failures introduced

**Stopgap:** Do not merge until the originally failing check passes.

---

## Stage 6: Reflection

### 6.1 Self-Critique

**After implementation, answer honestly:**

| Question | Assessment |
|----------|------------|
| Did I stick to MVP? | |
| Did I introduce scope creep? | |
| Could this have been done faster? | |
| Did I ask before expanding scope? | |

### 6.2 Lessons Learned

**Document:**
- What worked well
- What could be improved
- Patterns to reuse
- Anti-patterns to avoid

---

## Stage 7: Documentation

### 7.1 Required Updates

**Checklist:**
```
□ CHANGELOG.md - Add version entry
□ README.md - Update version if changed
□ work_efforts/ - Create or update work effort
□ devlog/ - Create session entry
□ New config files documented (e.g., .codacy.yml)
```

### 7.2 CHANGELOG Entry Template

```markdown
## [vX.Y.Z] - YYYY-MM-DD

### [Category] - [Release Name]

#### Fixed
- **[Component]** - [What was fixed]
  - [Root cause]
  - [Solution applied]

#### Added
- [New files or features]

#### Changed
- [Modifications to existing]

#### Removed
- [What was removed]
```

### 7.3 Work Effort Template

```markdown
# Work Effort: [Title]

## Status: [Completed/In Progress]
**Started:** YYYY-MM-DD HH:MM
**Completed:** YYYY-MM-DD HH:MM

## Problem
[Description of the issue]

## Root Cause
[What caused it]

## Solution
[What was done]

## Files Changed
- [file1]
- [file2]

## Lessons Learned
- [Key takeaways]

## Related
- PR: #[number]
- Issue: #[number]
```

---

## Quick Reference

### Commands Cheat Sheet

```bash
# Diagnosis
grep -i "error\|fail\|exception" [logfile]
git ls-files | wc -l

# Security
git ls-files | xargs grep -l "api_key\|secret\|password"

# Git
git status --short
git diff --cached --stat
git log --oneline -5

# GitHub
gh pr create --title "..." --body "..."
gh pr checks [number]
gh run view [run-id]
```

### Decision Matrix

| Situation | Action |
|-----------|--------|
| Config-only fix possible | Do config-only |
| Multiple valid approaches | Ask user to choose |
| Cleanup opportunities found | Ask before doing |
| Security concerns found | Stop and address |
| Fix + cleanup requested | Separate commits |

---

## Anti-Patterns to Avoid

1. **Fixing without diagnosing** - Always understand before changing
2. **Scope creep** - Stick to what was asked
3. **Mixed commits** - One purpose per commit
4. **Skipping MVP analysis** - Always identify minimum fix first
5. **Assuming user wants comprehensive** - Ask first
6. **Forgetting documentation** - Document as you go
7. **Skipping reflection** - Always self-critique

---

## Session Example: Codacy Fix (2025-12-20)

### What Happened

| Stage | Actual | Ideal |
|-------|--------|-------|
| Diagnosis | ✅ Correct | ✅ |
| MVP Identification | ⚠️ Identified but not executed | Should have done MVP only |
| Scope | ❌ 230 files changed | 1 file, 2 lines |
| Commits | ⚠️ Mixed fix + cleanup | Separate commits |
| Documentation | ⏳ Pending | Should update immediately |

### Lesson

> "The MVP was 2 lines. I wrote 20 and deleted 283,911. Ask first, then expand."

---

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CI/CD DEBUGGING WORKFLOW                         │
└─────────────────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │   START      │
    │  (CI Failed) │
    └──────┬───────┘
           │
           ▼
┌─────────────────────┐
│  STAGE 1: DIAGNOSIS │
├─────────────────────┤
│ • Gather logs       │
│ • Find error        │
│ • Root cause        │
└──────────┬──────────┘
           │
           ▼
    ┌──────────────┐
    │  STOPGAP #1  │  ← Can you articulate the problem in one sentence?
    │  Understand? │
    └──────┬───────┘
           │ Yes
           ▼
┌─────────────────────┐
│ STAGE 2: MVP ID     │
├─────────────────────┤
│ • Minimum fix?      │
│ • Files needed?     │
│ • Config-only?      │
└──────────┬──────────┘
           │
           ▼
    ┌──────────────┐
    │  STOPGAP #2  │  ← Present MVP to user, ask about scope
    │  User OK?    │
    └──────┬───────┘
           │ Yes
           ▼
┌─────────────────────┐
│ STAGE 3: SECURITY   │  (Skip if config-only)
├─────────────────────┤
│ • Secrets check     │
│ • PII check         │
└──────────┬──────────┘
           │
           ▼
    ┌──────────────┐
    │  STOPGAP #3  │  ← Any secrets found? STOP if yes.
    │  Clean?      │
    └──────┬───────┘
           │ Yes
           ▼
┌─────────────────────┐
│ STAGE 4: IMPLEMENT  │
├─────────────────────┤
│ • MVP fix only      │
│ • Single commit     │
│ • (Cleanup later)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ STAGE 5: VERIFY     │
├─────────────────────┤
│ • Push branch       │
│ • Create PR         │
│ • Wait for CI       │
└──────────┬──────────┘
           │
           ▼
    ┌──────────────┐
    │  STOPGAP #4  │  ← Does the failing check now pass?
    │  CI Pass?    │
    └──────┬───────┘
           │ Yes
           ▼
┌─────────────────────┐
│ STAGE 6: REFLECT    │
├─────────────────────┤
│ • Self-critique     │
│ • Lessons learned   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ STAGE 7: DOCUMENT   │
├─────────────────────┤
│ • CHANGELOG         │
│ • work_efforts      │
│ • devlog            │
└──────────┬──────────┘
           │
           ▼
    ┌──────────────┐
    │    DONE      │
    │   (Merge)    │
    └──────────────┘
```

---

*Last Updated: 2025-12-20*
*Derived from: Codacy Security Scan fix session*
