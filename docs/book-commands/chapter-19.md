# Chapter 19 — Connect the Full Clipping Pipeline — command sheet

Generated from the chapter source. Run commands in chapter order, not as one script.
Online, installation, transcription, and agent commands require the setup or input described in the chapter.
Replace clearly named placeholders before use. Use only the shell for your operating system.

## Command block 1

```bash
clipkit run --manifest examples/end-to-end/job.yaml --dry-run
```

## Command block 2

```bash
clipkit run --manifest examples/end-to-end/job.yaml
```

## Command block 3

```bash
clipkit status --run work/end-to-end/run-state.json
```

## Command block 4

```bash
clipkit qc --batch work/end-to-end/run-state.json
```

## Command block 5

```bash
clipkit approve --run work/end-to-end/run-state.json --reviewer "your name" --notes "full playback complete"
```

## Command block 6

```bash
clipkit package --run work/end-to-end/run-state.json --destination generic-vertical --output work/end-to-end-package
```

## Command block 7

```bash
clipkit validate-package --path work/end-to-end-package
```

## Command block 8

```bash
clipkit run --manifest examples/end-to-end/job.yaml --resume
```

## Command block 9

```bash
clipkit run --manifest examples/pipeline-repair/broken.yaml
```

## Command block 10

```bash
clipkit run --manifest examples/pipeline-repair/fixed.yaml --resume
```

## Command block 11

```bash
clipkit status --run work/pipeline-repair/run-state.json
```

## Command block 12

```bash
clipkit qc --batch work/pipeline-repair/run-state.json
```
