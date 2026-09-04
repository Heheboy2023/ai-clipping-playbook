# Rights-safe fixtures

Run `python scripts/generate_fixtures.py` from the repository root. The script creates short synthetic video and audio files from FFmpeg test sources and records their hashes in `fixture-manifest.json`. They contain no downloaded creator media, logos, human voices, or third-party music.

These files test mechanics only. They cannot validate editorial quality, speaker detection, natural speech transcription, or crop aesthetics.
