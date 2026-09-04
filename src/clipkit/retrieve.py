from __future__ import annotations

import json
from pathlib import Path

from .errors import ClipkitError
from .io import output_path, write_json
from .process import run_checked
from .settings import Settings


def retrieve_metadata(
    url: str,
    output_value: str | Path,
    *,
    confirmed_authorized: bool,
    overwrite: bool,
    settings: Settings,
) -> dict:
    if not confirmed_authorized:
        raise ClipkitError(
            "Retrieval is blocked until --confirmed-authorized is supplied.",
            kind="authorization_required",
        )
    target = output_path(output_value, overwrite=overwrite)
    completed = run_checked(
        [settings.yt_dlp, "--dump-single-json", "--skip-download", "--no-warnings", url],
        timeout=180,
    )
    try:
        raw = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise ClipkitError("yt-dlp returned invalid JSON metadata.") from exc
    sanitized = {
        "id": raw.get("id"),
        "title": raw.get("title"),
        "uploader": raw.get("uploader"),
        "duration": raw.get("duration"),
        "webpage_url": raw.get("webpage_url") or url,
        "upload_date": raw.get("upload_date"),
        "availability": raw.get("availability"),
        "live_status": raw.get("live_status"),
        "subtitle_languages": sorted((raw.get("subtitles") or {}).keys()),
        "automatic_caption_languages": sorted(
            (raw.get("automatic_captions") or {}).keys()
        ),
        "authorization_confirmed_by_operator": True,
        "media_downloaded": False,
    }
    write_json(target, sanitized)
    return {"output": str(target), "metadata": sanitized}
