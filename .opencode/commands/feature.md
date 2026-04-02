Deliver the following feature end-to-end.

Feature request:
{{args}}

Required workflow:
1. Understand the request and restate the acceptance criteria.
2. Create a small plan and get approval from user if the request says so.
3. Delegate implementation to implementer.
4. Delegate test creation and execution to tester.
5. If tests fail, delegate to debugger, then return to tester.
6. Finish only when the relevant tests pass and the acceptance criteria are satisfied.
7. Once finished, ask the user for permission to commit, and delegate to committer if approved. 

Constraints:
- Follow AGENTS.md.
- Keep changes minimal and reviewable.
- Do not make speculative product decisions; surface ambiguity.

Return:
- final status
- summary of work completed
- changed files
- tests run
- remaining risks
