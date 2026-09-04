# Claude Code Project Instructions

Follow `AGENTS.md` as the shared project contract.

For Claude Code specifically:

- Start interactively in plan mode for unfamiliar changes.
- Use the allow/ask/deny policy in `.claude/settings.json`.
- Never use `--dangerously-skip-permissions` or bypass-permission modes.
- In print mode, set a budget and request structured output only after an
  interactive dry run has established the task boundaries.
- Hooks may validate paths and tests. Hooks may not publish, delete broad paths,
  retrieve external media, or hide state-changing actions.

