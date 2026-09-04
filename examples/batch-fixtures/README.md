# Batch fixture exercise

Use `examples/batch-production/manifest.csv`. The automated tests also run a two-job manifest with one intentional unsupported operation, repair it, and verify that `--resume` preserves the completed job.

Chapter 20's exact five-item exercise uses `five-item-with-failure.csv` and then `five-item-repaired.csv`. Both point to generated fixtures and write outputs only under `work/ch20/batch/`. The first manifest deliberately gives `CH20-005` an unsupported operation. Run the repaired manifest with `--resume`; the four completed outputs must be skipped and only the repaired job should render. The hidden state file is written beside the manifest and is disposable after the exercise outputs and report are reviewed.
