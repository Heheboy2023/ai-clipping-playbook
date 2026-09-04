# Codex Task Contract

## Outcome

Ask Codex to make one fixture-backed repository change without widening scope or
gaining publishing authority.

## Replace these placeholders

- `[OBJECTIVE]`
- `[ALLOWED_FILES]`
- `[FORBIDDEN_FILES]`
- `[TEST_COMMANDS]`
- `[EXPECTED_ARTIFACT]`

## Prompt

```text
Read AGENTS.md, README.md, SECURITY.md, and the relevant docs before acting.

Objective: [OBJECTIVE]
Allowed files: [ALLOWED_FILES]
Forbidden files and actions: [FORBIDDEN_FILES]. Do not publish, upload, retrieve
online media, access credentials, or work outside the repository and declared
fixture workspace.

First report the plan and risks. Then make the smallest change, run
[TEST_COMMANDS], and produce [EXPECTED_ARTIFACT]. Use only generated fixtures.
Stop if a requirement needs network access, private media, a secret, broad
deletion, or a decision outside this task.

Finish with changed files, commands, test results, failures repaired, and the
remaining human playback checks. Do not claim publication approval.
```

## Verified command shape

```bash
codex exec -C . --sandbox workspace-write --ephemeral --json - \
  < prompts/codex/task-contract.md
```

Run interactively first with `codex` and inspect the plan. The command shape was
verified against the installed CLI help; an authenticated execution was not run
as part of repository construction.
