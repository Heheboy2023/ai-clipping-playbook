# Changelog

All notable changes to Clipkit are documented here. The project uses semantic versioning.

## 0.2.0

Companion pack for *Clip It & Cash In*.

- Reorganized the reader path around an immediate first clip and the reset book's 27 chapters.
- Added original recording exercises, chapter command sheets, AI slate repair, transcript checks, and business worksheets.
- Added tested cut-planner and clock-time repair exercises for Codex and Claude Code; reference implementations are not claims of authenticated model runs.
- Added a reproducible broken-caption pipeline repair lab with resume and QC inspection.
- Repaired stale-output reuse, incomplete-run approval, changed-file packaging, duplicate output handling, caption text truncation, and nonfinite caption times.
- Added diagnostics, one-pass FFmpeg commands, caption-retiming math, and workflow-template checks.
- Expanded the suite to 97 passing tests on macOS. Windows remains documented, not clean-machine verified.

### Migration

Commands retain their earlier names. Generate fixtures after installation. Old work folders do not become approved automatically: rerun QC and review the actual outputs. Use the new chapter command sheets for this book; the earlier release served the former manuscript.

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
