# File organization

Create one local working project with `clipkit init work/my-project`. Clipkit creates:

```text
work/my-project/
├── 00_admin/
├── 01_source/
├── 02_proxy/
├── 03_transcript/
├── 04_candidates/
├── 05_edit/
├── 06_render/
├── 07_delivery/
├── 08_archive/
├── logs/
└── 00_admin/project.json
```

Copy an authorized source and record its hash:

```bash
clipkit intake --project work/my-project --input /absolute/path/to/source.mp4 --mode copy --confirmed-authorized
```

Use `--mode reference` for large masters that must stay in managed storage. Do not rename, transcode, or overwrite the original. Store source IDs in transcript, candidate, render, and delivery records so an exported claim can be traced back.

Recommended output names use lowercase portable characters and stable IDs:

```text
project_candidate-platform-v01.mp4
project_candidate-platform-v02-review.mp4
```

See [output naming](output-naming.md) and the intake templates in `templates/`.
