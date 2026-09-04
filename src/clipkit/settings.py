from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path

from .errors import ClipkitError


@dataclass(frozen=True)
class Settings:
    work_root: Path
    ffmpeg: str = "ffmpeg"
    ffprobe: str = "ffprobe"
    yt_dlp: str = "yt-dlp"
    whisper: str = "whisper"
    width: int = 1080
    height: int = 1920
    crf: int = 20
    preset: str = "medium"
    integrated_loudness: float = -16.0
    loudness_range: float = 11.0
    true_peak: float = -1.5
    batch_jobs: int = 2


def load_settings(config_path: str | None = None) -> Settings:
    data: dict = {}
    selected: Path | None = None
    if config_path:
        selected = Path(config_path).expanduser().resolve()
        if not selected.is_file():
            raise ClipkitError(f"Configuration file does not exist: {selected}")
    else:
        candidate = Path.cwd() / "clipkit.toml"
        if candidate.is_file():
            selected = candidate

    if selected:
        try:
            with selected.open("rb") as handle:
                data = tomllib.load(handle)
        except tomllib.TOMLDecodeError as exc:
            raise ClipkitError(f"Invalid TOML in {selected}: {exc}") from exc

    paths = data.get("paths", {})
    video = data.get("video", {})
    audio = data.get("audio", {})
    batch = data.get("batch", {})
    work_value = os.getenv("CLIPKIT_WORK_ROOT") or paths.get("work_root") or "work"

    return Settings(
        work_root=Path(work_value).expanduser().resolve(),
        ffmpeg=os.getenv("CLIPKIT_FFMPEG") or paths.get("ffmpeg", "ffmpeg"),
        ffprobe=os.getenv("CLIPKIT_FFPROBE") or paths.get("ffprobe", "ffprobe"),
        yt_dlp=os.getenv("CLIPKIT_YTDLP") or paths.get("yt_dlp", "yt-dlp"),
        whisper=os.getenv("CLIPKIT_WHISPER") or paths.get("whisper", "whisper"),
        width=int(video.get("width", 1080)),
        height=int(video.get("height", 1920)),
        crf=int(video.get("crf", 20)),
        preset=str(video.get("preset", "medium")),
        integrated_loudness=float(audio.get("integrated_loudness", -16.0)),
        loudness_range=float(audio.get("loudness_range", 11.0)),
        true_peak=float(audio.get("true_peak", -1.5)),
        batch_jobs=max(1, int(batch.get("jobs", 2))),
    )

