from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest


def run(command: list[str]) -> None:
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    assert completed.returncode == 0, completed.stderr


def test_documented_optional_maps_are_shell_quoted(repository_root: Path) -> None:
    documentation = (repository_root / "docs" / "ffmpeg-commands.md").read_text()
    assert re.search(r"-map\s+0:[vasd]:\d+\?", documentation) is None
    assert "-map '0:a:0?'" in documentation


def test_caption_documentation_has_a_build_safe_fallback(repository_root: Path) -> None:
    documentation = (repository_root / "docs" / "ffmpeg-commands.md").read_text()
    assert "requires an FFmpeg build with the `subtitles` filter" in documentation
    assert "ffmpeg -hide_banner -filters" in documentation
    assert "clipkit captions burn" in documentation


@pytest.mark.integration
def test_stream_copy_rotation_blur_and_pip(fixtures_dir: Path, media_settings, tmp_path: Path) -> None:
    ffmpeg = media_settings.ffmpeg
    source = str(fixtures_dir / "sample-youtube.mp4")
    stream_copy = tmp_path / "stream-copy.mp4"
    rotated = tmp_path / "rotated.mp4"
    blurred = tmp_path / "blurred.mp4"
    pip = tmp_path / "pip.mp4"
    run([ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin", "-y", "-i", source, "-ss", "0", "-t", "2", "-map", "0:v:0?", "-map", "0:a:0?", "-c", "copy", str(stream_copy)])
    run([ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin", "-y", "-noautorotate", "-i", source, "-t", "2", "-vf", "transpose=clock", "-metadata:s:v:0", "rotate=0", "-c:v", "libx264", "-c:a", "aac", str(rotated)])
    run([ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin", "-y", "-i", source, "-t", "2", "-filter_complex", "[0:v]split=2[bg][fg];[bg]scale=180:320:force_original_aspect_ratio=increase,crop=180:320,boxblur=10:1[bgv];[fg]scale=180:320:force_original_aspect_ratio=decrease[fgv];[bgv][fgv]overlay=(W-w)/2:(H-h)/2[v]", "-map", "[v]", "-map", "0:a:0?", "-c:v", "libx264", "-c:a", "aac", "-shortest", str(blurred)])
    run([ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin", "-y", "-i", str(fixtures_dir / "sample-livestream.mp4"), "-i", source, "-filter_complex", "[1:v]scale=80:-2[pip];[0:v][pip]overlay=W-w-10:10[v]", "-map", "[v]", "-map", "0:a:0?", "-t", "2", "-c:v", "libx264", "-c:a", "aac", str(pip)])
    assert all(path.is_file() and path.stat().st_size > 0 for path in [stream_copy, rotated, blurred, pip])
