# Claude Code workflow

Install and verify Claude Code using [Anthropic’s official setup guide](https://code.claude.com/docs/en/quickstart):

```bash
brew install --cask claude-code
claude --version
claude doctor
```

Windows users can follow the current official WinGet instructions. Read `CLAUDE.md`, `AGENTS.md`, and `.claude/settings.json` before granting access.

The included task contract can be inspected with a plan-only print invocation:

```bash
claude -p --permission-mode plan --output-format json \
  --no-session-persistence < prompts/claude/task-contract.md
```

Replace placeholders, review the permission preview, and begin with fixtures. Do not use bypass-permission modes. Hooks may validate paths or tests; they may not hide state changes, retrieve unapproved media, publish, or delete broad paths.

The tracked `.claude/settings.json` registers a `PreToolUse` command hook for `Write` and `Edit`. It sends hook JSON to `scripts/hooks/validate_output_root.py`, which exits with status 2 when `file_path` is outside `$CLAUDE_PROJECT_DIR`. Test the same validator directly and through its hook-input mode before relying on it.

Installation, authentication, and safe task completion are distinct checks. Verify the resulting files and run the repository tests yourself.
