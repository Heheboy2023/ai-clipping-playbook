# Make your first automated practice clip

This route creates a short vertical file with captions and sound on your computer.
No paid AI tool or API key is needed. The source is a moving pattern with tones:
it tests the commands, not your editing taste. For a real first clip in Resolve,
start with the [recording exercise](../examples/first-clip/README.md).

## 1. Finish setup once

Use the [macOS guide](macos-install.md) or [Windows guide](windows-install.md).
Open the repository's top folder in your terminal and activate its environment.
You should be in the folder containing `README.md`, `pyproject.toml`, and `src/`.

```bash
clipkit doctor
```

Find `core_ready: true` in the report. If it is false, fix the missing Python,
FFmpeg, or ffprobe setup before continuing. Optional transcription or account
fields do not need to be enabled for this exercise.

## 2. Generate the practice source

```bash
python scripts/generate_fixtures.py
```

The fixture files appear in `examples/fixtures/`. Keep the extensions as written.

```bash
clipkit probe --input examples/fixtures/sample-podcast.mp4
```

Look for video, audio, and a duration close to eight seconds. It is a test pattern,
not a podcast conversation despite the filename.

## 3. Preview the four-step job

Open `examples/end-to-end/job.yaml` in a text editor. Its steps are cut, vertical,
captions, and audio. Later steps use `@previous`, meaning the earlier result.

```bash
clipkit run --manifest examples/end-to-end/job.yaml --dry-run
```

Read the source and output paths. The output folder is `work/end-to-end/`.
The dry run does not create video. The sample's confirmation fields refer to
the provided test source and selected interval; choose those fields deliberately
when adapting the job to another source.

## 4. Render

```bash
clipkit run --manifest examples/end-to-end/job.yaml
```

A successful chain finishes as `awaiting_human_qc`. Four videos should exist:

```text
work/end-to-end/
  01-cut.mp4
  02-vertical.mp4
  03-captioned.mp4
  04-final.mp4
```

If this folder already contains a completed unchanged run, use the resume route
below. For changed settings, make a new work folder in a copied manifest.
Keep your previous work.

## 5. Check the files

```bash
clipkit status --run work/end-to-end/run-state.json
clipkit qc --batch work/end-to-end/run-state.json
```

`status` reads progress. `qc` checks the completed files and writes `qc-report.json`.
Find `automated_pass: true`. This confirms basic file checks, not a good edit.

Open `04-final.mp4` in a player. Watch the entire six-second clip. You should see
the moving pattern in a tall frame with changing words, and hear the test tone.
The supplied SRT is test text, not a transcription of that tone.

If something is wrong, open the earlier files to find where it first appears.
An error in `02-vertical.mp4` points toward framing, not the audio step.

## 6. Record your playback check

After you really watched the file:

```bash
clipkit approve --run work/end-to-end/run-state.json --reviewer "your name" --notes "full playback complete"
```

Replace `your name` with your name or editor role. This saves a local review record
tied to the checked output. It does not upload anything.

## 7. Make the delivery folder

```bash
clipkit package --run work/end-to-end/run-state.json --destination generic-vertical --output work/end-to-end-package
clipkit validate-package --path work/end-to-end-package
```

Open the MP4 inside `work/end-to-end-package/media/`. This is the packaged copy,
separate from the working outputs. Validation checks its recorded file hash.

## When a step fails

Read the first failed step and fix that exact problem. Missing captions need a
correct caption path. A missing source needs the right source file. An existing
output needs a new version folder, or resume when the job is unchanged.

```bash
clipkit run --manifest examples/end-to-end/job.yaml --resume
```

Resume reuses only matching completed work. A real run clears prior playback
approval, so repeat QC and playback before making a new package.

| Message or symptom | First check |
|---|---|
| Command not found | Active environment and installation |
| Source missing | Fixture generation and current folder |
| Output outside work root | Paths in the copied YAML |
| Caption does not fit | Split long cues with correct new timings |
| Captions appear late | Use captions timed to the actual cut |
| Package refused | Completed run, current QC, playback record, unchanged files |

## Use the skill on your own material

Finish a clean short edit first. Choose a fresh job folder, reviewed captions, and
the needed vertical layout. Test one output before processing a package.

- [Three checked selections into cuts](../examples/agent-clip-plan/README.md)
- [Exact chapter command sheets](book-commands/)
- [Pipeline details](pipeline.md)
- [Troubleshooting](troubleshooting.md)

Keep private media and real secrets outside the tracked public pack.
