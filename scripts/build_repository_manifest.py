#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import io
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "REPOSITORY_MANIFEST.csv"
EXCLUDED_PARTS = {
    ".git",
    ".venv",
    ".pytest_cache",
    "__pycache__",
    ".clipkit-trash",
    "work",
    "ai_clipping_playbook_clipkit.egg-info",
}


def mapping(path: str) -> tuple[str, str]:
    if path == "LOCAL_RELEASE_MANIFEST.md":
        return "Appendix D; Appendix E", "Local verification and release-state record"
    if path == "REPOSITORY_MANIFEST.csv":
        return "21; Appendix D", "Generated repository-to-chapter map"
    if path in {"README.md", "LICENSE", "SECURITY.md", "CHANGELOG.md"}:
        return "Front matter; 21; Appendix D", "Repository orientation, license, or security policy"
    if path in {"AGENTS.md", "CLAUDE.md"} or path.startswith(".claude/"):
        return "21–24", "Agent instruction and permission contract"
    if path in {"pyproject.toml", "uv.lock", "Makefile", ".gitignore", ".env.example", "clipkit.example.toml"}:
        return "21; Appendix D", "Installation, configuration, or reproducibility control"
    if path.startswith("prompts/codex/"):
        return "22; 24", "Codex workflow prompt"
    if path.startswith("prompts/claude/"):
        return "23; 24", "Claude Code workflow prompt"
    if path.startswith("prompts/"):
        return "9–11; 17–18", "Transcript, moment, caption, or review prompt"
    if path.startswith("schemas/"):
        return "3; 9–10; 17–25", "Machine-readable workflow contract"
    if path.startswith("templates/destinations/"):
        return "25", "Destination packaging template"
    if path == "templates/printable-master-checklist.md":
        return "Appendix A", "Printable end-to-end quality checklist"
    if path == "templates/glossary.csv":
        return "Appendix C", "Book and repository glossary data"
    if path.startswith("templates/"):
        return "2–3; 9–10; 15; 18; 20–28", "Reusable workflow or review template"
    if path.startswith("examples/fixtures/"):
        return "3–5; 10; 15–25", "Rights-safe generated test fixture"
    if path.startswith("examples/podcast/"):
        return "4; 9–25", "Podcast clipping example"
    if path.startswith("examples/youtube-video/"):
        return "5; 9–25", "Authorized/local YouTube-style example"
    if path.startswith("examples/livestream/"):
        return "5; 9–25", "Livestream clipping example"
    if path.startswith("examples/gaming/"):
        return "5; 9; 14; 19–25", "Gaming clipping example"
    if path.startswith("examples/multi-speaker-podcast/"):
        return "4; 10; 14–25", "Multi-speaker podcast example"
    if path.startswith("examples/batch-production/"):
        return "20; 24", "Batch production example"
    if path.startswith("examples/end-to-end/"):
        return "24–25", "Complete local pipeline example"
    if path.startswith("examples/"):
        return "3–25", "Reusable example or expected output"
    if path.startswith("docs/macos") or path.startswith("docs/windows") or path.startswith("docs/required") or path.startswith("docs/installation"):
        return "21; Appendix D", "Installation guidance"
    if path.startswith("docs/ffmpeg"):
        return "19–20", "FFmpeg installation, commands, and verification"
    if path.startswith("docs/yt-dlp") or path.startswith("docs/authorized"):
        return "3; 5; 20", "Permission-aware yt-dlp guidance"
    if path.startswith("docs/transcription"):
        return "10; 17", "Transcription setup and verification"
    if path.startswith("docs/codex"):
        return "22; 24", "Codex workflow documentation"
    if path.startswith("docs/claude"):
        return "23; 24", "Claude Code workflow documentation"
    if path.startswith("docs/pipeline") or path.startswith("docs/data-contract"):
        return "21; 24", "Pipeline and data contract documentation"
    if path.startswith("docs/publishing"):
        return "25", "Local-only packaging boundary"
    if path == "docs/update-policy.md":
        return "Appendix E", "Book and repository synchronization policy"
    if path.startswith("docs/"):
        return "3; 19–25; Appendix D", "Operational documentation"
    if path.startswith("src/clipkit/project"):
        return "3", "Project intake and file organization implementation"
    if path.startswith("src/clipkit/transcript"):
        return "10; 17", "Transcription implementation"
    if path.startswith("src/clipkit/candidates"):
        return "9; 17–18", "Candidate validation and scoring implementation"
    if path.startswith("src/clipkit/captions"):
        return "10; 15; 17; 20", "Caption generation implementation"
    if path.startswith("src/clipkit/media") or path.startswith("src/clipkit/operations") or path.startswith("src/clipkit/render"):
        return "15; 19–20; 22–24", "FFmpeg-backed media implementation"
    if path.startswith("src/clipkit/batch"):
        return "20; 24", "Batch implementation"
    if path.startswith("src/clipkit/pipeline") or path.startswith("src/clipkit/qc"):
        return "24", "Pipeline state, approval, and QC implementation"
    if path.startswith("src/clipkit/package"):
        return "25–26", "Local packaging and mechanical brand audit"
    if path.startswith("src/clipkit/retrieve"):
        return "3; 5; 20", "Sanitized metadata retrieval implementation"
    if path.startswith("src/clipkit/doctor") or path.startswith("src/clipkit/settings"):
        return "21", "Environment and configuration implementation"
    if path.startswith("src/clipkit/"):
        return "21–25", "Core Clipkit command infrastructure"
    if path.startswith("scripts/hooks/"):
        return "23–24", "Agent output-root safety hook"
    if path.startswith("scripts/clipkit/"):
        return "17–25", "Thin runnable chapter wrapper"
    if path.startswith("scripts/"):
        return "3; 19–24; Appendix D", "Fixture, manifest, or maintenance script"
    if path.startswith("tests/"):
        return "17–25", "Automated verification"
    return "21; Appendix D", "Repository support file"


def rows() -> list[dict[str, str]]:
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in EXCLUDED_PARTS for part in path.parts):
            continue
        relative = path.relative_to(ROOT).as_posix()
        chapters, purpose = mapping(relative)
        suffix = path.suffix.lower()
        status = "generated fixture" if relative.startswith("examples/fixtures/") and suffix in {".mp4", ".wav"} else "implemented"
        if relative.startswith("docs/") or relative.startswith("prompts/") or relative.startswith("templates/"):
            status = "documented"
        if relative.startswith("tests/"):
            status = "tested by suite"
        files.append(
            {
                "path": relative,
                "chapters": chapters,
                "purpose": purpose,
                "status": status,
            }
        )
    if "REPOSITORY_MANIFEST.csv" not in {item["path"] for item in files}:
        chapters, purpose = mapping("REPOSITORY_MANIFEST.csv")
        files.append({"path": "REPOSITORY_MANIFEST.csv", "chapters": chapters, "purpose": purpose, "status": "generated"})
    return sorted(files, key=lambda item: item["path"])


def render() -> str:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=["path", "chapters", "purpose", "status"])
    writer.writeheader()
    writer.writerows(rows())
    return output.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the repository chapter manifest.")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = render()
    if args.check:
        if not TARGET.is_file() or TARGET.read_bytes() != content.encode("utf-8"):
            print("REPOSITORY_MANIFEST.csv is out of date")
            return 1
        print("REPOSITORY_MANIFEST.csv is current")
        return 0
    TARGET.write_text(content, encoding="utf-8", newline="")
    print(f"wrote {TARGET} with {len(rows())} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
