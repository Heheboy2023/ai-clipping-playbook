# Clipkit Agent Instructions

## Mission

Maintain a deterministic, local, human-approved clipping pipeline. Prefer small,
testable changes. The CLI and repository are the executable source of truth for
commands that may later appear in *The AI Clipping Playbook*.

## Required checks

1. Read `README.md`, `SECURITY.md`, and the relevant file under `docs/`.
2. Explain the planned files and tests before editing.
3. Work only inside this repository and a user-declared media workspace.
4. Run targeted tests, then `python -m pytest` for material changes.
5. For media changes, generate fixtures and run the integration tests.
6. Report changed files, commands run, failures, repairs, and unresolved holds.

## Forbidden actions

- Do not upload, post, schedule, publish, message, or create external accounts.
- Do not retrieve online media unless the user confirms authorization and the
  command is limited to the requested source.
- Do not expose, invent, request, or print secrets.
- Do not use client/private/copyrighted media as fixtures.
- Do not bypass sandbox or approval controls.
- Do not recursively delete broad paths or modify files outside declared scope.
- Do not claim a render is approved until automated checks and human playback
  review are both recorded.

## Implementation conventions

- Python 3.11+; `pathlib`; argument arrays for subprocesses; never `shell=True`.
- Safe defaults, stable JSON envelopes, useful nonzero exits, atomic final output.
- No overwrite without `--overwrite`; no path escape from a declared root.
- Update tests, docs, examples, and `REPOSITORY_MANIFEST.csv` with code changes.

