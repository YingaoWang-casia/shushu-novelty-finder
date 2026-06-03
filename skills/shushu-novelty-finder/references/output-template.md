# Output Template

Use this report format for full novelty-finding tasks.

## 0. Executive recommendation

Give the best 1-3 recommended ideas first.

```text
Recommended idea:
Novelty level:
Why this is the best option:
Evidence basis:
Minimum experiment:
Main risk:
```

## 1. Research Scope Card

Summarize the locked scope and assumptions.

## 2. Seed Paper Card

Only include this section if the user supplied a seed paper.

## 3. Literature Timeline

Group representative papers by time stage.

For every key paper, include:

```text
Title:
Year:
Venue/source:
Why it matters:
Relation to the user's task:
```

## 4. Trend Matrix

Use this table:

```text
Time period | Representative papers | Task shift | Method shift | Dataset/metric shift | Open gap
```

## 5. Gap Audit

For each gap:

```text
Gap:
Gap type:
Evidence type:
Supporting papers:
Why this matters:
Why it may be a bad idea:
Confidence:
```

## 6. Novelty Candidates

Separate into weak, medium, and strong ideas.

For each idea:

```text
Idea:
Novelty level:
Evidence:
Evidence type:
Feasibility:
Minimum experiment:
Risks:
Best target output:
```

## 7. Next-step plan

Give a concrete plan:

- papers to read next;
- datasets or benchmarks to inspect;
- baseline to reproduce;
- first experiment;
- decision checkpoint.

## 8. Uncertainty and search limits

State what the search may have missed. Do not hide weak evidence.
