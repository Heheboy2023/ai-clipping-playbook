from pathlib import Path

from clipkit.media import cut_media


def test_cut_command_is_an_argument_array(fixtures_dir: Path, media_settings, tmp_path: Path) -> None:
    result = cut_media(fixtures_dir / "sample-podcast.mp4", tmp_path / "cut.mp4", start="1", end="3", duration=None, stream_copy=False, overwrite=False, dry_run=True, settings=media_settings)
    assert result["command"][0] == media_settings.ffmpeg
    assert "-t" in result["command"]
