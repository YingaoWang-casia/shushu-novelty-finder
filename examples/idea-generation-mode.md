# Idea Generation Mode Example

This mode is for users who already have a paper or direction and want concrete paper-worthy innovation points.

## Example Input

```text
Use shushu-novelty-finder.

Mode:
Idea Generation.

Seed paper:
Towards Knowledge-and-Data-Driven Organic Reaction Prediction:
RAG-Enhanced and Reasoning-Powered Hybrid System with LLMs

Goal:
Based on this paper and its closest prior work, output paper-worthy innovation points.

Please include:
- weak / medium / strong novelty candidates;
- closest prior work for each idea;
- why each idea is not already solved;
- minimum experiment and baselines;
- reviewer objections;
- kill / continue criteria;
- paper-readiness verdict.
```

## Example Output

```text
Closest-Prior Snapshot:
Seed paper or direction: RAG-enhanced and reasoning-powered organic reaction prediction.
Closest prior work: Molecular Transformer-style reaction prediction; chemistry pretrained models; ChemCrow-style tool use; ChemRAG-style chemistry RAG; Reaction-Thinker-style RAG + CoT + tuning.
What those papers already did: product prediction, sequence/graph modeling, chemistry tool orchestration, retrieval augmentation, reasoning data, and tuning/RL for reaction prediction.
What cannot be claimed as new: "using RAG for reaction prediction", "using LLM reasoning for reaction prediction", or "using similar reactions as context" without a sharper contribution.
Open space for ideas: evidence faithfulness, mechanism-aware retrieval, counterfactual retrieval robustness, and better evaluation metrics.
Evidence status: partial until recent follow-up work is verified.

Executive Recommendation:
Recommended idea: Evidence-Faithful Reaction RAG.
Novelty level: medium to strong.
Reasonableness verdict: reasonable but underspecified.
Paper-readiness verdict: pilot-ready.
Best paper type: method + evaluation paper.
Fallback paper type: analysis / benchmark paper.
Why this is the best option: it turns the explainability claim of RAG-based reaction LLMs into a falsifiable evaluation target.
Evidence basis: RAG + reasoning systems already exist, but evidence-faithfulness and counterfactual retrieval audits are usually underdeveloped.
Strongest reason for: a model can be accurate while giving unfaithful chemistry rationales; this matters for scientific trust.
Strongest reason against: if perturbing retrieval evidence barely changes predictions, the method contribution may collapse into an analysis-only paper.
Minimum experiment: compare correct retrieval, random retrieval, and hard-negative retrieval on a small USPTO subset, measuring prediction accuracy and rationale-evidence alignment.
Baseline plan: no-retrieval LLM, vanilla RAG LLM, Reaction-Thinker-style prompt, mechanism-aware retrieval variant.
Main risk: lack of reliable labels for mechanism/evidence alignment.
Likely accept reason: exposes and measures a concrete failure mode in current reasoning-based reaction prediction.
Likely reject reason: evaluation may be too small or too dependent on LLM-judged rationales.
Continue / narrow / downgrade / kill: continue if counterfactual retrieval changes both predictions and rationales in chemically meaningful ways; downgrade if effects are weak; kill if current systems already solve this with published metrics.

Novelty Candidates:

Idea: Counterfactual Evidence Audit for Reaction RAG
Novelty level: medium.
Novelty mechanism: new evaluation target and stress-test protocol.
Core claim: RAG reaction predictors should be evaluated by whether their predictions and explanations depend on correct retrieved chemical evidence.
Closest prior work: RAG-based reaction prediction and chemistry RAG benchmarks.
Why it is not already solved: standard exact match and fingerprint similarity do not test evidence causality.
Minimum experiment: perturb top-k retrieved examples and measure prediction/rationale stability.
Baseline plan: no retrieval, random retrieval, similarity retrieval, hard-negative retrieval.
Reasonableness verdict: reasonable but underspecified.

Idea: Mechanism-Aware Retrieval For Reaction Prediction
Novelty level: medium.
Novelty mechanism: retrieval criterion changes from surface similarity to reaction-center and bond-change consistency.
Core claim: mechanism-consistent retrieval improves OOD robustness more than SMILES similarity retrieval.
Closest prior work: graph-to-sequence reaction models, RAG reaction predictors.
Why it is not already solved: existing retrieval often focuses on similarity, not explicit mechanism consistency.
Minimum experiment: evaluate rare reaction classes or scaffold splits with mechanism-aware reranking.
Baseline plan: BM25/dense retrieval, fingerprint retrieval, vanilla similar-case retrieval.
Reasonableness verdict: high-risk but worth piloting.

Idea: ReactionEval-R For Reasoning-Based Reaction Prediction
Novelty level: medium.
Novelty mechanism: benchmark / metric refinement.
Core claim: exact match misses product equivalence, mechanism plausibility, and evidence support.
Closest prior work: standard USPTO evaluation, chemistry RAG benchmarks, RAG reaction prediction papers.
Why it is not already solved: most reaction predictors still optimize product-level metrics rather than reasoning/evidence quality.
Minimum experiment: annotate a focused error set and compare exact match, fingerprint similarity, expert plausibility, and evidence support.
Baseline plan: Molecular Transformer, ChemFormer/T5Chem, vanilla RAG LLM, seed-paper model if reproducible.
Reasonableness verdict: reasonable but annotation-heavy.

Idea Reasonableness Audit:
Idea: Evidence-Faithful Reaction RAG.
One-sentence thesis: Organic reaction LLMs should not only predict products correctly, but also ground each reasoning step in retrieved chemical evidence that causally supports the prediction.
Novelty mechanism: evaluation target + method constraint.
Why now: RAG + CoT systems are emerging, making explanation faithfulness a natural next bottleneck.
Assumptions: retrieved examples can be labeled or scored for chemical relevance; counterfactual retrieval can expose causal reliance.
Evidence that supports the idea: RAG systems often require faithfulness checks; reaction prediction metrics do not capture rationale quality.
Evidence that weakens the idea: strong models may rely mostly on internal knowledge, reducing the value of retrieval audits.
Closest prior work: RAG-enhanced reaction prediction systems.
Difference from closest prior work: focuses on whether retrieved evidence causally supports reasoning, not only whether RAG improves accuracy.
Who would care: ML-for-chemistry researchers, chemists using LLM assistants, benchmark builders.
Minimum experiment: 500-1000 reaction samples with correct/hard-negative/random retrieval conditions.
What result would support it: correct evidence improves both accuracy and rationale alignment, while hard negatives expose meaningful failures.
What result would weaken it: evidence changes rationales but not predictions or chemical validity.
What result would kill it: existing methods already include robust counterfactual evidence-faithfulness evaluation.
Decision: pursue a pilot before committing to a full method paper.

Paper Thesis Card:
Working title: Evidence-Faithful Retrieval-Augmented Reasoning for Organic Reaction Prediction.
Paper type: method + evaluation.
Core claim: mechanism-aware and evidence-faithful retrieval improves the reliability of LLM-based reaction prediction under retrieval noise and OOD reaction settings.
What existing work assumes: retrieved similar reactions and generated rationales improve interpretability.
What breaks that assumption: generated reasoning can be fluent but not causally supported by retrieved evidence.
What evidence supports the claim: counterfactual retrieval tests, alignment metrics, OOD split results.
What reviewers may reject: weak annotation protocol, insufficient baselines, or unclear difference from existing RAG reaction predictors.

Experiment Card:
Claim: evidence-faithful retrieval improves reaction prediction reliability.
Independent variable: retrieval condition and evidence-linking constraint.
Dependent variable: exact match, fingerprint similarity, rationale-evidence alignment, counterfactual consistency.
Datasets: USPTO-50K subset, rare-class split, optional seed-paper dataset.
Metrics: exact match, FTS, invalid SMILES, evidence relevance, rationale faithfulness.
Baselines: no retrieval, vanilla RAG, similarity retrieval, mechanism-aware retrieval, seed-paper system if available.
Ablations: remove evidence links, remove mechanism reranker, replace top-k evidence with hard negatives.
Robustness checks: reaction class split, low-frequency reactions, noisy retrieval.
Falsification result: no difference between correct and corrupted retrieval, or existing baseline already passes the faithfulness test.
```
