# Engineering acceptance audit

Audit date: 2026-07-20

This document separates implemented gates from evidence that requires external model runs, API
credentials, GitHub, or human reviewers. Missing external evidence is not replaced with synthetic
results.

## Verification performed

- `ruff check .`: passed;
- `pytest -q`: 108 tests passed;
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
- two opaque rater packs: 480 scalar assignments, 720 pairwise assignments, 480 hidden key
  records, 494 rater-side artifacts hash-verified, zero contextual identity hits, and pre-rating
  manifest commitment SHA-256
  `9e34a730d2f2509e1e3a33bad4dd95dfaf355e68f37dd5d2667f3d9892f98312`;
- isolated sdist and wheel build plus clean Python 3.9 install/import/CLI smoke test: passed for
  `0.2.0a1`;
- wheel SHA-256: `46f831f0952a4ced90a3bc34611cc339cb10b41159e338ca1ccec17c67c76b75`;
- the wheel and sdist both passed isolated CLI smoke tests, and the sdist contains no dynamic model
  outputs, execution checkpoints, or blind-evaluation artifacts;
- fixed 20-topic live run without provider keys: arXiv and OpenReview 20/20 success, OpenAlex 0/20,
  Semantic Scholar 4/20, 214 serializable canonical records, zero post-dedup duplicates, and all
  20 manifests hash-verified by offline replay;
- draft PR [#1](https://github.com/YingaoWang-casia/shushu-novelty-finder/pull/1)
  triggered the configured workflow for both push and pull-request events; Python 3.12 exposed an
  invalid cross-interpreter lock-regeneration invariant, while the Python 3.9 job reached and
  passed lint plus all tests before matrix fail-fast cancellation;

## Fourteen acceptance criteria

| # | Criterion | Audit result | Evidence |
|---:|---|---|---|
| 1 | One command starts a complete run | Pass | `shushu run --mode full` creates the P0–P9 state and directories. |
| 2 | Interrupted runs resume | Pass | Deterministic `next`, primary/auxiliary bundle hashes, legacy migration, tamper and non-overwrite tests. |
| 3 | At least four real retrieval sources | Pass (implementation); live credential gate pending | arXiv and OpenReview passed 20/20. OpenAlex requires a caller key; anonymous Semantic Scholar traffic was throttled to 4/20. |
| 4 | Cross-source papers deduplicate | Pass | Identifier/title merge tests plus zero remaining duplicates across 214 live canonical records. |
| 5 | Every strong claim has traceable evidence | Pass | Strong claims require full-text support; P3 binds extracted text, claims, failures, pages and hashes. |
| 6 | Abstract-only evidence cannot impersonate full text | Pass | Schema and ledger regression tests. |
| 7 | Ideas undergo independent novelty collision | Pass | Isolated context hashes plus P7 six-axis cross-artifact gate. |
| 8 | Scooped ideas downgrade or abandon | Pass | Scoop/application-transfer regression tests and real-paper controls. |
| 9 | At least 60 fixed eval seeds | Pass | Versioned 60-seed JSONL suite. |
| 10 | Bare and old-version baselines | Pass (execution); human scoring pending | All 240 real runs completed on the same model, with four 60-run systems, immutable prompt/adapter/output provenance, exact-matrix merge, a completed execution manifest, and two generated opaque rater packs. |
| 11 | Core code has automated tests | Pass | 108 tests across schemas, retrieval/replay, evidence, orchestration, lineage, gaps, ideas, collision, review, reports, adapters, blinding and evaluation. |
| 12 | CI runs on every PR | Pass for PR triggering; green release gate pending | Draft PR #1 triggered both push and pull-request runs. Python 3.12 correctly rejected regeneration of the Python 3.9 canonical lock; the focused workflow correction is awaiting explicit approval. |
| 13 | Reports expose failure and uncertainty | Pass | P9 requires disclosure and hashes the report body, mode-required inputs and every declared failure log. |
| 14 | README effectiveness claims have public eval support | Safety gate passes; comparative evidence pending | Both READMEs disclose no comparative claim. Adding one requires a hashed, publishable, human-primary 60-seed report. |

## Remaining release evidence

The engineering runtime is alpha-complete, but a stable `v0.2.0` comparative release is not yet
justified. The following work requires external actors or credentials:

1. have at least two research-experienced humans independently complete 480 scalar and 720 blind
   pairwise judgments;
2. publish the aggregate report with scalar and pairwise Cohen's kappa;
3. apply the approved canonical-Python lock check and obtain green Python 3.9/3.12 jobs on draft
   PR #1;
4. supply `OPENALEX_API_KEY` and `SEMANTICSCHOLAR_API_KEY`, then rerun the retained 20-topic live
   connector benchmark to meet the per-source 95% gate;

Three complete machine-readable P0–P9 real-paper runs are now stored under `examples/runs/` and
pass offline replay, bundle-hash, cross-artifact, report-content and `shushu next` verification.

Until those items exist, keep version `0.2.0a1` and keep the README no-claim disclosure intact.
