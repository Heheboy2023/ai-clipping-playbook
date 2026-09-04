from pathlib import Path

from clipkit.media import vertical_media


def test_reframe_dry_run_contains_selected_mode(fixtures_dir: Path, media_settings, tmp_path: Path) -> None:
    crop = vertical_media(fixtures_dir / "sample-youtube.mp4", tmp_path / "crop.mp4", mode="crop", width=180, height=320, overwrite=False, dry_run=True, settings=media_settings)
    pad = vertical_media(fixtures_dir / "sample-youtube.mp4", tmp_path / "pad.mp4", mode="pad", width=180, height=320, overwrite=False, dry_run=True, settings=media_settings)
    assert "crop=" in crop["command"][crop["command"].index("-vf") + 1]
    assert "pad=" in pad["command"][pad["command"].index("-vf") + 1]
