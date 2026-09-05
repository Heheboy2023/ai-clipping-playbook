# Chapter 18 — Build and Fix a Workflow With Claude Code — command sheet

Generated from the chapter source. Run commands in chapter order, not as one script.
Online, installation, transcription, and agent commands require the setup or input described in the chapter.
Replace clearly named placeholders before use. Use only the shell for your operating system.

## Command block 1

```bash
brew install --cask claude-code
```

## Command block 2

```powershell
winget install Anthropic.ClaudeCode
```

## Command block 3

```bash
claude --version
claude doctor
```

## Command block 4

```bash
claude --permission-mode plan
```

## Command block 5

```bash
claude
```

## Command block 6

```bash
python work/claude-practice/clip_name.py --creator "Nova Show" --moment "Intro Fix!" --version 12
```

## Command block 7

```bash
python work/claude-practice/clip_name.py --creator "Nova" --moment "intro" --version 0
```

## Command block 8

```bash
python -m pytest work/claude-practice/test_clip_name.py -q
python -m pytest -q
```

## Command block 9

```bash
python examples/agent-clip-plan/prepare_repair.py
```

## Command block 10

```bash
python -m pytest work/clock-repair/test_clock.py -q
```

## Command block 11

```bash
python -m pytest work/clock-repair/test_clock.py -q
```

## Command block 12

```bash
python work/clock-repair/clip_plan.py --moments examples/agent-clip-plan/moments-clock.csv --output work/clock-plan/jobs.csv --dry-run
```

## Command block 13

```bash
python -m pytest -q
```

## Command block 14

```bash
python examples/agent-clip-plan/clip_plan.py --moments examples/agent-clip-plan/moments-clock.csv --output work/reference-clock/jobs.csv --dry-run
```

## Command block 15

```bash
python -m pytest tests/test_caption_readability.py -q
```
