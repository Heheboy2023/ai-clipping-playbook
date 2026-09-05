# Chapter 28 — PowerShell command sheet

Run these one-line commands in order from the repository root with the environment active.

```powershell
ffprobe -v error -show_streams -show_format    -of json examples/fixtures/sample-podcast.mp4
```

```powershell
clipkit cut --input examples/fixtures/sample-podcast.mp4    --output work/pack/cut.mp4 --start 1 --duration 4
```

```powershell
clipkit vertical --input work/pack/cut.mp4    --output work/pack/crop.mp4 --mode crop
```

```powershell
clipkit vertical --input work/pack/cut.mp4    --output work/pack/pad.mp4 --mode pad
```

```powershell
clipkit captions burn    --input examples/fixtures/sample-podcast.mp4    --captions examples/fixtures/sample.srt    --output work/pack/caption-test.mp4
```

```powershell
clipkit audio normalize --input work/pack/cut.mp4    --output work/pack/audio.mp4
```

```powershell
clipkit batch    --manifest examples/batch-production/manifest.csv    --jobs 2 --dry-run
```
