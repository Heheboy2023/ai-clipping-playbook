from __future__ import annotations


class ClipkitError(Exception):
    """Expected command failure with a stable exit code and optional details."""

    def __init__(
        self,
        message: str,
        *,
        code: int = 2,
        kind: str = "clipkit_error",
        details: dict | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.kind = kind
        self.details = details or {}

