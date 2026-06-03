# Bad Output vs Good Output

This example shows why the Skill must act like a paper idea auditor rather than a generic prompt pack.

## User Input

```text
I want to find novelty ideas around RAG evaluation.
```

## Bad Output

```text
RAG evaluation is underexplored. You can build a new benchmark. This is strong novelty.
```

Why this is bad:

- no scope lock;
- no concrete papers;
- no evidence type;
- no baseline;
- no falsifiable claim;
- overclaims novelty.

More specifically, it never says whether `RAG evaluation` means retrieval quality, answer faithfulness, citation correctness, robustness, latency, cost, long-context comparison, or agentic RAG. It also claims strength without showing a paper timeline, benchmark overlap search, or a minimum experiment.

## Good Output

```text
Mode: Research Mode

Scope:
RAG evaluation for LLM question answering with citations. Exclude retriever training, generic long-context evaluation, and broad agent evaluation.

Evidence plan:
1. Search accepted NLP / IR / LLM systems papers and benchmark papers from the last 10 years.
2. Build Paper Evidence Cards for retrieval metrics, faithfulness metrics, citation correctness, and end-to-end answer utility.
3. Mark arXiv preprints separately and do not treat them as accepted papers.
4. Run contrary-evidence search for existing benchmarks that already separate these axes.

Candidate gap:
RAG evaluations may mix retrieval quality, citation correctness, and answer utility into one end-to-end score.

Evidence type:
Cross-paper pattern plus benchmark absence. Current confidence is weak until the literature matrix is populated.

Medium idea:
Create a multi-axis RAG evaluation protocol that reports retrieval support, citation support, answer utility, latency, and cost separately, then test whether system rankings change across axes.

Minimum experiment:
Compare lexical retrieval, dense retrieval, reranker vs no reranker, prompt-only / closed-book, and long-context baseline if relevant on one shared QA dataset.

Reject risk:
If existing accepted benchmark papers already separate these axes with comparable baselines, downgrade the idea to a reproduction, analysis report, or technical note.
```

The good output is better because it locks scope, states the evidence plan, avoids unsupported novelty claims, and gives a falsifiable experiment.
