# Local verification manifest

Verification date: 2026-09-03  
Release state: public `v0.1.0` release candidate; URL verification is recorded in the parent book project's QA report  
Host checked: macOS  
Windows state: documented, not clean-machine verified  

## Verified locally

- Python 3.12.11 against the package requirement of Python 3.11 or newer.
- FFmpeg and ffprobe 8.1.1.
- yt-dlp 2026.03.17 command availability; no live external media retrieval performed.
- OpenAI Whisper CLI with a generated speech fixture.
- Codex CLI 0.153.0 and Claude Code 2.1.221 version/help surfaces; no authenticated model task performed.
- Full automated suite: 42 tests passed after the documentation, agent-contract, and FFmpeg fallback checks were updated.
- Real FFmpeg integration paths for cuts, crop/pad, captions, loudness, concat, batch recovery, QC, packaging, and filename audit.
- Generated fixture provenance and repository manifest checks.
- Clean lockfile installation in a temporary Python 3.12.11 environment, followed by the complete beginner walkthrough and all six reusable example dry runs.
- Exact documented raw commands for accurate cutting, center crop, fit/pad, blurred background, picture-in-picture, rotation, loudness, concat, and frame extraction.
- Current Codex and Claude Code version/help surfaces plus `claude doctor`; no authenticated model task or paid API call was made.

## Environment-specific finding

The checked FFmpeg build does not expose the native `subtitles` filter. Clipkit uses its tested raster-caption fallback on this host. Native subtitle-filter instructions remain capability-conditional.

The concat example produced a readable output from compatible generated inputs. FFmpeg emitted a non-monotonic timestamp warning when two copies of the same cut were joined; the documentation therefore continues to require compatible inputs and output inspection rather than promising warning-free concat behavior.

## Not verified or not performed

- Windows clean-machine installation and execution.
- DaVinci Resolve project archives or final UI screenshots.
- Authenticated Codex or Claude Code model behavior, cost, or output quality.
- Live yt-dlp extractor behavior against an authorized external source.
- Uploading, scheduling, publishing, or live destination verification.
- A Windows-generated release artifact; GitHub source archives remain the supported downloads.

The local approval command was exercised only to verify state transitions and package gating. That test used an operator assertion and does not stand in for real-time listening or final human playback review.

This file records the local verification behind `v0.1.0`. Public reachability and logged-out link checks are recorded separately because they depend on GitHub rather than the local toolchain.
