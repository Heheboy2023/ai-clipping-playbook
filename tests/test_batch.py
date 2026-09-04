from __future__ import annotations

import csv
from pathlib import Path

import pytest

from clipkit.batch import run_batch


FIELDS = ["job_id", "operation", "input", "output", "start", "duration", "mode", "captions"]


def write_manifest(path: Path, source: Path, output_root: Path, second_operation: str) -> None:
    rows = [
        {"job_id": "A", "operation": "cut", "input": str(source), "output": str(output_root / "a.mp4"), "start": "0", "duration": "2", "mode": "", "captions": ""},
        {"job_id": "B", "operation": second_operation, "input": str(source), "output": str(output_root / "b.mp4"), "start": "", "duration": "", "mode": "pad", "captions": ""},
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


@pytest.mark.integration
def test_batch_records_failure_then_resumes(fixtures_dir: Path, media_settings, tmp_path: Path) -> None:
    manifest = tmp_path / "batch.csv"
    output_root = tmp_path / "outputs"
    write_manifest(manifest, fixtures_dir / "sample-gaming.mp4", output_root, "not_supported")
    first = run_batch(manifest, jobs=2, resume=False, dry_run=False, settings=media_settings)
    assert first["completed"] == 1
    assert first["failed"] == 1
    write_manifest(manifest, fixtures_dir / "sample-gaming.mp4", output_root, "vertical")
    second = run_batch(manifest, jobs=2, resume=True, dry_run=False, settings=media_settings)
    assert second["failed"] == 0
    assert second["completed"] == 2
    assert next(item for item in second["results"] if item["job_id"] == "A")["status"] == "skipped_completed"


def test_batch_dry_run_plans_all(fixtures_dir: Path, media_settings, tmp_path: Path) -> None:
    manifest = tmp_path / "batch.csv"
    output_root = tmp_path / "outputs"
    write_manifest(manifest, fixtures_dir / "sample-gaming.mp4", output_root, "vertical")
    result = run_batch(manifest, jobs=99, resume=False, dry_run=True, settings=media_settings)
    assert result["failed"] == 0
    assert all(item["status"] == "planned" for item in result["results"])
    assert not (tmp_path / ".clipkit-batch-state.json").exists()
    assert not output_root.exists()
