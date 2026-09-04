#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Move generated work to a recoverable local trash folder.")
    parser.add_argument("--yes", action="store_true", help="Confirm moving companion-repo/work.")
    args = parser.parse_args()
    target = (ROOT / "work").resolve()
    if target != (ROOT.resolve() / "work"):
        raise SystemExit("Refusing unexpected work path")
    if not args.yes:
        raise SystemExit("Pass --yes to move generated work")
    if not target.exists():
        print("No generated work directory exists")
        return 0
    trash = ROOT / ".clipkit-trash"
    trash.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    destination = trash / f"work-{stamp}"
    shutil.move(str(target), str(destination))
    print(f"Moved generated work to {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

