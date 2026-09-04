---
name: clipkit
description: Operate or extend this repository's local, rights-gated media clipping workflows when a task involves Clipkit commands, manifests, fixtures, tests, or packaging.
---

# Clipkit

Read `AGENTS.md` and the relevant guide under `docs/` before changing or running a workflow.

## Choose the path

- For installation or diagnosis, run `clipkit --json doctor` and read `docs/installation.md` or `docs/troubleshooting.md`.
- For a new production workspace, use `clipkit init`, then `clipkit intake` only after the operator confirms authorization.
- For a media command, rehearse with `--dry-run`, use generated fixtures first, and preserve the no-overwrite default.
- For multiple independent outputs, use a CSV batch. For ordered cut/reframe/caption/audio steps, use a pipeline manifest.
- For repository code changes, run targeted tests and then `python -m pytest`; rebuild `REPOSITORY_MANIFEST.csv` afterward.

## Invariants

- Do not upload, post, schedule, publish, obtain credentials, or broaden external access.
- Keep outputs inside the declared work root. Never use a home folder, `/`, or the repository root as a workaround.
- Treat rights/editorial fields as human attestations, not legal conclusions.
- Do not claim speaker identity, transcript accuracy, crop quality, caption accuracy, audio quality, or editorial integrity from an exit code.
- Run automated QC, require full human playback, and record `clipkit approve` before local packaging.
- Approval and packaging never grant publishing authority.
- Parse `--json` output by fields and respect nonzero exits; code 3 can represent per-job or per-step failures.

Use `examples/end-to-end/job.yaml` for a complete fixture rehearsal and `docs/commands.md` for the maintained command surface.
