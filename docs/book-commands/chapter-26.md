# Chapter 26 — Handle Several Creators With Batch Production — command sheet

Generated from the chapter source. Run commands in chapter order, not as one script.
Online, installation, transcription, and agent commands require the setup or input described in the chapter.
Replace clearly named placeholders before use. Use only the shell for your operating system.

## Command block 1

```bash
clipkit batch --manifest examples/multi-creator-batch/broken.csv --jobs 2 --dry-run
```

## Command block 2

```bash
clipkit batch --manifest examples/multi-creator-batch/broken.csv --jobs 2
```

## Command block 3

```bash
clipkit batch --manifest examples/multi-creator-batch/fixed.csv --jobs 2 --resume
```
