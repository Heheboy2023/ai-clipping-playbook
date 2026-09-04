# Clipkit command reference

Run `clipkit COMMAND --help` for current flags. Add `--json` anywhere to receive a stable success/error envelope; add `--config FILE` before the command.

| Command | Purpose | Destructive or external behavior |
|---|---|---|
| `doctor`, `version-report` | Tool and capability report | Read-only |
| `init` | Create standard local folders | Adds missing directories/files |
| `intake` | Copy or reference authorized local media and hash it | Requires explicit authorization |
| `probe` | Return ffprobe JSON | Read-only |
| `retrieve-metadata` | Record sanitized yt-dlp metadata | Network; authorization required; no media download |
| `transcribe` | Run local Whisper and normalize output | Writes transcript artifacts |
| `validate-transcript` | Check timing and required fields | Read-only |
| `candidates validate` | Validate candidate records | Read-only |
| `candidates score` | Apply disclosed editorial heuristic | Writes scored data; no performance prediction |
| `compare-candidates` | Compare human and AI boundaries | Read-only or writes requested report |
| `cut` | Accurate local clip | Writes new media; refuses overwrite by default |
| `vertical` | Center crop or pad to a vertical frame | Writes new media |
| `captions generate` | Convert segment records to SRT | Writes SRT |
| `captions burn` | Render SRT into video | Writes new media |
| `audio normalize` | Apply review-required loudness normalization | Writes new media |
| `concat` | Concatenate compatible local inputs | Writes new media |
| `render` | Run one operation manifest | Writes planned output unless dry-run |
| `batch` | Run bounded independent CSV jobs | Writes outputs/state; supports resume |
| `run` | Run rights/editorial-gated steps | Writes outputs/state; supports resume |
| `status` | Read a run state | Read-only |
| `qc` | Probe completed outputs | Writes QC report; still requires playback |
| `approve` | Record local human QC | Changes local state; never grants publishing authority |
| `package` | Copy approved final output to a local package | Writes local package and hashes |
| `validate-package` | Verify package existence and hashes | Read-only |
| `audit-brand` | Check filename portability | Read-only mechanical check |

Examples:

```bash
clipkit --json doctor
clipkit probe --input examples/fixtures/sample-podcast.mp4
clipkit cut --input examples/fixtures/sample-podcast.mp4 --output work/cut.mp4 --start 1 --duration 4
clipkit vertical --input work/cut.mp4 --output work/vertical.mp4 --mode crop
clipkit captions generate --segments examples/fixtures/sample-segments.json --output work/captions.srt
clipkit captions burn --input work/vertical.mp4 --captions work/captions.srt --output work/captioned.mp4
clipkit audio normalize --input work/captioned.mp4 --output work/final.mp4
clipkit batch --manifest examples/batch-production/manifest.csv --jobs 2 --dry-run
clipkit run --manifest examples/end-to-end/job.yaml --dry-run
```

Exit code `0` means success, `2` means validation/safety refusal, `3` means a batch or pipeline completed with one or more failures, and `130` means interruption. Parse JSON fields, not prose.
