# Troubleshooting

## `clipkit` is not found

Activate the virtual environment or call it directly:

```bash
source .venv/bin/activate
python -m clipkit --help
```

On Windows: `.venv\Scripts\clipkit.exe --help`.

## FFmpeg or ffprobe is missing

Run `clipkit doctor`. Verify the executable is on `PATH`, or set an absolute path in `clipkit.toml`/`CLIPKIT_FFMPEG` and `CLIPKIT_FFPROBE`. Confirm the installed build includes `libx264`, `subtitles`, and `loudnorm`.

## Caption burn says no renderer is available

Clipkit prefers FFmpeg’s libass-backed `subtitles` filter. When it is absent, the tested fallback converts reviewed SRT blocks into transparent caption cards and burns them with FFmpeg’s `overlay` filter. If both filters are missing, install a fuller build linked from the official FFmpeg page and rerun `clipkit doctor`. Do not silently replace burned captions with none.

## Output already exists

This is a safety refusal. Choose a new versioned filename, verify and move the old generated output, or deliberately pass `--overwrite` for a single command. Pipelines never overwrite; remove only a known generated failed output before `--resume`.

## Pipeline says an output escaped `work_root`

Correct the manifest paths. Do not widen the root to `/`, a home folder, or the repository just to bypass containment.

## Pipeline is blocked by rights/editorial gates

Do not flip booleans as a workaround. Record the authorization and editorial decision, then set them truthfully. Dry-run is available for planning without attestation.

## A batch returned exit code 3

Open `.clipkit-batch-state.json`, inspect each job’s structured error, repair the manifest or missing dependency, and run with `--resume`. Completed outputs are skipped only when both state and file exist.

## Whisper fails or downloads a model

Confirm FFmpeg and `whisper --help`, available disk/memory, and network access for a first model download. Start with a short authorized file. A small model is a smoke test, not a quality guarantee.

## Transcript or speaker labels look wrong

That is an editorial failure even if the command exited zero. Compare with source audio, correct names/numbers, reconcile speaker labels, and revalidate. Never infer identity from an unlabeled model token.

## Crop follows the wrong person

Clipkit’s `crop` is a static center crop. Use `pad`, a manual Resolve layout, or a reviewed shot/layout list for speaker changes. It does not promise face or active-speaker tracking.

## Package is blocked

Run automated QC, watch all outputs in full, and record `clipkit approve`. Packaging deliberately refuses an unreviewed run. `validate-package --path` expects the package directory, not the JSON filename.

## Codex or Claude Code is installed but cannot run a task

Version availability does not prove authentication, account entitlements, network access, model availability, or permissions. Use the vendor’s official diagnostic, preserve permission controls, and do not paste tokens into prompts or project files.
