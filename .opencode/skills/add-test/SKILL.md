---
name: add-test
description: Add tests to the Sanskrit parser. Use when implementing new test cases or expanding test coverage.
argument-hint: "[test-description]"
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, Todowrite
---

# Add Tests to Sanskrit Parser

Use this skill when adding new test cases or expanding test coverage in the Sanskrit parser.

## When to Use

- Adding new unit tests for existing functionality
- Creating test cases for newly implemented features
- Expanding test coverage for edge cases
- Adding integration tests
- Creating test utilities or helper functions

## Test Types

Depending on what you're testing, you might need to add to:

1. **Generator sutra tests**: `sanskrit_parser/generator/test/test_sutras.py`
2. **Vibhakti tests**: `sanskrit_parser/generator/test/test_vibhaktis.py` 
3. **Prakriya tests**: `sanskrit_parser/generator/test/test_prakriya.py`
4. **Utility function tests**: Module-specific test files
5. **CLI/interface tests**: Tests for command-line interface

## Implementation Steps

### Step 1 — Understand What Needs Testing
1. Identify the specific behavior or function to test
2. Determine what assertions need to be made
3. Identify test inputs and expected outputs

### Step 2 — Find the Appropriate Test File
1. Locate existing tests for similar functionality
2. Choose the test file that best matches what you're testing
3. If no suitable file exists, create a new test file following existing patterns

### Step 3 — Examine Existing Test Patterns
1. Read the test file to understand:
   - Test naming conventions
   - Setup/teardown patterns
   - Mocking or fixture usage
   - Assertion styles

### Step 4 — Write the Test
1. Follow the Arrange-Act-Assert pattern
2. Use descriptive test names
3. Keep tests focused on a single behavior
4. Use appropriate test data (edge cases, typical cases, etc.)

### Step 5 — Run and Verify
1. Run the specific test to ensure it fails before implementation
2. Run after implementation to confirm it passes
3. Run related tests to ensure no regressions

## Special Cases

### For Generator Sutra Rules
When testing a specific sutra rule implementation, consider:
- Testing the rule in isolation
- Testing rule interactions
- Testing with various input combinations
- Testing edge cases where rule should/not fire

### For Vibhakti Tests
When adding vibhakti test entries:
1. Use the `gen-vibhakti-test` skill instead
2. Follow the 8×3 table format (3 vibhakti × 3 numbers)
3. Add appropriate comments marking which forms test specific rules
4. Ensure SLP1 → Devanagari conversion is correct

### For Prakriya Tests
When testing complete derivations:
1. Test known word forms from reference grammars
2. Test intermediate steps if relevant
3. Test both successful derivations and expected failures
4. Use the `prakriya()` function to generate test cases

## Codebase Context

| File/Directory | Purpose |
|----------------|---------|
| `sanskrit_parser/generator/test/` | Generator-specific tests |
| `sanskrit_parser/generator/test/test_sutras.py` | Sutra rule tests |
| `sanskrit_parser/generator/test/test_vibhaktis.py` | Vibhakti inflection tests |
| `sanskrit_parser/generator/test/test_prakriya.py` | Complete derivation tests |
| `sanskrit_parser/test/` | General library tests |
| `tests/` | Project-level tests |

## Related Skills

- For adding Paninian sutra rules: Use `gen-sutra-rule` skill
- For generating vibhakti test entries: Use `gen-vibhakti-test` skill
- For debugging test failures: Use `gen-debug` skill