from pathlib import Path

from clipkit.subtitle_raster import parse_srt
from clipkit.captions import validate_segments
from clipkit.errors import ClipkitError
import pytest


def test_fixture_srt_is_parseable(fixtures_dir: Path) -> None:
    captions = parse_srt(fixtures_dir / "sample.srt")
    assert len(captions) == 3
    assert captions[0]["start"] == 0


@pytest.mark.parametrize('start,end', [(float('nan'), 1), (0, float('nan')),
                                      (float('inf'), 2), (0, float('inf'))])
def test_nonfinite_caption_times_are_rejected(start, end):
    with pytest.raises(ClipkitError, match='invalid timing'):
        validate_segments([{'start':start, 'end':end, 'text':'Practice'}])
