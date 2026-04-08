---
name: debug
description: Debug unexpected behavior in the Sanskrit parser. Use when a prakriya produces the wrong form, a rule fires unexpectedly, or a rule fails to fire when expected.
argument-hint: "[debug-description]"
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Debug Sanskrit Parser

Use this skill when debugging unexpected behavior in the Sanskrit parser, such as incorrect output, unexpected rule firing, or rules failing to fire.

## When to Use

- A prakriya produces the wrong form
- A rule fires when it shouldn't
- A rule fails to fire when it should
- Unexpected interactions between rules
- Test failures that need investigation

## Debugging Approach

### Step 1 — Reproduce the Issue
1. Create a minimal test case that reproduces the problem
2. Use the exact input that shows the incorrect behavior
3. Capture the actual vs expected output

### Step 2 — Trace the Execution
1. Enable debugging/tracing if available
2. Trace which rules are fired and in what order
3. Examine the state at each step of the prakriya

### Step 3 — Investigate Rule Conditions
1. Check the conditions of suspected rules
2. Verify if condition expressions evaluate as expected
3. Look for conflicts with other rules (overrides, priority)

### Step 4 — Examine Rule Implementation
1. Check the actual YAML rule definition
2. Verify helper functions work correctly
3. Look for typos or incorrect SLP1 encoding

### Step 5 — Fix and Verify
1. Make minimal changes to fix the root cause
2. Ensure the fix doesn't break other functionality
3. Add tests to prevent regression

## Codebase Context

| File/Directory | Purpose |
|----------------|---------|
| `sanskrit_parser/generator/` | Core generator implementation |
| `sanskrit_parser/generator/sutras_antaranga.yaml` | Sutra rules |
| `sanskrit_parser/generator/paribhasha.py` | Helper functions |
| `sanskrit_parser/generator/antaranga_prakriya.py` | Prakriya engine |
| `sanskrit_parser/generator/process_yaml.py` | YAML DSL evaluator |
| `Generator.md` | Developer guide |

## Debugging Tools

1. **Rule tracing**: Modify prakriya execution to log fired rules
2. **Condition testing**: Test condition expressions in isolation
3. **Helper function verification**: Test paribhasha.py functions directly
4. **YAML validation**: Check rule syntax and formatting

## Related Skills

- For implementing new sutra rules: Use `gen-sutra-rule` skill
- For generating vibhakti test entries: Use `gen-vibhakti-test` skill
- For adding features: Use `add-feature` skill
- For adding tests: Use `add-test` skill