import json
from pathlib import Path

import pytest

from clipkit.errors import ClipkitError
from clipkit.package import validate_package


def test_package_validation_detects_tampering(tmp_path: Path) -> None:
    media = tmp_path / "media"
    media.mkdir()
    target = media / "clip.mp4"
    target.write_bytes(b"changed")
    (tmp_path / "package-manifest.json").write_text(
        json.dumps({"files": [{"path": "media/clip.mp4", "sha256": "0" * 64}]}),
        encoding="utf-8",
    )
    with pytest.raises(ClipkitError) as error:
        validate_package(tmp_path)
    assert error.value.kind == "invalid_package"
