# Book and repository update policy

The book explains durable decisions; this repository holds executable and volatile details. Update the repository when a command, dependency, schema, platform field, model behavior, safety boundary, or documented path changes.

For every material update:

1. Record the reason, affected chapters/files, compatibility impact, and migration note.
2. Update implementation, documentation, examples, prompts, and schemas together.
3. Add or change a fixture/test that exposes the old failure or new contract.
4. Run the complete test suite and documented smoke checks in a clean environment.
5. Rebuild `REPOSITORY_MANIFEST.csv` and run its freshness check.
6. Check secrets, licenses, fixture provenance, paths, and publishing boundaries.
7. Recheck living platform facts from current official sources.
8. Update `LOCAL_RELEASE_MANIFEST.md`; do not claim an operating system, agent run, account action, or public release that was not actually verified.

Breaking command/schema changes require a migration note. A correction that affects book meaning requires an errata/update record before a later edition or format is generated. Keep credentials and private user/client data out of update records.

