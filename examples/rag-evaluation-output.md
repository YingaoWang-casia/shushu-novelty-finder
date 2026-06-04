# Example Output: RAG Evaluation

This is an illustrative output example. It demonstrates structure and evidence discipline, not a verified literature review. Paper names marked `illustrative placeholder` must be replaced by real papers after search.

## Executive Recommendation

```text
Recommended idea: multi-axis RAG evaluation for retrieval support, citation support, answer utility, latency, and cost
Novelty level: medium
Paper-readiness verdict: pilot-ready
Best paper type: analysis / evaluation paper
Fallback paper type: technical report
Why this is the best option: it is testable, useful, and can be scoped to limited compute
Evidence basis: placeholder papers only; no verified search yet
Minimum experiment: compare 4-6 RAG variants across separated axes
Baseline plan: lexical retrieval, dense retrieval, reranker vs no reranker, closed-book, long-context if relevant
Main risk: existing RAG evaluation benchmarks may already separate these axes
Likely accept reason: exposes hidden ranking changes across evaluation axes
Likely reject reason: may duplicate existing RAG evaluation frameworks
Continue / narrow / downgrade / kill: continue only after closest benchmark papers are verified
```

## Research Scope Card

```text
Direction: RAG evaluation
Subfield: NLP / IR / LLM systems
Task: evaluate whether generated answers are supported by retrieved evidence
Input: user question, retrieved passages, generated answer, citations
Output: multi-axis evaluation report and system ranking
Datasets: existing open-domain QA or domain QA datasets; exact dataset unverified
Metrics: recall@k, citation precision, answer F1, faithfulness, latency, cost
Included directions: answer support, citation support, retrieval support
Excluded directions: retriever training, long-context-only evaluation, general agent evaluation
Constraints: 2 months, limited compute
```

## Paper Evidence Cards

```text
Title: <retrieval benchmark paper A> (illustrative placeholder)
Year: <year>
Venue or source: <venue or source>
Paper type: benchmark
URL, DOI, or arXiv id: <unknown>
Task: retrieval evaluation
Dataset: <unknown>
Metric: recall@k / nDCG
Main contribution: <placeholder>
Why it is relevant: anchors retrieval-side evaluation
Evidence status: placeholder
Evidence role: benchmark baseline
Used to support which claim: retrieval support must be evaluated separately
Confidence: weak
```

```text
Title: <RAG evaluation framework B> (illustrative placeholder)
Year: <year>
Venue or source: <venue or source>
Paper type: evaluation framework
URL, DOI, or arXiv id: <unknown>
Task: RAG evaluation
Dataset: <unknown>
Metric: faithfulness / answer relevance / context relevance
Main contribution: <placeholder>
Why it is relevant: closest contrary evidence candidate
Evidence status: placeholder
Evidence role: contrary evidence; metric source
Used to support which claim: checks whether multi-axis RAG evaluation already exists
Confidence: weak
```

## Claim-Evidence Map

```text
Claim: RAG system rankings may change when retrieval support, citation support, answer utility, latency, and cost are evaluated separately.
Claim type: evaluation / novelty
Supporting papers: <retrieval benchmark paper A> (placeholder)
Contrary papers: <RAG evaluation framework B> (placeholder)
Background papers: <RAG method paper C> (placeholder)
Evidence strength: weak
What can be safely claimed: this is a candidate idea that requires verified related work.
What must not be claimed: nobody has done multi-axis RAG evaluation.
Confidence: weak
Next verification step: verify closest RAGAS / ARES / ALCE-like evaluation papers.
```

## Literature Timeline

| Time stage | Representative papers | Main task definition | Dataset / metric pattern | What changed |
| --- | --- | --- | --- | --- |
| Retrieval benchmark stage | `<retrieval benchmark paper A>` placeholder | retrieve relevant passages | recall@k, nDCG | retrieval quality becomes measurable |
| RAG system stage | `<RAG method paper C>` placeholder | answer with retrieved evidence | QA / generation metrics | retrieval and generation become coupled |
| RAG evaluation stage | `<RAG evaluation framework B>` placeholder | judge RAG output quality | faithfulness, answer relevance | multi-axis evaluation emerges |

## Trend Matrix

| Time Period | Representative Papers | Task Shift | Method Shift | Dataset/Metric Shift | Open Gap |
| --- | --- | --- | --- | --- | --- |
| Earlier retrieval | placeholders | retrieval only | lexical / dense retrieval | recall@k / nDCG | weak link to final answer utility |
| RAG systems | placeholders | retrieval + generation | retriever-generator pipelines | answer accuracy | citation support may be implicit |
| RAG evaluation | placeholders | judge answer support | automated judges / metrics | faithfulness / citation support | axes may still be mixed |

## Gap Audit

```text
Gap: retrieval support, citation support, answer utility, latency, and cost may be mixed in single evaluation summaries.
Gap type: metric gap / protocol gap
Evidence type: cross-paper pattern, currently placeholder-only
Supporting papers: placeholders
Why this matters: one score hides whether a failure came from retrieval, attribution, or generation.
Why it may be a bad idea: existing evaluation frameworks may already separate these dimensions.
Confidence: weak until verified
```

## Novelty Candidates

```text
Idea: report separated RAG evaluation axes and test whether rankings change.
Novelty level: medium after verification; pilot-only before verification
Evidence: placeholder-only
Evidence type: suspected cross-paper pattern plus contrary-evidence search
Feasibility: medium
Minimum experiment: evaluate 4-6 RAG variants on one shared dataset
Baseline plan: lexical retrieval, dense retrieval, reranker vs no reranker, closed-book, long-context if relevant
Risks: duplicate of existing RAG evaluation frameworks; annotation cost
Best target output: workshop-ready if verified and ranking changes appear
```

## Paper Type Routing

```text
Best paper type: analysis / evaluation paper
Fallback paper type: technical report
Why this type fits: contribution is an evaluation protocol and empirical finding, not a new model.
Required evidence: verified closest evaluation frameworks and benchmark papers
Required baselines: retrieval, reranking, closed-book, long-context when relevant
Main reviewer risk: reviewers may say existing frameworks already do this.
Readiness verdict: pilot-ready
```

## Paper Thesis Card

```text
Working title: When RAG Systems Disagree With Themselves: Separating Retrieval Support, Citation Support, and Answer Utility
Paper type: analysis / evaluation paper
Core claim: system rankings change when RAG outputs are evaluated across separated axes.
Why now: RAG systems are widely used and evaluation failures are often mixed.
What existing work assumes: a compact evaluation summary is enough to compare systems.
What breaks that assumption: systems can score well on one axis and fail another.
What evidence supports the claim: currently none verified; requires pilot experiment.
What reviewers may reject: insufficient novelty or weak baselines.
```

## Experiment Card

```text
Claim: multi-axis evaluation changes comparative ranking.
Independent variable: RAG pipeline and evaluation axis
Dependent variable: ranking under retrieval support, citation support, answer utility, latency, cost
Datasets: one open QA or long-form QA dataset
Metrics: recall@k, nDCG, citation precision, faithfulness, answer F1, latency, cost
Baselines: lexical retrieval, dense retrieval, reranker, closed-book, long-context if relevant
Ablations: remove reranker, vary top-k, remove citations
Robustness checks: distractor passages, unsupported answer cases
Falsification result: rankings do not change and no axis-specific failure appears
```

## Reviewer Objection Pre-Mortem

```text
Likely reviewer objection: existing RAG evaluation frameworks already separate these dimensions.
Why plausible: RAG evaluation is an active area.
Evidence needed: closest benchmark and framework comparison.
Current defense: none until verified.
Weakness: novelty may collapse.
Action to strengthen: map exact axes covered by closest frameworks.
Verdict impact: downgrade if overlap is high.
```

```text
Likely reviewer objection: this is engineering-only.
Why plausible: reporting more metrics may be a tool contribution, not research.
Evidence needed: show non-obvious ranking changes or failure-mode insight.
Current defense: minimum experiment can test this.
Weakness: result may be obvious.
Action to strengthen: add falsification and contrary-hypothesis analysis.
Verdict impact: technical-report-only if no insight appears.
```

```text
Likely reviewer objection: baselines are too weak.
Why plausible: RAG has strong recent systems and evaluation frameworks.
Evidence needed: include strongest feasible evaluation baseline.
Current defense: baseline plan includes retrieval and long-context alternatives.
Weakness: no verified strongest baseline yet.
Action to strengthen: identify closest accepted benchmark protocol.
Verdict impact: not workshop-ready until done.
```

## Kill / Continue Criteria

```text
Continue condition: closest frameworks do not cover the exact scoped axes, and pilot shows ranking changes.
Narrow condition: overlap exists but one failure mode remains under-tested.
Downgrade condition: only descriptive metrics are added with no new insight.
Kill condition: closest verified work already makes the same claim and experiment gives no ranking change.
Next checkpoint: verify closest RAG evaluation papers and run a 3-system pilot.
Smallest next action that changes the decision: build a 5-paper Claim-Evidence Map.
```

## Paper-readiness Verdict

Verdict: `pilot-ready`.

Upgrade path: `workshop-ready` if verified literature shows a scoped gap and the minimum experiment shows ranking changes.

Downgrade path: `technical-report-only` if existing frameworks already cover the protocol or the experiment only confirms obvious behavior.
