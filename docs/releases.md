# Releases and book synchronization

The current public release is `v0.1.0`. Tagged source archives and release notes are available from the [GitHub Releases page](https://github.com/Heheboy2023/ai-clipping-playbook/releases).

Before each release:

1. Run a clean installation on every operating system claimed as verified.
2. Generate fixtures and pass the complete test suite.
3. Execute documented smoke commands and compare `clipkit --help` with `docs/commands.md`.
4. Rebuild and check `REPOSITORY_MANIFEST.csv`.
5. Review secrets, licenses, fixture provenance, volatile platform notes, and public links.
6. Tag the repository and record compatibility notes after the manuscript command set is locked.
7. Record migration notes whenever a command, schema, path, or default changes.
8. Open the repository, release page, and raw README without authentication before printing their destination in the book.

Release archives contain source code and documentation. They intentionally omit virtual environments, generated work, credentials, private media, and client data. Generate the synthetic fixtures locally after installation.

The book should use the stable repository root, not an asset URL tied to one release. A future breaking release must preserve the tagged `v0.1.0` archive and publish migration guidance before a book revision changes commands.
