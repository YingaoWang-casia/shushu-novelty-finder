# Paper Evidence Schema

Use this schema for every paper used as evidence. A paper title alone is not enough.

## Paper Evidence Card

```text
Title:
Year:
Venue or source:
Paper type: method / benchmark / dataset / survey / system / analysis / preprint
URL, DOI, or arXiv id:
Task:
Main contribution:
Dataset:
Metric:
Why it is relevant:
Evidence role: trend / limitation / baseline / benchmark / method / negative signal
Used to support which claim:
Confidence:
```

## Evidence quality levels

### Strong

Accepted paper, directly relevant task, clear method or benchmark, and directly supports the claim.

### Moderate

Relevant but adjacent task, survey evidence, benchmark evidence, or preprint with clear technical detail.

### Weak

Only loosely related, unverified venue, unclear method, missing source link, or used only as background.

## Rules

- Do not use unverifiable papers as evidence.
- Mark preprints separately.
- Separate survey conclusions from original experimental evidence.
- Do not use one paper to claim a field-wide trend.
- If only weak evidence exists, downgrade the novelty recommendation.
