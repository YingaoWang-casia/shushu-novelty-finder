# RAG Domain Guide

Use for retrieval augmented generation topics.

Subdirections: retrieval quality, reranking, answer faithfulness, citation correctness, robustness, long-context comparison, domain-specific RAG, agentic RAG.

Metrics: recall@k, precision@k, nDCG, answer F1, faithfulness, citation precision, latency, cost.

Fake novelty patterns:

- claims a new benchmark without checking existing benchmarks;
- mixes retrieval failure and generation failure;
- reports only answer accuracy;
- compares only with weak baselines;
- calls an ordinary pipeline a new method.

Minimum baselines: lexical retrieval, dense retrieval, reranker versus no reranker, prompt-only or closed-book baseline, long-context baseline when relevant.

Strong idea pattern: show that conclusions change when retrieval support, citation support, and answer utility are evaluated separately.
