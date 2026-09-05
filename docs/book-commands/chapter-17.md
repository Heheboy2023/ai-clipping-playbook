# Chapter 17 — Build and Fix a Workflow With Codex — command sheet

Generated from the chapter source. Run commands in chapter order, not as one script.
Online, installation, transcription, and agent commands require the setup or input described in the chapter.
Replace clearly named placeholders before use. Use only the shell for your operating system.

## Command block 1

```bash
codex --version
```

## Command block 2

```bash
codex
```

## Command block 3

```bash
python work/agent-practice/clip_name.py --creator "Nova Show" --moment "Intro Fix!" --version 1
```

## Command block 4

```bash
python -m pytest work/agent-practice/test_clip_name.py -q
```

## Command block 5

```bash
python -m pytest -q
```

## Command block 6

```bash
python examples/agent-clip-plan/clip_plan.py --moments examples/agent-clip-plan/moments.csv --output work/clip-plan/jobs.csv --dry-run
```

## Command block 7

```bash
python examples/agent-clip-plan/clip_plan.py --moments examples/agent-clip-plan/moments.csv --output work/clip-plan/jobs.csv
```

## Command block 8

```bash
clipkit batch --manifest work/clip-plan/jobs.csv --jobs 2 --dry-run
```

## Command block 9

```bash
clipkit batch --manifest work/clip-plan/jobs.csv --jobs 2
```

## Command block 10

```bash
clipkit probe --input work/clip-plan/exports/C02-cut-v01.mp4
```

## Command block 11

```bash
python -m pytest tests/test_clip_plan_reference.py -q
```
