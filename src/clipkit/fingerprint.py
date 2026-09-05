"""Bind reusable media outputs to the exact input bytes and operation settings."""
from dataclasses import asdict
import hashlib
import json
from pathlib import Path

from .io import sha256_file
from .settings import Settings


def operation_fingerprint(item: dict, settings: Settings) -> str:
    source = Path(item["input"])
    caption_value = item["options"].get("captions")
    captions = Path(caption_value) if caption_value else None
    record = {key: item[key] for key in ("operation", "input", "output", "options")}
    record["source_hash"] = sha256_file(source) if source.is_file() else None
    record["caption_hash"] = sha256_file(captions) if captions and captions.is_file() else None
    record["settings"] = asdict(settings)
    return hashlib.sha256(json.dumps(record, sort_keys=True, default=str).encode()).hexdigest()
