# Output Template

Use this report format for full novelty-finding tasks. The output should read like a CS paper idea audit, not a generic brainstorm.

## 0. Executive Recommendation

Give the best 1-3 recommended ideas first.

```text
Recommended idea:
Novelty level: weak / medium / strong
Paper-readiness verdict: not ready / pilot-ready / workshop-ready / main-track candidate / technical-report-only
Best paper type:
Fallback paper type:
Why this is the best option:
Evidence basis:
Minimum experiment:
Baseline plan:
Main risk:
Likely accept reason:
Likely reject reason:
Continue / narrow / downgrade / kill:
```

## 1. Input Mode

```text
Mode: Direction Mode / Seed Paper Mode / Hybrid Mode / Paper-Readiness Mode
Output level: Quick / Research / Paper
Assumptions:
Search status: verified / partial / placeholder-only / not searched
```

## 2. Research Scope Card

Summarize the locked scope and assumptions.

```text
Direction:
Subfield:
Task:
Input:
Output:
Datasets:
Metrics:
Included directions:
Excluded directions:
Constraints:
```

## 3. Seed Paper Card

Only include this section if the user supplied a seed paper.

```text
Title:
Year:
Venue/source:
Paper type:
Task:
Input:
Output:
Dataset:
Metric:
Main method:
Claimed contribution:
Limitations:
Expansion keywords:
Excluded directions:
```

## 4. Paper Evidence Cards

For every key paper, include a card. If a paper is only a placeholder or search candidate, say so.

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

## 5. Claim-Evidence Map

For each top claim:

```text
Claim:
Claim type: novelty / feasibility / limitation / baseline / evaluation / task importance
Supporting papers:
Contrary papers:
Background papers:
Evidence strength:
What can be safely claimed:
What must not be claimed:
Confidence:
Next verification step:
```

## 6. Literature Timeline

Group representative papers by time stage.

```text
Time stage:
Representative papers:
Main task definition:
Main method family:
Dataset / metric pattern:
What changed from previous stage:
```

## 7. Trend Matrix

Use this table:

```text
Time period | Representative papers | Task shift | Method shift | Dataset/metric shift | Open gap
```

## 8. Gap Audit

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

## 9. Novelty Candidates

Separate into weak, medium, and strong ideas.

For each idea:

```text
Idea:
Novelty level:
Evidence:
Evidence type:
Feasibility:
Minimum experiment:
Baseline plan:
Risks:
Best target output:
```

## 10. Paper Type Routing

For each top idea:

```text
Best paper type:
Fallback paper type:
Why this type fits:
Required evidence:
Required baselines:
Main reviewer risk:
Readiness verdict:
```

## 11. Paper Thesis Card

For the top idea:

```text
Working title:
Paper type:
Core claim:
Why now:
What existing work assumes:
What breaks that assumption:
What evidence supports the claim:
What reviewers may reject:
```

## 12. Experiment Card

For the top idea:

```text
Claim:
Independent variable:
Dependent variable:
Datasets:
Metrics:
Baselines:
Ablations:
Robustness checks:
Falsification result:
```

## 13. Baseline Decision

```text
Minimum baselines:
Strong baselines:
Why each baseline is necessary:
What result would make the idea look weak:
What result would make the idea publishable:
```

## 14. Related Work Argument Map

```text
Closest prior work:
Follow-up work:
Sibling work:
Contrary evidence:
How the proposed idea differs:
What should not be claimed:
```

## 15. Reviewer Objection Pre-Mortem

For each top idea, include at least three objections.

```text
Likely reviewer objection:
Why the objection is plausible:
Evidence needed to answer it:
Current defense:
Weakness in current defense:
Action to strengthen:
Verdict impact: no change / downgrade / kill
```

## 16. Kill / Continue Criteria

```text
Continue condition:
Narrow condition:
Downgrade condition:
Kill condition:
Next checkpoint:
Smallest next action that changes the decision:
```

## 17. Threats to Validity

```text
Internal validity:
External validity:
Dataset validity:
Metric validity:
Reproducibility risk:
Reviewer concern:
```

## 18. Next-Step Plan

Give a concrete plan:

- papers to verify next;
- datasets or benchmarks to inspect;
- baseline to reproduce;
- first experiment;
- decision checkpoint.

## 19. Uncertainty and Search Limits

State what the search may have missed. Do not hide weak evidence. If no verified search has been performed, mark all paper names as `placeholder`, `candidate`, or `unverified`.
