from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .errors import ClipkitError
from .fingerprint import operation_fingerprint
from .io import assert_within, load_data, sha256_file, write_json
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
    ids: set[str] = set()
    outputs: set[Path] = set()
    for index, step in enumerate(steps, start=1):
        if not isinstance(step, dict) or not step.get("id") or not step.get("output"):
            raise ClipkitError(f"Pipeline step {index} needs a unique id and output.")
        step_id = str(step["id"]).strip()
        target = assert_within(resolve_relative(base, step["output"]), work_root)
        if not step_id or step_id in ids or target in outputs:
            raise ClipkitError("Pipeline step IDs and output paths must be unique.")
        ids.add(step_id)
        outputs.add(target)
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
        try:
            options = dict(step.get("options") or {})
            if options.get("captions"):
                options["captions"] = str(resolve_relative(base, options["captions"]))
            fingerprint = operation_fingerprint({
                "operation": operation, "input": str(input_path),
                "output": str(output_path), "options": options,
            }, settings)
            old = completed_by_id.get(step_id)
            if (resume and old and old.get("fingerprint") == fingerprint
                    and output_path.is_file()
                    and old.get("output_hash") == sha256_file(output_path)):
                results.append({**old, "status": "completed", "resumed": True})
                continue
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
                    "fingerprint": fingerprint,
                    "output_hash": sha256_file(output_path) if not dry_run else None,
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
        "approvals": [],
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
    steps = state.get("steps", [])
    if state.get("status") == "failed" or not steps or any(
        item.get("status") != "completed" for item in steps
    ):
        raise ClipkitError("Complete every pipeline step before recording playback review.")
    hashes = {}
    for item in steps:
        output = Path(item["output"])
        if not output.is_file() or sha256_file(output) != item.get("output_hash"):
            raise ClipkitError("A run output is missing or changed; rerun and review it.")
        hashes[str(output)] = item["output_hash"]
    qc_path = state_path.parent / "qc-report.json"
    qc = load_data(qc_path) if qc_path.is_file() else {}
    if not qc.get("automated_pass") or qc.get("source_state") != str(state_path):
        raise ClipkitError("Run clipkit qc successfully before recording playback review.")
    checked = {item["path"]: item.get("sha256") for item in qc.get("outputs", [])}
    if checked != hashes:
        raise ClipkitError("QC describes different output bytes; run clipkit qc again.")
    approval = {
        "gate": gate,
        "decision": "approved",
        "reviewer": reviewer.strip(),
        "notes": notes.strip(),
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "publishing_authority": False,
        "output_hashes": hashes,
    }
    approvals = [item for item in state.get("approvals", []) if item.get("gate") != gate]
    approvals.append(approval)
    state["approvals"] = approvals
    state["status"] = "human_qc_approved"
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    write_json(state_path, state)
    return {"state": str(state_path), "approval": approval, "status": state["status"]}
