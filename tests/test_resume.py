from pathlib import Path

import pytest
import yaml

from clipkit.pipeline import run_pipeline


@pytest.mark.integration
def test_pipeline_resume_skips_completed_step(fixtures_dir: Path, media_settings, tmp_path: Path) -> None:
    work = tmp_path / "work"
    manifest = tmp_path / "job.yaml"
    manifest.write_text(
        yaml.safe_dump(
            {
                "project_id": "resume",
                "rights_confirmed": True,
                "editorial_approved": True,
                "work_root": str(work),
                "steps": [
                    {
                        "id": "cut",
                        "operation": "cut",
                        "input": str(fixtures_dir / "sample-podcast.mp4"),
                        "output": str(work / "cut.mp4"),
                        "options": {"start": 0, "duration": 2},
                    }
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    run_pipeline(manifest, dry_run=False, resume=False, settings=media_settings)
    resumed = run_pipeline(manifest, dry_run=False, resume=True, settings=media_settings)
    assert resumed["steps"][0]["resumed"] is True
    again = run_pipeline(manifest, dry_run=False, resume=True, settings=media_settings)
    assert again["steps"][0]["resumed"] is True
    data = yaml.safe_load(manifest.read_text())
    data["steps"][0]["options"]["duration"] = 1
    manifest.write_text(yaml.safe_dump(data), encoding="utf-8")
    changed = run_pipeline(manifest, dry_run=False, resume=True, settings=media_settings)
    assert changed["status"] == "failed"
    assert changed["steps"][0].get("resumed") is not True
    assert "exists" in changed["steps"][0]["error"]["message"].lower()
