# Chapter 15 — PowerShell command sheet

Run these one-line commands in order from the repository root with the environment active.

```powershell
New-Item -ItemType Directory -Force work/ch15
```

```powershell
ffprobe -v error -show_streams -show_format -of json examples/fixtures/sample-podcast.mp4
```

```powershell
ffmpeg -hide_banner -nostdin -n    -i examples/fixtures/sample-podcast.mp4    -ss 1 -t 4 -map 0:v:0 -map '0:a:0?'    -c:v libx264 -crf 20 -pix_fmt yuv420p    -c:a aac -b:a 192k -movflags +faststart work/ch15/cut.mp4
```

```powershell
clipkit cut --input examples/fixtures/sample-podcast.mp4 --output work/ch15/kit-cut.mp4 --start 1 --duration 4
```

```powershell
ffmpeg -hide_banner -nostdin -n -i work/ch15/cut.mp4    -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1"    -map 0:v:0 -map '0:a:0?' -c:v libx264 -crf 20    -pix_fmt yuv420p -c:a aac -b:a 192k    -movflags +faststart work/ch15/crop.mp4
```

```powershell
clipkit vertical --input work/ch15/cut.mp4 --output work/ch15/kit-crop.mp4 --mode crop
```

```powershell
ffmpeg -hide_banner -nostdin -n -i work/ch15/cut.mp4    -vf "scale=1080:1920:force_original_aspect_ratio=decrease:force_divisible_by=2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1"    -map 0:v:0 -map '0:a:0?' -c:v libx264 -crf 20    -pix_fmt yuv420p -c:a aac -b:a 192k    -movflags +faststart work/ch15/pad.mp4
```

```powershell
clipkit vertical --input work/ch15/cut.mp4 --output work/ch15/kit-pad.mp4 --mode pad
```

```powershell
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate -show_entries format=duration -of json work/ch15/crop.mp4
```

```powershell
ffmpeg -hide_banner -nostdin -n -i work/ch15/crop.mp4 -ss 2 -frames:v 1 -update 1 work/ch15/frame.png
```

```powershell
ffmpeg -hide_banner -nostdin -n    -i examples/fixtures/sample-podcast.mp4    -ss 1 -t 4    -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1"    -map 0:v:0 -map '0:a:0?' -c:v libx264 -crf 20    -pix_fmt yuv420p -c:a aac -b:a 192k    -movflags +faststart work/ch15/one-pass.mp4
```

```powershell
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate -show_entries format=duration -of json work/ch15/one-pass.mp4
```

```powershell
ffmpeg -v error -nostdin -i work/ch15/one-pass.mp4 -map 0:v:0 -map '0:a:0?' -f null -
```
