import csv
from decimal import Decimal
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

from clipkit.batch import run_batch
from clipkit.media import probe_media


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("book_clip_plan", ROOT / "examples/agent-clip-plan/clip_plan.py")
plan = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(plan)


@pytest.mark.parametrize("value,want", [("0", "0"), ("2.500", "2.5"), ("00:01:02.250", "62.25"), ("01:00:00", "3600")])
def test_seconds_accepts_both_notations(value, want):
    assert plan.seconds(value) == Decimal(want)


@pytest.mark.parametrize("value", ["NaN", "Infinity", "-1", "", "00:60:01", "00:00:60", "1:2", "00:00:01:15"])
def test_seconds_rejects_ambiguous_or_invalid_times(value):
    with pytest.raises(ValueError):
        plan.seconds(value)


def write_moments(tmp_path, fixtures_dir, **changes):
    row = {"id": "C01", "source": str(fixtures_dir / "sample-podcast.mp4"),
           "start": "1", "end": "3", "checked": "yes", **changes}
    source = tmp_path / "moments.csv"
    with source.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)
    return source


@pytest.mark.parametrize("changes", [{"end": "1"}, {"end": "30"}, {"checked": "no"},
    {"source": "missing.mp4"}, {"id": "../C01"}, {"start": "NaN"}])
def test_bad_row_writes_nothing(tmp_path, fixtures_dir, changes):
    source = write_moments(tmp_path, fixtures_dir, **changes)
    target = tmp_path / "new-run/jobs.csv"
    with pytest.raises(ValueError, match="CSV row 2"):
        plan.make_plan(source, target)
    assert not target.parent.exists()


def test_dry_run_then_create_refuses_overwrite(tmp_path, fixtures_dir):
    source = write_moments(tmp_path, fixtures_dir)
    target = tmp_path / "new-run/jobs.csv"
    jobs = plan.make_plan(source, target, dry_run=True)
    assert jobs[0]["duration"] == "2"
    assert not target.parent.exists()
    plan.make_plan(source, target)
    before = target.read_bytes()
    with pytest.raises(ValueError, match="already exists"):
        plan.make_plan(source, target)
    assert target.read_bytes() == before


def test_duplicate_ids_rejected(tmp_path, fixtures_dir):
    source = write_moments(tmp_path, fixtures_dir)
    with source.open("a") as handle:
        handle.write(source.read_text().splitlines()[1] + "\n")
    with pytest.raises(ValueError, match="unique"):
        plan.make_plan(source, tmp_path / "jobs.csv")


@pytest.mark.integration
def test_both_sample_notations_produce_three_real_cuts(tmp_path, fixtures_dir, media_settings):
    shutil.copytree(ROOT / "examples/agent-clip-plan", tmp_path / "examples/agent-clip-plan")
    shutil.copytree(fixtures_dir, tmp_path / "examples/fixtures")
    folder = tmp_path / "examples/agent-clip-plan"
    decimal_jobs = plan.make_plan(folder / "moments.csv", tmp_path / "run/jobs.csv")
    clock_jobs = plan.make_plan(folder / "moments-clock.csv", tmp_path / "clock/jobs.csv", dry_run=True)
    assert [Decimal(x["duration"]) for x in decimal_jobs] == [Decimal(x["duration"]) for x in clock_jobs]
    result = run_batch(tmp_path / "run/jobs.csv", jobs=2, resume=False, dry_run=False, settings=media_settings)
    assert (result["completed"], result["failed"]) == (3, 0)
    for item, wanted in zip(result["results"], [2, 2.5, 2.3]):
        actual = float(probe_media(item["output"], media_settings)["format"]["duration"])
        assert abs(actual - wanted) < 0.1


def test_repair_exercise_fails_then_reference_passes(tmp_path):
    spec = importlib.util.spec_from_file_location("prepare_clock", ROOT / "examples/agent-clip-plan/prepare_repair.py")
    exercise = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(exercise)
    target = exercise.prepare(tmp_path / "clock-repair")
    command = [sys.executable, "-m", "pytest", str(target / "test_clock.py"), "-q"]
    broken = subprocess.run(command, capture_output=True, text=True)
    assert broken.returncode == 1
    assert "9 failed, 1 passed" in broken.stdout
    shutil.copy2(ROOT / "examples/agent-clip-plan/clip_plan.py", target / "clip_plan.py")
    fixed = subprocess.run(command, capture_output=True, text=True)
    assert fixed.returncode == 0, fixed.stdout + fixed.stderr
    assert "10 passed" in fixed.stdout
    with pytest.raises(ValueError, match="exists"):
        exercise.prepare(target)
