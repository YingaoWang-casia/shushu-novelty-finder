# Example Output: RAG Evaluation

This is a compact example of the expected output style.

## Executive recommendation

Best direction: separate RAG evaluation into retrieval support, citation support, and answer utility.

Novelty level: medium.

Why: many RAG evaluations mix retrieval success, citation quality, and answer correctness into one result. A useful project can test whether model rankings change when these axes are separated.

Main risk: existing benchmark papers may already cover part of this split. The first action is to verify closest benchmark work.

## Research Scope Card

```text
Direction: RAG evaluation
Subfield: NLP / IR / LLM systems
Task: evaluate whether generated answers are supported by retrieved evidence
Input: question, retrieved passages, generated answer, citations
Output: multi-axis evaluation report
Metrics: retrieval support, citation support, answer utility, latency, cost
Excluded: general long-context evaluation, pure retriever training, generic agent evaluation
```

## Trend Matrix

```text
Period | Trend | Open gap
Early neural retrieval | focus on retrieval quality | weak link to final answer utility
LLM RAG | focus on grounded generation | faithfulness and citation quality become central
Recent evaluation work | more benchmarks and judge models | metrics may mix different failure sources
Production RAG | latency and cost matter | offline scores may not predict deployment quality
```

## Gap Audit

Gap: retrieval quality, citation support, and answer utility are often not separated clearly.

Gap type: metric gap / benchmark gap.

Evidence type: cross-paper pattern, requires verification through paper matrix.

Why it matters: a system can retrieve relevant text, cite it incorrectly, and still answer correctly. A single score hides this failure.

## Novelty Candidates

### Weak idea

Run existing RAG systems on one benchmark and report separate retrieval, citation, and answer metrics.

Risk: may be only an analysis report.

### Medium idea

Build a multi-axis RAG evaluation protocol and show that system rankings change across axes.

Minimum experiment: compare several RAG pipelines across retrieval support, citation support, answer utility, latency, and cost.

### Strong idea

Define a new benchmark where evidence relevance and citation support are independently controlled.

Risk: requires careful data construction and annotation.

## Paper-readiness verdict

Current best idea: medium idea.

Verdict: pilot-ready, possibly workshop-ready after literature verification and baseline implementation.

Main reason to accept: the claim is testable and useful.

Main reason to reject: novelty depends on whether existing RAG benchmarks already separate these axes.
