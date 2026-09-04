from __future__ import annotations

import json
from pathlib import Path

from .errors import ClipkitError
from .io import existing_file, load_data, read_csv, write_csv, write_json


CRITERIA = [
    "clarity",
    "standalone_value",
    "audience_fit",
    "tension",
    "emotion",
    "surprise",
    "utility",
    "payoff",
    "source_integrity",
    "visual_viability",
]


def _truthy(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def load_candidate_rows(path_value: str | Path) -> list[dict]:
    path = existing_file(path_value, label="candidate file")
    if path.suffix.lower() == ".csv":
        rows = read_csv(path)
    else:
        data = load_data(path)
        rows = data.get("candidates") if isinstance(data, dict) else data
    if not isinstance(rows, list):
        raise ClipkitError("Candidate input must contain a list of candidate objects.")
    return [dict(row) for row in rows]


def validate_candidates(path_value: str | Path) -> dict:
    path = existing_file(path_value, label="candidate file")
    rows = load_candidate_rows(path)
    errors: list[str] = []
    seen: set[str] = set()
    for index, row in enumerate(rows, start=1):
        candidate_id = str(row.get("candidate_id", "")).strip()
        if not candidate_id:
            errors.append(f"row {index}: candidate_id is required")
        elif candidate_id in seen:
            errors.append(f"row {index}: duplicate candidate_id {candidate_id}")
        seen.add(candidate_id)
        try:
            start = float(row.get("start", ""))
            end = float(row.get("end", ""))
            if start < 0 or end <= start:
                raise ValueError
        except (TypeError, ValueError):
            errors.append(f"row {index}: start/end must define a positive interval")
        if not str(row.get("summary", "")).strip():
            errors.append(f"row {index}: summary is required")
    if errors:
        raise ClipkitError(
            "Candidate validation failed.",
            kind="invalid_candidates",
            details={"errors": errors},
        )
    return {"input": str(path), "candidates": len(rows), "valid": True}


def score_candidates(
    input_value: str | Path,
    output_value: str | Path,
    *,
    weights_value: str | Path | None = None,
) -> dict:
    validate_candidates(input_value)
    rows = load_candidate_rows(input_value)
    weights = {criterion: 1.0 for criterion in CRITERIA}
    if weights_value:
        loaded = load_data(weights_value)
        if not isinstance(loaded, dict):
            raise ClipkitError("Weights must be a JSON or YAML object.")
        for key, value in loaded.items():
            if key not in CRITERIA:
                raise ClipkitError(f"Unknown scoring criterion: {key}")
            weights[key] = float(value)

    scored: list[dict] = []
    for row in rows:
        score = 0.0
        for criterion in CRITERIA:
            try:
                value = float(row.get(criterion, 0))
            except (TypeError, ValueError) as exc:
                raise ClipkitError(
                    f"{row.get('candidate_id')}: {criterion} must be numeric."
                ) from exc
            if not 0 <= value <= 5:
                raise ClipkitError(
                    f"{row.get('candidate_id')}: {criterion} must be between 0 and 5."
                )
            score += value * weights[criterion]
        rights_clear = _truthy(row.get("rights_clear", "false"))
        disqualifier = str(row.get("disqualifier", "")).strip()
        disqualified = (not rights_clear) or bool(disqualifier)
        result = dict(row)
        result["total_score"] = f"{score:.2f}"
        result["disqualified"] = "true" if disqualified else "false"
        scored.append(result)

    eligible = [row for row in scored if row["disqualified"] == "false"]
    eligible.sort(key=lambda row: float(row["total_score"]), reverse=True)
    ranks = {row["candidate_id"]: index for index, row in enumerate(eligible, start=1)}
    for row in scored:
        row["rank"] = ranks.get(row["candidate_id"], "")
    scored.sort(key=lambda row: (row["disqualified"] == "true", -(float(row["total_score"]))))

    fieldnames: list[str] = []
    for row in scored:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    target = write_csv(output_value, scored, fieldnames)
    return {
        "output": str(target),
        "candidates": len(scored),
        "eligible": len(eligible),
        "disqualified": len(scored) - len(eligible),
        "performance_prediction": False,
    }


def compare_candidates(
    human_value: str | Path,
    ai_value: str | Path,
    output_value: str | Path | None,
    *,
    tolerance: float = 0.5,
) -> dict:
    validate_candidates(human_value)
    validate_candidates(ai_value)
    human = {row["candidate_id"]: row for row in load_candidate_rows(human_value)}
    ai = {row["candidate_id"]: row for row in load_candidate_rows(ai_value)}
    ids = sorted(set(human) | set(ai))
    comparisons: list[dict] = []
    for candidate_id in ids:
        human_row = human.get(candidate_id)
        ai_row = ai.get(candidate_id)
        if human_row and ai_row:
            start_delta = abs(float(human_row["start"]) - float(ai_row["start"]))
            end_delta = abs(float(human_row["end"]) - float(ai_row["end"]))
            status = "aligned" if max(start_delta, end_delta) <= tolerance else "review"
        else:
            start_delta = None
            end_delta = None
            status = "human_only" if human_row else "ai_only"
        comparisons.append(
            {
                "candidate_id": candidate_id,
                "status": status,
                "start_delta": start_delta,
                "end_delta": end_delta,
            }
        )
    result = {
        "human_count": len(human),
        "ai_count": len(ai),
        "tolerance_seconds": tolerance,
        "comparisons": comparisons,
        "human_review_required": True,
    }
    if output_value:
        target = write_json(output_value, result)
        result["output"] = str(target)
    return result

