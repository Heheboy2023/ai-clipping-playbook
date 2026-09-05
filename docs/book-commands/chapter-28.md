# Resource Pack — Keep These Pages Open — command sheet

Generated from the chapter source. Run commands in chapter order, not as one script.
Online, installation, transcription, and agent commands require the setup or input described in the chapter.
Replace clearly named placeholders before use. Use only the shell for your operating system.

## Command block 1

```bash
ffprobe -v error -show_streams -show_format \
  -of json examples/fixtures/sample-podcast.mp4
```

## Command block 2

```bash
clipkit cut --input examples/fixtures/sample-podcast.mp4 \
  --output work/pack/cut.mp4 --start 1 --duration 4
```

## Command block 3

```bash
clipkit vertical --input work/pack/cut.mp4 \
  --output work/pack/crop.mp4 --mode crop
```

## Command block 4

```bash
clipkit vertical --input work/pack/cut.mp4 \
  --output work/pack/pad.mp4 --mode pad
```

## Command block 5

```bash
clipkit captions burn \
  --input examples/fixtures/sample-podcast.mp4 \
  --captions examples/fixtures/sample.srt \
  --output work/pack/caption-test.mp4
```

## Command block 6

```bash
clipkit audio normalize --input work/pack/cut.mp4 \
  --output work/pack/audio.mp4
```

## Command block 7

```bash
clipkit batch \
  --manifest examples/batch-production/manifest.csv \
  --jobs 2 --dry-run
```
