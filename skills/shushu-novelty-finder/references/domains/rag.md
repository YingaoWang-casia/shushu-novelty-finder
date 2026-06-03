# Domain Pack: RAG

Use this pack when the topic is retrieval-augmented generation, open-domain QA, citation quality, retrieval evaluation, reranking, or knowledge-grounded generation.

## Scope questions

Ask or infer:

- Is the focus retrieval, generation, citation, evaluation, robustness, or system deployment?
- Is the setting open-domain QA, enterprise QA, scientific QA, code QA, multimodal RAG, or agentic RAG?
- Is the target contribution a method, benchmark, metric, system, or analysis?
- Are closed-source LLMs allowed as baselines?
- Is the user able to build or annotate data?

## Common tasks

- retrieval quality evaluation;
- answer faithfulness;
- citation correctness;
- context selection;
- reranking;
- long-context versus retrieval comparison;
- robustness under noisy or conflicting documents;
- multi-hop evidence aggregation;
- enterprise or domain-specific knowledge QA.

## Common metrics

- retrieval recall, precision, MRR, nDCG;
- answer exact match or F1;
- faithfulness or groundedness;
- citation precision and recall;
- hallucination rate;
- latency and cost;
- human preference or expert rating.

## Common weak novelty

- testing one new embedding model without deeper analysis;
- adding a reranker without ablations;
- using a new document collection without explaining why it changes the task;
- reporting only end-to-end answer score.

## Promising medium novelty

- separate evaluation axes for retrieval support, citation support, and answer utility;
- benchmark realistic noisy documents or conflicting evidence;
- analyze when long context beats retrieval and when retrieval beats long context;
- build an error taxonomy for RAG failures;
- evaluate RAG under domain shift or stale knowledge.

## Strong novelty candidates

Strong ideas need proof, but possible directions include:

- a new evaluation protocol that changes model ranking;
- a benchmark exposing systematic failure of popular RAG pipelines;
- a method that optimizes evidence selection under realistic cost or latency;
- a theory or diagnostic framework for retrieval-generation mismatch.

## Baseline reminders

Include:

- BM25 or lexical retrieval;
- dense retrieval;
- rerank and no-rerank variants;
- long-context baseline;
- prompt-only baseline where relevant;
- strong commercial or open LLMs if feasible;
- ablations for chunk size, top-k, reranking, and context formatting.
