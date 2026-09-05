# Clip It & Cash In — Free Companion Pack

Make a clip. Improve it. Build a small offer around it.

This is the buyer pack for **Clip It & Cash In** by **Vidlly Media**. It includes recording exercises, editing checklists, AI prompts, business worksheets, and Clipkit: the book's local video-command tool.

**New to clipping?** Start with the [first-clip recording exercise](examples/first-clip/README.md). Open your video in DaVinci Resolve and follow Chapter 1. You do not need Python, a paid AI plan, or an API key for that route.

**Ready for automation?** Start with the [beginner walkthrough](docs/beginner-walkthrough.md), then use the commands in Chapters 14–19.

## Pick what you need

| Your next job | Open this |
|---|---|
| Record material for your first clip | [First-clip exercise](examples/first-clip/README.md) |
| Build three practice portfolio pieces | [Portfolio recording exercises](examples/portfolio-practice/README.md) |
| Find stronger moments | [Five-point moment worksheet](templates/moment-finder.csv) |
| Study a niche | [Page-study sheet](templates/page-study-sheet.csv) |
| Ask AI for ideas | [Prompt folder](prompts/) |
| Install the command tools | [macOS](docs/macos-install.md) · [Windows](docs/windows-install.md) |
| Copy a command from the book | [Exact chapter command sheets](docs/book-commands/) |
| Test a Codex task | [Codex exercise](examples/agent-task-codex/README.md) |
| Test a Claude Code task | [Claude Code exercise](examples/agent-task-claude/README.md) |
| Build a real cut planner | [Planner and clock-time repair](examples/agent-clip-plan/README.md) |
| Resume a failed video job | [Pipeline repair lab](examples/pipeline-repair/README.md) |
| Cut and crop in one render | [One-pass FFmpeg lab](docs/ffmpeg-one-pass-lab.md) |
| Price or pitch a small service | [Business worksheets](templates/business/) |
| Fix a failed command | [Troubleshooting](docs/troubleshooting.md) |

## The command-tool route

Clipkit can cut video, make vertical versions, burn captions, process audio, and run batches. Everything stays on your computer. It does not upload or post your files.

Install Python 3.11 or newer, FFmpeg, and ffprobe using the [software guide](docs/required-software.md). Then open a terminal in this repository's top folder.

On macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python scripts/generate_fixtures.py
clipkit doctor
python -m pytest
```

On Windows, use the [PowerShell installation steps](docs/windows-install.md). If script activation is blocked, that guide shows how to call the environment's programs directly.

The generated fixtures are **patterns and tones for code tests**. They are not conversations, gaming highlights, or portfolio work. Use your own recordings for the manual-editing exercises.

## Try a complete local job

Preview the job, then render it:

```bash
clipkit run --manifest examples/end-to-end/job.yaml --dry-run
clipkit run --manifest examples/end-to-end/job.yaml
clipkit qc --batch work/end-to-end/run-state.json
```

Watch the finished files. Check the cut, crop, captions, and sound. After full playback:

```bash
clipkit approve --run work/end-to-end/run-state.json --reviewer "your name" --notes "full playback complete"
clipkit package --run work/end-to-end/run-state.json --destination generic-vertical --output work/end-to-end-package
clipkit validate-package --path work/end-to-end-package
```

Here, `approve` records your local playback check so the files can be packaged. It does not post anything or grant rights to a source.

## What lives where

| Folder | What's inside |
|---|---|
| `docs/` | Setup, command help, and troubleshooting |
| `examples/` | Recording exercises, sample jobs, and test fixtures |
| `prompts/` | Copy-ready instructions for AI tools |
| `templates/` | Editing, planning, and business sheets |
| `src/clipkit/` | The Python program |
| `tests/` | Checks for important behavior |
| `work/` | Your generated practice outputs; ignored by Git |

[`REPOSITORY_MANIFEST.csv`](REPOSITORY_MANIFEST.csv) maps the files to book chapters. [.env.example](.env.example) lists optional settings without real secrets. Basic practice commands need no API key.

## Versions and downloads

Use **v0.2.0** with *Clip It & Cash In*. [Download the matching release](https://github.com/Heheboy2023/ai-clipping-playbook/releases/tag/v0.2.0). The older v0.1.0 archive served the former manuscript and does not contain these chapter sheets. Local verification: 97 automated tests passed on macOS; Windows setup is documented but not clean-machine tested.

Published archives appear on [GitHub Releases](https://github.com/Heheboy2023/ai-clipping-playbook/releases). Source downloads do not contain a Python environment, private media, or generated work. Run setup and tests after downloading.

## Keep the work useful

- Compare AI suggestions with the actual source. A score does not predict views or income.
- Use the original recording exercises when you need practice material. Keep private client files out of this public project.
- Do not put passwords or API keys in prompts, screenshots, issues, or commits.
- Read the command before running it. Use a small test job before a large batch.

Code is available under the [MIT License](LICENSE). For reporting a sensitive bug, see [SECURITY.md](SECURITY.md).
