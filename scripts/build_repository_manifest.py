#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import io
import re
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
    # Reset-book chapter map. Keep this before legacy branches until all support
    # material has been revised; no archived chapter numbers reach the manifest.
    exact = {
        "AGENTS.md": ("17", "Codex project instructions"),
        "CLAUDE.md": ("18", "Claude Code project instructions"),
        "templates/first-week-plan.md": ("3", "First-week practice plan"),
        "templates/mini-portfolio.md": ("3;21", "Starter portfolio"),
        "templates/page-study-sheet.csv": ("6", "Study page formats"),
        "templates/automation-labor-audit.md": ("27", "Measure work before handing it off"),
        "templates/candidate-slate.csv": ("4;11;13", "Checked clip list"),
        "templates/content-calendar.csv": ("13;25", "Posting calendar"),
        "templates/final-playback-review.md": ("1;10;19;27", "Playback checklist"),
        "templates/printable-master-checklist.md": ("1;19;Resource Pack", "Printable workflow checklist"),
        "templates/glossary.csv": ("Resource Pack", "Plain-English terms"),
        "templates/analytics-decision-sheet.md": ("25", "Twenty-minute goal-based analytics review"),
        "templates/transcript-check-log.csv": ("11", "Two-pass transcript correction log"),
        "templates/caption-retime-exercise.csv": ("16", "Internal-cut subtitle timing arithmetic"),
        "templates/slate-repair.md": ("13", "Repair unsupported or duplicate clip ideas"),
        "templates/ffmpeg-cut-sheet.csv": ("15", "Source clock and duration worksheet"),
        "templates/business/multi-creator-week.csv": ("26", "Three-creator weekly capacity exercise"),
        "templates/business/creator-style-card.md": ("26;27", "Repeatable creator-specific style handoff"),
        "templates/business/team-trial-log.csv": ("27", "Paid task trial and owner review-time log"),
        "templates/business/theme-page-test.csv": ("23", "Six-post niche page exercise"),
        "templates/business/extra-income-ledger.csv": ("23", "Separate pending confirmed and received affiliate amounts"),
        "templates/business/small-team-handoff.md": ("24", "Small-team weekly handoff"),
        "templates/business/job-time-log.csv": ("20;24;27", "Full job time accounting"),
        "templates/business/payment-tracker.csv": ("20;22;24", "Invoice and cash collection record"),
        "templates/business/posting-service-sheet.csv": ("22", "Separate edited files from account placements"),
        "templates/business/prospect-scorecard.csv": ("21", "Four-point prospect fit check"),
        "docs/setup-checks.md": ("14", "Exact four-layer setup diagnostics"),
        "docs/ffmpeg-one-pass-lab.md": ("15", "Exact combined cut crop probe and decode exercise"),
        "prompts/repair-clip-slate.md": ("13", "Source-grounded slate repair prompt"),
    }
    if path in exact:
        return exact[path]
    command_chapter = re.fullmatch(r"docs/book-commands/chapter-(\d+)(?:-powershell)?\.md", path)
    if command_chapter:
        chapter = int(command_chapter.group(1))
        return ("Resource Pack" if chapter == 28 else str(chapter), "Exact chapter commands")
    groups = [
        ("prompts/codex/", "17", "Codex task or review prompt"),
        ("prompts/claude/", "18", "Claude Code task or review prompt"),
        (".claude/", "18", "Claude Code settings"),
        ("prompts/", "11;12;13", "AI editing and packaging prompt"),
        ("templates/business/", "20;21;22;23;24;26;27", "Business worksheet"),
        ("templates/resolve/", "7;8;9;10", "Resolve workflow reference"),
        ("templates/destinations/", "19;25", "Output packaging specification"),
        ("templates/", "3;4;6;10;13;19;25;26;27", "Reusable editing or production worksheet"),
        ("examples/first-clip/", "1;2;7;8;9;10", "Original phone-recording exercise"),
        ("examples/portfolio-practice/", "3", "Original portfolio recording exercises"),
        ("examples/clip-structure/", "2;5", "Three-version editing and paper-edit exercise"),
        ("examples/clip-room/", "11;12;13", "Fictional transcript-style text exercise"),
        ("examples/fixtures/", "14;15;16;19", "Synthetic patterns and tones for code tests"),
        ("examples/resolve", "7;8;9;10", "Manual editing example"),
        ("examples/agent-task-codex/", "17", "Codex practice task"),
        ("examples/agent-task-claude/", "18", "Claude Code practice task"),
        ("examples/agent-clip-plan/", "17;18", "Checked moments planner and isolated clock-repair lab"),
        ("examples/end-to-end/", "19", "Complete local pipeline"),
        ("examples/pipeline-repair/", "19", "Missing-caption failure and exact resume exercise"),
        ("examples/batch-production/", "16;26", "Batch production exercise"),
        ("examples/multi-creator-batch/", "26", "Five-job failure and resume exercise"),
        ("examples/analytics", "25", "Synthetic analytics exercise"),
        ("examples/", "6;13;15;16;19", "Adaptable source-format example"),
        ("docs/codex", "17", "Codex workflow documentation"),
        ("docs/claude", "18", "Claude Code workflow documentation"),
        ("docs/transcription", "11;16", "Local transcription setup"),
        ("docs/speaker", "11", "Speaker-label checks"),
        ("docs/ffmpeg", "14;15;16", "FFmpeg setup and recipes"),
        ("docs/yt-dlp", "16", "yt-dlp setup and source preparation"),
        ("docs/pipeline", "19", "Pipeline and recovery instructions"),
        ("docs/file-organization", "26", "Organize multi-creator jobs"),
        ("docs/output-naming", "26", "Output-name rules"),
        ("docs/", "14;19;Resource Pack", "Installation and operational reference"),
        ("src/clipkit/transcript", "11;16", "Transcription code"),
        ("src/clipkit/candidates", "11;13", "Candidate validation and scoring code"),
        ("src/clipkit/batch", "16;26", "Batch code"),
        ("src/clipkit/pipeline", "19", "Pipeline code"),
        ("src/clipkit/", "14;15;16;19", "Clipkit implementation"),
        ("scripts/hooks/", "18", "Claude Code hook example"),
        ("scripts/", "14;15;16;17;18;19", "Runnable wrapper or maintenance script"),
        ("tests/", "14;15;16;17;18;19", "Automated test source; run suite for results"),
        ("schemas/", "11;13;16;19", "Structured data reference"),
    ]
    for prefix, chapters, purpose in groups:
        if path.startswith(prefix):
            return chapters, purpose
    return "14;Resource Pack", "Repository orientation, configuration, or support file"


def archived_mapping(path: str) -> tuple[str, str]:
    """Historical reference only; never used in the active book manifest."""
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
            status = "test source; execution recorded separately"
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
