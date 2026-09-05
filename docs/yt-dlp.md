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

Use one individual supported item, not a channel or playlist. Inspect its title and duration in the resulting JSON. Metadata retrieval does not create an editable media file.

## One-item download and subtitle recipes

Chapter 16's complete copies are in `book-commands/chapter-16.md`. Replace `PASTE_ONE_VIDEO_URL_HERE` with the one creator item you intend to process. These are documented site-dependent recipes, not a promise that every platform replay works.

```bash
yt-dlp --ignore-config --no-playlist --max-downloads 1 --no-overwrites -P work/source -o "%(id)s.%(ext)s" "PASTE_ONE_VIDEO_URL_HERE"
yt-dlp --ignore-config --no-playlist --skip-download --write-subs --sub-langs en --sub-format vtt -o "work/source/%(id)s.%(ext)s" "PASTE_ONE_VIDEO_URL_HERE"
yt-dlp --ignore-config --no-playlist --list-subs "PASTE_ONE_VIDEO_URL_HERE"
```

The download keeps the actual output extension; it does not guarantee MP4/H.264. ffprobe and your editor must inspect the result. Subtitle availability is item-specific; `--write-auto-subs` requests available automatic captions instead of creator-supplied subtitles. Review both.

The official project currently recommends its `yt-dlp-ejs` component and a supported JavaScript runtime for full YouTube support. Follow its linked dependency instructions; installing the Python package named `ffmpeg` does not install the FFmpeg executable. Updating uses the method that installed your copy. The simple Clipkit local labs do not require online retrieval.

When the rights holder has authorized subtitle retrieval, yt-dlp’s documented no-video pattern is:

```bash
yt-dlp --skip-download --write-subs --sub-langs en --sub-format vtt -o "work/authorized/%(id)s.%(ext)s" "AUTHORIZED_URL"
```

For a managed archive record without video, a project may combine `--skip-download`, `--write-info-json`, and `--download-archive work/authorized/archive.txt`. Test the exact extractor against a disposable authorized item before production, and keep archive paths inside the project.

Extractors and platform behavior change. Recheck yt-dlp’s current documentation, the source platform’s rules, and the rights holder’s authorization. Prefer a creator-supplied master or transcript. This repository does not include a general-purpose download command.
