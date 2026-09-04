#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def validate(output_value: str, root_value: str, *, hook_mode: bool = False) -> int:
    output = Path(output_value).expanduser().resolve()
    root = Path(root_value).expanduser().resolve()
    try:
        output.relative_to(root)
    except ValueError:
        stream = sys.stderr if hook_mode else sys.stdout
        print(f"blocked: {output} is outside {root}", file=stream)
        return 2
    print(f"allowed: {output}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Reject an output outside an allowed root.")
    parser.add_argument("output", nargs="?")
    parser.add_argument("allowed_root", nargs="?")
    parser.add_argument(
        "--hook-root",
        help="Read Claude Code hook JSON from stdin and validate its file_path against this root.",
    )
    args = parser.parse_args()
    if args.hook_root:
        payload = json.load(sys.stdin)
        tool_input = payload.get("tool_input") or {}
        output = tool_input.get("file_path") or tool_input.get("path")
        if not output:
            print("blocked: hook input does not include file_path", file=sys.stderr)
            return 2
        return validate(str(output), args.hook_root, hook_mode=True)
    if not args.output or not args.allowed_root:
        parser.error("output and allowed_root are required outside hook mode")
    return validate(args.output, args.allowed_root)


if __name__ == "__main__":
    raise SystemExit(main())
