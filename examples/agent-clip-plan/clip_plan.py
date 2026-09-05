"""Turn checked source ranges into independent Clipkit cut jobs. Never render here."""
from __future__ import annotations

import argparse
import csv
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import re

from clipkit.errors import ClipkitError
from clipkit.media import probe_media
from clipkit.settings import Settings


FIELDS = ["job_id", "operation", "input", "output", "start", "duration"]


def seconds(value: str) -> Decimal:
    """Accept decimal seconds or HH:MM:SS.sss, without a frame field."""
    value = value.strip()
    try:
        if ":" in value:
            if not re.fullmatch(r"\d{2,}:\d{2}:\d{2}(?:\.\d+)?", value):
                raise ValueError("Use HH:MM:SS.sss, not frame timecode")
            hours, minutes, secs = (Decimal(x) for x in value.split(":"))
            if minutes >= 60 or secs >= 60:
                raise ValueError("Clock minutes and seconds must be below 60")
            result = hours * 3600 + minutes * 60 + secs
        else:
            result = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError("Time must be decimal seconds or HH:MM:SS.sss") from exc
    if not result.is_finite() or result < 0:
        raise ValueError("Time must be finite and nonnegative")
    return result


def decimal_text(value: Decimal) -> str:
    return format(value, "f")


def make_plan(source_csv: Path, target: Path, *, dry_run: bool = False) -> list[dict]:
    source_csv = source_csv.resolve()
    target = target.resolve()
    if target.exists():
        raise ValueError("Manifest already exists; use a new output name")
    durations: dict[Path, Decimal] = {}
    jobs: list[dict] = []
    seen: set[str] = set()
    with source_csv.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"id", "source", "start", "end", "checked"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("CSV needs id, source, start, end, checked columns")
        for row_number, row in enumerate(reader, start=2):
            try:
                if None in row or any(row.get(key) is None for key in required):
                    raise ValueError("Row has too many or too few cells")
                job_id = row["id"].strip()
                if not re.fullmatch(r"[A-Z][A-Z0-9_-]{0,39}", job_id) or job_id in seen:
                    raise ValueError("ID must be unique uppercase letters/digits/hyphens/underscores")
                if row["checked"].strip().lower() != "yes":
                    raise ValueError("Review this source range and mark checked as yes")
                source = (source_csv.parent / row["source"].strip()).resolve()
                if not source.is_file():
                    raise ValueError("Source file is missing")
                if source not in durations:
                    probe = probe_media(source, Settings(work_root=target.parent))
                    if not any(s.get("codec_type") == "video" for s in probe.get("streams", [])):
                        raise ValueError("Source needs a video stream")
                    durations[source] = seconds(str(probe["format"]["duration"]))
                start, end = seconds(row["start"]), seconds(row["end"])
                if end <= start:
                    raise ValueError("End must be after start")
                if end > durations[source]:
                    raise ValueError("End is past the probed source duration")
                output = target.parent / "exports" / f"{job_id}-cut-v01.mp4"
                if output.exists() or output.resolve() == source:
                    raise ValueError("Clip output already exists; use a new run folder")
                seen.add(job_id)
                jobs.append({"job_id": job_id, "operation": "cut", "input": str(source),
                             "output": f"exports/{output.name}", "start": decimal_text(start),
                             "duration": decimal_text(end - start)})
            except (ValueError, KeyError, ClipkitError) as exc:
                raise ValueError(f"CSV row {row_number}: {exc}") from exc
    if not jobs:
        raise ValueError("CSV contains no clip rows")
    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation also refuses an output created during validation.
        with target.open("x", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(jobs)
    return jobs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--moments", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        rows = make_plan(args.moments, args.output, dry_run=args.dry_run)
    except (ValueError, OSError, ClipkitError) as exc:
        parser.exit(2, f"clip plan: {exc}\n")
    print(json.dumps({"written": not args.dry_run, "jobs": rows}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
