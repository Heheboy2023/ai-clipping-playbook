# Reusable examples

| Example | What it demonstrates | Important limitation |
|---|---|---|
| `podcast/` | Cut → crop → captions → audio | Synthetic split-screen, no real speech |
| `youtube-video/` | Authorized local landscape source | Not a downloader or platform endorsement |
| `livestream/` | VOD excerpt with padded layout | Chat/context must be reviewed separately |
| `gaming/` | Preserve game frame in vertical output | No publisher/music rights conclusion |
| `multi-speaker-podcast/` | Multi-panel source and captions | No automatic identity or active-speaker tracking |
| `batch-production/` | Bounded independent jobs and state | Editorial/QC gates remain per output |
| `end-to-end/` | Render, QC, approve, package, validate | Local-only; no publishing |

Use `--dry-run` first. Generated work lands under ignored `work/` paths so examples do not overwrite repository fixtures.
