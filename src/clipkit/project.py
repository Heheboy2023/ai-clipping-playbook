from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path

from .errors import ClipkitError
from .io import existing_file, sha256_file, write_json


PROJECT_FOLDERS = [
    "00_admin",
    "01_source",
    "02_proxy",
    "03_transcript",
    "04_candidates",
    "05_edit",
    "06_render",
    "07_delivery",
    "08_archive",
    "logs",
]


def init_project(path_value: str | Path, name: str | None = None) -> dict:
    root = Path(path_value).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    for folder in PROJECT_FOLDERS:
        target = root / folder
        if not target.exists():
            target.mkdir(parents=True)
            created.append(folder)

    manifest_path = root / "00_admin" / "project.json"
    if not manifest_path.exists():
        write_json(
            manifest_path,
            {
                "schema_version": 1,
                "project_id": name or root.name,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "authorization_status": "unconfirmed",
                "notes": "Confirm rights before intake or processing.",
            },
        )
        created.append("00_admin/project.json")
    return {"project_root": str(root), "created": created, "folders": PROJECT_FOLDERS}


def intake_source(
    project_value: str | Path,
    input_value: str | Path,
    *,
    confirmed_authorized: bool,
    mode: str = "copy",
) -> dict:
    if not confirmed_authorized:
        raise ClipkitError(
            "Intake is blocked until --confirmed-authorized is supplied.",
            kind="authorization_required",
        )
    project = Path(project_value).expanduser().resolve()
    if not (project / "00_admin" / "project.json").is_file():
        raise ClipkitError("Project is not initialized. Run clipkit init first.")
    source = existing_file(input_value, label="source")
    digest = sha256_file(source)
    destination = project / "01_source" / source.name

    if mode == "copy":
        if destination.exists():
            if sha256_file(destination) != digest:
                raise ClipkitError(
                    f"A different file already uses this source name: {destination}",
                    kind="name_collision",
                )
        else:
            shutil.copy2(source, destination)
        stored_path = destination
    elif mode == "reference":
        stored_path = source
    else:
        raise ClipkitError(f"Unsupported intake mode: {mode}")

    record = {
        "schema_version": 1,
        "authorization_confirmed": True,
        "mode": mode,
        "original_path": str(source),
        "stored_path": str(stored_path),
        "filename": source.name,
        "size_bytes": source.stat().st_size,
        "sha256": digest,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    manifest_path = project / "00_admin" / "source-manifest.json"
    write_json(manifest_path, record)
    return {"manifest": str(manifest_path), "source": record}
