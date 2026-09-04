from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .batch import run_batch
from .candidates import compare_candidates, score_candidates, validate_candidates
from .captions import segments_to_srt
from .doctor import doctor
from .errors import ClipkitError
from .media import (
    burn_captions,
    concat_media,
    cut_media,
    normalize_audio,
    probe_media,
    vertical_media,
)
from .package import audit_brand, package_run, validate_package
from .pipeline import approve_run, run_pipeline, run_status
from .project import init_project, intake_source
from .qc import qc_state
from .render import render_manifest
from .retrieve import retrieve_metadata
from .settings import load_settings
from .transcript import transcribe_whisper, validate_transcript


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="clipkit",
        description=(
            "Local, testable clipping utilities. No command publishes to an external platform."
        ),
    )
    parser.add_argument("--version", action="version", version=f"clipkit {__version__}")
    parser.add_argument("--config", help="Path to clipkit TOML configuration.")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit a stable JSON success or error envelope.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor", help="Check Python, media tools, optional agents, and auth presence.")
    sub.add_parser("version-report", help="Alias of doctor for reproducibility records.")

    init = sub.add_parser("init", help="Create the standard rights-aware project folder tree.")
    init.add_argument("project", help="Project directory to create or complete.")
    init.add_argument("--name", help="Stable project identifier; defaults to folder name.")

    intake = sub.add_parser("intake", help="Copy or reference an authorized source and hash it.")
    intake.add_argument("--project", required=True)
    intake.add_argument("--input", required=True)
    intake.add_argument("--mode", choices=["copy", "reference"], default="copy")
    intake.add_argument("--confirmed-authorized", action="store_true")

    probe = sub.add_parser("probe", help="Read raw ffprobe stream/container JSON.")
    probe.add_argument("--input", required=True)
    probe.add_argument("--raw", action="store_true", help="Compatibility flag; JSON is preserved.")

    retrieve = sub.add_parser(
        "retrieve-metadata",
        help="Use yt-dlp to record sanitized metadata without downloading media.",
    )
    retrieve.add_argument("--url", required=True)
    retrieve.add_argument("--output", required=True)
    retrieve.add_argument("--confirmed-authorized", action="store_true")
    retrieve.add_argument("--overwrite", action="store_true")

    transcribe = sub.add_parser("transcribe", help="Transcribe local authorized media with Whisper CLI.")
    transcribe.add_argument("--input", required=True)
    transcribe.add_argument("--output", required=True, help="Output directory.")
    transcribe.add_argument("--provider", choices=["whisper-cli"], default="whisper-cli")
    transcribe.add_argument("--model", default="tiny.en")
    transcribe.add_argument("--language")
    transcribe.add_argument("--overwrite", action="store_true")

    validate_transcript_parser = sub.add_parser(
        "validate-transcript", help="Validate normalized transcript timing and segment fields."
    )
    validate_transcript_parser.add_argument("--manifest", required=True)

    candidates = sub.add_parser("candidates", help="Validate or score candidate moments.")
    candidate_sub = candidates.add_subparsers(dest="candidate_command", required=True)
    candidate_validate = candidate_sub.add_parser("validate", help="Validate candidate records.")
    candidate_validate.add_argument("--input", required=True)
    candidate_score = candidate_sub.add_parser(
        "score", help="Apply an editorial heuristic; this does not predict performance."
    )
    candidate_score.add_argument("--input", required=True)
    candidate_score.add_argument("--output", required=True)
    candidate_score.add_argument("--weights")

    validate_candidate_alias = sub.add_parser(
        "validate-candidates", help="Top-level alias for candidates validate."
    )
    validate_candidate_alias.add_argument("--input", required=True)

    compare = sub.add_parser(
        "compare-candidates", help="Compare human and AI candidate boundaries by stable ID."
    )
    compare.add_argument("--human", required=True)
    compare.add_argument("--ai", required=True)
    compare.add_argument("--output")
    compare.add_argument("--tolerance", type=float, default=0.5)

    cut = sub.add_parser("cut", help="Create an accurate local clip with FFmpeg.")
    cut.add_argument("--input", required=True)
    cut.add_argument("--output", required=True)
    cut.add_argument("--start", default="0")
    end_group = cut.add_mutually_exclusive_group(required=True)
    end_group.add_argument("--end")
    end_group.add_argument("--duration")
    cut.add_argument("--stream-copy", action="store_true")
    cut.add_argument("--overwrite", action="store_true")
    cut.add_argument("--dry-run", action="store_true")

    vertical = sub.add_parser("vertical", help="Convert video to a vertical crop or padded layout.")
    vertical.add_argument("--input", required=True)
    vertical.add_argument("--output", required=True)
    vertical.add_argument("--mode", choices=["crop", "pad"], default="crop")
    vertical.add_argument("--width", type=int)
    vertical.add_argument("--height", type=int)
    vertical.add_argument("--overwrite", action="store_true")
    vertical.add_argument("--dry-run", action="store_true")

    captions = sub.add_parser("captions", help="Generate or burn caption files.")
    caption_sub = captions.add_subparsers(dest="caption_command", required=True)
    caption_generate = caption_sub.add_parser("generate", help="Create SRT from segment JSON/YAML.")
    caption_generate.add_argument("--segments", required=True)
    caption_generate.add_argument("--output", required=True)
    caption_generate.add_argument("--overwrite", action="store_true")
    caption_burn = caption_sub.add_parser("burn", help="Burn an SRT file into a local video.")
    caption_burn.add_argument("--input", required=True)
    caption_burn.add_argument("--captions", required=True)
    caption_burn.add_argument("--output", required=True)
    caption_burn.add_argument("--overwrite", action="store_true")
    caption_burn.add_argument("--dry-run", action="store_true")

    audio = sub.add_parser("audio", help="Run documented audio workflows.")
    audio_sub = audio.add_subparsers(dest="audio_command", required=True)
    audio_normalize = audio_sub.add_parser(
        "normalize", help="Apply a review-required single-pass loudness normalization."
    )
    audio_normalize.add_argument("--input", required=True)
    audio_normalize.add_argument("--output", required=True)
    audio_normalize.add_argument("--overwrite", action="store_true")
    audio_normalize.add_argument("--dry-run", action="store_true")

    concat = sub.add_parser("concat", help="Concatenate compatible local files without re-encoding.")
    concat.add_argument("--input", action="append", required=True, dest="inputs")
    concat.add_argument("--output", required=True)
    concat.add_argument("--overwrite", action="store_true")
    concat.add_argument("--dry-run", action="store_true")

    render = sub.add_parser("render", help="Run one manifest-defined media operation.")
    render.add_argument("--manifest", required=True)
    render.add_argument("--dry-run", action="store_true")
    render.add_argument("--overwrite", action="store_true")

    batch = sub.add_parser("batch", help="Run a CSV batch with bounded workers and resume state.")
    batch.add_argument("--manifest", required=True)
    batch.add_argument("--jobs", type=int)
    batch.add_argument("--resume", action="store_true")
    batch.add_argument("--dry-run", action="store_true")

    run = sub.add_parser("run", help="Run a rights-confirmed, human-gated pipeline manifest.")
    run.add_argument("--manifest", required=True)
    run.add_argument("--dry-run", action="store_true")
    run.add_argument("--resume", action="store_true")

    status = sub.add_parser("status", help="Read a pipeline run state without changing it.")
    status.add_argument("--run", required=True, dest="state")

    approve = sub.add_parser("approve", help="Record local human QC; never grants publish authority.")
    approve.add_argument("--run", required=True, dest="state")
    approve.add_argument("--gate", default="human-qc")
    approve.add_argument("--reviewer", required=True)
    approve.add_argument("--notes", default="")

    qc = sub.add_parser("qc", help="Probe completed outputs and write an automated QC report.")
    qc.add_argument("--batch", required=True, dest="state")

    package = sub.add_parser("package", help="Create a local delivery package from an approved run.")
    package.add_argument("--run", required=True, dest="state")
    package.add_argument("--destination", required=True)
    package.add_argument("--output")
    package.add_argument("--overwrite", action="store_true")

    validate_package_parser = sub.add_parser(
        "validate-package", help="Verify package paths, files, and recorded hashes."
    )
    validate_package_parser.add_argument("--path", required=True)

    brand = sub.add_parser("audit-brand", help="Audit package filenames for portable naming.")
    brand.add_argument("--package", required=True)
    return parser


def _dispatch(args: argparse.Namespace) -> dict:
    settings = load_settings(args.config)
    command = args.command
    if command in {"doctor", "version-report"}:
        return doctor(settings)
    if command == "init":
        return init_project(args.project, args.name)
    if command == "intake":
        return intake_source(
            args.project,
            args.input,
            confirmed_authorized=args.confirmed_authorized,
            mode=args.mode,
        )
    if command == "probe":
        return probe_media(args.input, settings)
    if command == "retrieve-metadata":
        return retrieve_metadata(
            args.url,
            args.output,
            confirmed_authorized=args.confirmed_authorized,
            overwrite=args.overwrite,
            settings=settings,
        )
    if command == "transcribe":
        return transcribe_whisper(
            args.input,
            args.output,
            model=args.model,
            language=args.language,
            overwrite=args.overwrite,
            settings=settings,
        )
    if command == "validate-transcript":
        return validate_transcript(args.manifest)
    if command == "candidates":
        if args.candidate_command == "validate":
            return validate_candidates(args.input)
        return score_candidates(args.input, args.output, weights_value=args.weights)
    if command == "validate-candidates":
        return validate_candidates(args.input)
    if command == "compare-candidates":
        return compare_candidates(
            args.human,
            args.ai,
            args.output,
            tolerance=args.tolerance,
        )
    if command == "cut":
        return cut_media(
            args.input,
            args.output,
            start=args.start,
            end=args.end,
            duration=args.duration,
            stream_copy=args.stream_copy,
            overwrite=args.overwrite,
            dry_run=args.dry_run,
            settings=settings,
        )
    if command == "vertical":
        return vertical_media(
            args.input,
            args.output,
            mode=args.mode,
            width=args.width or settings.width,
            height=args.height or settings.height,
            overwrite=args.overwrite,
            dry_run=args.dry_run,
            settings=settings,
        )
    if command == "captions":
        if args.caption_command == "generate":
            return segments_to_srt(args.segments, args.output, overwrite=args.overwrite)
        return burn_captions(
            args.input,
            args.captions,
            args.output,
            overwrite=args.overwrite,
            dry_run=args.dry_run,
            settings=settings,
        )
    if command == "audio":
        return normalize_audio(
            args.input,
            args.output,
            overwrite=args.overwrite,
            dry_run=args.dry_run,
            settings=settings,
        )
    if command == "concat":
        return concat_media(
            args.inputs,
            args.output,
            overwrite=args.overwrite,
            dry_run=args.dry_run,
            settings=settings,
        )
    if command == "render":
        return render_manifest(
            args.manifest,
            dry_run=args.dry_run,
            overwrite=args.overwrite,
            settings=settings,
        )
    if command == "batch":
        result = run_batch(
            args.manifest,
            jobs=args.jobs or settings.batch_jobs,
            resume=args.resume,
            dry_run=args.dry_run,
            settings=settings,
        )
        if result["failed"]:
            result["_exit_code"] = 3
        return result
    if command == "run":
        result = run_pipeline(
            args.manifest,
            dry_run=args.dry_run,
            resume=args.resume,
            settings=settings,
        )
        if result["status"] == "failed":
            result["_exit_code"] = 3
        return result
    if command == "status":
        return run_status(args.state)
    if command == "approve":
        return approve_run(
            args.state,
            gate=args.gate,
            reviewer=args.reviewer,
            notes=args.notes,
        )
    if command == "qc":
        result = qc_state(args.state, settings)
        if not result["automated_pass"]:
            result["_exit_code"] = 3
        return result
    if command == "package":
        return package_run(
            args.state,
            args.destination,
            args.output,
            overwrite=args.overwrite,
        )
    if command == "validate-package":
        return validate_package(args.path)
    if command == "audit-brand":
        return audit_brand(args.package)
    raise ClipkitError(f"Unknown command: {command}")


def _emit_success(command: str, data: dict, json_mode: bool) -> int:
    exit_code = int(data.pop("_exit_code", 0))
    if json_mode:
        print(json.dumps({"ok": exit_code == 0, "command": command, "data": data}, sort_keys=True))
    else:
        print(f"clipkit {command}: {'complete' if exit_code == 0 else 'completed with failures'}")
        print(json.dumps(data, indent=2, sort_keys=True))
    return exit_code


def main(argv: list[str] | None = None) -> int:
    raw = list(sys.argv[1:] if argv is None else argv)
    json_mode = "--json" in raw
    if json_mode:
        raw = [item for item in raw if item != "--json"]
    parser = _parser()
    try:
        args = parser.parse_args(raw)
        args.json = json_mode
        data = _dispatch(args)
        return _emit_success(args.command, data, json_mode)
    except ClipkitError as exc:
        payload = {
            "ok": False,
            "error": {"type": exc.kind, "message": str(exc), "details": exc.details},
        }
        if json_mode:
            print(json.dumps(payload, sort_keys=True))
        else:
            print(f"clipkit error: {exc}", file=sys.stderr)
            if exc.details:
                print(json.dumps(exc.details, indent=2, sort_keys=True), file=sys.stderr)
        return exc.code
    except KeyboardInterrupt:
        if json_mode:
            print(json.dumps({"ok": False, "error": {"type": "interrupted", "message": "Interrupted."}}))
        else:
            print("clipkit: interrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
