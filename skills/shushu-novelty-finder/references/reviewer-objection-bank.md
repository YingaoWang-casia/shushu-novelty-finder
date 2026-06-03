# Reviewer Objection Bank

Use this reference before calling an idea paper-ready. The Skill should pre-review the idea like a strict reviewer, not only explain why the idea sounds good.

## Required Objection Pass

For every top idea, answer these questions:

```text
Is this just an engineering integration?
Is this just a benchmark without insight?
Is this just a metric without validation?
Are the baselines too weak?
Is the dataset too small, private, synthetic, or unreproducible?
Does the task matter beyond one setting?
Has a recent arXiv or workshop paper already done this?
Can the claim be falsified?
Would a reviewer call the contribution incremental?
What would Reviewer 2 reject first?
```

## Objection Types

### 1. Not Novel

Signals:

- closest prior work already solves the main claim;
- the idea only renames an existing metric, benchmark, or pipeline;
- novelty depends on saying `nobody has done this` without evidence.

Required response:

```text
Downgrade novelty level or narrow the claim.
```

### 2. Engineering Only

Signals:

- combines known components without a new claim;
- no controlled comparison isolates the contribution;
- output is mostly a tool or pipeline.

Required response:

```text
Reframe as system paper, analysis paper, or technical report unless there is a testable insight.
```

### 3. Weak Baselines

Signals:

- compares only against old or trivial baselines;
- excludes strongest recent work;
- ignores closed-book, long-context, reranker, or task-specific baseline when relevant.

Required response:

```text
Add minimum and strong baseline plan before paper-readiness verdict.
```

### 4. Dataset Problem

Signals:

- private data only;
- small synthetic dataset;
- annotation protocol unclear;
- no reproducibility path.

Required response:

```text
Downgrade to pilot-ready or technical-report-only unless a public benchmark or reproducible data plan exists.
```

### 5. Metric Problem

Signals:

- metric does not measure the claim;
- offline metric used for real-time claim;
- human judgment is needed but absent;
- single aggregate score hides failure modes.

Required response:

```text
Add metric-source evidence and falsification condition.
```

### 6. Scope Problem

Signals:

- idea tries to cover an entire field;
- task, input, output, dataset, and metric are not locked;
- trend claim is field-wide but evidence is narrow.

Required response:

```text
Run scope narrowing before literature audit.
```

## Reviewer Pre-Mortem Template

```text
Likely reviewer objection:
Why the objection is plausible:
Evidence needed to answer it:
Current defense:
Weakness in current defense:
Action to strengthen:
Verdict impact: no change / downgrade / kill
```

## Final Output Requirement

For each top idea, include at least three reviewer objections and say whether each objection changes the readiness verdict.
