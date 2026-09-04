# Security Policy

## Supported versions

Security fixes are applied to the current tagged release and the default branch.
Older releases may not receive backports.

| Version | Supported |
|---|---|
| 0.1.x | Yes |
| Earlier prereleases | No |

Report a suspected vulnerability through GitHub's private vulnerability-reporting
feature when it is available. Otherwise contact the repository owner privately.
Do not publish secrets, private transcripts, client media, or proof-of-concept
data in an issue, pull request, or sample file.

## Boundaries

- `clipkit` processes local files and never publishes to a platform.
- Source intake requires an explicit authorization confirmation.
- Existing outputs are not overwritten unless `--overwrite` is supplied.
- Agent prompts prohibit publishing, credential access, broad deletion, and work
  outside the repository or declared media workspace.
- `.env.example` contains variable names only. Real credentials belong in the
  operating system credential store or an untracked environment file.

## Before sharing a diagnostic

Remove usernames, absolute paths, client identifiers, URLs with tokens, media
metadata, transcript text, and environment values. `clipkit doctor` reports only
whether optional credentials are present; it never prints them.
