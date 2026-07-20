# Blind human evaluation protocol

This protocol produces the only evidence allowed to support comparative README claims.

## Roles and blinding

1. A coordinator collects the 240 hashed outputs and replaces system names with randomized labels
   independently for each seed.
2. At least two raters with research experience collectively cover all 60 seeds without seeing the
   system, prompt profile, model name, or the other rater's decisions. Each assigned seed contains
   all four outputs.
3. The recommended preregistered design gives each of two raters 36 seeds: 12 stratified shared
   seeds and 24 disjoint seeds. Each rater evaluates all six pairwise combinations for every seed
   in their pack. Left/right order is randomized. Complete duplicate rating remains available as a
   more expensive fallback.
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
  --rating-design balanced-overlap \
  --shared-seeds 12 \
  --output-dir evals/blind-balanced-v1
```

Each rater receives only their `raters/<id>/` directory: 36 assigned seed records, 144 opaque
scalar assignments, 216 randomized left/right pairs, and copied outputs whose paths contain no
system name. Across both packs there are 288 scalar and 432 pairwise assignments, a 40% reduction
from complete duplicate rating. The 12 shared seeds are selected in the suite's 4/4/2/2 case-type
proportion and cover all eight domains; the remaining seeds are balanced jointly by case type and
domain. The manifest preregisters every seed assignment and stratum count.

The directory also contains an identity-free scoring guide and JSON Schemas for both response
files. Every rater-side seed, assignment, guide, schema, and copied output is hash-bound in the
coordinator manifest. Rater-side seed provenance is coordinator-neutral while the manifest retains
the original benchmark hash. Run prompt hashes are checked against the original seed records
before packaging, and contextual system/profile identity patterns inside answer text cause
packaging to fail closed without rejecting ordinary research uses of terms such as
self-reflection. The
`coordinator/blind-key.jsonl` file must never be shared before both response files are locked.
Responses use the `blind-scalar-response` and `blind-pairwise-response` schemas. The coordinator
publishes the package-manifest SHA-256 commitment to both raters before rating, then joins
identities deterministically only after the response files and their hashes are locked:

```bash
shushu benchmark collect-responses \
  evals/blind-balanced-v1/raters/rater-a \
  --rater-dir evals/blind-balanced-v1/raters/rater-b \
  --blind-manifest-sha256 \
    552dfbd1ef0517bd632ea0540beca3505674229ddaf856f5b2f82073e63a6c40 \
  --blind-manifest evals/blind-balanced-v1/coordinator/manifest.json \
  --blind-key evals/blind-balanced-v1/coordinator/blind-key.jsonl \
  --output evals/blind-scalar-responses.jsonl \
  --pairwise-output evals/blind-pairwise-responses.jsonl

shushu benchmark unblind evals/blind-scalar-responses.jsonl \
  --blind-pairwise evals/blind-pairwise-responses.jsonl \
  --blind-key evals/blind-balanced-v1/coordinator/blind-key.jsonl \
  --blind-manifest evals/blind-balanced-v1/coordinator/manifest.json \
  --output evals/judgments.jsonl \
  --pairwise-output evals/pairwise-judgments.jsonl
```

`collect-responses` refuses unlocked, modified, duplicate, foreign-package, or differently
committed rater directories. It verifies the package manifest and key, both response locks,
assignment/output hashes, immutable fields, exact per-pack coverage, and research-experience value
before writing the combined files. Do not concatenate response JSONL by hand.

The generated `evals/blind-balanced-v1` package is ready for human rating. Its pre-rating coordinator
manifest commitment is
`552dfbd1ef0517bd632ea0540beca3505674229ddaf856f5b2f82073e63a6c40`; it is also recorded in
`evals/blind-balanced-v1/MANIFEST-COMMITMENT.txt`. No response or human judgment is present yet.
Each rater uses the identity-neutral `blind-eval init` command to create non-overwriting,
assignment-bound response drafts, and `blind-eval status` for read-only progress checks. The draft
uses `null` for every unfinished human judgment so it cannot silently pass final validation. Before
submission, `blind-eval lock` requires exact 144 scalar/216 pairwise coverage for the retained
balanced packs, rechecks
copied-output hashes and immutable assignment fields, enforces one rater and one
research-experience value, and writes an immutable `response-lock.json` binding both response
hashes to the pre-rating manifest commitment. The legacy `blind-eval-lock` alias remains available.

Minimum balanced-overlap evidence is 288 scalar judgments ((60 + 12) × 4) and 432 pairwise
judgments ((60 + 12) × 6). The union must cover all 60 seeds, every rater must completely rate all
four outputs and six pairs for every seed assigned to them, and at least 12 seeds must have two
complete human ratings. Agreement is computed only from shared items. System metrics give each
seed total weight one, so a shared seed does not receive twice the influence of a singly rated
seed. The legacy `complete` design still produces 480 scalar and 720 pairwise judgments.

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
  --blind-key evals/blind-balanced-v1/coordinator/blind-key.jsonl \
  --blind-manifest evals/blind-balanced-v1/coordinator/manifest.json \
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

Recruitment requirements, paid-pilot guidance, workload disclosure, and a copy-ready role brief are
in [`rater-recruitment.md`](rater-recruitment.md).
