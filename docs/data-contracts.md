# Data contracts

The JSON Schemas under `schemas/` describe source intake, transcripts, candidates, single renders, batches, pipeline jobs, and QC results. Templates and examples add human-review fields that schemas cannot prove.

Core rules:

- Stable IDs connect source → transcript → candidate → render → package.
- Times are nonnegative seconds with `end > start`.
- Transcript text is source-derived; generated summaries are separate fields.
- Candidate scores retain their inputs and reviewer notes.
- Rights/editorial booleans are operator attestations, not legal findings.
- Run state and package hashes are evidence of process, not proof of content quality.
- Schema versions allow migrations rather than silent shape changes.

The current CLI performs targeted runtime validation. JSON Schema files are also reference contracts for agents, integrations, and future validation tooling.
