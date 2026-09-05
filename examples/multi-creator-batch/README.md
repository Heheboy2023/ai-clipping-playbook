# Five-job recovery exercise

Nova, Mira, and Reed are fictional labels. All inputs are synthetic test patterns and tones.
The `broken.csv` manifest deliberately references one missing source. It should report
four completed jobs and one failure, with an unsuccessful overall exit.

```bash
clipkit batch --manifest examples/multi-creator-batch/broken.csv --jobs 2 --dry-run
clipkit batch --manifest examples/multi-creator-batch/broken.csv --jobs 2
clipkit batch --manifest examples/multi-creator-batch/fixed.csv --jobs 2 --resume
```

`fixed.csv` repairs only REED-01's source. Both manifests sit in the same folder and therefore use the same `.clipkit-batch-state.json` record. After the first actual run, the fixed resume should reuse four unchanged outputs and complete the fifth. A second fixed resume should reuse all five.

The dry run is expected to report the missing input too. Do not copy the broken example into a real production job. Do not overwrite source media to manufacture a failure.

Output: `work/multi-creator/`, with one subfolder per fictional creator. Repeat a fresh experiment in a separate copied example folder and new work path if outputs from an earlier exercise already exist.
