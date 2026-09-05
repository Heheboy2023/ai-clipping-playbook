# Codex filename-helper exercise

Goal: create a print-only filename helper in `work/agent-practice/`.

Ask the agent to create `clip_name.py` and `test_clip_name.py` in that folder.
Use `prompts/codex/task-contract.md` with these filled-in requirements:

- Accept `--creator`, `--moment`, `--version`.
- Lowercase each name; replace runs outside ASCII a-z and 0-9 with one hyphen; strip edge hyphens; reject an empty result.
- Version must be an integer of at least 1.
- Print `creator__moment__vNN.mp4` with at least two version digits.
- Example: `Nova Show`, `Intro Fix!`, `1` → `nova-show__intro-fix__v01.mp4`.
- Never create, rename, or move media; no added packages or changes outside the two practice files. Do not publish.
- Test normal input, punctuation, empty slugs, version zero, and version 12. Run the focused tests and the full suite.

After the agent writes the files:

```bash
python work/agent-practice/clip_name.py --creator "Nova Show" --moment "Intro Fix!" --version 1
python -m pytest work/agent-practice/test_clip_name.py -q
python -m pytest -q
```

Compare with `reference/clip_name.py` after trying the exercise. That reference is an authored, tested solution, not a recorded agent conversation. It is tested by `tests/test_filename_reference.py` and does not imply a particular model will generate identical code.

Run the reference directly:

```bash
python examples/agent-task-codex/reference/clip_name.py --creator "Nova Show" --moment "Intro Fix!" --version 1
python -m pytest tests/test_filename_reference.py -q
```
