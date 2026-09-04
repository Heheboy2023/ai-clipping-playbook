# Codex workflow

Install and verify Codex from the [official OpenAI CLI documentation](https://learn.chatgpt.com/docs/codex/cli):

```bash
npm install -g @openai/codex@latest
codex --version
codex --help
```

Read `AGENTS.md`, then begin with a plan or read-only explanation. The included noninteractive contract can be supplied on standard input:

```bash
codex exec -C . --sandbox workspace-write --ephemeral --json - \
  < prompts/codex/task-contract.md
```

Before running it:

- Replace every placeholder and restrict allowed files.
- Keep generated/client media in an explicit workspace.
- Require exact tests and a changed-file/failure report.
- Review the sandbox and approval mode shown by the installed CLI.
- Never grant publishing, credential access, broad deletion, or work outside scope.
- Run the task against generated fixtures before real authorized media.

Authentication and model execution are separate from installation. A successful `codex --version` does not prove login, service availability, correct model behavior, or permission safety. The repository’s own tests remain the source of evidence for code changes.
