from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_agent_contracts_prohibit_publishing(repository_root: Path) -> None:
    for relative in ["AGENTS.md", "CLAUDE.md", "prompts/codex/task-contract.md", "prompts/claude/task-contract.md"]:
        text = (repository_root / relative).read_text(encoding="utf-8").lower()
        assert "publish" in text
        assert any(word in text for word in ["never", "forbidden", "prohibited", "not allowed"])


def test_documented_agent_commands_preserve_review_boundaries(repository_root: Path) -> None:
    codex_files = [
        "docs/codex-workflow.md",
        "prompts/codex/task-contract.md",
    ]
    for relative in codex_files:
        text = (repository_root / relative).read_text(encoding="utf-8")
        assert "codex exec -C ." in text
        assert "--sandbox workspace-write" in text
        assert "--ephemeral" in text
        assert "--json" in text

    claude_files = [
        "docs/claude-code-workflow.md",
        "prompts/claude/task-contract.md",
    ]
    for relative in claude_files:
        text = (repository_root / relative).read_text(encoding="utf-8")
        assert "claude -p" in text
        assert "--permission-mode plan" in text
        assert "--output-format json" in text
        assert "--no-session-persistence" in text


def test_agent_docs_use_current_official_documentation_roots(repository_root: Path) -> None:
    combined = "\n".join(
        (repository_root / relative).read_text(encoding="utf-8")
        for relative in [
            "docs/codex-workflow.md",
            "docs/claude-code-workflow.md",
            "docs/required-software.md",
            "docs/windows-install.md",
        ]
    )
    assert "learn.chatgpt.com/docs/codex" in combined
    assert "code.claude.com/docs/en" in combined
    assert "docs.anthropic.com/en/docs/claude-code/setup" not in combined


def test_claude_permission_file_denies_push(repository_root: Path) -> None:
    settings = json.loads((repository_root / ".claude/settings.json").read_text(encoding="utf-8"))
    denied = " ".join(settings["permissions"]["deny"])
    assert "git push" in denied
    assert "rm -rf" in denied


def test_output_root_hook(repository_root: Path, tmp_path: Path) -> None:
    script = repository_root / "scripts" / "hooks" / "validate_output_root.py"
    allowed = subprocess.run([sys.executable, str(script), str(tmp_path / "inside.mp4"), str(tmp_path)], capture_output=True, text=True, check=False)
    blocked = subprocess.run([sys.executable, str(script), str(tmp_path.parent / "outside.mp4"), str(tmp_path)], capture_output=True, text=True, check=False)
    assert allowed.returncode == 0
    assert blocked.returncode == 2


def test_output_root_hook_accepts_claude_hook_json(repository_root: Path, tmp_path: Path) -> None:
    script = repository_root / "scripts" / "hooks" / "validate_output_root.py"
    allowed = subprocess.run(
        [sys.executable, str(script), "--hook-root", str(tmp_path)],
        input=json.dumps({"tool_name": "Write", "tool_input": {"file_path": str(tmp_path / "inside.md")}}),
        capture_output=True,
        text=True,
        check=False,
    )
    blocked = subprocess.run(
        [sys.executable, str(script), "--hook-root", str(tmp_path)],
        input=json.dumps({"tool_name": "Edit", "tool_input": {"file_path": str(tmp_path.parent / "outside.md")}}),
        capture_output=True,
        text=True,
        check=False,
    )
    assert allowed.returncode == 0
    assert blocked.returncode == 2
