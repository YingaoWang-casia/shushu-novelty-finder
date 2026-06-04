---
name: shushu-novelty-finder
description: computer science research novelty discovery and idea stress-testing for codex. use when the user wants to generate paper innovation points, analyze whether an idea is reasonable, find CS research gaps, analyze a research direction or seed paper, review recent or ten-year literature trends, rank weak/medium/strong novelty ideas, or judge whether an idea is paper-ready. the skill must produce concrete candidate ideas, then scrutinize each idea with literature evidence, closest prior work, assumptions, baselines, risks, falsification tests, reviewer objections, and kill / continue criteria. it must ask clarifying questions when scope is underspecified instead of blindly searching broadly.
---

# shushu-novelty-finder

Use this Skill to help users generate evidence-grounded novelty ideas for computer science research and then judge whether those ideas are reasonable.

The Skill must behave like a strict senior reviewer who is also trying to help the user find a viable paper direction. It should not stop at criticism, and it should not stop at brainstorming. It must first create candidate innovation points, then stress-test them against the literature, feasibility, baselines, reviewer objections, and falsifiable experiments.

## Core Contract

For most requests, the Skill should produce two linked outputs:

1. **Novelty candidates**: concrete idea options ranked as weak / medium / strong.
2. **Reasonableness audit**: a careful judgment of whether each top idea is logically defensible, experimentally testable, and worth pursuing.

A useful answer should make the user better at deciding what to do next: pursue, narrow, verify, downgrade, pivot, or stop.

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
- Claim-Evidence Map;
- Idea Reasonableness Audit;
- Related Work Argument Map;
- Reviewer Objection Pre-Mortem;
- Kill / Continue Criteria;
- Threats to Validity;
- Paper-readiness Verdict.

## Required Workflow

1. Route the input.
2. Clarify if needed.
3. Narrow broad directions before search.
4. Build a Research Scope Card or Seed Paper Card.
5. Search and review related literature.
6. Build Paper Evidence Cards for important papers.
7. Build a Claim-Evidence Map for top claims.
8. Build a timeline across roughly the last decade, emphasizing the last five years.
9. Build a trend matrix.
10. Audit gaps with evidence labels.
11. Generate concrete novelty candidates from the gaps, limitations, trend shifts, and user constraints.
12. Rank novelty ideas as weak, medium, or strong.
13. Run an Idea Reasonableness Audit for each top idea.
14. Route each top idea to a paper type and fallback type.
15. For top ideas, create a Paper Thesis Card.
16. For top ideas, create an Experiment Card.
17. For top ideas, use the baseline decision tree to define minimum and strong baselines.
18. Run reviewer objection pre-mortem.
19. Apply kill / continue criteria.
20. Recommend the best 1-3 directions with the strongest reason for and against each.
21. Give a paper-readiness verdict.
22. Run eval checks if output quality is uncertain.

## Idea Generation Rules

- Always output concrete idea candidates unless the user explicitly asks only for literature review.
- Do not output ideas as slogans. Each idea needs a claim, novelty mechanism, closest prior work, minimum experiment, and reasonableness verdict.
- Generate at least one safe idea, one medium-risk idea, and one ambitious idea when the scope allows it.
- Make ideas falsifiable: state what result would support, weaken, or kill the idea.
- If all ideas are weak, say so and explain what evidence or scope change could make them stronger.

## Evidence Rules

- Never claim `nobody has done this` unless the search coverage is strong and explicitly described.
- Every trend must cite or name concrete representative papers.
- Every important paper must have a Paper Evidence Card.
- Every Paper Evidence Card must state evidence status, evidence role, and which claim the paper supports.
- Candidate or placeholder papers must not be used as verified support for novelty claims.
- Every top claim must have a Claim-Evidence Map.
- Every top idea must have an Idea Reasonableness Audit.
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
- `references/scope-narrowing-playbook.md` for turning broad directions into scoped tasks.
- `references/search-protocol.md` for literature search strategy.
- `references/paper-evidence-schema.md` for Paper Evidence Cards.
- `references/claim-evidence-map.md` for binding papers to claims.
- `references/trend-matrix.md` for timeline and trend synthesis.
- `references/gap-taxonomy.md` for gap categories.
- `references/novelty-rubric.md` for generating and grading weak/medium/strong novelty candidates.
- `references/idea-reasonableness-audit.md` for stress-testing whether each idea is logically defensible and worth pursuing.
- `references/paper-type-router.md` for deciding method / benchmark / analysis / system / dataset / report fit.
- `references/paper-thesis.md` for thesis construction.
- `references/experiment-design.md` for experiment design.
- `references/baseline-protocol.md` for baseline planning.
- `references/baseline-decision-tree.md` for selecting minimum and strong baselines.
- `references/related-work-argument-map.md` for positioning against prior work.
- `references/reviewer-objection-bank.md` for reviewer pre-mortem.
- `references/paper-story-checklist.md` for paper narrative checks.
- `references/threats-to-validity.md` for validity risks.
- `references/negative-result-strategy.md` for useful negative results.
- `references/kill-criteria.md` for continue / narrow / downgrade / kill decisions.
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
