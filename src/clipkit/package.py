from __future__ import annotations

import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

from .errors import ClipkitError
from .io import assert_within, load_data, sha256_file, write_json


SAFE_NAME = re.compile(r"^[a-z0-9][a-z0-9._-]*$")


def _approved(state: dict) -> bool:
    return any(
        item.get("gate") == "human-qc" and item.get("decision") == "approved"
        for item in state.get("approvals", [])
    )


def package_run(
    state_value: str | Path,
    destination: str,
    output_value: str | Path | None,
    *,
    overwrite: bool,
) -> dict:
    state_path = Path(state_value).expanduser().resolve()
    state = load_data(state_path)
    if not isinstance(state, dict):
        raise ClipkitError("Run state must be an object.")
    if not _approved(state):
        raise ClipkitError(
            "Packaging is blocked until clipkit approve records human-qc approval.",
            kind="approval_required",
        )
    if not SAFE_NAME.fullmatch(destination):
        raise ClipkitError("Destination must use lowercase letters, numbers, dots, dashes, or underscores.")
    steps = [
        item
        for item in state.get("steps", [])
        if item.get("status") == "completed" and item.get("output")
    ]
    if not steps:
        raise ClipkitError("Run state contains no completed media output.")
    source = Path(steps[-1]["output"]).expanduser().resolve()
    if not source.is_file():
        raise ClipkitError(f"Final run output is missing: {source}")

    package_root = (
        Path(output_value).expanduser().resolve()
        if output_value
        else state_path.parent / f"package-{destination}"
    )
    if package_root.exists() and any(package_root.iterdir()) and not overwrite:
        raise ClipkitError(
            f"Package directory is not empty: {package_root}. Pass --overwrite to update known files."
        )
    media_dir = package_root / "media"
    media_dir.mkdir(parents=True, exist_ok=True)
    media_name = source.name.lower().replace(" ", "-")
    media_target = media_dir / media_name
    if media_target.exists() and not overwrite:
        raise ClipkitError(f"Package media already exists: {media_target}")
    shutil.copy2(source, media_target)
    relative_media = media_target.relative_to(package_root)
    manifest = {
        "schema_version": 1,
        "destination": destination,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_run_state": str(state_path),
        "publishing_authority": False,
        "files": [
            {
                "path": relative_media.as_posix(),
                "size_bytes": media_target.stat().st_size,
                "sha256": sha256_file(media_target),
            }
        ],
    }
    manifest_path = package_root / "package-manifest.json"
    write_json(manifest_path, manifest)
    return {
        "package": str(package_root),
        "manifest": str(manifest_path),
        "destination": destination,
        "files": len(manifest["files"]),
        "publishing_authority": False,
    }


def validate_package(path_value: str | Path) -> dict:
    root = Path(path_value).expanduser().resolve()
    manifest_path = root / "package-manifest.json"
    manifest = load_data(manifest_path)
    if not isinstance(manifest, dict) or not isinstance(manifest.get("files"), list):
        raise ClipkitError("Package manifest is invalid.")
    records: list[dict] = []
    for item in manifest["files"]:
        relative = Path(str(item.get("path", "")))
        target = assert_within(root / relative, root)
        exists = target.is_file()
        actual_hash = sha256_file(target) if exists else None
        passed = exists and actual_hash == item.get("sha256")
        records.append(
            {
                "path": relative.as_posix(),
                "exists": exists,
                "sha256_matches": passed,
            }
        )
    valid = bool(records) and all(item["sha256_matches"] for item in records)
    if not valid:
        raise ClipkitError(
            "Package validation failed.",
            kind="invalid_package",
            details={"files": records},
        )
    return {
        "package": str(root),
        "manifest": str(manifest_path),
        "files": records,
        "valid": True,
        "publishing_authority": False,
    }


def audit_brand(path_value: str | Path) -> dict:
    root = Path(path_value).expanduser().resolve()
    if not root.is_dir():
        raise ClipkitError(f"Package directory does not exist: {root}")
    findings: list[dict] = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix()
        safe = all(SAFE_NAME.fullmatch(part) for part in Path(relative).parts)
        findings.append({"path": relative, "portable_name": safe})
    return {
        "package": str(root),
        "files": len(findings),
        "portable_names": all(item["portable_name"] for item in findings),
        "findings": findings,
        "note": "This mechanical audit does not judge design quality or brand rights.",
    }

