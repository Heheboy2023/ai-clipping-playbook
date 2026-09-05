from __future__ import annotations

import json
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.integration
def test_ch15_exact_documented_commands(repository_root: Path, fixtures_dir: Path, tmp_path: Path) -> None:
    source = tmp_path / "examples" / "fixtures"
    source.mkdir(parents=True)
    shutil.copy2(fixtures_dir / "sample-podcast.mp4", source / "sample-podcast.mp4")
    doc = (repository_root / "docs" / "reset-ffmpeg-lab.md").read_text()
    blocks = re.findall(r"```bash\n(.*?)```", doc, re.S)
    assert len(blocks) == 10
    for block in blocks:
        args = shlex.split(block.replace("\\\n", " "))
        assert args[0] in {"mkdir", "ffmpeg", "ffprobe", "clipkit"}
        if args[0] == "clipkit":
            args = [sys.executable, "-m", "clipkit", *args[1:]]
        result = subprocess.run(args, cwd=tmp_path, capture_output=True, text=True, timeout=120)
        assert result.returncode == 0, result.stderr
    for name in ("crop.mp4", "pad.mp4", "kit-crop.mp4", "kit-pad.mp4"):
        result = subprocess.run([
            "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json",
            str(tmp_path / "work" / "ch15" / name),
        ], check=True, capture_output=True, text=True)
        probe = json.loads(result.stdout)
        video = next(stream for stream in probe["streams"] if stream["codec_type"] == "video")
        assert (video["width"], video["height"]) == (1080, 1920)
        assert any(stream["codec_type"] == "audio" for stream in probe["streams"])
        assert abs(float(probe["format"]["duration"]) - 4.0) < 0.15
    assert (tmp_path / "work" / "ch15" / "frame.png").is_file()


def command_blocks(repository_root, chapter):
    doc = (repository_root / f"docs/book-commands/chapter-{chapter}.md").read_text()
    return re.findall(r"```bash\n(.*?)```", doc, re.S)


def run_clipkit(block, cwd):
    args = shlex.split(block.replace("\\\n", " "))
    assert args[0] == "clipkit"
    # Recorded approval here is a test of the state machine, not human playback.
    if "approve" in args:
        args[args.index("--reviewer") + 1] = "automated fixture test"
        args[args.index("--notes") + 1] = "simulated review for packaging test only"
    result = subprocess.run([sys.executable, "-m", "clipkit", *args[1:]],
                            cwd=cwd, capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stdout + result.stderr
    return result


@pytest.mark.integration
def test_ch16_local_command_sheet(repository_root, fixtures_dir, tmp_path):
    shutil.copytree(fixtures_dir, tmp_path / "examples/fixtures")
    shutil.copytree(repository_root / "examples/batch-production", tmp_path / "examples/batch-production",
                    ignore=shutil.ignore_patterns(".clipkit-batch-state.json"))
    used = 0
    for block in command_blocks(repository_root, "16"):
        if block.startswith(("clipkit captions", "clipkit vertical", "clipkit audio", "clipkit batch")):
            run_clipkit(block, tmp_path)
            used += 1
    assert used == 7
    assert (tmp_path / "work/ch16/final.mp4").is_file()
    assert len(list((tmp_path / "work/batch-production").glob("*"))) == 3


@pytest.mark.integration
def test_ch19_exact_cli_chain(repository_root, fixtures_dir, tmp_path):
    shutil.copytree(fixtures_dir, tmp_path / "examples/fixtures")
    shutil.copytree(repository_root / "examples/end-to-end", tmp_path / "examples/end-to-end")
    blocks = command_blocks(repository_root, "19")
    assert len(blocks) == 12
    for block in blocks[:8]:
        run_clipkit(block, tmp_path)
    package = tmp_path / "work/end-to-end-package"
    assert (package / "media/04-final.mp4").is_file()
    state = json.loads((tmp_path / "work/end-to-end/run-state.json").read_text())
    assert len(state["steps"]) == 4
    assert all(item["resumed"] for item in state["steps"])
    assert state["approvals"] == [], "resuming must clear the previous playback review"


@pytest.mark.integration
def test_resource_pack_exact_commands(repository_root, fixtures_dir, tmp_path):
    shutil.copytree(fixtures_dir, tmp_path / "examples/fixtures")
    shutil.copytree(repository_root / "examples/batch-production", tmp_path / "examples/batch-production",
                    ignore=shutil.ignore_patterns(".clipkit-batch-state.json"))
    blocks = command_blocks(repository_root, "28")
    assert len(blocks) == 7
    for block in blocks:
        if block.startswith("clipkit"):
            run_clipkit(block, tmp_path)
        else:
            args = shlex.split(block.replace("\\\n", " "))
            assert args[0] == "ffprobe"
            subprocess.run(args, cwd=tmp_path, capture_output=True, check=True, timeout=30)
    for name in ("cut", "crop", "pad", "caption-test", "audio"):
        assert (tmp_path / f"work/pack/{name}.mp4").is_file()
    for name in ("crop", "pad"):
        result = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-of", "json",
                                 str(tmp_path / f"work/pack/{name}.mp4")],
                                capture_output=True, text=True, check=True)
        video = next(s for s in json.loads(result.stdout)["streams"] if s["codec_type"] == "video")
        assert (video["width"], video["height"]) == (1080, 1920)
