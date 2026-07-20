# Engineering Upgrade Status

Updated: 2026-07-20

## Implemented

- installable Python 3.9+ package using `src/` layout, with a hash-locked development/build
  environment consumed by CI;
- CLI commands for retrieval and replay, live retrieval benchmarking, schema export, resumable
  runs, evidence, lineage, gaps, idea portfolios, collision, reviewer audit, benchmark execution
  and scoring, final reports, and release checks;
- strict v1 schemas for all durable P0–P9 and evaluation records;
- evidence gates preventing abstract-only support from becoming a strong claim;
- resumable P0–P9 artifact navigator with primary/auxiliary bundle hashes, legacy migration,
  tamper detection, and non-overwrite behavior;
- arXiv, OpenAlex, Semantic Scholar, and OpenReview connectors;
- bounded retry/backoff, durable per-source failures, and no silent empty search;
- identifier/title-based cross-source deduplication and accepted/preprint merging;
- portable retrieval replay manifests with record/failure counts and SHA-256 verification;
- backward-compatible wrappers for all three v0.1 scripts;
- PDF and HTML acquisition with bounded downloads, PDF size/magic checks, content-addressed
  caching, deterministic text hashes, durable checkpoints, and PDF-to-HTML fallback;
- cross-record Claim-Evidence Ledger validation for paper IDs, page locators, and page hashes;
- lineage graph schemas and cross-record gates for relation endpoints, relation evidence,
  chronological warnings, and contribution saturation;
- independent six-axis novelty collision audits with 3–7 dangerous priors, context-isolation
  hashes, scoop/application-transfer rejection, and bounded structural rewrites;
- a fixed 60-seed benchmark with exact case distribution, eight-domain coverage, and a default
  240-run bare/self-reflection/v0.1/v0.2 matrix;
- a completed 240-run `gpt-5.6-sol` matrix with four 60-run systems, per-output hashes, a completed
  execution manifest, retained failure history, and two hash-bound opaque human-rater packs;
- human-primary aggregation for every specified retrieval, evidence, lineage, idea, and calibration
  metric, full scalar and pairwise coverage gates, and Cohen's kappa;
- external command adapters that execute the fixed run matrix without a shell, persist failures,
  hash outputs, checkpoint after every run, validate prompt/adapter provenance, and safely resume
  completed runs, with a circuit breaker for quota, authentication, and 429 failures;
- coordinator tooling that produces per-rater opaque scalar and pairwise packs, randomizes pair
  order, keeps system identity in a separate key, and unblinds only locked response files;
- deterministic reviewer-audit gates with independent context, evidence-backed objections, one
  structural revision, and fatal-objection abandonment;
- final-report manifests that expose failures, uncertainty, limitations, strong claims, hashes,
  and public-evaluation provenance while binding report text, inputs, and failure logs;
- README release gates that prohibit comparative claims without a complete, human-primary,
  hashed 60-seed evaluation;
- three offline-verifiable real-paper P0–P9 example runs for RAG, LoRA, and CLIP known-scoop
  controls, including PDFs and page-level evidence;
- pytest, Ruff, and GitHub Actions for Python 3.9 and 3.12.

## Current limitations

- OpenAlex requires the caller's `OPENALEX_API_KEY` under the current official API contract;
- raw HTTP response caching is not implemented; replay operates on canonical records plus durable
  failure logs;
- PDF text extraction does not perform semantic entailment or OCR, and visual verification remains
  explicit per document;
- lineage relation classification remains LLM-assisted;
- benchmark system execution and blind-pack generation are complete, while the real two-person
  ratings remain pending; the judgment contracts, coverage checks, aggregation, and agreement
  statistic are implemented;
- the credential-free 20-topic live connector run measured arXiv/OpenReview at 100%, OpenAlex at
  0%, Semantic Scholar at 20%, and zero post-dedup duplicates; a publishable rerun still requires
  caller-owned OpenAlex and Semantic Scholar credentials.

## Final acceptance progress

| # | Acceptance criterion | Status |
|---:|---|---|
| 1 | One command starts a complete run | Implemented (`shushu run --mode full`) |
| 2 | Interrupted runs resume | Implemented |
| 3 | Four real retrieval sources | Implemented; OpenAlex needs user key |
| 4 | Cross-source deduplication | Implemented and contract-tested; 214-record live run had zero remaining duplicates |
| 5 | Every strong claim has traceable evidence | Implemented at schema/ledger level |
| 6 | Abstract-only evidence cannot impersonate full text | Implemented |
| 7 | Independent novelty collision | Implemented at schema/gate level |
| 8 | Scooped ideas downgrade or abandon | Implemented and regression-tested |
| 9 | At least 60 fixed eval seeds | Implemented |
| 10 | Bare-model and old-version baselines | 240/240 real runs complete; matrix, execution manifest, and two-rater blind packs hash-verified |
| 11 | Core code has automated tests | Implemented for current runtime (104 tests) |
| 12 | CI runs on every PR | Workflow configured for push/PR; remote execution not verified here |
| 13 | Reports expose failures and uncertainty | Implemented as a P9 manifest/report gate |
| 14 | README claims are supported by public evals | Enforced: no comparative claim until a hashed public eval passes |

The remaining comparative-release evidence is external: collect paired blind judgments from at
least two research-experienced humans, publish the aggregate report, rerun credentialed connector
reliability, verify remote pull-request CI, and only then update the guarded README claim block
with the report SHA-256.

The command-by-command evidence and remaining external requirements are recorded in
[`acceptance-audit.md`](acceptance-audit.md).
