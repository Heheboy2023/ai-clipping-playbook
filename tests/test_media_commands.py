from __future__ import annotations

from pathlib import Path

import pytest

from clipkit.errors import ClipkitError
from clipkit.media import burn_captions, concat_media, cut_media, normalize_audio, probe_media, seconds, vertical_media


def test_timestamp_parser() -> None:
    assert seconds("01:02:03.5") == 3723.5
    assert seconds("02:03") == 123
    with pytest.raises(ClipkitError):
        seconds("bad")


@pytest.mark.integration
def test_cut_vertical_caption_and_audio(fixtures_dir: Path, media_settings, tmp_path: Path) -> None:
    cut = tmp_path / "01-cut.mp4"
    vertical = tmp_path / "02-vertical.mp4"
    captioned = tmp_path / "03-captioned.mp4"
    final = tmp_path / "04-final.mp4"
    cut_media(fixtures_dir / "sample-podcast.mp4", cut, start="0", end=None, duration="3", stream_copy=False, overwrite=False, dry_run=False, settings=media_settings)
    vertical_media(cut, vertical, mode="crop", width=180, height=320, overwrite=False, dry_run=False, settings=media_settings)
    burn_captions(vertical, fixtures_dir / "sample.srt", captioned, overwrite=False, dry_run=False, settings=media_settings)
    normalize_audio(captioned, final, overwrite=False, dry_run=False, settings=media_settings)
    probe = probe_media(final, media_settings)
    video = next(item for item in probe["streams"] if item["codec_type"] == "video")
    assert (video["width"], video["height"]) == (180, 320)
    assert any(item["codec_type"] == "audio" for item in probe["streams"])


def test_dry_run_does_not_create_output(fixtures_dir: Path, media_settings, tmp_path: Path) -> None:
    target = tmp_path / "planned.mp4"
    result = cut_media(fixtures_dir / "sample-podcast.mp4", target, start="0", end=None, duration="2", stream_copy=False, overwrite=False, dry_run=True, settings=media_settings)
    assert result["dry_run"] is True
    assert not target.exists()
    assert isinstance(result["command"], list)


@pytest.mark.integration
def test_concat_compatible_inputs(fixtures_dir: Path, media_settings, tmp_path: Path) -> None:
    output = tmp_path / "joined.mp4"
    result = concat_media(
        [str(fixtures_dir / "sample-youtube.mp4"), str(fixtures_dir / "sample-youtube.mp4")],
        output,
        overwrite=False,
        dry_run=False,
        settings=media_settings,
    )
    assert result["size_bytes"] > 0
    assert float(probe_media(output, media_settings)["format"]["duration"]) >= 15
