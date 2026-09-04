# Installation index

1. Read [required software](required-software.md).
2. Follow [macOS installation](macos-install.md) or [Windows installation](windows-install.md).
3. Verify FFmpeg with [FFmpeg setup](ffmpeg.md).
4. Add optional [yt-dlp](yt-dlp.md), [transcription](transcription.md), [Codex](codex-workflow.md), or [Claude Code](claude-code-workflow.md) only when the workflow needs them.
5. Run `clipkit doctor`, generate fixtures, and run `python -m pytest`.

The offline core needs no API key. A clean core installation should be able to run generated-fixture tests without network access after dependencies are installed.
