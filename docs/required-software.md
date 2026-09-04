# Required software

| Component | Status | Used for | Verify |
|---|---|---|---|
| Python 3.11+ | Required | Clipkit, schemas, tests | `python --version` |
| FFmpeg | Required | Rendering and fixture generation | `ffmpeg -version` |
| ffprobe | Required | Media inspection and QC | `ffprobe -version` |
| Git | Recommended | Version control and later repository use | `git --version` |
| yt-dlp | Optional | Authorized metadata-only retrieval | `yt-dlp --version` |
| OpenAI Whisper | Optional | Local transcription | `whisper --help` |
| Codex CLI | Optional | Bounded repository automation | `codex --version` |
| Claude Code | Optional | Bounded repository automation | `claude --version` |
| DaVinci Resolve | Optional/manual | Detailed manual editing and review | Verify inside Resolve |

`clipkit doctor` reports the available tools and FFmpeg capabilities. It does not install software, authenticate accounts, or print credential values.

Use current official installers and documentation: [Python](https://www.python.org/downloads/), [FFmpeg](https://ffmpeg.org/download.html), [yt-dlp](https://github.com/yt-dlp/yt-dlp/wiki/Installation), [OpenAI Whisper](https://github.com/openai/whisper), [OpenAI Codex CLI](https://learn.chatgpt.com/docs/codex/cli), and [Claude Code](https://code.claude.com/docs/en/quickstart).
