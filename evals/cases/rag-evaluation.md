# Eval Case: RAG Evaluation

## Input

```text
Use shushu-novelty-finder.
Direction: RAG evaluation.
Goal: paper-oriented project.
Constraints: 2 months, limited compute.
```

## Expected Behavior

The Skill should not search all RAG papers blindly. It should first narrow the scope into one or more of:

- retrieval quality;
- reranking;
- answer faithfulness;
- citation correctness;
- robustness;
- long-context comparison;
- domain-specific RAG;
- agentic RAG;
- production cost and latency.

If the scope remains too broad, the Skill should ask at most 5 questions. If the user does not answer, it should continue with explicit assumptions.

## Required Output Checks

- has input mode: Direction Mode / Research Mode or Paper Mode
- has Research Scope Card
- has concrete paper names or marks placeholder / candidate / unverified
- has Paper Evidence Cards
- has Claim-Evidence Map for the top claim
- venue clusters include NLP and IR where relevant
- Trend Matrix is not just a paper list
- gaps have evidence labels
- novelty candidates are ranked weak / medium / strong
- at least one idea is downgraded because of feasibility, weak evidence, or overlap risk
- top idea includes paper type routing
- top idea includes Paper Thesis Card or clear thesis claim
- top idea includes minimum experiment and baseline decision
- top idea includes reviewer objection pre-mortem
- top idea includes kill / continue criteria
- paper-readiness verdict uses an allowed label

## Failure Signs

- claims that no RAG evaluation benchmark exists without evidence
- mixes retrieval failure, generation failure, citation failure, and agent failure without separation
- gives strong novelty without baselines or metrics
- compares only against weak baselines
- ignores latency and cost when the claim is deployment-oriented
- treats arXiv preprints as accepted papers
- treats candidate papers as verified support
- calls a pipeline a new method without isolating what is new
- has no reviewer objection section
- has no condition for downgrading or killing the idea

## Passing Pattern

A passing output can say: `Current confidence is weak because the literature search is incomplete; this is pilot-ready, not workshop-ready yet.` Honest uncertainty is better than unsupported novelty.
