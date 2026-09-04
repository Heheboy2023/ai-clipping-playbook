# FFmpeg command examples

Clipkit builds argument arrays and never invokes a shell. These raw commands mirror the tested fixture operations and are included for learning and troubleshooting.

Inspect:

```bash
ffprobe -v error -show_format -show_streams -of json examples/fixtures/sample-podcast.mp4
```

Accurate re-encoded cut:

```bash
ffmpeg -hide_banner -nostdin -y \
  -i examples/fixtures/sample-podcast.mp4 \
  -ss 1.000 -t 4.000 -map '0:v:0?' -map '0:a:0?' \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart work/cut.mp4
```

Fast keyframe-aligned stream copy (boundaries may not be frame-exact):

```bash
clipkit cut --input examples/fixtures/sample-podcast.mp4 --output work/stream-copy.mp4 --start 0 --duration 4 --stream-copy
```

Center crop and scale to vertical:

```bash
ffmpeg -hide_banner -nostdin -y -i work/cut.mp4 \
  -map 0:v:0 -map '0:a:0?' \
  -vf "crop='min(iw,ih*1080/1920)':'min(ih,iw*1920/1080)': \
  (iw-ow)/2:(ih-oh)/2,scale=1080:1920:flags=lanczos" \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart work/vertical.mp4
```

Fit and pad to vertical:

```bash
ffmpeg -hide_banner -nostdin -y -i work/cut.mp4 \
  -map 0:v:0 -map '0:a:0?' \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease: \
  flags=lanczos,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black" \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart work/padded.mp4
```

Blurred-background vertical layout:

```bash
ffmpeg -hide_banner -nostdin -y \
  -i examples/fixtures/sample-youtube.mp4 \
  -filter_complex \
  "[0:v]split=2[bg][fg]; \
   [bg]scale=1080:1920:force_original_aspect_ratio=increase, \
   crop=1080:1920,boxblur=30:2[bgv]; \
   [fg]scale=1080:1920:force_original_aspect_ratio=decrease[fgv]; \
   [bgv][fgv]overlay=(W-w)/2:(H-h)/2[v]" \
  -map "[v]" -map '0:a:0?' \
  -c:v libx264 -c:a aac -shortest work/blurred.mp4
```

Picture-in-picture from two authorized local inputs:

```bash
ffmpeg -hide_banner -nostdin -y \
  -i examples/fixtures/sample-livestream.mp4 \
  -i examples/fixtures/sample-youtube.mp4 \
  -filter_complex \
  "[1:v]scale=360:-2[pip];[0:v][pip]overlay=W-w-40:40[v]" \
  -map "[v]" -map '0:a:0?' -t 5 \
  -c:v libx264 -c:a aac work/pip.mp4
```

Explicit clockwise rotation after checking display metadata and the image itself:

```bash
ffmpeg -hide_banner -nostdin -y -noautorotate \
  -i examples/fixtures/sample-youtube.mp4 \
  -vf "transpose=clock" -metadata:s:v:0 rotate=0 \
  -c:v libx264 -c:a aac work/rotated.mp4
```

Burn reviewed SRT captions:

```bash
ffmpeg -hide_banner -nostdin -y -i work/vertical.mp4 \
  -map 0:v:0 -map '0:a:0?' \
  -vf "subtitles=filename='examples/fixtures/sample.srt'" \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart work/captioned.mp4
```

This raw command requires an FFmpeg build with the `subtitles` filter. Check
`ffmpeg -hide_banner -filters` first. If the filter is absent, use the tested
Clipkit raster-caption fallback instead:

```bash
clipkit captions burn --input work/vertical.mp4 \
  --captions examples/fixtures/sample.srt \
  --output work/captioned.mp4
```

Single-pass loudness normalization for review:

```bash
ffmpeg -hide_banner -nostdin -y -i work/captioned.mp4 \
  -af "loudnorm=I=-16:LRA=11:TP=-1.5" \
  -map '0:v:0?' -map 0:a:0 \
  -c:v copy -c:a aac -b:a 192k work/final.mp4
```

Concatenate codec-compatible local files with Clipkit’s temporary list handling:

```bash
clipkit concat --input work/part-01.mp4 --input work/part-02.mp4 --output work/joined.mp4
```

`-y` overwrites files, while Clipkit refuses overwrite by default and renders through a temporary file before atomic replacement. Prefer Clipkit for repeatable work. Rotation, blur, and picture-in-picture require visual inspection; values are examples, not editorial decisions. Listen to loudness-processed output and do not treat one target as universal across destinations or programs.

The quotes around optional stream maps such as `'0:a:0?'` are intentional. They stop shells such as zsh from treating `?` as a filename wildcard.

Extract one frame for a visual QC contact point:

```bash
ffmpeg -hide_banner -nostdin -y -i work/vertical.mp4 \
  -ss 2 -frames:v 1 -update 1 work/qc-frame.png
```

A still frame can reveal geometry or caption placement problems, but it does not replace full-speed playback with sound.
