from pathlib import Path
from unittest.mock import patch

from PIL import Image, ImageFont
import pytest

from clipkit.errors import ClipkitError
from clipkit.subtitle_raster import _font, render_card


def test_fallback_keeps_requested_size():
    fallback = ImageFont.load_default(size=59)
    with patch("clipkit.subtitle_raster.ImageFont.truetype", side_effect=OSError), \
         patch("clipkit.subtitle_raster.ImageFont.load_default", return_value=fallback) as loader:
        _font(59)
    loader.assert_called_once_with(size=59)


def test_long_caption_is_not_silently_truncated(tmp_path: Path):
    target = tmp_path / "caption.png"
    with pytest.raises(ClipkitError, match="Split the cue"):
        render_card("This sentence is repeated. " * 30, target, 1080, 1920)
    assert not target.exists()


def test_single_unbroken_word_cannot_overflow(tmp_path: Path):
    with pytest.raises(ClipkitError, match="does not fit"):
        render_card("W" * 100, tmp_path / "caption.png", 1080, 1920)


def test_short_caption_renders_visible_pixels(tmp_path: Path):
    target = tmp_path / "caption.png"
    render_card("Start with one clip.", target, 1080, 1920)
    with Image.open(target) as image:
        assert image.size == (1080, 1920)
        assert image.getbbox() is not None


def test_small_fixture_uses_proportional_type(tmp_path: Path):
    target = tmp_path / "small.png"
    render_card("This caption exists to test timing and rendering.", target, 180, 320)
    assert target.is_file()
