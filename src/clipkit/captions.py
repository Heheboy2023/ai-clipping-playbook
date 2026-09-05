from __future__ import annotations

from pathlib import Path
import math

from .errors import ClipkitError
from .io import load_data, output_path


def _srt_time(value: float) -> str:
    if not math.isfinite(value) or value < 0:
        raise ClipkitError("Caption timestamps must be finite and nonnegative.")
    milliseconds = round(value * 1000)
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, milliseconds = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def validate_segments(data: object) -> list[dict]:
    if isinstance(data, dict):
        segments = data.get("segments")
    else:
        segments = data
    if not isinstance(segments, list) or not segments:
        raise ClipkitError("Transcript must contain a nonempty segments list.")
    validated: list[dict] = []
    previous_start = -1.0
    for index, segment in enumerate(segments, start=1):
        if not isinstance(segment, dict):
            raise ClipkitError(f"Segment {index} is not an object.")
        try:
            start = float(segment["start"])
            end = float(segment["end"])
            text = str(segment["text"]).strip()
        except (KeyError, TypeError, ValueError) as exc:
            raise ClipkitError(f"Segment {index} has invalid start/end/text fields.") from exc
        if not math.isfinite(start) or not math.isfinite(end) or start < 0 or end <= start or start < previous_start or not text:
            raise ClipkitError(f"Segment {index} has invalid timing, order, or empty text.")
        previous_start = start
        validated.append(
            {
                "id": segment.get("id", index - 1),
                "start": start,
                "end": end,
                "text": text,
                "speaker": segment.get("speaker"),
            }
        )
    return validated


def segments_to_srt(input_value: str | Path, output_value: str | Path, *, overwrite: bool) -> dict:
    source = Path(input_value).expanduser().resolve()
    data = load_data(source)
    segments = validate_segments(data)
    target = output_path(output_value, overwrite=overwrite)
    blocks: list[str] = []
    for index, segment in enumerate(segments, start=1):
        speaker = f"{segment['speaker']}: " if segment.get("speaker") else ""
        blocks.append(
            f"{index}\n{_srt_time(segment['start'])} --> {_srt_time(segment['end'])}\n"
            f"{speaker}{segment['text']}"
        )
    target.write_text("\n\n".join(blocks) + "\n", encoding="utf-8", newline="\n")
    return {"output": str(target), "segments": len(segments), "format": "srt"}
