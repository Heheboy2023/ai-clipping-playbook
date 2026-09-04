from pathlib import Path

from clipkit.media import normalize_audio


def test_audio_dry_run_maps_loudnorm(fixtures_dir: Path, media_settings, tmp_path: Path) -> None:
    result = normalize_audio(fixtures_dir / "sample-audio.wav", tmp_path / "normalized.wav", overwrite=False, dry_run=True, settings=media_settings)
    assert any("loudnorm=" in argument for argument in result["command"])
