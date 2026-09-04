from __future__ import annotations

import csv
import subprocess
import sys


def test_repository_manifest_is_current(repository_root) -> None:
    completed = subprocess.run([sys.executable, "scripts/build_repository_manifest.py", "--check"], cwd=repository_root, capture_output=True, text=True, check=False)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    with (repository_root / "REPOSITORY_MANIFEST.csv").open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows
    mapped = {row["path"] for row in rows}
    assert "README.md" in mapped
    assert "src/clipkit/cli.py" in mapped
    assert "examples/end-to-end/job.yaml" in mapped
