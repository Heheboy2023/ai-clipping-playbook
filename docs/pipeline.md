# Complete local pipeline

A pipeline manifest declares `project_id`, `rights_confirmed`, `editorial_approved`, a contained `work_root`, and ordered steps. Supported operations are `cut`, `vertical`, `captions_burn`, and `audio_normalize`. `input: "@previous"` passes the prior output forward.

```bash
clipkit run --manifest examples/end-to-end/job.yaml --dry-run
clipkit run --manifest examples/end-to-end/job.yaml
clipkit status --run work/end-to-end/run-state.json
```

Safety behavior:

- A real run refuses false/missing rights or editorial gates.
- Every declared output must stay inside `work_root`.
- Existing outputs are not overwritten.
- A failure is recorded and returns exit code 3.
- `--resume` skips only unchanged completed steps: operation, options, input bytes, captions, settings, and output bytes must match. Changed jobs need new output names or a fresh work folder; existing files are never silently replaced.
- Every real run clears its earlier playback approval. Run QC and review again before packaging.
- Dry runs write no state or media.

After automated checks, perform full human playback and record local approval:

```bash
clipkit qc --batch work/end-to-end/run-state.json
clipkit approve --run work/end-to-end/run-state.json --reviewer "your name" --notes "full playback complete"
```

Packaging requires a complete run and playback approval tied to the actual output bytes. `approve` first requires a passing, current QC report. A failed run or changed output cannot be packaged as reviewed. Approval and packaging both record `publishing_authority: false`.

```bash
clipkit package --run work/end-to-end/run-state.json --destination generic-vertical --output work/end-to-end-package
clipkit validate-package --path work/end-to-end-package
```
