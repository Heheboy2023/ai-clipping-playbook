# Folder structure

```text
companion-repo/
├── docs/                 guides and workflow boundaries
├── examples/             generated fixtures and reusable manifests
├── prompts/              transcript, scoring, Codex, and Claude contracts
├── schemas/              JSON data contracts
├── scripts/              wrappers, fixture builder, and maintenance tools
├── src/clipkit/           tested Python package
├── templates/            production and business worksheets
├── tests/                unit and media integration tests
└── work/                 ignored local inputs, renders, state, and packages
```

`work/` is intentionally untracked. Generated examples can be recreated; client media, secrets, and rights evidence should never be committed to a public repository.
