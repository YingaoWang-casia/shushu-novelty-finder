# RAG Domain Guide

Use this guide for retrieval augmented generation topics. It helps prevent fake novelty by forcing the Skill to separate retrieval, generation, citation, robustness, and deployment claims.

## Subdirections

- retrieval quality
- reranking
- answer faithfulness
- citation correctness
- robustness
- long-context comparison
- domain-specific RAG
- agentic RAG

## Metrics

- recall@k
- precision@k
- nDCG
- answer F1
- faithfulness
- citation precision
- latency
- cost

## Fake Novelty

- claiming a new benchmark without checking existing benchmarks
- mixing retrieval failure and generation failure
- only using answer accuracy
- comparing only weak baselines
- calling a pipeline a new method

## Minimum Baselines

- lexical retrieval
- dense retrieval
- reranker vs no reranker
- prompt-only / closed-book baseline
- long-context baseline when relevant

## Scope-Lock Questions

Ask these when `RAG evaluation` is too broad:

1. Are we evaluating retrieval quality, answer faithfulness, citation correctness, robustness, latency/cost, or end-to-end utility?
2. Is the target setting open-domain QA, domain-specific QA, long-document QA, enterprise knowledge base, or agentic tool use?
3. Does the user want a benchmark, metric, protocol, analysis paper, or system paper?
4. What compute, annotation, and dataset constraints exist?
5. Which baselines are mandatory for the claim?

## Strong Idea Pattern

A stronger idea usually shows that conclusions change when retrieval support, citation support, and answer utility are evaluated separately.

Required evidence:

- verified benchmark baselines;
- explicit comparison to accepted papers when possible;
- preprints marked separately;
- a baseline suite that includes retrieval, generation, and closed-book or long-context alternatives;
- a falsification result that would weaken the claim.
