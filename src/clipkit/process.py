from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Sequence

from .errors import ClipkitError


def executable(name_or_path: str) -> str | None:
    if Path(name_or_path).expanduser().is_file():
        return str(Path(name_or_path).expanduser().resolve())
    return shutil.which(name_or_path)


def run_checked(
    args: Sequence[str],
    *,
    cwd: Path | None = None,
    timeout: int | None = None,
) -> subprocess.CompletedProcess[str]:
    if not args:
        raise ClipkitError("No command was supplied.")
    if executable(str(args[0])) is None:
        raise ClipkitError(
            f"Required command is not available on PATH: {args[0]}",
            kind="missing_dependency",
            details={"command": str(args[0])},
        )
    try:
        return subprocess.run(
            list(args),
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise ClipkitError(
            f"Command timed out after {timeout} seconds: {args[0]}",
            kind="command_timeout",
        ) from exc
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "").strip()[-4000:]
        raise ClipkitError(
            f"Command failed with exit code {exc.returncode}: {args[0]}",
            kind="command_failed",
            details={"returncode": exc.returncode, "stderr": stderr},
        ) from exc


def version_line(command: str, args: list[str] | None = None) -> dict:
    path = executable(command)
    if path is None:
        return {"available": False, "path": None, "version": None, "error": None}
    argv = [command, *(args or ["--version"])]
    try:
        completed = run_checked(argv, timeout=20)
        combined = (completed.stdout or completed.stderr).strip().splitlines()
        return {
            "available": True,
            "path": path,
            "version": combined[0] if combined else "available",
            "error": None,
        }
    except ClipkitError as exc:
        return {
            "available": False,
            "path": path,
            "version": None,
            "error": exc.details.get("stderr") or str(exc),
        }

