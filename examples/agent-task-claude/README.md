# Claude Code fixture task

Use the filename rules from `examples/agent-task-codex/README.md`, with `CLAUDE.md`, `.claude/settings.json`, and `prompts/claude/task-contract.md`. Put this attempt in `work/claude-practice/` so it does not replace the Codex exercise.

Begin with `claude --permission-mode plan`. Review the small plan, exit, then start `claude` and paste the complete bounded task for an edit-capable interactive session. Do not use a bypass mode. Never publish or rename media in this exercise.

After the files exist:

```bash
python work/claude-practice/clip_name.py --creator "Nova Show" --moment "Intro Fix!" --version 12
python work/claude-practice/clip_name.py --creator "Nova" --moment "intro" --version 0
python -m pytest work/claude-practice/test_clip_name.py -q
python -m pytest -q
```

The version-zero invocation is supposed to fail with a useful message. The reference solution is `examples/agent-task-codex/reference/clip_name.py`; it is tested independently of a model session.
