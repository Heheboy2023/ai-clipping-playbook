# Chapter 14 — Learn the Terminal, GitHub, and the Starter Repo — command sheet

Generated from the chapter source. Run commands in chapter order, not as one script.
Online, installation, transcription, and agent commands require the setup or input described in the chapter.
Replace clearly named placeholders before use. Use only the shell for your operating system.

## Command block 1

```bash
pwd
ls
```

## Command block 2

```powershell
Get-Location
Get-ChildItem
```

## Command block 3

```bash
brew install python ffmpeg
python3 --version
ffmpeg -version
ffprobe -version
```

## Command block 4

```powershell
py -3 --version
ffmpeg -version
ffprobe -version
```

## Command block 5

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Command block 6

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Command block 7

```powershell
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -e ".[dev]"
.venv\Scripts\clipkit.exe doctor
```

## Command block 8

```bash
python scripts/generate_fixtures.py
clipkit doctor
python -m pytest
```

## Command block 9

```bash
source .venv/bin/activate
clipkit doctor
```

## Command block 10

```powershell
.venv\Scripts\Activate.ps1
clipkit doctor
```

## Command block 11

```bash
python -m pytest
```

## Command block 12

```bash
python -c "from pathlib import Path; print(Path('pyproject.toml').is_file())"
```

## Command block 13

```bash
python -c "import sys; print(sys.executable)"
```

## Command block 14

```bash
python -m pip --version
python -m clipkit doctor
```
