# Experiment Design

Every novelty idea must be converted into a testable experimental plan.

## Experiment Card

```text
Claim to test:
Independent variable:
Dependent variable:
Controlled variables:
Datasets:
Metrics:
Baselines:
Ablations:
Robustness checks:
Failure cases:
Qualitative analysis:
Expected result:
Result that would falsify the idea:
Minimum experiment:
Stretch experiment:
```

## Main experiment types

### Method paper

Required:

- compare against strong recent baselines;
- include simple baselines;
- include ablations for each claimed component;
- test robustness beyond one dataset when possible;
- report cost, latency, or parameter budget when relevant.

### Benchmark paper

Required:

- show why existing benchmarks are insufficient;
- define input, output, metrics, and annotation rules;
- evaluate diverse model families;
- show whether the benchmark changes model ranking;
- include human or expert agreement if labels are subjective.

### System paper

Required:

- define system constraints;
- measure latency, throughput, cost, reliability, and failure recovery;
- compare against simple engineering baselines;
- include stress tests and ablations.

### Analysis paper

Required:

- isolate the phenomenon;
- control confounding variables;
- test multiple datasets or model families;
- include counterexamples and failure slices.

### Negative-result paper

Required:

- reproduce the positive claim fairly;
- show failure under controlled changes;
- rule out trivial implementation mistakes;
- explain when the original claim still holds.

## Reviewer checks

Ask:

- Can the main claim be verified by the proposed experiment?
- Is there a strong baseline that may erase the contribution?
- Is the evaluation aligned with the claimed real-world problem?
- Are there enough ablations to prove which component matters?
- Would a negative result still be informative?
