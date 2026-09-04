# macOS installation

These commands assume Homebrew is already installed. If it is not, use the current instructions at [brew.sh](https://brew.sh/) instead of copying an unofficial installer.

```bash
brew install python ffmpeg yt-dlp
python3 --version
ffmpeg -version
ffprobe -version
yt-dlp --version
```

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python scripts/generate_fixtures.py
clipkit doctor
python -m pytest
```

Optional local transcription:

```bash
python -m pip install -e ".[transcription]"
whisper --help
```

Optional coding agents:

```bash
npm install -g @openai/codex@latest
codex --version
brew install --cask claude-code
claude --version
```

Agent installation does not imply authentication or permission to change the repository. Follow the bounded workflows in `docs/codex-workflow.md` and `docs/claude-code-workflow.md`.
