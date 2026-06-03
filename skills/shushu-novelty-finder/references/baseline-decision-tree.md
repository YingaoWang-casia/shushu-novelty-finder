# Baseline Decision Tree

Use this reference to select baselines based on paper type, domain, and claim. A paper idea is not paper-ready until the strongest obvious baseline is named.

## General Rule

Every top idea needs two baseline tiers:

```text
Minimum baselines: enough for a pilot or workshop-style check.
Strong baselines: needed for main-track credibility.
```

If the user cannot run strong baselines, say so and downgrade the readiness verdict.

## Baseline Selection Flow

```text
1. What is the paper type?
2. What is the core claim?
3. What is the closest prior work?
4. What baseline would a reviewer expect first?
5. What baseline would make the idea look weak if it wins?
6. What baseline would make the idea look publishable if it wins?
```

## By Paper Type

### Method Paper

Minimum baselines:

- strongest simple baseline;
- closest prior method;
- ablation without the proposed component.

Strong baselines:

- recent accepted SOTA or strong open implementation;
- reproduced benchmark baseline;
- compute-matched comparison.

### Benchmark Paper

Minimum baselines:

- simple heuristic;
- common existing model or pipeline;
- human or rule-based reference if appropriate.

Strong baselines:

- multiple model families;
- task-specific strong baselines;
- stress-test or adversarial baseline.

### Analysis Paper

Minimum baselines:

- existing aggregate metric or common evaluation protocol;
- random / majority / trivial control when relevant;
- controlled comparison that isolates the factor being analyzed.

Strong baselines:

- multiple datasets;
- multiple model families;
- contrary hypothesis baseline.

### System Paper

Minimum baselines:

- previous system or naive pipeline;
- no-component ablation;
- cost / latency baseline.

Strong baselines:

- production-like workload;
- robustness or failure-mode baseline;
- deployment constraints and monitoring comparison.

### Dataset Paper

Minimum baselines:

- simple model baseline;
- existing dataset comparison;
- annotation agreement or quality control.

Strong baselines:

- cross-dataset transfer;
- multiple model families;
- error analysis and data contamination checks.

## Domain Examples

### RAG Evaluation

Minimum baselines:

- lexical retrieval;
- dense retrieval;
- reranker vs no reranker;
- prompt-only / closed-book baseline;
- long-context baseline when relevant.

Strong baselines:

- strongest recent RAG benchmark protocol;
- citation-aware evaluation baseline;
- human annotation or verified evidence labels when citation correctness is the claim.

### LLM-as-a-Judge

Minimum baselines:

- human judgment subset;
- rule-based metric;
- GPT judge baseline;
- smaller open-model judge;
- pairwise vs pointwise comparison.

Strong baselines:

- bias / calibration baseline;
- adversarial or ambiguous cases;
- inter-annotator agreement;
- cross-domain generalization.

### Speech Turn-Taking

Minimum baselines:

- rule-based endpointing;
- classical VAD;
- neural VAD;
- simple timing heuristic.

Strong baselines:

- recent turn-taking model;
- real-time latency baseline;
- interruption and backchannel-specific evaluation.

## Final Output Requirement

For every top idea, include:

```text
Minimum baselines:
Strong baselines:
Why each baseline is necessary:
What result would make the idea weak:
What result would make the idea publishable:
```
