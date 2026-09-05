# Turn my checked moments into a cut plan

Read AGENTS.md, examples/agent-clip-plan/README.md, and src/clipkit/batch.py.
Build a small planner under work/codex-clip-plan/ with tests and a short README.
Do not change the checked-in reference or installed Clipkit implementation.

Input CSV columns: id, source, start, end, checked.
Use the reference README's naming, timing, source-relative-path, validation, and
no-overwrite rules. Plan only checked rows; reject the whole input if a row needs
repair. Compute duration as end minus start. Probe each distinct local source
once. Reuse Clipkit's probe function; do not invent another downloader or encoder.

Output a Clipkit CSV with job_id, operation, input, output, start, duration.
Each operation is cut; outputs belong in an exports folder beside that manifest.
The planner must not render, publish, retrieve media, rename originals, or need
new packages. Provide --dry-run that writes no files or directories.

Explain the proposed files and tests, then implement. Test decimal and clock
times, an end before start, a missing source, duplicate IDs, checked=no, NaN,
past-end ranges, empty input, and existing output refusal. Run the three-fixture
cut batch in a new work folder and verify count and approximate durations.
Run focused tests and the full repository suite. Report actual results and
anything not checked. Do not describe pattern fixtures as finished social clips.
