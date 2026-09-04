from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .errors import ClipkitError
from .io import assert_within, load_data, write_json
from .operations import resolve_relative, run_operation
from .settings import Settings


def _load_state(path: Path) -> dict:
    if not path.is_file():
        raise ClipkitError(f"Run state does not exist: {path}")
    data = load_data(path)
    if not isinstance(data, dict):
        raise ClipkitError("Run state must be an object.")
    return data


def run_pipeline(
    manifest_value: str | Path,
    *,
    dry_run: bool,
    resume: bool,
    settings: Settings,
) -> dict:
    manifest_path = Path(manifest_value).expanduser().resolve()
    manifest = load_data(manifest_path)
    if not isinstance(manifest, dict):
        raise ClipkitError("Pipeline manifest must be an object.")
    project_id = str(manifest.get("project_id", "")).strip()
    steps = manifest.get("steps")
    if not project_id or not isinstance(steps, list) or not steps:
        raise ClipkitError("Pipeline manifest requires project_id and a nonempty steps list.")
    if not dry_run and not manifest.get("rights_confirmed"):
        raise ClipkitError(
            "Pipeline blocked: rights_confirmed must be true.", kind="authorization_required"
        )
    if not dry_run and not manifest.get("editorial_approved"):
        raise ClipkitError(
            "Pipeline blocked: editorial_approved must be true.", kind="approval_required"
        )

    base = manifest_path.parent
    work_root = resolve_relative(base, manifest.get("work_root", f"work/{project_id}"))
    state_path = work_root / "run-state.json"
    previous_state: dict = {}
    if resume and state_path.is_file():
        previous_state = _load_state(state_path)
    completed_by_id = {
        item["step_id"]: item
        for item in previous_state.get("steps", [])
        if item.get("status") == "completed"
    }

    results: list[dict] = []
    prior_output: Path | None = None
    for index, step in enumerate(steps, start=1):
        if not isinstance(step, dict):
            raise ClipkitError(f"Pipeline step {index} must be an object.")
        step_id = str(step.get("id", "")).strip()
        operation = str(step.get("operation", "")).strip()
        output_value = step.get("output")
        if not step_id or not operation or not output_value:
            raise ClipkitError(f"Pipeline step {index} needs id, operation, and output.")
        output_path = assert_within(resolve_relative(base, output_value), work_root)
        input_value = step.get("input")
        if input_value == "@previous":
            if prior_output is None:
                raise ClipkitError(f"Step {step_id} uses @previous before an output exists.")
            input_path = prior_output
        elif input_value:
            input_path = resolve_relative(base, input_value)
        else:
            raise ClipkitError(f"Pipeline step {step_id} is missing input.")

        prior_output = output_path
        old = completed_by_id.get(step_id)
        if resume and old and output_path.is_file():
            results.append({**old, "status": "completed", "resumed": True})
            continue
        try:
            options = dict(step.get("options") or {})
            if options.get("captions"):
                options["captions"] = str(resolve_relative(base, options["captions"]))
            result = run_operation(
                operation,
                input_path=input_path,
                output_path=output_path,
                options=options,
                settings=settings,
                overwrite=False,
                dry_run=dry_run,
                allow_missing_input=bool(dry_run and input_value == "@previous"),
            )
            results.append(
                {
                    "step_id": step_id,
                    "operation": operation,
                    "input": str(input_path),
                    "output": str(output_path),
                    "status": "planned" if dry_run else "completed",
                    "result": result,
                }
            )
        except ClipkitError as exc:
            results.append(
                {
                    "step_id": step_id,
                    "operation": operation,
                    "input": str(input_path),
                    "output": str(output_path),
                    "status": "failed",
                    "error": {"type": exc.kind, "message": str(exc), "details": exc.details},
                }
            )
            break

    failed = [item for item in results if item["status"] == "failed"]
    state = {
        "schema_version": 1,
        "project_id": project_id,
        "manifest": str(manifest_path),
        "work_root": str(work_root),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "status": "failed" if failed else ("planned" if dry_run else "awaiting_human_qc"),
        "steps": results,
        "approvals": previous_state.get("approvals", []),
    }
    if not dry_run:
        work_root.mkdir(parents=True, exist_ok=True)
        write_json(state_path, state)
    return {
        "state": None if dry_run else str(state_path),
        "project_id": project_id,
        "status": state["status"],
        "steps": results,
    }


def run_status(state_value: str | Path) -> dict:
    state_path = Path(state_value).expanduser().resolve()
    state = _load_state(state_path)
    return {"state": str(state_path), **state}


def approve_run(
    state_value: str | Path,
    *,
    gate: str,
    reviewer: str,
    notes: str,
) -> dict:
    state_path = Path(state_value).expanduser().resolve()
    state = _load_state(state_path)
    if gate != "human-qc":
        raise ClipkitError("Only the human-qc gate is supported.")
    if not reviewer.strip():
        raise ClipkitError("A reviewer name or role is required.")
    approval = {
        "gate": gate,
        "decision": "approved",
        "reviewer": reviewer.strip(),
        "notes": notes.strip(),
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "publishing_authority": False,
    }
    approvals = [item for item in state.get("approvals", []) if item.get("gate") != gate]
    approvals.append(approval)
    state["approvals"] = approvals
    state["status"] = "human_qc_approved"
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    write_json(state_path, state)
    return {"state": str(state_path), "approval": approval, "status": state["status"]}
