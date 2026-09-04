from pathlib import Path

from clipkit.package import audit_brand


def test_brand_audit_flags_nonportable_filename(tmp_path: Path) -> None:
    (tmp_path / "Good-name.mp4").write_bytes(b"fixture")
    result = audit_brand(tmp_path)
    assert result["portable_names"] is False
    assert result["note"].startswith("This mechanical audit")
