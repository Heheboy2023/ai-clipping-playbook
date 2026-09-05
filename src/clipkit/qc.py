from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .errors import ClipkitError
from .io import load_data, sha256_file, write_json
from .media import probe_media
from .settings import Settings


def _outputs_from_state(state: dict) -> list[Path]:
    items = state.get("steps") or state.get("jobs")
    if not isinstance(items, list):
        raise ClipkitError("State does not contain steps or jobs.")
    outputs: list[Path] = []
    for item in items:
        if item.get("status") in {"completed", "skipped_completed"} and item.get("output"):
            outputs.append(Path(item["output"]).expanduser().resolve())
    if not outputs:
        raise ClipkitError("State contains no completed outputs to inspect.")
    return outputs


def qc_state(state_value: str | Path, settings: Settings) -> dict:
    state_path = Path(state_value).expanduser().resolve()
    data = load_data(state_path)
    if not isinstance(data, dict):
        raise ClipkitError("QC input must be a run or batch state object.")
    records: list[dict] = []
    for output in _outputs_from_state(data):
        record = {"path": str(output), "exists": output.is_file(), "checks": []}
        if not output.is_file() or output.stat().st_size == 0:
            record["checks"].append({"name": "nonempty_file", "pass": False})
            record["pass"] = False
            records.append(record)
            continue
        record["checks"].append({"name": "nonempty_file", "pass": True})
        try:
            probe = probe_media(output, settings)
            streams = probe.get("streams", [])
            duration_value = (probe.get("format") or {}).get("duration")
            duration = float(duration_value) if duration_value not in {None, "N/A"} else None
            has_video = any(item.get("codec_type") == "video" for item in streams)
            has_audio = any(item.get("codec_type") == "audio" for item in streams)
            record.update(
                {
                    "size_bytes": output.stat().st_size,
                    "duration": duration,
                    "has_video": has_video,
                    "has_audio": has_audio,
                    "sha256": sha256_file(output),
                }
            )
            record["checks"].extend(
                [
                    {"name": "readable_container", "pass": bool(streams)},
                    {"name": "positive_duration", "pass": duration is None or duration > 0},
                ]
            )
            record["pass"] = all(item["pass"] for item in record["checks"])
        except ClipkitError as exc:
            record["checks"].append(
                {"name": "ffprobe", "pass": False, "message": str(exc)}
            )
            record["pass"] = False
        records.append(record)

    report = {
        "schema_version": 1,
        "source_state": str(state_path),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "automated_pass": all(item["pass"] for item in records) and all(
            item.get("status") in {"completed", "skipped_completed"}
            for item in (data.get("steps") or data.get("jobs") or [])
        ),
        "human_playback_review_required": True,
        "publishing_approved": False,
        "outputs": records,
    }
    report_path = state_path.parent / "qc-report.json"
    write_json(report_path, report)
    return {"report": str(report_path), **report}
