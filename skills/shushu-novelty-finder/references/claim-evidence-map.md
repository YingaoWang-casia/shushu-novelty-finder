# Claim-Evidence Map

Use this reference to turn paper lists into paper arguments. A paper idea becomes useful only when each claim is tied to evidence, contrary evidence, and a safe wording boundary.

## Why This Exists

A Paper Evidence Card says what a paper is. A Claim-Evidence Map says what the paper proves or fails to prove for the user's idea.

Do not let the final output become a bibliography. The user needs to know which claims are safe.

## Claim-Evidence Map Format

```text
Claim:
Claim type: novelty / feasibility / limitation / baseline / evaluation / task importance
Supporting papers:
Contrary papers:
Background papers:
Evidence strength: weak / moderate / strong
What can be safely claimed:
What must not be claimed:
Confidence:
Next verification step:
```

## Claim Types

### Novelty Claim

A statement that the proposed idea differs from existing work.

Required support:

- closest prior work;
- closest follow-up work;
- sibling work in the same task family;
- at least one contrary-evidence search.

Unsafe wording:

```text
Nobody has done this.
```

Safer wording:

```text
Under the checked scope, the closest verified papers do not appear to evaluate X and Y jointly; this requires broader search before a strong novelty claim.
```

### Feasibility Claim

A statement that the idea can be tested within the user's constraints.

Required support:

- available dataset or benchmark;
- baseline that can be reproduced;
- metric that matches the claim;
- resource estimate.

### Limitation Claim

A statement that existing work has a gap or weakness.

Required support:

- explicit limitation from a paper; or
- repeated cross-paper pattern; or
- benchmark / metric absence; or
- carefully marked inference.

### Baseline Claim

A statement that a baseline is necessary or sufficient.

Required support:

- accepted paper using the baseline;
- benchmark protocol requiring the baseline;
- domain reference requiring the baseline.

### Evaluation Claim

A statement that an experiment can validate or falsify the idea.

Required support:

- metric source;
- dataset source;
- falsification condition.

## Safe Claim Ladder

Use this ladder when confidence is uncertain:

```text
Unsafe: Nobody has studied X.
Weak: I have not yet found verified work on X.
Moderate: In the checked papers, X is not evaluated directly.
Strong: Across verified prior, follow-up, and sibling work, X remains untested under scope Y.
```

## Final Output Requirement

For each top idea, include at least one Claim-Evidence Map. If the map contains only candidate or placeholder papers, the idea cannot be rated stronger than `pilot-ready`.
