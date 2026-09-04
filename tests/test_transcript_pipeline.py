from pathlib import Path

from clipkit.transcript import validate_transcript


def test_fixture_transcript_requires_human_review(fixtures_dir: Path) -> None:
    result = validate_transcript(fixtures_dir / "sample-transcript.json")
    assert result["segments"] == 3
    assert result["human_playback_review_required"] is True
