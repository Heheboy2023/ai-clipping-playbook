# Local verification manifest

## Current reset-book pack — 0.2.0

Internal verification: 2026-09-04. Book: *Clip It & Cash In*. This file records local test scope; the tagged GitHub release records publication.

- Expanded automated suite: **97 passed in 36.19 seconds** on macOS, Python 3.12.11, FFmpeg/ffprobe 8.1.1. The preceding 93-test suite also passed after a fresh documented installation; four nonfinite-caption regression cases were then added and passed.
- yt-dlp version/help: 2026.08.19. No live external-source retrieval was claimed.
- Tested exact chapter command sheets, one-pass cutting/cropping/probing/decoding, setup diagnostics, cut and caption-retiming arithmetic, CSV templates, and weekly capacity math.
- Tested cut planner, clock-time repair, missing-caption pipeline recovery, QC, stale-output detection, approval-state checks, and packaging.
- Repaired raster-caption sizing, overflow handling, and nonfinite timestamp validation.
- Repaired missing pip in the older environment; the fresh standard venv installation included pip normally.
- 342 files mapped to current book chapters. Buyer source archives exclude private manuscript material, personal media, environments, and generated work.
- Codex/Claude examples are locally tested reference implementations and prompt exercises, not claims of authenticated model conversations.
- Windows installation remains documented, not clean-machine tested. Native FFmpeg subtitles depend on the build; the local raster fallback was tested.
- The CLI does not upload, schedule, or publish media. The buyer resources are distributed through the tagged v0.2.0 GitHub release; manuscript and publishing-package files are not part of that repository.

## Historical baseline — 0.1.0

The record below describes the earlier release only. Its counts and tool versions are not the current reset-book verification.

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
