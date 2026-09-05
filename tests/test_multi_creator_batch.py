from pathlib import Path
import shutil

from clipkit.batch import run_batch
from clipkit.io import sha256_file


def test_five_job_failure_then_exact_repair(repository_root, fixtures_dir, media_settings, tmp_path):
    shutil.copytree(fixtures_dir, tmp_path / "examples/fixtures")
    root = tmp_path / "examples/multi-creator-batch"
    shutil.copytree(repository_root / "examples/multi-creator-batch", root,
                    ignore=shutil.ignore_patterns(".clipkit-batch-state.json"))
    first = run_batch(root / "broken.csv", jobs=2, resume=False, dry_run=False, settings=media_settings)
    assert (first["completed"], first["failed"]) == (4, 1)
    failed = next(item for item in first["results"] if item["status"] == "failed")
    assert failed["job_id"] == "REED-01"
    hashes = {item["job_id"]: sha256_file(Path(item["output"]))
              for item in first["results"] if item["status"] == "completed"}
    fixed = run_batch(root / "fixed.csv", jobs=2, resume=True, dry_run=False, settings=media_settings)
    assert (fixed["completed"], fixed["failed"]) == (5, 0)
    for item in fixed["results"]:
        if item["job_id"] in hashes:
            assert item["status"] == "skipped_completed"
            assert item["output_hash"] == hashes[item["job_id"]]
    again = run_batch(root / "fixed.csv", jobs=2, resume=True, dry_run=False, settings=media_settings)
    assert all(item["status"] == "skipped_completed" for item in again["results"])
