# Complete beginner walkthrough

This walkthrough uses only synthetic media generated on your computer. It creates no account and publishes nothing.

## 1. Install and enter the environment

Install Python, FFmpeg, and ffprobe using the platform guide. From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
clipkit doctor
```

On Windows PowerShell, use `py -3.11 -m venv .venv` and `.venv\Scripts\Activate.ps1`.

## 2. Generate safe practice media

```bash
python scripts/generate_fixtures.py
clipkit probe --input examples/fixtures/sample-podcast.mp4
```

The fixture manifest records the generated files and hashes. A real project needs its own authorization evidence.

## 3. Practice project intake

```bash
clipkit init work/walkthrough --name walkthrough
clipkit intake --project work/walkthrough --input examples/fixtures/sample-podcast.mp4 --mode copy --confirmed-authorized
```

For a real source, stop until the owner, allowed uses, guest/music issues, credit, destinations, and proof are recorded.

## 4. Validate transcript and candidates

```bash
clipkit validate-transcript --manifest examples/fixtures/sample-transcript.json
clipkit candidates validate --input examples/fixtures/sample-candidates.csv
clipkit candidates score --input examples/fixtures/sample-candidates.csv --output work/walkthrough/scored-candidates.csv
```

The score ranks supplied editorial criteria. It does not predict views or replace source playback.

## 5. Rehearse the plan

```bash
clipkit run --manifest examples/end-to-end/job.yaml --dry-run
```

Read every input, output, and FFmpeg argument before running it. The manifest is authorized only because it points to repository-generated fixtures.

## 6. Render the local example

```bash
clipkit run --manifest examples/end-to-end/job.yaml
clipkit status --run work/end-to-end/run-state.json
clipkit qc --batch work/end-to-end/run-state.json
```

The automated report checks file presence, readability, duration, and streams. It cannot judge a dishonest cut, wrong speaker, bad crop, typo, or unpleasant sound.

## 7. Perform human QC

Watch `work/end-to-end/01-cut.mp4` through `04-final.mp4`, compare them with the fixture source, and complete `templates/final-playback-review.md`. If a correction is needed, remove or rename only the affected generated output, correct the manifest or implementation, and rerun safely.

When the review passes:

```bash
clipkit approve --run work/end-to-end/run-state.json --reviewer "your name" --notes "full playback complete"
```

This is local QC approval, not permission to publish.

## 8. Package and validate

```bash
clipkit package --run work/end-to-end/run-state.json --destination generic-vertical --output work/end-to-end-package
clipkit validate-package --path work/end-to-end-package
clipkit audit-brand --package work/end-to-end-package
```

The package contains the final local media and a hash manifest. A human must separately recheck the destination’s current requirements, account, metadata, disclosures, and upload.

## 9. Try the other workflows

```bash
clipkit run --manifest examples/podcast/job.yaml --dry-run
clipkit run --manifest examples/youtube-video/job.yaml --dry-run
clipkit run --manifest examples/livestream/job.yaml --dry-run
clipkit run --manifest examples/gaming/job.yaml --dry-run
clipkit run --manifest examples/multi-speaker-podcast/job.yaml --dry-run
clipkit batch --manifest examples/batch-production/manifest.csv --jobs 2 --dry-run
```

Use [troubleshooting](troubleshooting.md) if a step fails. Do not add real secrets or source media to a commit.
