# One-pass cut and crop — Chapter 15 add-on

Run the main Chapter 15 lab first so `work/ch15` exists. Use an active project
environment at the repository root. These exact commands use generated test
patterns and tones, not speech. Existing outputs are not overwritten.

```bash
ffmpeg -hide_banner -nostdin -n \
  -i examples/fixtures/sample-podcast.mp4 \
  -ss 1 -t 4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1" \
  -map 0:v:0 -map '0:a:0?' -c:v libx264 -crf 20 \
  -pix_fmt yuv420p -c:a aac -b:a 192k \
  -movflags +faststart work/ch15/one-pass.mp4
```

```bash
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate -show_entries format=duration -of json work/ch15/one-pass.mp4
```

```bash
ffmpeg -v error -nostdin -i work/ch15/one-pass.mp4 -map 0:v:0 -map '0:a:0?' -f null -
```

Expect H.264 video, AAC audio, 1080 × 1920, and about four seconds. The final
command decodes to a discarded output and should report no error for the
fixture. Neither probing nor decoding substitutes for full visual/audio review.
One-pass and two-pass files need not have matching bytes.

Windows users: use the generated one-line Chapter 15 PowerShell sheet.
