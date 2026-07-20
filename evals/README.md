# Evals

This folder defines lightweight checks for `shushu-novelty-finder` outputs.

## Benchmark v1

`benchmark-v1.jsonl` is the fixed 60-seed engineering benchmark:

- 20 broad research directions;
- 20 title-only seed-paper cases with OpenReview identifiers;
- 10 known-scoop controls expected to downgrade or abandon;
- 10 mechanism-transfer cases expected to distinguish application transfer from mechanism novelty.

It covers `llm-rag`, `cv-multimodal`, `speech`, `agents`, `systems`, `data-mining`,
`security`, and `scientific-ml`. Validate its composition and create the default 240-run matrix:

```bash
shushu benchmark validate evals/benchmark-v1.jsonl
shushu benchmark plan evals/benchmark-v1.jsonl --output evals/run-matrix.jsonl
shushu benchmark execute evals/run-matrix.jsonl \
  --benchmark-seeds evals/benchmark-v1.jsonl \
  --adapters evals/adapters.local.json \
  --results-root . \
  --output evals/executed-run-matrix.jsonl
shushu benchmark collect evals/run-matrix.jsonl \
  --results-root . \
  --output evals/completed-run-matrix.jsonl
```

The default systems are bare model, self-reflection, Shushu v0.1, and Shushu v0.2. This
matrix is an execution plan, not an evaluation result. `execute` uses no-shell argv adapters,
passes the seed prompt on stdin, captures stdout, persists failures, checkpoints after every run,
and automatically resumes a matching `--output` matrix when the same command is repeated. A
systemic adapter failure such as an exhausted usage limit, missing login, or HTTP 429 is recorded
once and stops that queue immediately; remaining records retain their status for a later resume.
Single-run adapter failures remain isolated and do not stop unrelated runs.
`collect` requires all 240 output files,
rejects empty or escaping paths, and hashes each result. Public quality claims remain prohibited
until collection, two-person blind ratings, agreement statistics, and evidence/novelty metrics are
complete.

When execution is intentionally sharded, combine overlapping plan/checkpoint files with repeated
`--matrix` arguments. `merge` prefers a matching complete record over a pending plan record,
rejects conflicting results, and revalidates all 240 files before writing the final manifest.

The fixed 20-topic live connector suite is `retrieval-topics-v1.jsonl`. It gates every selected
source at ≥95% success and independently checks that duplicates remaining after canonical dedup are
≤5%:

```bash
shushu retrieval-benchmark evals/retrieval-topics-v1.jsonl \
  --output-dir evals/live-retrieval-v1 \
  --report evals/live-retrieval-v1/report.json
```

For repeatable or production OpenAlex retrieval, use its free `OPENALEX_API_KEY`. Without one, the
connector attempts OpenAlex's small anonymous demo allowance and persists quota exhaustion like
any other source failure. A dedicated `SEMANTICSCHOLAR_API_KEY` is optional: authenticated calls
use relevance search, while anonymous calls use Semantic Scholar's lower-cost bulk search with a
bounded zero-result relaxation. The credential-free 2026-07-16 run is retained under
`live-retrieval-v1/` as historical failure evidence rather than being rewritten. The 2026-07-20
anonymous Semantic Scholar rerun is retained under `live-retrieval-s2-anonymous-v1/`; it passed
20/20 topics with 97 serializable records and zero post-dedup duplicates. Its report SHA-256 is
`6bbd951a28234b258d36f37c2001f6bc44fc4719b844358cdab3659f78f89e30`.

The final credential-free four-source rerun is retained under
`live-retrieval-four-source-anonymous-v1/`. arXiv, OpenAlex, Semantic Scholar, and OpenReview each
passed 20/20 topics. The run produced 395 raw source records, 380 canonical records after
cross-source deduplication, zero remaining duplicates, zero source failures, and 20 offline-
verified replay manifests. Its report SHA-256 is
`acabc854490418f6a645caa83446d5dd479efa2d15a2a3a92df428f24cd33c74`.

The repository also includes a pinned Codex CLI adapter for reproducible real-system execution:

```bash
shushu benchmark execute evals/run-matrix.jsonl \
  --benchmark-seeds evals/benchmark-v1.jsonl \
  --adapters evals/adapters.codex-gpt-5.6-sol.json \
  --results-root . \
  --output evals/executed-run-matrix.jsonl
```

All four systems use the same `gpt-5.6-sol` model and web-search availability. Bare receives only
the seed, self-reflection receives one private critique/revision instruction, v0.1 receives the
pinned Skill, and v0.2 receives the same Skill plus the engineering protocol. The adapter locks
its wrapper and prompt files by SHA-256 and records an adapter fingerprint in every completed run.

The real execution completed on 2026-07-20. `completed-run-matrix.jsonl` contains 240 verified
runs (60 per system) and has SHA-256
`bbfee19d4466f168b482593e38e0145b0cf2acb7bcd0cb54a6ad0b71e88cbbc2`. The completed runtime
manifest and retained failure history are under `execution/codex-gpt-5.6-sol/`. Two human-rater
packs are under `blind-v1/`; their coordinator-manifest commitment is
`9e34a730d2f2509e1e3a33bad4dd95dfaf355e68f37dd5d2667f3d9892f98312`. These are execution and
blinding artifacts, not comparative effectiveness evidence; human responses remain pending.
Raters use the identity-neutral `blind-eval` entry point supplied in each pack to initialize
assignment-bound drafts, check progress, verify exact coverage and output bindings, and commit
their response hashes before unblinding.

Scoring also requires blind judgments for all six pairwise combinations of the four primary
systems, for every seed and every human rater:

```bash
shushu benchmark score evals/judgments.jsonl \
  --pairwise evals/pairwise-judgments.jsonl \
  --blind-scalar evals/blind-scalar-responses.jsonl \
  --blind-pairwise evals/blind-pairwise-responses.jsonl \
  --blind-key evals/blind-v1/coordinator/blind-key.jsonl \
  --blind-manifest evals/blind-v1/coordinator/manifest.json \
  --benchmark-seeds evals/benchmark-v1.jsonl \
  --run-matrix evals/completed-run-matrix.jsonl \
  --execution-manifest evals/execution/codex-gpt-5.6-sol/manifest.json \
  --results-root . \
  --output evals/public-results.json
```

The human-primary score report covers:

- retrieval: known-prior Recall@K, duplicate rate, metadata completeness, and publication-label
  accuracy;
- evidence: citation existence, claim entailment, unsupported claims, and full-text coverage;
- lineage: relation macro-F1, closest-prior Recall@5, saturated-contribution precision, and
  unsupported-edge rate;
- idea quality: all seven rubric dimensions;
- calibration: strong false positives, scoop recall, confidence/accuracy correlation, and kill
  precision.

The blinding, randomization, locking, and coordinator join procedure is specified in
[`docs/evaluation-protocol.md`](../docs/evaluation-protocol.md). The `*.example.jsonl` files are
schema examples only and must never be counted as human evidence.

The goal is not to automatically judge scientific truth. The goal is to check whether a run generates concrete innovation-point candidates and then follows the Skill's evidence, reasonableness-audit, novelty-ranking, reviewer-objection, and paper-readiness discipline.

## Files

- `cases/rag-evaluation.md` - Direction Mode eval case for RAG evaluation.
- `cases/seed-paper.md` - Seed Paper Mode eval case.
- `checks/output-checklist.md` - required output checklist.
- `checklist.md` - legacy checklist kept for compatibility.
- `benchmark-v1.jsonl` - fixed 60-seed benchmark.

## Required Checks

A valid output should include:

- input mode;
- Research Scope Card or Seed Paper Card;
- concrete paper names or explicit `placeholder / candidate / unverified` labels;
- Paper Evidence Cards for key papers;
- Claim-Evidence Map for top claims;
- Literature Timeline and Trend Matrix in Research / Paper Mode;
- gap evidence labels;
- concrete novelty candidates, not only a literature review;
- weak / medium / strong novelty ranking;
- novelty mechanism for each top idea;
- closest prior work for each top idea;
- reasonableness verdict for each top idea;
- strongest reason for and strongest reason against each top idea;
- paper type routing for top ideas;
- minimum experiments;
- baseline decision for top ideas;
- reviewer objection pre-mortem;
- kill / continue criteria;
- risks and reviewer reject reasons;
- paper-readiness verdict.

## Failure Checks

A bad output should be flagged if it:

- claims nobody has done something without search evidence;
- reviews literature but never proposes concrete ideas;
- lists ideas but never judges whether they are reasonable;
- lists papers without explaining their evidence role;
- gives innovation ideas without feasibility or risks;
- ignores closest prior work;
- ignores baselines;
- treats preprints as accepted papers;
- treats candidate papers as verified support;
- produces a paper plan without a falsifiable claim;
- gives no reviewer objections;
- gives no condition for downgrading or killing the idea;
- uses a seed paper title without extracting task, input, output, dataset, metric, and claim;
- calls an ordinary pipeline a new method without a controlled comparison.

## Usage

Use these checks after generating an output. If any required item is missing, downgrade the answer quality and ask the Skill to repair the missing section instead of accepting the report.
