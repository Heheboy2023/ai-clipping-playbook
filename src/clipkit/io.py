from __future__ import annotations

import csv
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any

import yaml

from .errors import ClipkitError


def existing_file(value: str | Path, *, label: str = "file") -> Path:
    path = Path(value).expanduser().resolve()
    if not path.is_file():
        raise ClipkitError(f"{label} does not exist or is not a file: {path}")
    return path


def existing_dir(value: str | Path, *, label: str = "directory") -> Path:
    path = Path(value).expanduser().resolve()
    if not path.is_dir():
        raise ClipkitError(f"{label} does not exist or is not a directory: {path}")
    return path


def output_path(value: str | Path, *, overwrite: bool = False) -> Path:
    path = Path(value).expanduser().resolve()
    if path.exists() and not overwrite:
        raise ClipkitError(
            f"Output already exists: {path}. Choose another path or pass --overwrite."
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def assert_within(path: Path, root: Path) -> Path:
    resolved = path.expanduser().resolve()
    root_resolved = root.expanduser().resolve()
    try:
        resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise ClipkitError(
            f"Path escapes the allowed root: {resolved}",
            kind="path_escape",
            details={"path": str(resolved), "allowed_root": str(root_resolved)},
        ) from exc
    return resolved


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_data(path_value: str | Path) -> Any:
    path = existing_file(path_value)
    text = path.read_text(encoding="utf-8")
    try:
        if path.suffix.lower() in {".yaml", ".yml"}:
            return yaml.safe_load(text)
        return json.loads(text)
    except (json.JSONDecodeError, yaml.YAMLError) as exc:
        raise ClipkitError(
            f"Could not parse {path.name}: {exc}", kind="invalid_manifest"
        ) from exc


def write_json(path_value: str | Path, data: Any) -> Path:
    path = Path(path_value).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.stem}.", suffix=path.suffix or ".json", dir=path.parent
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(data, handle, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise
    return path


def read_csv(path_value: str | Path) -> list[dict[str, str]]:
    path = existing_file(path_value)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path_value: str | Path, rows: list[dict], fieldnames: list[str]) -> Path:
    path = Path(path_value).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.stem}.", suffix=path.suffix or ".csv", dir=path.parent
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise
    return path

