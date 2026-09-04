from __future__ import annotations

import json
import os
import re
import tempfile
import uuid
from pathlib import Path

from .errors import ClipkitError
from .io import existing_file, output_path
from .process import run_checked
from .settings import Settings


def seconds(value: str | int | float) -> float:
    if isinstance(value, (int, float)):
        result = float(value)
    else:
        parts = str(value).strip().split(":")
        if not 1 <= len(parts) <= 3:
            raise ClipkitError(f"Invalid timestamp: {value}")
        try:
            numbers = [float(part) for part in parts]
        except ValueError as exc:
            raise ClipkitError(f"Invalid timestamp: {value}") from exc
        if any(number < 0 for number in numbers):
            raise ClipkitError("Timestamps cannot be negative.")
        if len(numbers) == 1:
            result = numbers[0]
        elif len(numbers) == 2:
            result = numbers[0] * 60 + numbers[1]
        else:
            result = numbers[0] * 3600 + numbers[1] * 60 + numbers[2]
    if result < 0:
        raise ClipkitError("Timestamps cannot be negative.")
    return result


def timestamp(value: str | int | float) -> str:
    return f"{seconds(value):.3f}"


def probe_media(input_value: str | Path, settings: Settings) -> dict:
    source = existing_file(input_value, label="media input")
    completed = run_checked(
        [
            settings.ffprobe,
            "-v",
            "error",
            "-show_format",
            "-show_streams",
            "-of",
            "json",
            str(source),
        ]
    )
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise ClipkitError("ffprobe returned invalid JSON.") from exc
    payload["input"] = str(source)
    return payload


def _encoding(settings: Settings) -> list[str]:
    return [
        "-c:v",
        "libx264",
        "-preset",
        settings.preset,
        "-crf",
        str(settings.crf),
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-movflags",
        "+faststart",
    ]


def build_cut_command(
    source: Path,
    output: Path,
    *,
    start: str,
    end: str | None,
    duration: str | None,
    stream_copy: bool,
    settings: Settings,
) -> list[str]:
    start_seconds = seconds(start)
    if duration is not None:
        duration_seconds = seconds(duration)
    elif end is not None:
        duration_seconds = seconds(end) - start_seconds
    else:
        raise ClipkitError("Supply --end or --duration.")
    if duration_seconds <= 0:
        raise ClipkitError("The clip duration must be greater than zero.")

    args = [
        settings.ffmpeg,
        "-hide_banner",
        "-nostdin",
        "-y",
        "-i",
        str(source),
        "-ss",
        f"{start_seconds:.3f}",
        "-t",
        f"{duration_seconds:.3f}",
        "-map",
        "0:v:0?",
        "-map",
        "0:a:0?",
    ]
    args.extend(["-c", "copy"] if stream_copy else _encoding(settings))
    args.append(str(output))
    return args


def build_vertical_command(
    source: Path,
    output: Path,
    *,
    mode: str,
    width: int,
    height: int,
    settings: Settings,
) -> list[str]:
    if width <= 0 or height <= 0:
        raise ClipkitError("Width and height must be positive integers.")
    if mode == "crop":
        video_filter = (
            f"crop='min(iw,ih*{width}/{height})':"
            f"'min(ih,iw*{height}/{width})':(iw-ow)/2:(ih-oh)/2,"
            f"scale={width}:{height}:flags=lanczos"
        )
    elif mode == "pad":
        video_filter = (
            f"scale={width}:{height}:force_original_aspect_ratio=decrease:flags=lanczos,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black"
        )
    else:
        raise ClipkitError("Vertical mode must be 'crop' or 'pad'.")
    return [
        settings.ffmpeg,
        "-hide_banner",
        "-nostdin",
        "-y",
        "-i",
        str(source),
        "-map",
        "0:v:0",
        "-map",
        "0:a:0?",
        "-vf",
        video_filter,
        *_encoding(settings),
        str(output),
    ]


def _filter_path(path: Path) -> str:
    value = str(path.resolve()).replace("\\", "/")
    for original, escaped in (
        ("'", r"\'"),
        (":", r"\:"),
        (",", r"\,"),
        ("[", r"\["),
        ("]", r"\]"),
    ):
        value = value.replace(original, escaped)
    return value


def build_caption_burn_command(
    source: Path,
    captions: Path,
    output: Path,
    *,
    settings: Settings,
) -> list[str]:
    subtitle_filter = f"subtitles=filename='{_filter_path(captions)}'"
    return [
        settings.ffmpeg,
        "-hide_banner",
        "-nostdin",
        "-y",
        "-i",
        str(source),
        "-map",
        "0:v:0",
        "-map",
        "0:a:0?",
        "-vf",
        subtitle_filter,
        *_encoding(settings),
        str(output),
    ]


def build_audio_command(
    source: Path,
    output: Path,
    *,
    settings: Settings,
) -> list[str]:
    loudnorm = (
        f"loudnorm=I={settings.integrated_loudness}:"
        f"LRA={settings.loudness_range}:TP={settings.true_peak}"
    )
    args = [
        settings.ffmpeg,
        "-hide_banner",
        "-nostdin",
        "-y",
        "-i",
        str(source),
        "-af",
        loudnorm,
    ]
    if output.suffix.lower() in {".mp4", ".mov", ".mkv", ".webm"}:
        args.extend(["-map", "0:v:0?", "-map", "0:a:0", "-c:v", "copy"])
        if output.suffix.lower() == ".webm":
            args.extend(["-c:a", "libopus", "-b:a", "160k"])
        else:
            args.extend(["-c:a", "aac", "-b:a", "192k"])
    elif output.suffix.lower() == ".wav":
        args.extend(["-vn", "-c:a", "pcm_s16le"])
    else:
        args.extend(["-vn", "-c:a", "libmp3lame", "-b:a", "192k"])
    args.append(str(output))
    return args


def _temporary_output(final_output: Path) -> Path:
    return final_output.with_name(
        f".{final_output.stem}.{uuid.uuid4().hex}.part{final_output.suffix}"
    )


def execute_media_command(
    builder,
    *,
    output_value: str | Path,
    overwrite: bool,
    dry_run: bool = False,
) -> dict:
    if dry_run:
        final_output = Path(output_value).expanduser().resolve()
        if final_output.exists() and not overwrite:
            raise ClipkitError(
                f"Output already exists: {final_output}. Choose another path or pass --overwrite."
            )
    else:
        final_output = output_path(output_value, overwrite=overwrite)
    temp_output = _temporary_output(final_output)
    args = builder(temp_output)
    display_args = [str(final_output) if item == str(temp_output) else item for item in args]
    if dry_run:
        return {"dry_run": True, "command": display_args, "output": str(final_output)}
    try:
        completed = run_checked(args)
        if not temp_output.is_file() or temp_output.stat().st_size == 0:
            raise ClipkitError("FFmpeg exited without creating a nonempty output.")
        os.replace(temp_output, final_output)
    finally:
        temp_output.unlink(missing_ok=True)
    return {
        "dry_run": False,
        "command": display_args,
        "output": str(final_output),
        "size_bytes": final_output.stat().st_size,
        "ffmpeg_stderr_tail": (completed.stderr or "").strip().splitlines()[-5:],
    }


def cut_media(
    input_value: str | Path,
    output_value: str | Path,
    *,
    start: str,
    end: str | None,
    duration: str | None,
    stream_copy: bool,
    overwrite: bool,
    dry_run: bool,
    settings: Settings,
    allow_missing_input: bool = False,
) -> dict:
    source = (
        Path(input_value).expanduser().resolve()
        if allow_missing_input
        else existing_file(input_value, label="media input")
    )
    return execute_media_command(
        lambda output: build_cut_command(
            source,
            output,
            start=start,
            end=end,
            duration=duration,
            stream_copy=stream_copy,
            settings=settings,
        ),
        output_value=output_value,
        overwrite=overwrite,
        dry_run=dry_run,
    )


def vertical_media(
    input_value: str | Path,
    output_value: str | Path,
    *,
    mode: str,
    width: int,
    height: int,
    overwrite: bool,
    dry_run: bool,
    settings: Settings,
    allow_missing_input: bool = False,
) -> dict:
    source = (
        Path(input_value).expanduser().resolve()
        if allow_missing_input
        else existing_file(input_value, label="media input")
    )
    return execute_media_command(
        lambda output: build_vertical_command(
            source,
            output,
            mode=mode,
            width=width,
            height=height,
            settings=settings,
        ),
        output_value=output_value,
        overwrite=overwrite,
        dry_run=dry_run,
    )


def burn_captions(
    input_value: str | Path,
    captions_value: str | Path,
    output_value: str | Path,
    *,
    overwrite: bool,
    dry_run: bool,
    settings: Settings,
    allow_missing_input: bool = False,
) -> dict:
    source = (
        Path(input_value).expanduser().resolve()
        if allow_missing_input
        else existing_file(input_value, label="media input")
    )
    captions = existing_file(captions_value, label="caption file")
    from .subtitle_raster import native_subtitles_available, parse_srt

    if dry_run:
        if not native_subtitles_available(settings):
            target = Path(output_value).expanduser().resolve()
            if target.exists() and not overwrite:
                raise ClipkitError(
                    f"Output already exists: {target}. Choose another path or pass --overwrite."
                )
            return {
                "dry_run": True,
                "command": [
                    settings.ffmpeg,
                    "<generated transparent caption PNG inputs>",
                    "-filter_complex",
                    "<timed overlay chain>",
                    str(target),
                ],
                "output": str(target),
                "caption_renderer": "ffmpeg-raster-overlay",
                "caption_blocks": len(parse_srt(captions)),
            }
        return execute_media_command(
            lambda output: build_caption_burn_command(
                source, captions, output, settings=settings
            ),
            output_value=output_value,
            overwrite=overwrite,
            dry_run=True,
        )
    from .subtitle_raster import burn_with_raster_overlays

    if not native_subtitles_available(settings):
        return burn_with_raster_overlays(
            source,
            captions,
            output_value,
            overwrite=overwrite,
            settings=settings,
        )
    return execute_media_command(
        lambda output: build_caption_burn_command(
            source, captions, output, settings=settings
        ),
        output_value=output_value,
        overwrite=overwrite,
        dry_run=dry_run,
    )


def normalize_audio(
    input_value: str | Path,
    output_value: str | Path,
    *,
    overwrite: bool,
    dry_run: bool,
    settings: Settings,
    allow_missing_input: bool = False,
) -> dict:
    source = (
        Path(input_value).expanduser().resolve()
        if allow_missing_input
        else existing_file(input_value, label="media input")
    )
    return execute_media_command(
        lambda output: build_audio_command(source, output, settings=settings),
        output_value=output_value,
        overwrite=overwrite,
        dry_run=dry_run,
    )


def concat_media(
    inputs: list[str],
    output_value: str | Path,
    *,
    overwrite: bool,
    dry_run: bool,
    settings: Settings,
) -> dict:
    sources = [existing_file(value, label="concat input") for value in inputs]
    if len(sources) < 2:
        raise ClipkitError("Concat requires at least two inputs.")
    with tempfile.TemporaryDirectory(prefix="clipkit-concat-") as temp_dir:
        list_path = Path(temp_dir) / "inputs.txt"
        lines = []
        for source in sources:
            escaped = str(source).replace("'", "'\\''")
            lines.append(f"file '{escaped}'")
        list_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return execute_media_command(
            lambda output: [
                settings.ffmpeg,
                "-hide_banner",
                "-nostdin",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(list_path),
                "-c",
                "copy",
                str(output),
            ],
            output_value=output_value,
            overwrite=overwrite,
            dry_run=dry_run,
        )
