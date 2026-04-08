---
name: add-feature
description: Add a new feature to the Sanskrit parser. Use when implementing new functionality that doesn't involve adding sutra rules or vibhakti tests.
argument-hint: "[feature-description]"
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, Todowrite
---

# Add Feature to Sanskrit Parser

Use this skill when implementing new functionality in the Sanskrit parser that doesn't involve adding Paninian sutra rules or generating vibhakti test tables.

## When to Use

- Adding new utility functions or helper methods
- Implementing new data structures or classes
- Adding new CLI commands or interface features
- Refactoring existing code for better organization
- Adding new test infrastructure or test utilities
- Implementing features that span multiple modules

## Implementation Steps

### Step 1 — Understand the Request
1. Clearly define what feature needs to be implemented
2. Identify which modules or files will be affected
3. Determine if this requires changes to public interfaces

### Step 2 — Inspect Existing Implementation
1. Read relevant files to understand current implementation
2. Look for similar patterns or existing functionality to reuse
3. Check for any existing tests that might need updating

### Step 3 — Plan the Changes
1. Break down the feature into smallest coherent changes
2. Identify the minimum set of files that need modification
3. Plan how to maintain backward compatibility

### Step 4 — Implement the Feature
1. Make minimal, focused changes to implement the feature
2. Follow existing code patterns and conventions
3. Keep implementation, testing, and debugging concerns separate

### Step 5 — Add Tests
1. Add tests covering the new behavior
2. Prefer focused tests over broad coverage
3. Ensure tests fail before implementation and pass after

### Step 6 — Verify Implementation
1. Run the narrowest relevant tests first
2. Broaden test scope if needed
3. Debug from evidence if failures occur

## Codebase Context

| File/Directory | Purpose |
|----------------|---------|
| `sanskrit_parser/` | Main library code |
| `sanskrit_parser/generator/` | Sanskrit generator implementation |
| `sanskrit_parser/generator/sutras_antaranga.yaml` | Sutra rules (use gen-sutra-rule skill instead) |
| `sanskrit_parser/generator/test/` | Generator tests |
| `sanskrit_parser/generator/test/vibhaktis_list.py` | Vibhakti test tables (use gen-vibhakti-test skill instead) |

## Related Skills

- For adding Paninian sutra rules: Use `gen-sutra-rule` skill
- For generating vibhakti test entries: Use `gen-vibhakti-test` skill
- For debugging unexpected behavior: Use `gen-debug` skill