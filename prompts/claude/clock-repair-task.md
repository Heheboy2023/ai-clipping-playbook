# Repair the clock-input bug

Read CLAUDE.md, AGENTS.md, and work/clock-repair/README.md.
Work only in work/clock-repair/. The decimal-time example works, but clock input
fails. Reproduce the supplied test failure before editing.

Repair seconds() in clip_plan.py. Accept decimal seconds and HH:MM:SS.sss.
Reject negative, NaN, infinite, bad-minute, bad-second, and frame-timecode values.
Return Decimal values, preserving subsecond precision. Do not change expected
test answers, skip cases, or replace a bad time with zero.

Leave the CSV, naming, no-overwrite, and source-validation rules unchanged.
Run the supplied focused tests. Use moments-clock.csv to make a dry-run plan
and verify the three durations match the decimal example. Run the full suite.
No downloads, installs, publishing, source-media changes, or settings changes.
Report the cause, changed lines, commands, and actual results in plain English.
