from __future__ import annotations

import json
from pathlib import Path

import pytest

from clipkit.errors import ClipkitError
from clipkit.io import assert_within, output_path
from clipkit.project import init_project, intake_source


def test_assert_within_rejects_escape(tmp_path: Path) -> None:
    with pytest.raises(ClipkitError, match="escapes") as error:
        assert_within(tmp_path.parent / "outside.mp4", tmp_path)
    assert error.value.kind == "path_escape"


def test_output_refuses_existing_file(tmp_path: Path) -> None:
    target = tmp_path / "exists.txt"
    target.write_text("preserve", encoding="utf-8")
    with pytest.raises(ClipkitError, match="already exists"):
        output_path(target)
    assert target.read_text(encoding="utf-8") == "preserve"


def test_project_intake_requires_authorization_and_hashes_source(tmp_path: Path) -> None:
    project = tmp_path / "project"
    source = tmp_path / "source.txt"
    source.write_text("safe fixture", encoding="utf-8")
    result = init_project(project, "demo")
    assert "00_admin/project.json" in result["created"]
    with pytest.raises(ClipkitError) as error:
        intake_source(project, source, confirmed_authorized=False)
    assert error.value.kind == "authorization_required"
    intake = intake_source(project, source, confirmed_authorized=True)
    manifest = json.loads(Path(intake["manifest"]).read_text(encoding="utf-8"))
    assert manifest["authorization_confirmed"] is True
    assert len(manifest["sha256"]) == 64
    assert Path(manifest["stored_path"]).read_text(encoding="utf-8") == "safe fixture"
