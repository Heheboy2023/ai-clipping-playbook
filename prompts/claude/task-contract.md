# Claude Code Task Contract

## Outcome

Give Claude Code the same bounded fixture-backed task used for Codex while using
Claude Code's own instruction and permission model.

## Replace these placeholders

- `[OBJECTIVE]`
- `[ALLOWED_FILES]`
- `[FORBIDDEN_FILES]`
- `[TEST_COMMANDS]`
- `[EXPECTED_ARTIFACT]`

## Prompt

```text
Read CLAUDE.md, AGENTS.md, README.md, SECURITY.md, and the relevant docs.

Objective: [OBJECTIVE]
Allowed files: [ALLOWED_FILES]
Forbidden files and actions: [FORBIDDEN_FILES]. Do not publish, upload, retrieve
online media, access credentials, or leave the repository and declared fixture
workspace.

Plan first. Make the smallest maintainable change, run [TEST_COMMANDS], and
produce [EXPECTED_ARTIFACT]. Stop for missing authority, secrets, private media,
network access, broad deletion, or ambiguous scope. Report diffs, commands,
tests, repaired failures, and human playback checks. Never claim publishing
approval.
```

## Verified command shape

```bash
claude -p --permission-mode plan --output-format json \
  --no-session-persistence < prompts/claude/task-contract.md
```

Use `claude --permission-mode plan` interactively before any edit-capable run.
For a bounded edit-capable print run, also restrict tools and add the current
documented `--max-budget-usd` flag with a deliberate numeric limit. Do not put a
placeholder value into an executable command.
The flags above were verified against the installed CLI help; an authenticated
model call was not made during repository construction.
