# Cut and vertical lab — Chapter 15

Run from the repository root after Chapter 14. These are the book's exact macOS/zsh commands. On Windows use the one-line equivalents (join each backslash-continued line with a space); do not paste the continuation backslashes into PowerShell. Clipkit one-line commands are shared by both systems.

Create the output folder:

```bash
mkdir -p work/ch15
```

Inspect the generated sample:

```bash
ffprobe -v error -show_streams -show_format -of json examples/fixtures/sample-podcast.mp4
```

Cut four seconds, starting one second into the file:

```bash
ffmpeg -hide_banner -nostdin -n \
  -i examples/fixtures/sample-podcast.mp4 \
  -ss 1 -t 4 -map 0:v:0 -map '0:a:0?' \
  -c:v libx264 -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart work/ch15/cut.mp4
```

Clipkit alternative, with a different output name:

```bash
clipkit cut --input examples/fixtures/sample-podcast.mp4 --output work/ch15/kit-cut.mp4 --start 1 --duration 4
```

Scale to fill and center-crop (square-pixel input):

```bash
ffmpeg -hide_banner -nostdin -n -i work/ch15/cut.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1" \
  -map 0:v:0 -map '0:a:0?' -c:v libx264 -crf 20 \
  -pix_fmt yuv420p -c:a aac -b:a 192k \
  -movflags +faststart work/ch15/crop.mp4
```

Scale to fit and pad:

```bash
ffmpeg -hide_banner -nostdin -n -i work/ch15/cut.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease:force_divisible_by=2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1" \
  -map 0:v:0 -map '0:a:0?' -c:v libx264 -crf 20 \
  -pix_fmt yuv420p -c:a aac -b:a 192k \
  -movflags +faststart work/ch15/pad.mp4
```

Clipkit equivalents:

```bash
clipkit vertical --input work/ch15/cut.mp4 --output work/ch15/kit-crop.mp4 --mode crop
```

```bash
clipkit vertical --input work/ch15/cut.mp4 --output work/ch15/kit-pad.mp4 --mode pad
```

Inspect and extract a frame:

```bash
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate -show_entries format=duration -of json work/ch15/crop.mp4
```

```bash
ffmpeg -hide_banner -nostdin -n -i work/ch15/crop.mp4 -ss 2 -frames:v 1 -update 1 work/ch15/frame.png
```

The source is an eight-second pattern-and-tone fixture, not real dialogue. The accurate cut should be about four seconds; the vertical files are 1080 × 1920. Crop removes picture from the sides; pad retains it with empty areas. No command tracks a moving face. `-n` refuses existing outputs. Use a new name to rerun an intentional revision.

The raw lab is tested by `tests/test_book_commands.py` in a temporary directory. See `docs/ffmpeg-commands.md` for additional recipes.
