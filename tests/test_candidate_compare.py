from pathlib import Path

from clipkit.candidates import compare_candidates


def test_repository_candidate_fixture_compares_with_itself(fixtures_dir: Path) -> None:
    source = fixtures_dir / "sample-candidates.csv"
    result = compare_candidates(source, source, None)
    assert all(item["status"] == "aligned" for item in result["comparisons"])
