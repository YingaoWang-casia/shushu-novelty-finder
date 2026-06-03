# Eval Case: RAG Evaluation

## Input

```text
Use shushu-novelty-finder.
Direction: RAG evaluation.
Goal: paper-oriented project.
Constraints: 2 months, limited compute.
```

## Expected behavior

The Skill should not search all RAG papers. It should first narrow the scope into one or more of:

- retrieval quality;
- answer faithfulness;
- citation accuracy;
- robustness;
- long-context comparison;
- production cost and latency;
- human preference alignment.

## Required output checks

- Research Scope Card exists.
- Venue clusters include NLP and IR.
- Trend Matrix is not just a paper list.
- Gaps have evidence labels.
- At least one novelty idea is downgraded because of feasibility or weak evidence.
- Top idea includes paper thesis and minimum experiment.

## Failure signs

- Claims that no RAG evaluation benchmark exists.
- Mixes retrieval, generation, and agent evaluation without separation.
- Gives strong novelty without baselines or metrics.
