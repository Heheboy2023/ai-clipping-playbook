from pathlib import Path

from clipkit.batch import run_batch


def test_repository_batch_fixture_plans_without_writes(repository_root: Path, media_settings) -> None:
    result = run_batch(repository_root / "examples" / "batch-production" / "manifest.csv", jobs=2, resume=False, dry_run=True, settings=media_settings)
    assert result["jobs"] == 3
    assert result["failed"] == 0
    assert all(item["status"] == "planned" for item in result["results"])
