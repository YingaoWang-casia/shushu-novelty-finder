# Migrating from v0.1 to v0.2

v0.2 keeps the three legacy script entry points, but the durable workflow now uses the `shushu`
CLI and versioned JSON/JSONL records.

## Command mapping

| v0.1 workflow | v0.2 command |
|---|---|
| arXiv-only search script | `shushu search --source arxiv` |
| paper JSONL normalization | `shushu normalize` |
| Markdown report check | `shushu validate` |
| no equivalent | `shushu run` / `shushu next` resumable workflow |
| no equivalent | `shushu fulltext`, `ledger`, `lineage`, `collision`, `reviewer`, `report` |
| no equivalent | `shushu benchmark validate|plan|score` |

## Data changes

- Durable records reject unknown fields and include `schema_version: "1.0"`.
- A paper must include a canonical identifier and provenance.
- A strong claim needs at least one full-text support reference with a locator and passage hash.
- Medium/strong ideas name their closest prior work and every idea has kill criteria.
- Collision and reviewer contexts are independently hashed.
- P9 now expects `report/manifest.json`; the Markdown report path lives in that manifest.
- A run that reaches reviewer audit also stores its claim ledger at `papers/claims.jsonl`.

Export a contract before migrating custom producers:

```bash
shushu schema paper --output schemas/paper.schema.json
shushu schema report-manifest --output schemas/report-manifest.schema.json
```

Do not relabel an old abstract-only record as full-text verified. Re-run acquisition and record the
page locator and passage hash.
