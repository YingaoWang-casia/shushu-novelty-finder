# Paper Evidence Schema

Use this schema for every paper used as evidence. A paper title alone is not enough.

The schema separates two concepts:

- `Evidence status`: whether the record is candidate, verified, rejected, or placeholder.
- `Evidence role`: what the paper is used for in the argument.

This prevents a search result from being treated as proof before it is verified.

## Paper Evidence Card

```text
Title:
Year:
Venue or source:
Paper type:
URL, DOI, or arXiv id:
Task:
Dataset:
Metric:
Main contribution:
Why it is relevant:
Evidence status:
Evidence role:
Used to support which claim:
Confidence:
```

## Evidence Status

Use one of these status labels:

```text
candidate
verified
placeholder
rejected
needs follow-up check
```

Rules:

- `candidate` means the paper matched a search query but has not been read or verified.
- `placeholder` means the paper is illustrative and must not be used as evidence.
- `verified` means the source, task, paper type, and relevance have been checked.
- `rejected` means the paper was checked and should not support the current claim.
- `needs follow-up check` means the paper is relevant but its exact role is uncertain.

## Evidence Roles

Use one or more of these roles:

```text
task anchor
method baseline
benchmark baseline
dataset source
metric source
limitation evidence
follow-up work
contrary evidence
survey support
```

Do not use `candidate` as an evidence role. Candidate is a status, not an argument role.

## Paper Types

Recommended paper type labels:

```text
method
benchmark
dataset
survey
system
analysis
preprint
position
negative result
```

## Evidence Quality Levels

### Strong

Accepted paper, directly relevant task, clear method or benchmark, verified source, and directly supports the claim.

### Moderate

Relevant but adjacent task, survey evidence, benchmark evidence, or preprint with clear technical detail.

### Weak

Only loosely related, unverified venue, unclear method, missing source link, candidate search result, placeholder, or used only as background.

## Rules

- Do not use unverifiable papers as core evidence.
- Do not support a claim with only a paper title.
- Candidate papers cannot support a novelty claim until verified.
- Preprints must be marked as preprints.
- Separate survey conclusions from original experimental evidence.
- One paper cannot support a field-wide trend.
- If only weak evidence exists, downgrade the novelty recommendation.
- A paper can have multiple evidence roles, but each role must say which claim it supports.
- Contrary evidence should be included when it weakens or narrows the novelty claim.

## Bad Evidence Pattern

```text
This is novel because Paper X did not solve it.
```

Why bad: it does not say what Paper X studied, what evidence role it has, whether it is accepted or preprint, whether the paper has been verified, or whether follow-up work solved the limitation.

## Good Evidence Pattern

```text
Paper Evidence Card:
Title: <verified paper>
Year: <year>
Venue or source: <venue>
Paper type: benchmark
URL, DOI, or arXiv id: <identifier>
Task: citation correctness evaluation for RAG answers
Dataset: <dataset>
Metric: citation precision
Main contribution: introduces an evaluation protocol for citation support
Why it is relevant: closest benchmark baseline for the proposed multi-axis evaluation
Evidence status: verified
Evidence role: benchmark baseline; contrary evidence
Used to support which claim: checks whether the proposed benchmark is actually new
Confidence: moderate
```
