from __future__ import annotations

from pathlib import Path

from .errors import ClipkitError
from .media import burn_captions, cut_media, normalize_audio, vertical_media
from .settings import Settings


def resolve_relative(base: Path, value: str | Path) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = base / path
    return path.resolve()


def run_operation(
    operation: str,
    *,
    input_path: Path,
    output_path: Path,
    options: dict,
    settings: Settings,
    overwrite: bool = False,
    dry_run: bool = False,
    allow_missing_input: bool = False,
) -> dict:
    if operation == "cut":
        return cut_media(
            input_path,
            output_path,
            start=str(options.get("start", "0")),
            end=str(options["end"]) if options.get("end") is not None else None,
            duration=(
                str(options["duration"])
                if options.get("duration") is not None
                else None
            ),
            stream_copy=bool(options.get("stream_copy", False)),
            overwrite=overwrite,
            dry_run=dry_run,
            settings=settings,
            allow_missing_input=allow_missing_input,
        )
    if operation == "vertical":
        return vertical_media(
            input_path,
            output_path,
            mode=str(options.get("mode", "crop")),
            width=int(options.get("width", settings.width)),
            height=int(options.get("height", settings.height)),
            overwrite=overwrite,
            dry_run=dry_run,
            settings=settings,
            allow_missing_input=allow_missing_input,
        )
    if operation == "captions_burn":
        captions = options.get("captions")
        if not captions:
            raise ClipkitError("captions_burn requires options.captions.")
        return burn_captions(
            input_path,
            resolve_relative(input_path.parent, str(captions)),
            output_path,
            overwrite=overwrite,
            dry_run=dry_run,
            settings=settings,
            allow_missing_input=allow_missing_input,
        )
    if operation == "audio_normalize":
        return normalize_audio(
            input_path,
            output_path,
            overwrite=overwrite,
            dry_run=dry_run,
            settings=settings,
            allow_missing_input=allow_missing_input,
        )
    raise ClipkitError(
        f"Unsupported operation: {operation}",
        details={"supported": ["cut", "vertical", "captions_burn", "audio_normalize"]},
    )
