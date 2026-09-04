from __future__ import annotations

import os
import platform
import sys

from .process import run_checked, version_line
from .settings import Settings


def _ffmpeg_capabilities(settings: Settings) -> dict:
    result = {
        "subtitles_filter": False,
        "overlay_filter": False,
        "loudnorm_filter": False,
        "libx264_encoder": False,
    }
    try:
        filters = run_checked([settings.ffmpeg, "-hide_banner", "-filters"], timeout=30)
        filter_text = f"{filters.stdout}\n{filters.stderr}"
        result["subtitles_filter"] = " subtitles " in filter_text
        result["overlay_filter"] = " overlay " in filter_text
        result["loudnorm_filter"] = " loudnorm " in filter_text
        encoders = run_checked([settings.ffmpeg, "-hide_banner", "-encoders"], timeout=30)
        encoder_text = f"{encoders.stdout}\n{encoders.stderr}"
        result["libx264_encoder"] = "libx264" in encoder_text
    except Exception as exc:  # Doctor must report rather than crash.
        result["error"] = str(exc)
    result["caption_burn_mode"] = (
        "native-subtitles" if result["subtitles_filter"] else (
            "ffmpeg-raster-overlay" if result["overlay_filter"] else "unavailable"
        )
    )
    return result


def doctor(settings: Settings) -> dict:
    tools = {
        "ffmpeg": version_line(settings.ffmpeg, ["-version"]),
        "ffprobe": version_line(settings.ffprobe, ["-version"]),
        "yt_dlp": version_line(settings.yt_dlp),
        "whisper": version_line(settings.whisper, ["--help"]),
        "codex": version_line("codex"),
        "claude": version_line("claude"),
    }
    required_ok = tools["ffmpeg"]["available"] and tools["ffprobe"]["available"]
    python_ok = sys.version_info >= (3, 11)
    return {
        "clipkit": "0.1.0",
        "python": {
            "available": python_ok,
            "version": platform.python_version(),
            "executable": sys.executable,
            "minimum": "3.11",
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "tools": tools,
        "ffmpeg_capabilities": _ffmpeg_capabilities(settings) if tools["ffmpeg"]["available"] else {},
        "optional_credentials": {
            "openai_api_key_present": bool(os.getenv("OPENAI_API_KEY")),
            "anthropic_api_key_present": bool(os.getenv("ANTHROPIC_API_KEY")),
            "hugging_face_token_present": bool(os.getenv("HF_TOKEN")),
        },
        "offline_core_requires_auth": False,
        "core_ready": bool(required_ok and python_ok),
        "work_root": str(settings.work_root),
    }
