from __future__ import annotations

import re
import tempfile
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .errors import ClipkitError
from .io import existing_file
from .media import _encoding, execute_media_command, probe_media
from .process import run_checked
from .settings import Settings


TIMING = re.compile(
    r"^(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s+-->\s+"
    r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})$"
)


def native_subtitles_available(settings: Settings) -> bool:
    completed = run_checked([settings.ffmpeg, "-hide_banner", "-filters"], timeout=30)
    return " subtitles " in f"{completed.stdout}\n{completed.stderr}"


def _time(groups: tuple[str, ...]) -> float:
    hours, minutes, seconds, milliseconds = (int(item) for item in groups)
    return hours * 3600 + minutes * 60 + seconds + milliseconds / 1000


def parse_srt(path_value: str | Path) -> list[dict]:
    path = existing_file(path_value, label="caption file")
    blocks = re.split(r"\r?\n\s*\r?\n", path.read_text(encoding="utf-8-sig").strip())
    captions: list[dict] = []
    for position, block in enumerate(blocks, start=1):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if lines and lines[0].isdigit():
            lines = lines[1:]
        if len(lines) < 2:
            raise ClipkitError(f"Caption block {position} is incomplete.")
        match = TIMING.fullmatch(lines[0])
        if not match:
            raise ClipkitError(f"Caption block {position} has invalid SRT timing.")
        start = _time(match.groups()[:4])
        end = _time(match.groups()[4:])
        if end <= start:
            raise ClipkitError(f"Caption block {position} has a nonpositive duration.")
        captions.append({"start": start, "end": end, "text": " ".join(lines[1:])})
    if not captions:
        raise ClipkitError("Caption file contains no blocks.")
    return captions


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size=size)
    except OSError:
        return ImageFont.load_default(size=size)


def render_card(text: str, path: Path, width: int, height: int) -> None:
    font_size = max(10, round(width * 0.055))
    font = _font(font_size)
    max_chars = max(12, round(width / (font_size * 0.58)))
    lines = textwrap.wrap(text, width=max_chars, break_long_words=False) or [text]
    if len(lines) > 3:
        raise ClipkitError("Caption needs more than three lines. Split the cue into shorter timed phrases.")
    display = "\n".join(lines)
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    spacing = max(4, font_size // 5)
    box = draw.multiline_textbbox((0, 0), display, font=font, spacing=spacing, align="center", stroke_width=max(1, font_size // 18))
    text_width = box[2] - box[0]
    text_height = box[3] - box[1]
    if text_width > width * 0.92 or text_height > height * 0.40:
        raise ClipkitError("Caption does not fit. Split the cue into shorter timed phrases.")
    pad_x = max(12, font_size // 2)
    pad_y = max(8, font_size // 3)
    x = (width - text_width) / 2
    y = height - text_height - max(24, round(height * 0.09))
    background = (x - pad_x, y - pad_y, x + text_width + pad_x, y + text_height + pad_y)
    draw.rounded_rectangle(background, radius=max(8, font_size // 3), fill=(0, 0, 0, 190))
    draw.multiline_text((x, y), display, font=font, fill="white", spacing=spacing, align="center", stroke_width=max(1, font_size // 18), stroke_fill="black")
    image.save(path, format="PNG", optimize=True)


def burn_with_raster_overlays(
    source: Path,
    captions_path: Path,
    output_value: str | Path,
    *,
    overwrite: bool,
    settings: Settings,
) -> dict:
    probe = probe_media(source, settings)
    video = next((item for item in probe.get("streams", []) if item.get("codec_type") == "video"), None)
    if not video:
        raise ClipkitError("Caption burn input contains no video stream.")
    width, height = int(video["width"]), int(video["height"])
    captions = parse_srt(captions_path)
    with tempfile.TemporaryDirectory(prefix="clipkit-captions-") as directory:
        images: list[Path] = []
        for index, caption in enumerate(captions, start=1):
            image = Path(directory) / f"caption-{index:04d}.png"
            render_card(caption["text"], image, width, height)
            images.append(image)

        def builder(output: Path) -> list[str]:
            args = [settings.ffmpeg, "-hide_banner", "-nostdin", "-y", "-i", str(source)]
            for image in images:
                args.extend(["-i", str(image)])
            filters: list[str] = []
            prior = "0:v"
            for index, caption in enumerate(captions, start=1):
                label = f"captioned{index}"
                filters.append(
                    f"[{prior}][{index}:v]overlay=0:0:enable='between(t,{caption['start']:.3f},{caption['end']:.3f})'[{label}]"
                )
                prior = label
            args.extend(["-filter_complex", ";".join(filters), "-map", f"[{prior}]", "-map", "0:a:0?"])
            args.extend(_encoding(settings))
            args.append(str(output))
            return args

        result = execute_media_command(
            builder,
            output_value=output_value,
            overwrite=overwrite,
            dry_run=False,
        )
    result["caption_renderer"] = "ffmpeg-raster-overlay"
    result["caption_blocks"] = len(captions)
    return result
