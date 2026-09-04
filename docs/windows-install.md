# Windows installation

Use 64-bit PowerShell. Install Python from [python.org](https://www.python.org/downloads/windows/) or the Microsoft Store and enable the Python launcher. Obtain FFmpeg through a build linked from the [official FFmpeg download page](https://ffmpeg.org/download.html), then add its `bin` folder to `PATH`.

yt-dlp provides an official WinGet package:

```powershell
winget install yt-dlp
py -3.11 --version
ffmpeg -version
ffprobe -version
yt-dlp --version
```

From the repository root:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python scripts\generate_fixtures.py
clipkit doctor
python -m pytest
```

If PowerShell blocks activation, do not weaken machine-wide policy. You can call `.venv\Scripts\python.exe` and `.venv\Scripts\clipkit.exe` directly.

Optional transcription:

```powershell
python -m pip install -e ".[transcription]"
whisper --help
```

Optional Claude Code installation follows Anthropic’s current WinGet guidance:

```powershell
winget install Anthropic.ClaudeCode
claude --version
```

For Codex, use the current official OpenAI CLI instructions. Verify Windows support details in the [Codex CLI documentation](https://learn.chatgpt.com/docs/codex/cli) before relying on it in production.

This project was implemented and integration-tested on macOS. The commands above are documented for Windows, but a clean Windows machine remains a separate release verification gate.
