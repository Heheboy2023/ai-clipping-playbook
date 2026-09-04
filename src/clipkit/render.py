from __future__ import annotations

from pathlib import Path

from .errors import ClipkitError
from .io import load_data
from .operations import resolve_relative, run_operation
from .settings import Settings


def render_manifest(
    manifest_value: str | Path,
    *,
    dry_run: bool,
    overwrite: bool,
    settings: Settings,
) -> dict:
    manifest_path = Path(manifest_value).expanduser().resolve()
    manifest = load_data(manifest_path)
    if not isinstance(manifest, dict):
        raise ClipkitError("Render manifest must be an object.")
    for field in ("operation", "input", "output"):
        if not manifest.get(field):
            raise ClipkitError(f"Render manifest is missing: {field}")
    base = manifest_path.parent
    input_path = resolve_relative(base, manifest["input"])
    output_path = resolve_relative(base, manifest["output"])
    options = dict(manifest.get("options") or {})
    if options.get("captions"):
        options["captions"] = str(resolve_relative(base, options["captions"]))
    result = run_operation(
        str(manifest["operation"]),
        input_path=input_path,
        output_path=output_path,
        options=options,
        settings=settings,
        overwrite=overwrite,
        dry_run=dry_run,
    )
    return {"manifest": str(manifest_path), "operation": manifest["operation"], **result}
