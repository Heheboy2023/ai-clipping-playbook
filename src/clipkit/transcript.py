from __future__ import annotations

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from .captions import segments_to_srt, validate_segments
from .errors import ClipkitError
from .io import existing_file, load_data, output_path, write_json
from .process import run_checked
from .settings import Settings


def validate_transcript(path_value: str | Path) -> dict:
    path = existing_file(path_value, label="transcript manifest")
    data = load_data(path)
    segments = validate_segments(data)
    speakers = sorted(
        {str(item["speaker"]) for item in segments if item.get("speaker")}
    )
    return {
        "manifest": str(path),
        "segments": len(segments),
        "duration": max(item["end"] for item in segments),
        "speakers": speakers,
        "valid": True,
        "human_playback_review_required": True,
    }


def transcribe_whisper(
    input_value: str | Path,
    output_value: str | Path,
    *,
    model: str,
    language: str | None,
    overwrite: bool,
    settings: Settings,
) -> dict:
    source = existing_file(input_value, label="transcription input")
    output_dir = Path(output_value).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_path(output_dir / "transcript.json", overwrite=overwrite)
    srt_path = output_dir / "transcript.srt"
    if srt_path.exists() and not overwrite:
        raise ClipkitError(
            f"Output already exists: {srt_path}. Pass --overwrite to replace it."
        )

    with tempfile.TemporaryDirectory(prefix="clipkit-whisper-") as temp_dir:
        args = [
            settings.whisper,
            str(source),
            "--model",
            model,
            "--output_dir",
            temp_dir,
            "--output_format",
            "json",
            "--word_timestamps",
            "True",
            "--verbose",
            "False",
        ]
        if language:
            args.extend(["--language", language])
        run_checked(args, timeout=3600)
        raw_path = Path(temp_dir) / f"{source.stem}.json"
        if not raw_path.is_file():
            matches = list(Path(temp_dir).glob("*.json"))
            if len(matches) != 1:
                raise ClipkitError("Whisper did not produce the expected JSON output.")
            raw_path = matches[0]
        raw = json.loads(raw_path.read_text(encoding="utf-8"))

    segments = validate_segments(raw)
    normalized = {
        "schema_version": 1,
        "provider": "openai-whisper-cli",
        "model": model,
        "language": raw.get("language") or language,
        "source": str(source),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "human_playback_review_required": True,
        "segments": segments,
    }
    write_json(manifest_path, normalized)
    segments_to_srt(manifest_path, srt_path, overwrite=overwrite)
    return {
        "manifest": str(manifest_path),
        "srt": str(srt_path),
        "segments": len(segments),
        "model": model,
        "human_playback_review_required": True,
    }

