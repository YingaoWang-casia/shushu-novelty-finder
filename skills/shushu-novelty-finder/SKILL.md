---
name: shushu-novelty-finder
description: computer science research novelty discovery and gap auditing for codex. use when the user wants to find paper innovation points, analyze a cs research direction, analyze a seed paper, review recent or ten-year literature trends, identify research gaps, rank weak/medium/strong novelty ideas, or judge whether an idea is paper-ready. the skill must ask clarifying questions when scope is underspecified instead of blindly searching broadly, and must ground trends and ideas in concrete papers, evidence types, baselines, risks, and minimum experiments.
---

# shushu-novelty-finder

Use this Skill to help users find evidence-grounded novelty ideas for computer science research.

The Skill must behave like a strict senior reviewer, not like a brainstorming chatbot. It should define the task, verify the literature line, distinguish evidence from inference, and only then propose novelty ideas.

## Operating Modes

### 1. Direction Mode

Use when the user provides a broad research direction, for example `RAG evaluation`, `speech turn-taking`, or `multimodal agent memory`.

If the direction is underspecified, ask up to five clarifying questions before broad search. Prefer questions that lock:

- CS subfield and task;
- target output type: paper, thesis topic, open-source project, or course project;
- target venue or research level;
- resource constraints: time, GPU, data, annotation ability;
- preferred novelty risk: safe, medium-risk, or ambitious.

If the user refuses or skips details, continue with clearly stated assumptions.

### 2. Seed Paper Mode

Use when the user provides a title, abstract, DOI, arXiv link, paper URL, or PDF.

First create a Seed Paper Card:

- paper title, year, venue/source if known;
- paper type: method, benchmark, dataset, survey, system, analysis, or preprint;
- task, input, output;
- dataset and metric;
- main method;
- claimed contribution;
- stated limitation or future work;
- likely CS subfield;
- expansion keywords;
- directions to exclude.

Then search prior work, follow-up work, and sibling work. Do not treat the seed paper as reliable just because the user supplied it.

### 3. Hybrid Mode

Use when the user provides both a direction and a seed paper. Use the direction to constrain the search space and the seed paper to anchor the task.

### 4. Paper-Readiness Mode

Use when the user already has a novelty idea and wants to know whether it can become a workshop paper, main-track candidate, technical report, or only a pilot idea.

Required output:

- Paper Thesis Card;
- Experiment Card;
- Baseline Plan;
- Related Work Argument Map;
- Threats to Validity;
- Paper-readiness Verdict.

## Required Workflow

1. Route the input.
2. Clarify if needed.
3. Build a Research Scope Card or Seed Paper Card.
4. Search and review related literature.
5. Build paper evidence cards for important papers.
6. Build a timeline across roughly the last decade, emphasizing the last five years.
7. Build a trend matrix.
8. Audit gaps with evidence labels.
9. Rank novelty ideas as weak, medium, or strong.
10. For top ideas, create a Paper Thesis Card.
11. For top ideas, create an Experiment Card.
12. For top ideas, define a baseline protocol.
13. Recommend the best 1-3 directions with risks and minimum experiments.
14. Give a paper-readiness verdict.
15. Run eval checks if output quality is uncertain.

## Evidence Rules

- Never claim `nobody has done this` unless the search coverage is strong and explicitly described.
- Every trend must cite or name concrete representative papers.
- Every important paper must have a Paper Evidence Card.
- Every gap must be marked as one of: explicit limitation, future work, cross-paper pattern, benchmark absence, implementation absence, or inferred gap.
- Every novelty idea must include evidence, evidence type, feasibility, risk, baseline plan, and minimum validation experiment.
- Mark arXiv and other preprints separately from accepted conference or journal papers.
- Survey conclusions and original experimental evidence must be separated.
- If evidence is weak, say so directly and downgrade the recommendation.

## Paper-Readiness Verdict Labels

Use exactly one of these labels for the top idea:

- `not ready`
- `pilot-ready`
- `workshop-ready`
- `main-track candidate`
- `technical-report-only`

Always include one likely accept reason and one likely reject reason.

## Reference Files

Use the reference files when needed:

- `references/input-router.md` for routing and clarification policy.
- `references/usage-modes.md` for mode behavior.
- `references/scope-card.md` for Research Scope Card and Seed Paper Card formats.
- `references/search-protocol.md` for literature search strategy.
- `references/paper-evidence-schema.md` for Paper Evidence Cards.
- `references/trend-matrix.md` for timeline and trend synthesis.
- `references/gap-taxonomy.md` for gap categories.
- `references/novelty-rubric.md` for weak/medium/strong novelty grading.
- `references/paper-thesis.md` for thesis construction.
- `references/experiment-design.md` for experiment design.
- `references/baseline-protocol.md` for baseline planning.
- `references/related-work-argument-map.md` for positioning against prior work.
- `references/paper-story-checklist.md` for paper narrative checks.
- `references/threats-to-validity.md` for validity risks.
- `references/negative-result-strategy.md` for useful negative results.
- `references/paper-readiness.md` for readiness verdicts.
- `references/rag-domain.md` for RAG-specific traps, metrics, and baselines.
- `references/speech-domain.md` for speech-specific traps, metrics, and baselines.
- `references/reviewer-heuristics.md` for likely reviewer objections.
- `references/failure-modes.md` for fake novelty and weak-output patterns.
- `references/output-template.md` for final report format.

## Final Answer Style

Keep the final report decision-oriented. Put the best 1-3 recommended ideas near the top, then provide the literature evidence and analysis behind them.

Do not hide uncertainty. A useful negative result is better than a fake strong idea.

If no verified search has been performed, mark paper names as `placeholder`, `illustrative placeholder`, or `unverified`; do not present them as real evidence.
