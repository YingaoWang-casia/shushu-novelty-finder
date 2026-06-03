# Example Output: RAG Evaluation

This is an illustrative example output. It demonstrates structure and evidence discipline, not a verified literature review. Paper names marked `illustrative placeholder` must be replaced by real papers after search.

## Executive Recommendation

Recommended directions:

1. Medium idea: evaluate retrieval support, citation support, and answer utility as separate axes, then test whether RAG system rankings change across axes.
2. Medium idea: build a low-cost citation correctness audit protocol for RAG answers with explicit failure categories.
3. Weak idea: run an existing RAG benchmark with additional latency and cost reporting.

Best next action: verify the closest RAG benchmark and citation evaluation papers before claiming novelty.

## Research Scope Card

```text
Direction: RAG evaluation
Subfield: NLP / IR / LLM systems
Task: evaluate whether generated answers are supported by retrieved evidence
Input: user question, retrieved passages, generated answer, citations
Output: multi-axis evaluation report and system ranking
Datasets: existing open-domain QA or domain QA datasets; exact dataset unverified
Metrics: recall@k, citation precision, answer F1, faithfulness, latency, cost
Excluded directions: retriever training, long-context-only evaluation, general agent evaluation, private enterprise RAG case studies
Assumptions: 2 months, limited compute, paper-oriented project
```

## Literature Timeline

### Paper Evidence Card 1

```text
Title: <retrieval benchmark paper A> (illustrative placeholder)
Year: <year>
Venue/source: <venue or source>
Paper type: benchmark
Evidence role: benchmark baseline
Why relevant: anchors retrieval-side evaluation metrics such as recall@k and nDCG
Confidence: weak until replaced with a verified paper
```

### Paper Evidence Card 2

```text
Title: <RAG faithfulness evaluation paper B> (illustrative placeholder)
Year: <year>
Venue/source: <venue or source>
Paper type: analysis / benchmark
Evidence role: metric source
Why relevant: anchors answer faithfulness or groundedness evaluation
Confidence: weak until replaced with a verified paper
```

### Paper Evidence Card 3

```text
Title: <citation correctness paper C> (illustrative placeholder)
Year: <year>
Venue/source: <venue or source>
Paper type: method / benchmark
Evidence role: metric source
Why relevant: anchors citation-level correctness and attribution checks
Confidence: weak until replaced with a verified paper
```

### Paper Evidence Card 4

```text
Title: <production RAG evaluation paper D> (illustrative placeholder)
Year: <year>
Venue/source: <venue or source>
Paper type: system / analysis
Evidence role: limitation evidence
Why relevant: motivates latency, cost, and deployment constraints
Confidence: weak until replaced with a verified paper
```

## Trend Matrix

| Time Period | Representative Papers | Task Shift | Method Shift | Dataset/Metric Shift | Open Gap |
| --- | --- | --- | --- | --- | --- |
| Earlier retrieval era | `<retrieval benchmark paper A>` (illustrative placeholder) | retrieve relevant passages | lexical and dense retrieval comparisons | recall@k, precision@k, nDCG | retrieval quality is not enough to judge final answer usefulness |
| Early RAG systems | `<RAG system paper>` (illustrative placeholder) | generate answers using retrieved context | retriever-generator pipelines | answer accuracy and retrieval recall | citation support may be implicit or missing |
| Recent grounded generation | `<RAG faithfulness evaluation paper B>` (illustrative placeholder) | judge answer support | LLM judges, entailment, human annotation | faithfulness, groundedness | faithfulness may mix retrieval failure and generation failure |
| Citation-aware evaluation | `<citation correctness paper C>` (illustrative placeholder) | verify cited evidence | citation matching and attribution checks | citation precision, evidence coverage | answer correctness and citation correctness can diverge |
| Production-oriented RAG | `<production RAG evaluation paper D>` (illustrative placeholder) | deploy under cost and latency constraints | pipeline audits, monitoring, ablations | latency, cost, failure rates | offline benchmark score may not predict deployment utility |

## Gap Audit

### Gap 1

```text
Gap: RAG evaluation often blends retrieval success, answer correctness, and citation support into a single score.
Gap type: metric gap / benchmark gap
Evidence type: cross-paper pattern, unverified until literature matrix is populated
Supporting papers: <retrieval benchmark paper A>, <RAG faithfulness evaluation paper B>, <citation correctness paper C> (illustrative placeholders)
Why it matters: a system can retrieve relevant passages, cite unsupported text, and still answer correctly. A single score hides the failure mode.
Why it may be a bad idea: existing benchmark papers may already separate these axes; novelty depends on verified coverage.
Confidence: weak before real search; medium if verified across accepted papers
```

### Gap 2

```text
Gap: Citation correctness may be evaluated without enough attention to retrieval-side availability of supporting evidence.
Gap type: evaluation protocol gap
Evidence type: inferred gap, requires contrary-evidence search
Supporting papers: <citation correctness paper C>, <retrieval benchmark paper A> (illustrative placeholders)
Why it matters: a citation error caused by missing retrieval evidence is different from a generation-side attribution error.
Why it may be a bad idea: annotation may be expensive, and reviewers may see the split as engineering rather than research.
Confidence: weak until verified
```

## Novelty Candidates

### Weak

```text
Idea: Re-run several RAG pipelines and report retrieval, citation, answer, latency, and cost metrics.
Novelty level: weak
Evidence: common evaluation axes are scattered across retrieval and RAG papers.
Evidence type: cross-paper pattern, unverified
Feasibility: high
Minimum experiment: compare lexical retrieval, dense retrieval, reranker, and closed-book baselines on one QA dataset.
Risks: likely to be an analysis report unless it reveals a non-obvious ranking change.
Best target output: technical-report-only or pilot-ready
```

### Medium

```text
Idea: Build a multi-axis RAG evaluation protocol that separates retrieval support, citation support, and answer utility, then show that model rankings change across axes.
Novelty level: medium
Evidence: retrieval, faithfulness, and citation papers appear to emphasize different axes.
Evidence type: cross-paper pattern plus benchmark absence, must be verified
Feasibility: medium
Minimum experiment: evaluate 4-6 RAG variants on one shared dataset; report recall@k, citation precision, answer F1, faithfulness, latency, and cost.
Risks: if existing benchmarks already do this split, downgrade to reproduction or extension.
Best target output: workshop-ready after verified related work and clean baselines
```

### Strong

```text
Idea: Construct a controlled benchmark where retrieval relevance, citation support, and answer utility are independently manipulated.
Novelty level: strong only if closest benchmarks do not already provide independent controls
Evidence: would require verified benchmark absence and reviewer-relevant failure modes.
Evidence type: benchmark absence plus contrary-evidence search
Feasibility: medium-low
Minimum experiment: create a small annotated set with controlled evidence availability and compare RAG systems under axis-specific perturbations.
Risks: annotation burden, benchmark validity, and possible overlap with existing datasets.
Best target output: main-track candidate only after strong literature verification and annotation quality evidence
```

## Paper Thesis Card

```text
Working title: When RAG Systems Disagree With Themselves: Separating Retrieval Support, Citation Support, and Answer Utility
Paper type: evaluation / analysis paper
Core claim: RAG system rankings change when retrieval support, citation support, and answer utility are evaluated separately.
Why now: RAG systems are widely used, but deployment failures often appear as mixed retrieval-generation-citation errors.
What existing work assumes: end-to-end answer quality or a single faithfulness score is sufficient for comparing systems.
What breaks that assumption: a system can score well on one axis and fail another axis.
What evidence supports the claim: verified paper evidence cards plus ranking-change experiments.
What reviewers may reject: insufficient novelty if prior benchmarks already separate these axes, or weak annotation if citation support labels are noisy.
```

## Experiment Card

```text
Claim: Multi-axis evaluation changes the comparative ranking of RAG systems.
Independent variable: RAG pipeline variant and evaluation axis.
Dependent variable: system ranking under retrieval support, citation support, answer utility, latency, and cost.
Datasets: one open QA dataset plus retrieved evidence corpus; exact dataset to be selected after literature check.
Metrics: recall@k, nDCG, citation precision, answer F1, faithfulness, latency, cost.
Baselines: lexical retrieval, dense retrieval, reranker vs no reranker, prompt-only / closed-book, long-context baseline if relevant.
Ablations: remove reranker, vary top-k, remove citation requirement, use oracle retrieval subset.
Robustness checks: paraphrased questions, distractor passages, unsupported answer cases.
Falsification result: if rankings do not change across axes and errors are not axis-specific, the core claim is weakened.
```

## Paper-readiness Verdict

Verdict: `pilot-ready`.

Reason: the idea is testable and useful, but the novelty level remains uncertain until real RAG evaluation papers are checked.

Upgrade path: becomes `workshop-ready` if verified literature shows the axes are not already cleanly separated and the minimum experiment shows ranking changes.

Downgrade path: becomes `technical-report-only` if existing benchmarks already cover the same protocol or if the experiment only confirms obvious behavior.
