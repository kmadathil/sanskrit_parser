Commit the completed feature work to git.

Commit scope:
$ARGUMENTS

Required workflow:
1. Inspect git status and diff.
2. Verify the changed files match the requested feature scope. 
3. Validate that tests have been run (but do not create or run any tests).
4. Stage only the intended files.
5. Create a clean git commit message in imperative mood.
6. Commit the changes.
7. Return the commit hash and final message.

Constraints:
- Follow AGENTS.md.
- Do not include unrelated files.
- Refuse to commit if the workspace contains ambiguous or unsafe changes.
- Refuse to commit if tests have not run or passed, unless specifically instructed to allow such a commit.
- Do not push.

Return:
- status
- files committed
- commit message
- commit hash
- blockers
