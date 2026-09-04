# Complete local pipeline

This is the smallest complete production rehearsal: cut, vertical render, captions, audio normalization, automated QC, human approval, local packaging, and package validation.

1. `clipkit run --manifest examples/end-to-end/job.yaml`
2. `clipkit qc --batch work/end-to-end/run-state.json`
3. Watch every output, compare it with the source, and complete the review template.
4. `clipkit approve --run work/end-to-end/run-state.json --reviewer "your name" --notes "full playback complete"`
5. `clipkit package --run work/end-to-end/run-state.json --destination generic-vertical --output work/end-to-end-package`
6. `clipkit validate-package --path work/end-to-end-package`

Approval is local QC only. Publishing remains a separate human action outside this repository.
