# Kill / Continue Criteria

Use this reference to decide whether an idea should continue, be narrowed, be downgraded, or be killed.

The goal is not to discourage ideas. The goal is to avoid spending weeks on an idea that cannot survive related work or experiment design.

## Continue If

```text
- the task boundary is clear;
- the top baseline has not already solved the core claim;
- the minimum experiment can falsify the claim;
- the dataset or benchmark is available or realistically constructible;
- the metric measures the actual claim;
- the evidence gap is not only a vague inference;
- the idea has at least one plausible reviewer accept reason;
- the user can run the minimum experiment under constraints.
```

## Narrow If

```text
- the direction is too broad;
- the claim is field-wide but evidence is local;
- the idea mixes multiple tasks;
- the dataset, metric, or user setting is unclear;
- the top baseline is too expensive but a smaller pilot can test the core claim.
```

## Downgrade If

```text
- novelty depends mostly on wording;
- only candidate or placeholder papers support the claim;
- strong baselines cannot be run;
- the experiment is descriptive but not explanatory;
- data is private and no reproducible benchmark plan exists;
- the idea is useful engineering but not a research contribution.
```

Possible downgrade targets:

```text
main-track candidate -> workshop-ready
workshop-ready -> pilot-ready
pilot-ready -> technical-report-only
any level -> not ready
```

## Kill If

```text
- closest verified prior work already answers the core claim;
- no falsifiable metric can be defined;
- no baseline can be named;
- no data path exists;
- reviewer objection cannot be answered without changing the task;
- the idea is only an implementation of an existing method with no new insight;
- the expected result would not change any research or engineering decision.
```

## Decision Checkpoint Template

```text
Idea:
Current verdict:
Continue / narrow / downgrade / kill:
Reason:
Evidence:
Minimum next action:
What result changes the decision:
```

## Final Output Requirement

For each top idea, include:

```text
Continue condition:
Downgrade condition:
Kill condition:
Next checkpoint:
```
