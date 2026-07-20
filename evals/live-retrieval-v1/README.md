# Live retrieval benchmark run — 2026-07-16

This directory is the durable output of the fixed 20-topic suite in
`evals/retrieval-topics-v1.jsonl`, run with five results per source and no OpenAlex or Semantic
Scholar API key.

Measured results:

| Source | Successful topics | Success rate |
|---|---:|---:|
| arXiv | 20/20 | 100% |
| OpenAlex | 0/20 | 0% |
| Semantic Scholar | 4/20 | 20% |
| OpenReview | 20/20 | 100% |

The run produced 217 source provenance records, 214 canonical records, zero remaining duplicate
records, and 214 serializable records. All 20 search manifests replay byte-for-byte after hash
verification.

This run is deliberately marked `publishable: false`. Every OpenAlex failure records the missing
`OPENALEX_API_KEY`; all 16 Semantic Scholar failures are HTTP 429 responses. Semantic Scholar's
official API page states that unauthenticated traffic shares a public rate limit and may be further
throttled during heavy use. A publishable reliability run therefore requires a caller-owned
OpenAlex key and should use a caller-owned Semantic Scholar key, followed by a fresh output
directory rather than editing this evidence.

See `report.json` for the machine-readable aggregate and each topic directory for canonical
records, failure logs, and replay manifests.
