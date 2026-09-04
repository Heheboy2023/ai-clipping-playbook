# Publishing boundary

Clipkit stops at a verified local package. It does not log into platforms, upload, schedule, post, approve a live preview, or modify a public account.

The separation is deliberate:

1. `run` creates local media after rights/editorial attestations.
2. `qc` performs mechanical checks.
3. A human watches the full output and uses `approve`.
4. `package` copies the final file and records its hash.
5. `validate-package` rechecks package integrity.
6. A separately authorized human rechecks current destination requirements, metadata, disclosures, account, and live result.

Use `templates/publish-record.csv` and `templates/live-verification.md` to record that later manual work. The generic destination template must be refreshed from official platform documentation before each production use.
