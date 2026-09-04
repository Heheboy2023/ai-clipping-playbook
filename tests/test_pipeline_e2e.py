from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from clipkit.errors import ClipkitError
from clipkit.package import audit_brand, package_run, validate_package
from clipkit.pipeline import approve_run, run_pipeline, run_status
from clipkit.qc import qc_state


def manifest_data(source: Path, captions: Path, work: Path, *, rights: bool = True) -> dict:
    return {
        "schema_version": 1,
        "project_id": "e2e",
        "rights_confirmed": rights,
        "editorial_approved": True,
        "work_root": str(work),
        "steps": [
            {"id": "cut", "operation": "cut", "input": str(source), "output": str(work / "01-cut.mp4"), "options": {"start": 0, "duration": 3}},
            {"id": "vertical", "operation": "vertical", "input": "@previous", "output": str(work / "02-vertical.mp4"), "options": {"mode": "crop", "width": 180, "height": 320}},
            {"id": "captions", "operation": "captions_burn", "input": "@previous", "output": str(work / "03-captioned.mp4"), "options": {"captions": str(captions)}},
            {"id": "audio", "operation": "audio_normalize", "input": "@previous", "output": str(work / "04-final.mp4"), "options": {}},
        ],
    }


@pytest.mark.integration
def test_complete_pipeline_qc_approval_and_package(fixtures_dir: Path, media_settings, tmp_path: Path) -> None:
    work = tmp_path / "work"
    manifest = tmp_path / "job.yaml"
    manifest.write_text(yaml.safe_dump(manifest_data(fixtures_dir / "sample-podcast.mp4", fixtures_dir / "sample.srt", work), sort_keys=False), encoding="utf-8")
    result = run_pipeline(manifest, dry_run=False, resume=False, settings=media_settings)
    assert result["status"] == "awaiting_human_qc"
    state = Path(result["state"])
    assert len(run_status(state)["steps"]) == 4
    qc = qc_state(state, media_settings)
    assert qc["automated_pass"] is True
    assert qc["human_playback_review_required"] is True
    with pytest.raises(ClipkitError) as blocked:
        package_run(state, "generic-vertical", tmp_path / "package", overwrite=False)
    assert blocked.value.kind == "approval_required"
    approval = approve_run(state, gate="human-qc", reviewer="test reviewer", notes="fixture playback")
    assert approval["approval"]["publishing_authority"] is False
    package = package_run(state, "generic-vertical", tmp_path / "package", overwrite=False)
    assert package["publishing_authority"] is False
    assert validate_package(package["package"])["valid"] is True
    assert audit_brand(package["package"])["portable_names"] is True


def test_pipeline_dry_run_has_no_state(fixtures_dir: Path, media_settings, tmp_path: Path) -> None:
    work = tmp_path / "dry-work"
    manifest = tmp_path / "dry.yaml"
    manifest.write_text(yaml.safe_dump(manifest_data(fixtures_dir / "sample-podcast.mp4", fixtures_dir / "sample.srt", work, rights=False), sort_keys=False), encoding="utf-8")
    result = run_pipeline(manifest, dry_run=True, resume=False, settings=media_settings)
    assert result["status"] == "planned"
    assert result["state"] is None
    assert not (work / "run-state.json").exists()


def test_pipeline_blocks_unconfirmed_rights(fixtures_dir: Path, media_settings, tmp_path: Path) -> None:
    manifest = tmp_path / "blocked.yaml"
    manifest.write_text(yaml.safe_dump(manifest_data(fixtures_dir / "sample-podcast.mp4", fixtures_dir / "sample.srt", tmp_path / "work", rights=False), sort_keys=False), encoding="utf-8")
    with pytest.raises(ClipkitError) as error:
        run_pipeline(manifest, dry_run=False, resume=False, settings=media_settings)
    assert error.value.kind == "authorization_required"


def test_pipeline_blocks_output_escape(fixtures_dir: Path, media_settings, tmp_path: Path) -> None:
    work = tmp_path / "work"
    data = manifest_data(fixtures_dir / "sample-podcast.mp4", fixtures_dir / "sample.srt", work)
    data["steps"][0]["output"] = str(tmp_path / "outside.mp4")
    manifest = tmp_path / "escape.yaml"
    manifest.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    with pytest.raises(ClipkitError) as error:
        run_pipeline(manifest, dry_run=True, resume=False, settings=media_settings)
    assert error.value.kind == "path_escape"
