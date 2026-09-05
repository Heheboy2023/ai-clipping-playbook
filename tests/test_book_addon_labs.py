from __future__ import annotations

import csv
import json
import re
import shlex
import shutil
import subprocess
import sys

import pytest


@pytest.mark.integration
def test_one_pass_exact_commands(repository_root, fixtures_dir, tmp_path):
    source_dir = tmp_path / "examples/fixtures"
    source_dir.mkdir(parents=True)
    shutil.copy2(fixtures_dir / "sample-podcast.mp4", source_dir)
    (tmp_path / "work/ch15").mkdir(parents=True)
    doc = (repository_root / "docs/ffmpeg-one-pass-lab.md").read_text()
    blocks = re.findall(r"```bash\n(.*?)```", doc, re.S)
    assert len(blocks) == 3
    results = []
    for block in blocks:
        args = shlex.split(block.replace("\\\n", " "))
        result = subprocess.run(args, cwd=tmp_path, capture_output=True,
                                text=True, timeout=120)
        assert result.returncode == 0, result.stderr
        results.append(result)
    probe = json.loads(results[1].stdout)
    video = next(s for s in probe["streams"] if s["codec_type"] == "video")
    audio = next(s for s in probe["streams"] if s["codec_type"] == "audio")
    assert (video["width"], video["height"], video["codec_name"]) == (1080, 1920, "h264")
    assert audio["codec_name"] == "aac"
    assert abs(float(probe["format"]["duration"]) - 4) < 0.15
    assert results[2].stderr == ""


def test_setup_diagnostic_commands(repository_root):
    doc = (repository_root / "docs/setup-checks.md").read_text()
    block, = re.findall(r"```bash\n(.*?)```", doc, re.S)
    lines = block.strip().splitlines()
    assert len(lines) == 4
    for index, line in enumerate(lines):
        args = shlex.split(line)
        assert args[0] == "python"
        result = subprocess.run([sys.executable, *args[1:]], cwd=repository_root,
                                capture_output=True, text=True, timeout=30)
        assert result.returncode == 0, result.stdout + result.stderr
        if index == 0:
            assert result.stdout.strip() == "True"


def test_reset_worksheet_column_counts_and_math(repository_root):
    paths = [
        "templates/ffmpeg-cut-sheet.csv",
        "templates/business/multi-creator-week.csv",
        "templates/business/team-trial-log.csv",
        "templates/business/theme-page-test.csv",
        "templates/business/extra-income-ledger.csv",
        "templates/business/job-time-log.csv",
        "templates/business/payment-tracker.csv",
        "templates/business/posting-service-sheet.csv",
        "templates/business/prospect-scorecard.csv",
    ]
    for name in paths:
        with (repository_root / name).open(newline="") as handle:
            rows = list(csv.reader(handle))
        assert len(rows) >= 2, name
        assert all(len(row) == len(rows[0]) for row in rows[1:]), name
    with (repository_root / paths[0]).open(newline="") as handle:
        for row in csv.DictReader(handle):
            assert float(row["end_seconds"]) - float(row["start_seconds"]) == float(row["duration_seconds"])
    with (repository_root / paths[1]).open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert sum(int(row["edit_minutes"]) for row in rows) == 330
    assert sum(int(row["review_minutes"]) for row in rows) == 140
    with (repository_root / "templates/caption-retime-exercise.csv").open(newline="") as handle:
        for row in csv.DictReader(handle):
            shift = float(row["total_removed_before_cue"])
            assert float(row["source_start"]) - shift == pytest.approx(float(row["clip_start"]))
            assert float(row["source_end"]) - shift == pytest.approx(float(row["clip_end"]))
