from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from clipkit.settings import Settings


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "examples" / "fixtures"


@pytest.fixture(scope="session")
def repository_root() -> Path:
    return ROOT


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    required = FIXTURES / "sample-podcast.mp4"
    if not required.is_file():
        pytest.fail("Generate fixtures first: python scripts/generate_fixtures.py")
    return FIXTURES


@pytest.fixture
def media_settings(tmp_path: Path) -> Settings:
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if not ffmpeg or not ffprobe:
        pytest.skip("FFmpeg and ffprobe are required for media integration tests")
    return Settings(
        work_root=tmp_path,
        ffmpeg=ffmpeg,
        ffprobe=ffprobe,
        width=180,
        height=320,
        crf=28,
        preset="ultrafast",
        batch_jobs=2,
    )
