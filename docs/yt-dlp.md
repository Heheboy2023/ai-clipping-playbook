# yt-dlp installation and verification

Use the project’s [official installation guide](https://github.com/yt-dlp/yt-dlp/wiki/Installation). Common package-manager options are:

```bash
brew install yt-dlp
yt-dlp --version
```

```powershell
winget install yt-dlp
yt-dlp --version
```

Clipkit deliberately exposes metadata-only retrieval:

```bash
clipkit retrieve-metadata --url "AUTHORIZED_URL" --output work/source-metadata.json --confirmed-authorized
```

The command calls yt-dlp with `--dump-single-json --skip-download --no-warnings`, stores a sanitized subset, and records `media_downloaded: false`. It will refuse to run without `--confirmed-authorized`.

When the rights holder has authorized subtitle retrieval, yt-dlp’s documented no-video pattern is:

```bash
yt-dlp --skip-download --write-subs --sub-langs en --sub-format vtt -o "work/authorized/%(id)s.%(ext)s" "AUTHORIZED_URL"
```

For a managed archive record without video, a project may combine `--skip-download`, `--write-info-json`, and `--download-archive work/authorized/archive.txt`. Test the exact extractor against a disposable authorized item before production, and keep archive paths inside the project.

Extractors and platform behavior change. Recheck yt-dlp’s current documentation, the source platform’s rules, and the rights holder’s authorization. Prefer a creator-supplied master or transcript. This repository does not include a general-purpose download command.
