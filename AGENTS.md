# AGENTS.md

## Project operating rules

This repository uses an agentic development workflow. Agents must preserve architecture, make minimal coherent changes, and avoid unrelated refactors.

### Core principles
- Prefer small, reviewable changes over broad rewrites.
- Follow existing module boundaries, naming conventions, and dependency direction.
- Keep implementation, testing, and debugging responsibilities separated unless explicitly instructed otherwise.
- Do not change public interfaces, schemas, or contracts unless the task requires it.
- Stop and surface ambiguity rather than guessing on product behavior.

### Feature delivery workflow
1. Understand the request and define acceptance criteria.
2. Inspect the existing implementation before editing files.
3. Implement the smallest correct feature slice.
4. Add or update tests covering the new behavior.
5. Run the narrowest relevant tests first, then broaden if needed.
6. If failures occur, debug from evidence and patch one root cause at a time.
7. Re-run the affected tests after each fix.

### Architecture rules
- Reuse existing patterns before introducing new abstractions.
- Prefer composition over new framework-like layers.
- Keep business logic out of transport, controller, or UI glue layers.
- Co-locate related tests with the codebase's existing conventions.
- Preserve backward compatibility unless the task explicitly authorizes a breaking change.

### Editing rules
- Touch the minimum set of files needed.
- Avoid opportunistic cleanup unless it is necessary for correctness.
- Keep diffs easy to review.
- Do not rename or move files unless there is a clear payoff for the current task.

### Testing rules
- Add tests for the behavior being introduced or changed.
- Prefer focused tests over broad snapshot-style coverage.
- Start with the smallest relevant command, then widen scope.
- If a test is flaky or unclear, explain why before changing it.

### Debugging rules
- Read the exact failing output before editing code.
- Form 1 to 3 hypotheses and test the most likely one first.
- Fix causes, not symptoms.
- Avoid bundling multiple speculative fixes in one patch.

### Output expectations for all agents
Every agent response should be concise and structured:
- Goal understood.
- Files inspected or changed.
- Result or blocker.
- Next recommended step.

### Model routing guidance
- Use reasoning-heavy models for planning and debugging.
- Use faster coding-focused models for implementation and test authoring.
- Keep context compact by delegating specialized work to the right agent.


### Repository structure

Sanskrit Parser is a Python library for morphological and syntactic
analysis of Sanskrit text. See [CLAUDE.md](CLAUDE.md) for details.

It also implements a Sanskrit generator that runs Paninian grammar
rules. See [Generator.md](Generator.md) for details. 

