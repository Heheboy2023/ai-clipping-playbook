# Repository security

The binding local policy is [SECURITY.md](../SECURITY.md). In short:

- Keep secrets in the operating-system credential store or an ignored environment file.
- Never place cookies, account exports, private URLs, client media, or transcripts in fixtures.
- Review agent scopes and command plans before granting write access.
- Sanitize absolute paths, identities, metadata, and transcript text before sharing diagnostics.
- Treat source authorization and publishing authority as separate human decisions.
- Do not bypass permission systems to make an agent command work.

`clipkit doctor` reports optional credential presence as booleans and never prints values.
