# Chapter 15 — Cut and Crop Video With FFmpeg — command sheet

Generated from the chapter source. Run commands in chapter order, not as one script.
Online, installation, transcription, and agent commands require the setup or input described in the chapter.
Replace clearly named placeholders before use. Use only the shell for your operating system.

## Command block 1

```bash
mkdir -p work/ch15
```

## Command block 2

```powershell
New-Item -ItemType Directory -Force work/ch15
```

## Command block 3

```bash
ffprobe -v error -show_streams -show_format -of json examples/fixtures/sample-podcast.mp4
```

## Command block 4

```bash
ffmpeg -hide_banner -nostdin -n \
  -i examples/fixtures/sample-podcast.mp4 \
  -ss 1 -t 4 -map 0:v:0 -map '0:a:0?' \
  -c:v libx264 -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart work/ch15/cut.mp4
```

## Command block 5

```bash
clipkit cut --input examples/fixtures/sample-podcast.mp4 --output work/ch15/kit-cut.mp4 --start 1 --duration 4
```

## Command block 6

```bash
ffmpeg -hide_banner -nostdin -n -i work/ch15/cut.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1" \
  -map 0:v:0 -map '0:a:0?' -c:v libx264 -crf 20 \
  -pix_fmt yuv420p -c:a aac -b:a 192k \
  -movflags +faststart work/ch15/crop.mp4
```

## Command block 7

```bash
clipkit vertical --input work/ch15/cut.mp4 --output work/ch15/kit-crop.mp4 --mode crop
```

## Command block 8

```bash
ffmpeg -hide_banner -nostdin -n -i work/ch15/cut.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease:force_divisible_by=2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1" \
  -map 0:v:0 -map '0:a:0?' -c:v libx264 -crf 20 \
  -pix_fmt yuv420p -c:a aac -b:a 192k \
  -movflags +faststart work/ch15/pad.mp4
```

## Command block 9

```bash
clipkit vertical --input work/ch15/cut.mp4 --output work/ch15/kit-pad.mp4 --mode pad
```

## Command block 10

```bash
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate -show_entries format=duration -of json work/ch15/crop.mp4
```

## Command block 11

```bash
ffmpeg -hide_banner -nostdin -n -i work/ch15/crop.mp4 -ss 2 -frames:v 1 -update 1 work/ch15/frame.png
```

## Command block 12

```bash
ffmpeg -hide_banner -nostdin -n \
  -i examples/fixtures/sample-podcast.mp4 \
  -ss 1 -t 4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1" \
  -map 0:v:0 -map '0:a:0?' -c:v libx264 -crf 20 \
  -pix_fmt yuv420p -c:a aac -b:a 192k \
  -movflags +faststart work/ch15/one-pass.mp4
```

## Command block 13

```bash
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate -show_entries format=duration -of json work/ch15/one-pass.mp4
```

## Command block 14

```bash
ffmpeg -v error -nostdin -i work/ch15/one-pass.mp4 -map 0:v:0 -map '0:a:0?' -f null -
```
