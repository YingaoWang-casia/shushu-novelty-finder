# Baseline Protocol

A novelty idea is weak if it only beats weak baselines. Use this protocol before recommending a paper idea.

## Baseline Card

```text
Target claim:
Closest prior work:
Recent strong baselines:
Simple baselines:
Heuristic baselines:
Human or expert baseline, if relevant:
Commercial or closed model baseline, if relevant:
Ablation baselines:
Cost or latency baselines:
Fairness constraints:
What baseline could invalidate the claim:
```

## Baseline types

### Strong recent baselines

Use the best or most relevant recent papers in the scoped literature line. If the exact SOTA is too expensive, explain the approximation.

### Simple baselines

Always consider simple alternatives:

- heuristic rules;
- majority or random baselines;
- BM25 or lexical retrieval for retrieval tasks;
- small models versus large models;
- prompt-only baselines for LLM systems;
- no-rerank or no-tool baselines for agentic systems.

### Ablation baselines

Remove or replace each claimed component. If removing a component does not hurt, the component is not a contribution.

### Cost baselines

For systems and LLM papers, report cost, latency, throughput, memory, API calls, or annotation effort when relevant.

## Contribution-specific requirements

### Method paper

Needs recent SOTA, simple baseline, and ablations.

### Benchmark paper

Needs existing benchmarks, model family coverage, and evidence that the new benchmark reveals different behavior.

### Dataset paper

Needs data quality checks, inter-annotator agreement if applicable, and baseline models.

### System paper

Needs throughput, latency, cost, reliability, and stress-test baselines.

### Analysis paper

Needs controlled comparisons and alternative explanations.

## Reject warning

If the idea depends on beating only a weak baseline, downgrade it or mark it as not paper-ready.
