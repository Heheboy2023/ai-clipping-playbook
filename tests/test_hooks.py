import subprocess
import sys
from pathlib import Path


def test_hook_rejects_path_escape(repository_root: Path, tmp_path: Path) -> None:
    completed = subprocess.run([sys.executable, str(repository_root / "scripts/hooks/validate_output_root.py"), str(tmp_path.parent / "outside.mp4"), str(tmp_path)], capture_output=True, text=True, check=False)
    assert completed.returncode == 2
    assert completed.stdout.startswith("blocked:")
