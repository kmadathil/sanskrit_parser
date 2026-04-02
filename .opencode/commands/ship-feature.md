Perform a final acceptance pass for the following feature.

Feature context:
{{args}}

Required workflow:
1. Check the delivered implementation against the stated acceptance criteria.
2. Confirm tests exist for the changed behavior.
3. Confirm the relevant tests were run and passed.
4. Identify any remaining risks, missing validations, or polish items.
5. State whether the feature is ready to merge.

Constraints:
- Follow AGENTS.md.
- Do not reopen solved work unless there is a concrete gap.

Return:
- ready_to_merge: yes | no
- acceptance_review
- test_review
- remaining risks
- recommended next action
