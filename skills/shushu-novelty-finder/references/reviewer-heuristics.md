# Reviewer Heuristics

Use these checks to judge whether a proposed novelty idea would survive serious review.

## Core reviewer questions

1. What is the exact problem, and why does it matter now?
2. What has already been tried, and what is actually missing?
3. Is the claimed gap explicit in papers, or inferred by comparing papers?
4. Does the idea change the task, method, benchmark, metric, system setting, or only the wording?
5. Can the idea be validated with available data and compute?
6. What baseline would make this idea look weak?
7. What negative result would falsify the claim?
8. Why would a reviewer care beyond one dataset or one demo?

## Contribution types

A serious CS paper usually needs one or more of these:

- new task definition;
- new dataset or benchmark;
- new metric or evaluation protocol;
- new method with convincing comparison;
- new system with measurable constraints;
- new analysis that changes how people understand a failure;
- strong reproduction and negative result that corrects the field.

## Weak signals

Treat these as warning signs:

- only replaces one model name with another;
- uses a new dataset but gives no reason the dataset matters;
- claims a benchmark gap without checking existing benchmark papers;
- proposes a method without baseline or ablation plan;
- depends on private data that the user cannot access;
- reports only accuracy while ignoring cost, latency, robustness, or failure severity;
- sounds like a product feature rather than a research contribution.

## Strong signals

Treat these as promising signals:

- multiple papers share the same limitation;
- a benchmark is widely used but misaligned with deployment;
- a real-world constraint is repeatedly ignored;
- a popular method fails under a realistic but under-tested setting;
- a new task has clear input, output, metric, and baseline;
- the minimum experiment can validate or falsify the idea quickly.

## Review-style verdict

For each recommended idea, include a verdict:

```text
Reviewer confidence:
Main reason to accept:
Main reason to reject:
What experiment would change the verdict:
```
