# Changelog

All notable changes to Clipkit are documented here. The project uses semantic versioning.

## 0.1.0

Initial public companion release for *The AI Clipping Playbook*.

### Included

- Local Python CLI with stable JSON output and explicit exit codes.
- FFmpeg-backed cutting, vertical conversion, caption, audio, and batch workflows.
- Transcript, candidate, speaker, QC, package, and run-state validation.
- Human approval gates with no upload, scheduling, or publishing command.
- Rights-safe generated fixtures and six reusable workflow examples.
- ChatGPT, Codex, and Claude Code prompts and agent task contracts.
- macOS and Windows installation guidance, troubleshooting, and automated tests.

### Known limits

- Windows instructions are documented but were not clean-machine tested for this release.
- Native FFmpeg subtitle-filter support depends on the installed FFmpeg build; Clipkit includes a tested raster-caption fallback.
- Authenticated model quality, paid API behavior, live media retrieval, and publishing behavior are outside the verified release scope.
