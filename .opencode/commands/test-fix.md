Investigate and fix the following failing test or command.

Failure context:
{{args}}

Required workflow:
1. Identify the most likely root cause from the evidence.
2. Apply the smallest viable fix.
3. Recommend the exact command(s) that should be re-run.
4. Do not broaden scope unless the evidence requires it.

Constraints:
- Follow AGENTS.md.
- Fix causes, not symptoms.
- Avoid unrelated cleanup.

Return:
- status
- root cause summary
- files changed
- retest recommendation
- remaining uncertainty
