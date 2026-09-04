# Batch production example

The CSV runs independent fixture jobs with bounded concurrency. One failed row does not hide the other job results, and `--resume` skips completed outputs recorded in `.clipkit-batch-state.json`.

Dry run: `clipkit batch --manifest examples/batch-production/manifest.csv --jobs 2 --dry-run`

Execute: `clipkit batch --manifest examples/batch-production/manifest.csv --jobs 2`
