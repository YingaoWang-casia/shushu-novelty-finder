# Paper Thesis

A novelty idea is not paper-ready until it can be converted into a clear thesis.

## Paper Thesis Card

Use this card for every recommended medium or strong idea.

```text
Working title:
Paper type: method / benchmark / dataset / system / analysis / negative result
Core claim:
Why now:
What existing work assumes:
What breaks that assumption:
What evidence supports the claim:
What contribution type this paper makes:
What is new compared with the closest papers:
What would make reviewers reject it:
Minimum evidence needed before writing:
```

## Claim quality checks

A strong paper thesis should satisfy these checks:

1. The problem is specific enough to test.
2. The gap is supported by literature or by a reproducible pilot observation.
3. The contribution type is explicit.
4. The paper can be rejected or supported by experiments.
5. The contribution is not only a product feature or prompt trick.
6. The story can be explained in one paragraph.

## Bad thesis patterns

Avoid these:

- We improve X with LLMs.
- We build a framework for Y.
- We propose a benchmark because no benchmark exists.
- We combine A and B without explaining why the combination exposes a new question.
- We apply a known method to a new dataset without showing why the dataset changes the problem.

## Good thesis patterns

Prefer these:

- Existing evaluations overestimate model ability because they ignore X; we show this with Y and propose Z.
- A common assumption in prior work fails under condition X; we define a testbed and show which methods break.
- Current benchmarks measure Y, but real deployments require Z; we introduce an evaluation protocol that changes model ranking.
- Existing methods optimize for metric X but fail on failure mode Y; we propose a diagnostic method and validation protocol.
