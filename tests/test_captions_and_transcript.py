from __future__ import annotations

import json
from pathlib import Path

import pytest

from clipkit.captions import segments_to_srt, validate_segments
from clipkit.errors import ClipkitError
from clipkit.transcript import validate_transcript


def test_generate_and_validate_srt(tmp_path: Path) -> None:
    source = tmp_path / "segments.json"
    source.write_text(
        json.dumps({"segments": [{"id": "S1", "start": 0, "end": 1.25, "speaker": "Host", "text": "Hello."}]}),
        encoding="utf-8",
    )
    output = tmp_path / "captions.srt"
    result = segments_to_srt(source, output, overwrite=False)
    assert result["segments"] == 1
    assert "00:00:01,250" in output.read_text(encoding="utf-8")
    validated = validate_transcript(source)
    assert validated["valid"] is True
    assert validated["speakers"] == ["Host"]


def test_segments_reject_bad_timing() -> None:
    with pytest.raises(ClipkitError, match="invalid timing"):
        validate_segments([{"start": 2, "end": 1, "text": "backward"}])
