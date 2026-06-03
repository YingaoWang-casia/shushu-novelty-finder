# Gap Taxonomy

Use this taxonomy to classify research gaps.

## Gap types

### Dataset gap

The field lacks data diversity, scale, realism, language coverage, domain coverage, noise conditions, or annotation quality.

### Benchmark gap

There is no unified benchmark, the existing benchmark is outdated, or the benchmark does not match real use cases.

### Metric gap

Common metrics fail to measure what matters. Examples: ignoring latency, cost, robustness, user experience, fairness, calibration, or failure severity.

### Method gap

Main methods share a weakness: poor generalization, high cost, brittle assumptions, weak interpretability, or dependence on unavailable labels.

### System gap

Methods work offline but not in real-time, production, low-resource, edge, privacy-sensitive, or multi-user settings.

### Robustness gap

Performance under domain shift, noise, adversarial input, long-tail cases, multilingual settings, or out-of-distribution data is underexplored.

### Interpretability gap

The field lacks diagnosis, explanation, causal analysis, attribution, or clear failure-mode taxonomy.

### Negative-result gap

Papers rarely report failure conditions, ablations that did not help, or boundaries where the method stops working.

## Evidence labels

Mark every gap with one evidence label:

- explicit limitation: directly stated in a paper limitation section;
- future work: directly stated as future work;
- cross-paper pattern: appears after comparing multiple papers;
- benchmark absence: no suitable benchmark found in scoped search;
- implementation absence: no code/data/evaluation pipeline found;
- inferred gap: plausible but not directly verified.

Inferred gaps are hypotheses, not conclusions.
