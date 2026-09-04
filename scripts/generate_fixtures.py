#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
from hashlib import sha256
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "examples" / "fixtures"


def digest(path: Path) -> str:
    value = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def run_ffmpeg(output: Path, inputs: list[str], filters: list[str] | None = None) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("ffmpeg is required to generate fixtures")
    output.parent.mkdir(parents=True, exist_ok=True)
    temp = output.with_name(f".{output.stem}.part{output.suffix}")
    command = [ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin", "-y", *inputs]
    if filters:
        command.extend(filters)
    command.extend(
        [
            "-t",
            "8",
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-crf",
            "28",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "96k",
            "-shortest",
            str(temp),
        ]
    )
    try:
        subprocess.run(command, check=True, capture_output=True, text=True, shell=False)
        os.replace(temp, output)
    except subprocess.CalledProcessError as exc:
        temp.unlink(missing_ok=True)
        raise SystemExit(exc.stderr) from exc


def generate(force: bool) -> dict:
    FIXTURES.mkdir(parents=True, exist_ok=True)
    jobs = {
        "sample-podcast.mp4": (
            [
                "-f", "lavfi", "-i", "testsrc2=size=320x360:rate=30",
                "-f", "lavfi", "-i", "smptebars=size=320x360:rate=30",
                "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000",
            ],
            ["-filter_complex", "[0:v][1:v]hstack=inputs=2[v]", "-map", "[v]", "-map", "2:a"],
        ),
        "sample-youtube.mp4": (
            [
                "-f", "lavfi", "-i", "testsrc2=size=640x360:rate=30",
                "-f", "lavfi", "-i", "sine=frequency=523:sample_rate=48000",
            ],
            ["-map", "0:v", "-map", "1:a"],
        ),
        "sample-livestream.mp4": (
            [
                "-f", "lavfi", "-i", "smptehdbars=size=640x360:rate=30",
                "-f", "lavfi", "-i", "sine=frequency=659:sample_rate=48000",
            ],
            ["-map", "0:v", "-map", "1:a"],
        ),
        "sample-gaming.mp4": (
            [
                "-f", "lavfi", "-i", "testsrc2=size=640x360:rate=60",
                "-f", "lavfi", "-i", "sine=frequency=330:sample_rate=48000",
            ],
            ["-map", "0:v", "-map", "1:a"],
        ),
        "sample-multispeaker.mp4": (
            [
                "-f", "lavfi", "-i", "testsrc=size=320x180:rate=30",
                "-f", "lavfi", "-i", "testsrc2=size=320x180:rate=30",
                "-f", "lavfi", "-i", "smptebars=size=320x180:rate=30",
                "-f", "lavfi", "-i", "smptehdbars=size=320x180:rate=30",
                "-f", "lavfi", "-i", "sine=frequency=392:sample_rate=48000",
            ],
            [
                "-filter_complex",
                "[0:v][1:v]hstack=inputs=2[top];[2:v][3:v]hstack=inputs=2[bottom];[top][bottom]vstack=inputs=2[v]",
                "-map", "[v]", "-map", "4:a",
            ],
        ),
    }
    created: list[str] = []
    for filename, (inputs, filters) in jobs.items():
        target = FIXTURES / filename
        if force or not target.is_file():
            run_ffmpeg(target, inputs, filters)
            created.append(filename)

    audio = FIXTURES / "sample-audio.wav"
    if force or not audio.is_file():
        ffmpeg = shutil.which("ffmpeg")
        if not ffmpeg:
            raise SystemExit("ffmpeg is required to generate fixtures")
        with tempfile.NamedTemporaryFile(suffix=".wav", dir=FIXTURES, delete=False) as handle:
            temp_audio = Path(handle.name)
        command = [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-nostdin",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=440:sample_rate=16000:duration=8",
            "-c:a",
            "pcm_s16le",
            str(temp_audio),
        ]
        subprocess.run(command, check=True, capture_output=True, text=True, shell=False)
        os.replace(temp_audio, audio)
        created.append(audio.name)

    records = []
    for path in sorted(FIXTURES.glob("sample-*")):
        if path.is_file():
            records.append(
                {
                    "path": path.name,
                    "bytes": path.stat().st_size,
                    "sha256": digest(path),
                    "provenance": "Generated locally from FFmpeg lavfi test sources; no third-party media.",
                }
            )
    manifest = {
        "schema_version": 1,
        "fixture_license": "MIT License; synthetic test material generated locally only.",
        "files": records,
    }
    (FIXTURES / "fixture-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return {"created": created, "fixtures": len(records)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate rights-safe FFmpeg fixtures.")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    print(json.dumps(generate(args.force), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
