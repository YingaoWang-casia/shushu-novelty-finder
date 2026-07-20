# Blind human evaluation protocol

This protocol produces the only evidence allowed to support comparative README claims.

## Roles and blinding

1. A coordinator collects the 240 hashed outputs and replaces system names with randomized labels
   independently for each seed.
2. At least two raters with research experience score every output without seeing the system,
   prompt profile, model name, or the other rater's decisions.
3. Each rater also evaluates all six pairwise combinations of the four primary systems for every
   seed. Left/right order is randomized.
4. After both raters lock their files, the coordinator joins the hidden mapping and writes final
   `EvaluationJudgment` and `PairwiseJudgment` JSONL records. `blind: true` attests to the process;
   it is not inferred merely from the field value.
5. Independent records are never edited to manufacture agreement. Any adjudication is reported
   separately and cannot replace the pre-adjudication Cohen's kappa.

The coordinator can generate identity-free packs after collecting the 240 hashed runs:

```bash
shushu benchmark blind-pack evals/completed-run-matrix.jsonl \
  --benchmark-seeds evals/benchmark-v1.jsonl \
  --results-root . \
  --rater rater-a --rater rater-b \
  --output-dir evals/blind-v1
```

Each rater receives only their `raters/<id>/` directory: the 60 fixed seed records, 240 opaque
scalar assignments, 360 randomized left/right pairs, and copied outputs whose paths contain no
system name. The directory also contains an identity-free scoring guide and JSON Schemas for both
response files. Every rater-side seed, assignment, guide, schema, and copied output is hash-bound
in the coordinator manifest. Run prompt hashes are checked against the seed records before
packaging, and contextual system/profile identity patterns inside
answer text cause packaging to fail closed without rejecting ordinary research uses of terms such
as self-reflection. The
`coordinator/blind-key.jsonl` file must never be shared before both response files are locked.
Responses use the `blind-scalar-response` and `blind-pairwise-response` schemas. The coordinator
publishes the package-manifest SHA-256 commitment to both raters before rating, then joins
identities deterministically only after the response files and their hashes are locked:

```bash
shushu benchmark unblind evals/blind-scalar-responses.jsonl \
  --blind-pairwise evals/blind-pairwise-responses.jsonl \
  --blind-key evals/blind-v1/coordinator/blind-key.jsonl \
  --blind-manifest evals/blind-v1/coordinator/manifest.json \
  --output evals/judgments.jsonl \
  --pairwise-output evals/pairwise-judgments.jsonl
```

The generated `evals/blind-v1` package is ready for human rating. Its pre-rating coordinator
manifest commitment is
`9e34a730d2f2509e1e3a33bad4dd95dfaf355e68f37dd5d2667f3d9892f98312`; it is also recorded in
`evals/blind-v1/MANIFEST-COMMITMENT.txt`. No response or human judgment is present yet.
Each rater uses the identity-neutral `blind-eval init` command to create non-overwriting,
assignment-bound response drafts, and `blind-eval status` for read-only progress checks. The draft
uses `null` for every unfinished human judgment so it cannot silently pass final validation. Before
submission, `blind-eval lock` requires exact 240 scalar/360 pairwise coverage, rechecks
copied-output hashes and immutable assignment fields, enforces one rater and one
research-experience value, and writes an immutable `response-lock.json` binding both response
hashes to the pre-rating manifest commitment. The legacy `blind-eval-lock` alias remains available.

Minimum human evidence is 480 scalar judgments (60 × 4 × 2) and 720 pairwise judgments
(60 × 6 × 2). Extra raters are allowed, but every included human rater must cover the complete
matrix.

## Scalar rubric

Retrieval and evidence fields are counts, not impressions. Lineage relation counts are entered for
all seven relation types. Idea dimensions use 1–5 ratings. Calibration fields compare the system's
confidence/decision against the curated case outcome.

The coordinator should preserve annotation guidance, rater training examples, output hashes, and
the system-label mapping alongside the public result. Names may be pseudonymized, but reported
research-experience years must remain accurate.

## Scoring and publication

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

shushu release-check \
  --readme README.md \
  --public-evaluation evals/public-results.json
```

LLM ratings may be included with `rater_type: "llm"`; the aggregator reports their count but
excludes them from primary system metrics and agreement. A result with missing coverage, duplicate
ratings, an incomplete metric family, or fewer than two human raters is not publishable.
The scorer deterministically replays unblinding and rejects any scalar or pairwise judgment that
differs from the locked blind responses/key. The public report hashes the blind responses, key,
package manifest, and completed execution-environment manifest in addition to the benchmark, run
matrix, and unblinded judgments.
