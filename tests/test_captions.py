from pathlib import Path

from clipkit.subtitle_raster import parse_srt


def test_fixture_srt_is_parseable(fixtures_dir: Path) -> None:
    captions = parse_srt(fixtures_dir / "sample.srt")
    assert len(captions) == 3
    assert captions[0]["start"] == 0
