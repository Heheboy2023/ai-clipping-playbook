from pathlib import Path

from clipkit.media import probe_media


def test_probe_reports_video_and_audio(fixtures_dir: Path, media_settings) -> None:
    result = probe_media(fixtures_dir / "sample-podcast.mp4", media_settings)
    kinds = {stream["codec_type"] for stream in result["streams"]}
    assert {"video", "audio"} <= kinds
