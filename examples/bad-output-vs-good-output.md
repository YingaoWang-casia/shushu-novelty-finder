# Bad Output vs Good Output

This example shows the value of the Skill discipline.

## User input

```text
I want to find novelty ideas around RAG evaluation.
```

## Bad output pattern

```text
RAG evaluation is underexplored. You can build a new benchmark for factuality, robustness, and citation accuracy. This is a strong innovation because no existing work fully solves it.
```

Why this is bad:

- no scope lock;
- no concrete papers;
- no evidence type;
- overclaims that the gap is unsolved;
- no baseline or minimum experiment;
- no risk analysis.

## Good output pattern

```text
Mode: Research Mode
Scope: RAG evaluation for LLM question answering, not general retrieval or long-context evaluation.

Evidence plan:
- collect accepted papers and benchmark papers from NLP, IR, and LLM system venues;
- separate faithfulness, citation correctness, retrieval quality, and end-to-end answer utility;
- mark preprints separately.

Candidate gap:
Existing RAG evaluations often mix retrieval quality, answer correctness, and citation quality into one end-to-end score.
Evidence type: cross-paper pattern, to be verified by literature matrix.

Medium idea:
Design an evaluation protocol that reports retrieval support, citation support, and answer utility as separate axes.
Minimum experiment:
Run several RAG pipelines on a shared QA set and show that system rankings change across axes.
Risk:
If existing benchmarks already separate these axes well, downgrade to a reproduction or analysis project.
```

The good output is not longer for its own sake. It is better because it makes claims auditable.
