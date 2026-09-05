from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from .errors import ClipkitError
from .fingerprint import operation_fingerprint
from .io import read_csv, sha256_file, write_json
from .operations import resolve_relative, run_operation
from .settings import Settings


def _batch_options(row: dict[str, str], base: Path) -> dict:
    options: dict = {}
    for key in ("start", "end", "duration", "mode", "width", "height"):
        if row.get(key, "").strip():
            options[key] = row[key].strip()
    if row.get("captions", "").strip():
        options["captions"] = str(resolve_relative(base, row["captions"].strip()))
    if row.get("stream_copy", "").strip().lower() in {"1", "true", "yes"}:
        options["stream_copy"] = True
    return options


def run_batch(
    manifest_value: str | Path,
    *,
    jobs: int,
    resume: bool,
    dry_run: bool,
    settings: Settings,
) -> dict:
    manifest_path = Path(manifest_value).expanduser().resolve()
    rows = read_csv(manifest_path)
    if not rows:
        raise ClipkitError("Batch manifest contains no jobs.")
    base = manifest_path.parent
    state_path = base / ".clipkit-batch-state.json"
    previous: dict = {}
    if resume and state_path.is_file():
        from .io import load_data

        loaded = load_data(state_path)
        previous = {
            item["job_id"]: item for item in loaded.get("jobs", [])
        } if isinstance(loaded, dict) else {}

    prepared: list[dict] = []
    seen: set[str] = set()
    outputs: set[Path] = set()
    for index, row in enumerate(rows, start=1):
        job_id = row.get("job_id", "").strip()
        operation = row.get("operation", "").strip()
        if not job_id or job_id in seen:
            raise ClipkitError(f"Batch row {index} has a missing or duplicate job_id.")
        if not operation or not row.get("input") or not row.get("output"):
            raise ClipkitError(f"Batch row {index} is missing operation/input/output.")
        seen.add(job_id)
        input_path = resolve_relative(base, row["input"])
        output_path = resolve_relative(base, row["output"])
        if output_path in outputs:
            raise ClipkitError(f"Batch rows share an output path: {output_path}")
        outputs.add(output_path)
        prepared.append(
            {
                "job_id": job_id,
                "operation": operation,
                "input": str(input_path),
                "output": str(output_path),
                "options": _batch_options(row, base),
                "status": "pending",
            }
        )

    inputs = {Path(item["input"]) for item in prepared}
    if inputs & outputs:
        raise ClipkitError(
            "Batch inputs and outputs must be separate. Use run for dependent steps."
        )

    def execute(item: dict) -> dict:
        try:
            fingerprint = operation_fingerprint(item, settings)
            old = previous.get(item["job_id"])
            output = Path(item["output"])
            if (
                resume and old
                and old.get("status") in {"completed", "skipped_completed"}
                and old.get("fingerprint") == fingerprint
                and output.is_file()
                and old.get("output_hash") == sha256_file(output)
            ):
                return {**old, "status": "skipped_completed"}
            result = run_operation(
                item["operation"],
                input_path=Path(item["input"]),
                output_path=Path(item["output"]),
                options=item["options"],
                settings=settings,
                overwrite=False,
                dry_run=dry_run,
            )
            return {
                **item, "status": "planned" if dry_run else "completed",
                "result": result, "fingerprint": fingerprint,
                "output_hash": sha256_file(output) if not dry_run else None,
            }
        except ClipkitError as exc:
            return {
                **item,
                "status": "failed",
                "error": {"type": exc.kind, "message": str(exc), "details": exc.details},
            }

    results: list[dict] = []
    worker_count = max(1, min(int(jobs), 8))
    with ThreadPoolExecutor(max_workers=worker_count) as pool:
        futures = [pool.submit(execute, item) for item in prepared]
        for future in as_completed(futures):
            results.append(future.result())
    results.sort(key=lambda item: item["job_id"])
    state = {
        "schema_version": 1,
        "manifest": str(manifest_path),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": dry_run,
        "worker_count": worker_count,
        "jobs": results,
    }
    if not dry_run:
        write_json(state_path, state)
    failed = sum(item["status"] == "failed" for item in results)
    return {
        "state": None if dry_run else str(state_path),
        "jobs": len(results),
        "failed": failed,
        "completed": sum(item["status"] in {"completed", "skipped_completed"} for item in results),
        "results": results,
    }
