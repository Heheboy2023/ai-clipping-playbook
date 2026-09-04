# Configuration

Copy `clipkit.example.toml` to `clipkit.toml` in the working directory, then change only settings your environment requires. `clipkit.toml` is ignored so machine-specific paths do not leak into commits.

```toml
[paths]
work_root = "work"
ffmpeg = "ffmpeg"
ffprobe = "ffprobe"
yt_dlp = "yt-dlp"
whisper = "whisper"

[video]
width = 1080
height = 1920
crf = 20
preset = "medium"

[batch]
jobs = 2
```

Pass a non-default file before the subcommand:

```bash
clipkit --config /absolute/path/to/clipkit.toml doctor
```

Supported environment overrides are `CLIPKIT_WORK_ROOT`, `CLIPKIT_FFMPEG`, `CLIPKIT_FFPROBE`, `CLIPKIT_YTDLP`, and `CLIPKIT_WHISPER`. `.env.example` also names optional agent/service variables but Clipkit does not load `.env` automatically.

Never commit `.env`, access tokens, cookies, account exports, or client credentials. `clipkit doctor` reports only whether selected variables are present.
