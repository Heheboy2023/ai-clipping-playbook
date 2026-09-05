import subprocess
import sys

import pytest


@pytest.mark.parametrize("creator,moment,version,expected", [
    ("Nova Show", "Intro Fix!", "1", "nova-show__intro-fix__v01.mp4"),
    (" NOVA ", "intro   !! fix", "12", "nova__intro-fix__v12.mp4"),
    ("nova", "intro", "100", "nova__intro__v100.mp4"),
])
def test_reference_names(repository_root, tmp_path, creator, moment, version, expected):
    helper = repository_root / "examples/agent-task-codex/reference/clip_name.py"
    result = subprocess.run([sys.executable, str(helper), "--creator", creator,
                             "--moment", moment, "--version", version],
                            cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 0
    assert result.stdout.strip() == expected
    assert not list(tmp_path.iterdir()), "helper must not write media or any other file"


@pytest.mark.parametrize("creator,moment,version,message", [
    ("!!!", "intro", "1", "English letter or digit"),
    ("nova", "", "1", "English letter or digit"),
    ("nova", "intro", "0", "at least 1"),
    ("nova", "intro", "-1", "at least 1"),
    ("nova", "intro", "1.5", "invalid int value"),
])
def test_reference_bad_inputs(repository_root, tmp_path, creator, moment, version, message):
    helper = repository_root / "examples/agent-task-codex/reference/clip_name.py"
    result = subprocess.run([sys.executable, str(helper), "--creator", creator,
                             "--moment", moment, "--version", version],
                            cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode != 0
    assert message in result.stderr
    assert not list(tmp_path.iterdir())
