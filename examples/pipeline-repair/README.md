# Repair the caption path without recutting

This exercise is separate from the normal end-to-end job. Generate fixtures first.
The broken file intentionally points to a nonexistent SRT. It should complete the
cut and crop, then fail at captions.

```bash
clipkit run --manifest examples/pipeline-repair/broken.yaml
```

Expected exit: 3, a failed pipeline. This is the lesson's intended failure.

Compare the two YAML files. Only the caption path differs. Resume with the fixed one:

```bash
clipkit run --manifest examples/pipeline-repair/fixed.yaml --resume
```

```bash
clipkit status --run work/pipeline-repair/run-state.json
```

```bash
clipkit qc --batch work/pipeline-repair/run-state.json
```

Expected: cut and vertical steps are reused; caption and audio steps complete.
The final state awaits playback. Open all four MP4s under `work/pipeline-repair/`.
The fixture contains patterns/tones, not spoken captions or client work.

Do not restart the broken file after completing the exercise. Keep this working
run. For another attempt, copy both manifests and change their work/output folder
consistently. Existing media is never silently replaced.
