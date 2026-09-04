# Output naming and organization

Use stable, sortable names: `{project}_{candidate}_{destination}_{version}.{ext}`.

Good: `show42_c-014_generic-vertical_v03.mp4`  
Avoid: `FINAL final USE THIS!!.mp4`

Rules:

- Lowercase ASCII letters, numbers, dots, dashes, and underscores travel most reliably.
- Increment versions; do not overwrite prior approved review exports.
- Keep the source ID and candidate ID in manifests even if the public filename omits them.
- Separate working renders, approved local delivery packages, and public publishing records.
- Run `clipkit audit-brand --package work/package-name` for a mechanical filename check. It does not judge aesthetics, rights, or editorial quality.
