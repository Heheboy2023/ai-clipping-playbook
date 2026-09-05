# Four-layer setup check

Run from the repository root, using the project's active Python environment.
These are read-only diagnostics; doctor reports tool availability but does not
install software or contact a transcription service.

```bash
python -c "from pathlib import Path; print(Path('pyproject.toml').is_file())"
python -c "import sys; print(sys.executable)"
python -m pip --version
python -m clipkit doctor
```

Expect True for the root-file check. The Python path should point into your
project environment. Check doctor's core readiness, not the presence of every
optional program. Missing optional agents/transcription tools do not prevent
the core FFmpeg exercises. A skipped media test is not a passed media test.

If activation is unavailable on Windows, use `.venv\Scripts\python.exe` in
place of `python` on every line above. See the installation guide for setup;
these diagnostics do not replace installation.
