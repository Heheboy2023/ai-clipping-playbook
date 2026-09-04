from __future__ import annotations

import json
from pathlib import Path

from clipkit.cli import main


def test_json_doctor_never_prints_secret(monkeypatch, capsys) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "do-not-print-this")
    code = main(["--json", "doctor"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert code == 0
    assert payload["ok"] is True
    assert payload["data"]["optional_credentials"]["openai_api_key_present"] is True
    assert "do-not-print-this" not in captured.out


def test_json_error_has_stable_shape(capsys, tmp_path: Path) -> None:
    code = main(["--json", "probe", "--input", str(tmp_path / "missing.mp4")])
    payload = json.loads(capsys.readouterr().out)
    assert code == 2
    assert payload["ok"] is False
    assert set(payload["error"]) == {"type", "message", "details"}


def test_retrieval_refuses_without_authorization(capsys, tmp_path: Path) -> None:
    code = main(["--json", "retrieve-metadata", "--url", "https://example.invalid/video", "--output", str(tmp_path / "metadata.json")])
    payload = json.loads(capsys.readouterr().out)
    assert code == 2
    assert payload["error"]["type"] == "authorization_required"
    assert not (tmp_path / "metadata.json").exists()
