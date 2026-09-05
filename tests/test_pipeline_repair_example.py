from pathlib import Path
import shutil

from clipkit.io import sha256_file
from clipkit.pipeline import run_pipeline
from clipkit.qc import qc_state


def test_documented_caption_repair_reuses_cut_and_crop(repository_root, fixtures_dir, tmp_path, media_settings):
    shutil.copytree(fixtures_dir, tmp_path / "examples/fixtures")
    folder = tmp_path / "examples/pipeline-repair"
    shutil.copytree(repository_root / "examples/pipeline-repair", folder)
    broken = run_pipeline(folder / "broken.yaml", dry_run=False, resume=False, settings=media_settings)
    assert broken["status"] == "failed"
    outputs = tmp_path / "work/pipeline-repair"
    before = {p.name: sha256_file(p) for p in outputs.glob("*.mp4")}
    assert set(before) == {"01-cut.mp4", "02-vertical.mp4"}
    fixed = run_pipeline(folder / "fixed.yaml", dry_run=False, resume=True, settings=media_settings)
    assert fixed["status"] == "awaiting_human_qc"
    assert all(step["resumed"] for step in fixed["steps"][:2])
    for name, digest in before.items():
        assert sha256_file(outputs / name) == digest
    report = qc_state(outputs / "run-state.json", media_settings)
    assert report["automated_pass"]
    assert report["human_playback_review_required"]
