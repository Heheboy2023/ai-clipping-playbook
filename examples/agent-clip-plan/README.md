# Checked moments → three cut files

Chapters 17–18 use this small planner to connect an agent task to real media work.
The code is a tested reference, not a transcript of an authenticated model session.

Start in the repository root with its Python environment active. Generate the
fixtures first if Chapter 14's setup has not been completed. They contain patterns
and tones, not speech or portfolio material.

## Preview, save, render

```bash
python examples/agent-clip-plan/clip_plan.py --moments examples/agent-clip-plan/moments.csv --output work/clip-plan/jobs.csv --dry-run
```

This validates all rows and probes the source. It creates no folder or manifest.

```bash
python examples/agent-clip-plan/clip_plan.py --moments examples/agent-clip-plan/moments.csv --output work/clip-plan/jobs.csv
```

```bash
clipkit batch --manifest work/clip-plan/jobs.csv --jobs 2 --dry-run
```

```bash
clipkit batch --manifest work/clip-plan/jobs.csv --jobs 2
```

Expected: three cuts under `work/clip-plan/exports/`, lasting about 2, 2.5, and
2.3 seconds. Check the last result's `failed` count is zero, then play the files.
This step cuts only. It does not crop, caption, judge the moment, or post.

```bash
clipkit probe --input work/clip-plan/exports/C02-cut-v01.mp4
```

To repeat a completed batch without replacing outputs:

```bash
clipkit batch --manifest work/clip-plan/jobs.csv --jobs 2 --resume
```

The planner itself refuses an existing manifest. For changed selections, choose
a fresh folder such as `work/clip-plan-v02/jobs.csv`. Relative source paths are
resolved from the moments CSV's folder. Generated manifests include local source
paths; do not post them with private client filenames.

## Input rules

The input has five columns: `id,source,start,end,checked`. IDs use uppercase
letters/digits/hyphens/underscores, start with a letter, and must be unique.
`checked` must say `yes`. This field records your decision; software cannot prove
you listened. Start/end are source times, not times in the exported clip.

Use decimal seconds or `HH:MM:SS.sss`. This is not `HH:MM:SS:FF` frame timecode.
The planner calculates duration as end minus start, rejects negative/non-finite
times, and checks the end against the source's probed duration. It refuses empty
tables, missing media, malformed rows, and existing outputs.

The `moments-clock.csv` file expresses the same ranges in clock notation.

## Agent exercises

- Codex: [build a planner](../../prompts/codex/clip-plan-task.md).
- Claude Code: [repair clock input](../../prompts/claude/clock-repair-task.md).
- Focused reference tests: `python -m pytest tests/test_clip_plan_reference.py -q`.
- Whole repository: `python -m pytest -q`.

The checked-in implementation is the reference answer. Put agent-created versions
under `work/`, so practicing never replaces the answer or the main Clipkit code.
