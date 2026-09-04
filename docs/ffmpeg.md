# FFmpeg installation and verification

Install a current build from a source linked by the [official FFmpeg download page](https://ffmpeg.org/download.html). macOS users can run `brew install ffmpeg`; Windows users can select a linked build and add its `bin` directory to `PATH`.

Verify both programs and the features Clipkit needs:

```bash
ffmpeg -version
ffprobe -version
ffmpeg -hide_banner -filters
ffmpeg -hide_banner -encoders
clipkit doctor
```

`doctor` checks for `subtitles`, `overlay`, and `loudnorm` filters plus the `libx264` encoder. If native `subtitles` support is missing but `overlay` is available, Clipkit renders reviewed SRT blocks to transparent images and burns them through FFmpeg’s overlay filter. A version string alone does not prove the required capabilities are present.

Run a safe generated-fixture smoke test:

```bash
python scripts/generate_fixtures.py
clipkit cut --input examples/fixtures/sample-podcast.mp4 --output work/ffmpeg-smoke.mp4 --start 0 --duration 3
clipkit probe --input work/ffmpeg-smoke.mp4
```

See [FFmpeg command examples](ffmpeg-commands.md) for the raw equivalents and [troubleshooting](troubleshooting.md) for missing filters or encoders.
