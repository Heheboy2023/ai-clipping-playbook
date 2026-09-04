from __future__ import annotations

import csv
from pathlib import Path

from clipkit.candidates import compare_candidates, score_candidates, validate_candidates


FIELDS = [
    "candidate_id", "start", "end", "summary", "clarity", "standalone_value",
    "audience_fit", "tension", "emotion", "surprise", "utility", "payoff",
    "source_integrity", "visual_viability", "rights_clear", "disqualifier",
]


def write_candidates(path: Path, start: float = 0.0, rights: str = "true") -> None:
    row = {field: "4" for field in FIELDS}
    row.update({"candidate_id": "C-001", "start": str(start), "end": "5", "summary": "A complete thought", "rights_clear": rights, "disqualifier": ""})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerow(row)


def test_validate_score_and_compare(tmp_path: Path) -> None:
    human = tmp_path / "human.csv"
    ai = tmp_path / "ai.csv"
    scored = tmp_path / "scored.csv"
    write_candidates(human)
    write_candidates(ai, start=0.25)
    assert validate_candidates(human)["valid"] is True
    result = score_candidates(human, scored)
    assert result["eligible"] == 1
    assert result["performance_prediction"] is False
    comparison = compare_candidates(human, ai, None, tolerance=0.5)
    assert comparison["comparisons"][0]["status"] == "aligned"
    assert comparison["human_review_required"] is True


def test_missing_rights_disqualifies(tmp_path: Path) -> None:
    source = tmp_path / "source.csv"
    output = tmp_path / "output.csv"
    write_candidates(source, rights="false")
    result = score_candidates(source, output)
    assert result["disqualified"] == 1
