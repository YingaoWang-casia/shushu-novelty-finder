# Engineering acceptance audit

Audit date: 2026-07-20

This document separates implemented gates from evidence that requires external model runs, API
credentials, GitHub, or human reviewers. Missing external evidence is not replaced with synthetic
results.

## Verification performed

- `ruff check .`: passed;
- `pytest -q`: 117 tests passed;
- hash-locked install from the Python 3.9 bootstrap pip 21.2, lock regeneration, editable install,
  lint, tests, runtime check, and no-isolation build: passed; the regenerated lock retained SHA-256
  `70329256c53949be19a72b61f6db294bda704229b6c625de96848fe4c6d30353`;
- the final lock resolved to 27 hash-verified binary distributions for each simulated GitHub Actions
  target, Linux x86_64 CPython 3.9 and 3.12;
- `shushu benchmark validate evals/benchmark-v1.jsonl`: 60 seeds with the required 20/20/10/10
  distribution and all eight domains;
- `shushu benchmark plan ...`: 240 runs;
- `shushu benchmark merge ...`: 240/240 real `gpt-5.6-sol` runs complete, four systems × 60,
  with final run-matrix SHA-256
  `bbfee19d4466f168b482593e38e0145b0cf2acb7bcd0cb54a6ad0b71e88cbbc2`;
- two balanced-overlap opaque rater packs: 288 scalar assignments, 432 pairwise assignments, 288
  hidden key records, 302 rater-side artifacts hash-verified, 60 collective seeds, 12 stratified
  shared seeds, 36 seeds per rater, coordinator-neutral rater provenance, and pre-rating manifest
  commitment SHA-256
  `552dfbd1ef0517bd632ea0540beca3505674229ddaf856f5b2f82073e63a6c40`;
- isolated sdist and wheel build plus clean Python 3.9 install/import/CLI smoke test: passed for
  `0.2.0a1`;
- wheel-backed Python 3.12 container run: all 117 tests passed from a read-only source mount;
- wheel SHA-256: `de26e305e7b2f82bc2a8ac56edbca0d75c01b082383994e1f0268e3631dd4102`;
- the wheel and sdist both passed isolated CLI smoke tests, and the sdist contains no dynamic model
  outputs, execution checkpoints, or blind-evaluation artifacts;
- fixed 20-topic live run without provider keys: arXiv and OpenReview 20/20 success, OpenAlex 0/20,
  Semantic Scholar 4/20, 214 serializable canonical records, zero post-dedup duplicates, and all
  20 manifests hash-verified by offline replay;
- fixed 20-topic anonymous Semantic Scholar bulk-search rerun: 20/20 success, 97 serializable
  canonical records, zero post-dedup duplicates, and report SHA-256
  `6bbd951a28234b258d36f37c2001f6bc44fc4719b844358cdab3659f78f89e30`;
- fixed 20-topic credential-free four-source rerun: arXiv, OpenAlex, Semantic Scholar, and
  OpenReview each passed 20/20; 395 raw records became 380 serializable canonical records, with
  zero source failures, zero remaining duplicates, 20 offline-verified replay manifests, and
  report SHA-256 `acabc854490418f6a645caa83446d5dd479efa2d15a2a3a92df428f24cd33c74`;
- draft PR [#1](https://github.com/YingaoWang-casia/shushu-novelty-finder/pull/1)
  exposed and then fixed an invalid cross-interpreter lock-regeneration invariant. The workflow-fix
  [CI run 29735638352](https://github.com/YingaoWang-casia/shushu-novelty-finder/actions/runs/29735638352)
  passed clean Python 3.9 and 3.12 jobs; only Python 3.9 regenerates the canonical lock,
  `fail-fast` is disabled, feature branches run one pull-request workflow, and the Node 24
  `actions/checkout@v7` and `actions/setup-python@v7` runtimes emit no deprecation annotation;

## Fourteen acceptance criteria

| # | Criterion | Audit result | Evidence |
|---:|---|---|---|
| 1 | One command starts a complete run | Pass | `shushu run --mode full` creates the P0–P9 state and directories. |
| 2 | Interrupted runs resume | Pass | Deterministic `next`, primary/auxiliary bundle hashes, legacy migration, tamper and non-overwrite tests. |
| 3 | At least four real retrieval sources | Pass | The retained credential-free joint rerun passed all 20 topics for arXiv, OpenAlex, Semantic Scholar, and OpenReview with zero failures. |
| 4 | Cross-source papers deduplicate | Pass | Identifier/title merge tests plus zero remaining duplicates across 380 live canonical records. |
| 5 | Every strong claim has traceable evidence | Pass | Strong claims require full-text support; P3 binds extracted text, claims, failures, pages and hashes. |
| 6 | Abstract-only evidence cannot impersonate full text | Pass | Schema and ledger regression tests. |
| 7 | Ideas undergo independent novelty collision | Pass | Isolated context hashes plus P7 six-axis cross-artifact gate. |
| 8 | Scooped ideas downgrade or abandon | Pass | Scoop/application-transfer regression tests and real-paper controls. |
| 9 | At least 60 fixed eval seeds | Pass | Versioned 60-seed JSONL suite. |
| 10 | Bare and old-version baselines | Pass (execution); human scoring pending | All 240 real runs completed on the same model, with four 60-run systems, immutable prompt/adapter/output provenance, exact-matrix merge, a completed execution manifest, and two generated balanced-overlap opaque rater packs. |
| 11 | Core code has automated tests | Pass | 117 tests across schemas, retrieval/replay, evidence, orchestration, lineage, gaps, ideas, collision, review, reports, adapters, blinding and evaluation. |
| 12 | CI runs on every PR | Pass | Draft PR #1 passes both Python 3.9 and 3.12 jobs from a single pull-request workflow. |
| 13 | Reports expose failure and uncertainty | Pass | P9 requires disclosure and hashes the report body, mode-required inputs and every declared failure log. |
| 14 | README effectiveness claims have public eval support | Safety gate passes; comparative evidence pending | All three READMEs disclose no comparative claim and pass the release gate. Adding one requires a hashed, publishable, human-primary 60-seed report. |

## Remaining release evidence

The engineering runtime is alpha-complete, but a stable `v0.2.0` comparative release is not yet
justified. The following work requires external human raters:

1. have at least two research-experienced humans independently complete the retained 288 scalar
   and 432 blind pairwise assignments, collectively covering 60 seeds with 12 shared seeds;
2. publish the aggregate report with scalar and pairwise Cohen's kappa;
Three complete machine-readable P0–P9 real-paper runs are now stored under `examples/runs/` and
pass offline replay, bundle-hash, cross-artifact, report-content and `shushu next` verification.

Until those items exist, keep version `0.2.0a1` and keep the README no-claim disclosure intact.
