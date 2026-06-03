# Threats to Validity

Every paper-ready idea must include expected limitations and validity threats.

## Threats Card

```text
Internal validity:
External validity:
Construct validity:
Dataset bias:
Annotation reliability:
Metric mismatch:
Model selection bias:
Baseline weakness:
Reproducibility risk:
Compute or cost limitation:
Ethical or privacy concern:
Mitigation plan:
```

## Common threats

### Dataset bias

The dataset may be too narrow, synthetic, English-only, clean, small, or domain-specific.

### Annotation subjectivity

Human labels may be inconsistent. Require annotation guidelines, agreement measures, or expert review when applicable.

### Benchmark leakage

Models may have seen benchmark data or near-duplicates during training.

### Metric mismatch

The chosen metric may not reflect the real problem. For example, accuracy may ignore cost, latency, calibration, robustness, or failure severity.

### Model selection bias

The conclusion may depend on a small or biased set of models.

### Baseline weakness

Weak baselines can make the contribution look stronger than it is.

### Generalization risk

The finding may not transfer across datasets, domains, languages, modalities, or deployment settings.

### Reproducibility risk

Closed data, closed models, hidden prompts, or unstable APIs can weaken the paper.

## Rule

Do not treat limitations as an afterthought. Use them to improve experiment design before the paper is written.
