# Chapter 16 — Use yt-dlp, Captions, Audio, and Batch Commands — command sheet

Generated from the chapter source. Run commands in chapter order, not as one script.
Online, installation, transcription, and agent commands require the setup or input described in the chapter.
Replace clearly named placeholders before use. Use only the shell for your operating system.

## Command block 1

```bash
yt-dlp --version
```

## Command block 2

```bash
clipkit retrieve-metadata --url "PASTE_ONE_VIDEO_URL_HERE" --output work/source-metadata.json --confirmed-authorized
```

## Command block 3

```bash
yt-dlp --ignore-config --no-playlist --skip-download --write-subs --sub-langs en --sub-format vtt -o "work/source/%(id)s.%(ext)s" "PASTE_ONE_VIDEO_URL_HERE"
```

## Command block 4

```bash
yt-dlp --ignore-config --no-playlist --max-downloads 1 --no-overwrites -P work/source -o "%(id)s.%(ext)s" "PASTE_ONE_VIDEO_URL_HERE"
```

## Command block 5

```bash
clipkit captions generate --segments examples/fixtures/sample-segments.json --output work/ch16/captions.srt
```

## Command block 6

```bash
clipkit transcribe --input work/practice-speech.wav --output work/practice-transcript --model tiny.en --language en
```

## Command block 7

```bash
clipkit validate-transcript --manifest work/practice-transcript/transcript.json
```

## Command block 8

```bash
clipkit vertical --input examples/fixtures/sample-podcast.mp4 --output work/ch16/vertical.mp4 --mode pad
```

## Command block 9

```bash
clipkit captions burn --input work/ch16/vertical.mp4 --captions work/ch16/captions.srt --output work/ch16/captioned.mp4
```

## Command block 10

```bash
clipkit audio normalize --input work/ch16/captioned.mp4 --output work/ch16/final.mp4
```

## Command block 11

```bash
clipkit batch --manifest examples/batch-production/manifest.csv --jobs 2 --dry-run
```

## Command block 12

```bash
clipkit batch --manifest examples/batch-production/manifest.csv --jobs 2
```

## Command block 13

```bash
clipkit batch --manifest examples/batch-production/manifest.csv --jobs 2 --resume
```
