# Verified Mini Audit: RAG Evaluation

This is a small, verified example showing how to use real papers as evidence without pretending to have completed a full systematic review.

Scope: RAG evaluation for question answering and long-form answer support.

Search status: partial verified mini-audit. This is not a complete survey of RAG evaluation.

## Executive Recommendation

Recommended idea: evaluate RAG systems with separated axes for retrieval support, citation / attribution support, answer utility, latency, and cost.

Novelty level: medium if the claim is narrowed to a specific setting such as long-form QA with citations.

Paper-readiness verdict: pilot-ready now; workshop-ready only after checking the closest citation-evaluation and RAG-evaluation papers more exhaustively.

Likely accept reason: the idea turns a known pain point into a controlled evaluation protocol.

Likely reject reason: existing RAG evaluation frameworks and citation benchmarks may already cover parts of the claim.

## Research Scope Card

```text
Direction: RAG evaluation
Subfield: NLP / IR / LLM evaluation
Task: evaluate whether generated answers are supported by retrieved evidence and citations
Input: question, retrieved passages, generated answer, citations
Output: multi-axis evaluation report
Datasets: open-domain QA / long-form QA / citation-oriented benchmark candidates
Metrics: recall@k, evidence coverage, citation precision, factual precision, answer utility, latency, cost
Excluded directions: retriever training, generic long-context evaluation, general agent evaluation
```

## Paper Evidence Cards

### Paper 1

```text
Title: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
Year: 2020
Venue or source: NeurIPS 2020
Paper type: method
URL, DOI, or arXiv id: https://papers.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html
Task: knowledge-intensive NLP tasks including open-domain QA
Dataset: multiple QA and generation tasks
Metric: task-specific QA / generation metrics
Main contribution: combines parametric seq2seq memory with non-parametric retrieval memory for generation
Why it is relevant: task anchor for RAG as retrieval-augmented generation
Evidence status: verified
Evidence role: task anchor; method baseline
Used to support which claim: RAG evaluation must account for both retrieval and generation components
Confidence: strong
```

### Paper 2

```text
Title: KILT: a Benchmark for Knowledge Intensive Language Tasks
Year: 2021
Venue or source: NAACL 2021
Paper type: benchmark
URL, DOI, or arXiv id: https://aclanthology.org/2021.naacl-main.200/
Task: knowledge-intensive language tasks grounded in a common Wikipedia snapshot
Dataset: KILT benchmark suite
Metric: task-specific metrics plus retrieval / provenance considerations
Main contribution: benchmark suite for knowledge-intensive tasks with shared knowledge source
Why it is relevant: benchmark baseline and dataset source for retrieval-grounded tasks
Evidence status: verified
Evidence role: benchmark baseline; dataset source
Used to support which claim: benchmark design matters for comparing retrieval-augmented systems
Confidence: strong
```

### Paper 3

```text
Title: FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation
Year: 2023
Venue or source: EMNLP 2023
Paper type: evaluation / metric
URL, DOI, or arXiv id: https://aclanthology.org/2023.emnlp-main.741/
Task: factual precision evaluation for long-form generated text
Dataset: people biographies and model generations
Metric: FActScore based on atomic facts supported by reliable knowledge source
Main contribution: decomposes long-form text into atomic facts for fine-grained factual precision
Why it is relevant: metric-source evidence for answer factuality beyond a binary quality label
Evidence status: verified
Evidence role: metric source
Used to support which claim: answer support should be evaluated at a finer granularity than whole-answer correctness
Confidence: strong
```

### Paper 4

```text
Title: RAGAs: Automated Evaluation of Retrieval Augmented Generation
Year: 2024
Venue or source: EACL 2024 demo
Paper type: evaluation framework
URL, DOI, or arXiv id: https://aclanthology.org/2024.eacl-demo.16/
Task: reference-free evaluation of RAG pipelines
Dataset: framework / demo setting
Metric: RAGAS metrics for retrieval and generation dimensions
Main contribution: automated evaluation framework for RAG systems
Why it is relevant: contrary evidence against claiming that multi-dimensional RAG evaluation is absent
Evidence status: verified
Evidence role: contrary evidence; metric source
Used to support which claim: the proposed idea must differentiate from existing automated RAG evaluation frameworks
Confidence: strong
```

### Paper 5

```text
Title: Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection
Year: 2024
Venue or source: ICLR 2024
Paper type: method
URL, DOI, or arXiv id: https://research.ibm.com/publications/self-rag-learning-to-retrieve-generate-and-critique-through-self-reflection
Task: adaptive retrieval and generation with self-reflection
Dataset: open-domain QA, reasoning, fact verification, long-form generation tasks
Metric: task metrics plus factuality / citation-related evaluation
Main contribution: trains a model to retrieve, generate, and critique with reflection tokens
Why it is relevant: method baseline and evidence that citation / factuality claims appear in modern RAG-style systems
Evidence status: verified
Evidence role: method baseline; follow-up work
Used to support which claim: any evaluation idea should consider adaptive retrieval and self-critique systems, not only fixed top-k RAG
Confidence: strong
```

### Paper 6

```text
Title: Enabling Large Language Models to Generate Text with Citations
Year: 2023
Venue or source: arXiv / project repository
Paper type: benchmark / preprint
URL, DOI, or arXiv id: https://arxiv.org/abs/2305.14627
Task: automatic evaluation of LLM citation generation
Dataset: ALCE benchmark
Metric: citation-oriented evaluation metrics
Main contribution: proposes ALCE for automatic citation evaluation
Why it is relevant: closest citation-evaluation benchmark candidate; must be checked before claiming citation-evaluation novelty
Evidence status: verified source, preprint status
Evidence role: contrary evidence; benchmark baseline
Used to support which claim: citation correctness is already an active evaluation target
Confidence: moderate
```

### Paper 7

```text
Title: ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems
Year: 2023
Venue or source: arXiv
Paper type: preprint / evaluation framework
URL, DOI, or arXiv id: https://arxiv.org/abs/2311.09476
Task: automated RAG evaluation
Dataset: RAG evaluation settings
Metric: context relevance, answer faithfulness, answer relevance
Main contribution: automated evaluation framework for RAG systems
Why it is relevant: contrary evidence and baseline candidate for multi-axis RAG evaluation
Evidence status: verified source, preprint status
Evidence role: contrary evidence; metric source
Used to support which claim: multi-axis RAG evaluation exists, so a new idea must narrow or improve the protocol
Confidence: moderate
```

## Claim-Evidence Map

```text
Claim: RAG evaluation should separate retrieval support, citation / attribution support, and answer utility.
Claim type: evaluation / novelty
Supporting papers: RAG 2020, KILT 2021, FActScore 2023
Contrary papers: RAGAS 2024, ALCE 2023, ARES 2023
Background papers: Self-RAG 2024
Evidence strength: moderate
What can be safely claimed: existing work motivates multi-dimensional evaluation, and a scoped protocol may still be useful if it isolates a specific failure mode.
What must not be claimed: nobody evaluates RAG along multiple axes.
Confidence: moderate
Next verification step: read ALCE, RAGAS, and ARES in detail and map exactly which axes they cover.
```

## Gap Audit

```text
Gap: Existing RAG evaluation work covers multiple dimensions, but a specific scoped protocol may still be useful if it shows when system rankings change across retrieval support, citation support, answer utility, latency, and cost.
Gap type: evaluation protocol gap
Evidence type: cross-paper pattern plus contrary-evidence search
Supporting papers: RAG 2020, KILT 2021, FActScore 2023, RAGAS 2024, ALCE 2023, ARES 2023
Why it matters: a single answer-quality score can hide whether failures come from retrieval, attribution, or generation.
Why it may be a bad idea: RAGAS, ALCE, and ARES may already cover the proposed axes closely enough to make this only an implementation report.
Confidence: moderate
```

## Novelty Candidate

```text
Idea: Build a scoped evaluation protocol for long-form RAG answers that reports retrieval support, citation support, answer utility, latency, and cost separately, then tests whether system rankings change across axes.
Novelty level: medium
Evidence: accepted RAG and benchmark papers motivate retrieval-grounded tasks; RAGAS / ALCE / ARES are contrary evidence that force a narrower claim.
Evidence type: verified papers plus preprint contrary evidence
Feasibility: medium
Minimum experiment: compare lexical retrieval, dense retrieval, reranker vs no reranker, closed-book, and one long-context baseline on a small long-form QA / citation setting.
Baseline plan: include RAGAS-style automated evaluation and citation benchmark checks if feasible.
Risks: novelty collapses if existing frameworks already cover the same protocol; annotation cost may be high.
Best target output: workshop-ready after detailed related-work mapping and pilot results.
```

## Reviewer Objection Pre-Mortem

```text
Objection 1: This is not novel because RAGAS and ARES already do multi-axis RAG evaluation.
Defense needed: show a narrower axis, dataset setting, or decision-use case that they do not cover.
Verdict impact: downgrade to pilot-ready until verified.
```

```text
Objection 2: Citation evaluation is already covered by ALCE-style work.
Defense needed: show the difference between citation correctness, evidence availability, and answer utility.
Verdict impact: narrow the claim.
```

```text
Objection 3: The protocol may be engineering-only.
Defense needed: show a non-obvious ranking change or failure-mode insight that changes evaluation practice.
Verdict impact: technical-report-only if no insight appears.
```

## Kill / Continue Criteria

```text
Continue if: pilot experiments show rankings change across axes and closest frameworks do not already make the same decision visible.
Downgrade if: results only reproduce known RAGAS / ARES / ALCE behavior.
Kill if: no axis-specific disagreement appears and no reviewer-relevant failure mode is found.
Next checkpoint: read RAGAS, ALCE, and ARES carefully; then run a 3-system pilot.
```

## Paper-Readiness Verdict

Verdict: `pilot-ready`.

Upgrade path: `workshop-ready` if the pilot reveals a non-obvious ranking or failure-mode difference and the closest contrary papers are clearly differentiated.

Do not call it `main-track candidate` before a stronger benchmark, verified annotations, and robust baselines exist.
