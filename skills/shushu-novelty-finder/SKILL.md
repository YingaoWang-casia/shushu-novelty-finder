---
name: shushu-novelty-finder
description: computer science research lineage mapping, novelty discovery, and idea stress-testing for codex. use when the user wants to map extremely similar papers in a research direction, extract each paper's innovation points, generate paper innovation ideas, analyze whether an idea is reasonable, find CS research gaps, analyze a research direction or seed paper, review recent or ten-year literature trends, rank weak/medium/strong novelty ideas, or judge whether an idea is paper-ready. the skill supports two primary outputs: literature-lineage mode for detailed paper-context mapping, and idea-generation mode for concrete novelty candidates. it must ground claims in papers and ask clarifying questions when scope is underspecified instead of blindly searching broadly.
---

# shushu-novelty-finder

Use this Skill to help users first understand the paper lineage of a computer science research direction, then generate evidence-grounded novelty ideas and judge whether those ideas are reasonable.

The Skill must behave like a strict senior reviewer who is also trying to help the user find a viable paper direction. It should not stop at criticism, and it should not stop at brainstorming. It must first map the closest paper lineage when the user asks for context, then create candidate innovation points, then stress-test them against the literature, feasibility, baselines, reviewer objections, and falsifiable experiments.

## Core Contract

For most full research requests, the Skill should produce three linked outputs:

1. **Closest-paper lineage**: a detailed map of extremely similar papers, grouped by stage or method family, with each paper's concrete innovation points, assumptions, datasets, metrics, limitations, and relationship to the user's direction.
2. **Novelty candidates**: concrete idea options ranked as weak / medium / strong.
3. **Reasonableness audit**: a careful judgment of whether each top idea is logically defensible, experimentally testable, and worth pursuing.

A useful answer should make the user better at deciding what to do next: pursue, narrow, verify, downgrade, pivot, or stop.

## Operating Modes

### 0. Literature Lineage Mode

Use when the user asks to first understand the direction, paper context, closest prior work, very similar papers, research lineage, or "what has been done". Trigger phrases include:

- "先梳理论文脉络"
- "极度相似的论文"
- "这个方向当前任务"
- "把每篇论文创新点列出来"
- "先综述，再给 idea"
- "literature lineage"
- "closest papers"
- "survey this direction before ideas"

Required output:

- Scope and task map: task definition, input, output, standard datasets, metrics, deployment setting, and what counts as real progress.
- Closest-paper clusters: group papers by stage, method route, benchmark route, or assumption.
- Per-paper innovation card for each important paper:
  - title, year, venue/source, URL/DOI/arXiv if known;
  - task and setting;
  - core innovation points, numbered and concrete;
  - method/data/metric/system contribution type;
  - datasets and metrics;
  - what it solves;
  - what it leaves open;
  - relation to the user's target paper or direction: ancestor / closest prior / sibling / follow-up / contrary evidence / benchmark.
- Trend matrix and saturation map.
- Gap audit with evidence labels.
- If the user explicitly asks for ideas in the same request, continue into Idea Generation Mode after the lineage.

Do not output only a paper list. Convert papers into a lineage: what changed from paper to paper, which assumptions became dominant, which contributions are saturated, and which gaps remain defensible.

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

### 5. Idea Generation Mode

Use when the user asks for innovation points, paper ideas, extension directions, "how to do idea", or "what can I write based on this paper/direction".

Required output:

- A concise lineage summary or closest-prior-work snapshot unless a detailed lineage was already provided in the same answer.
- Weak / medium / strong novelty candidates.
- For each candidate: core claim, novelty mechanism, closest prior work, why it is not already solved, minimum experiment, baseline plan, risks, reasonableness verdict, and kill / continue criteria.
- For the top 1-3 ideas: Paper Thesis Card, Experiment Card, reviewer objection pre-mortem, paper-readiness verdict.

## Required Workflow

1. Route the input.
2. Clarify if needed.
3. Narrow broad directions before search.
4. Build a Research Scope Card or Seed Paper Card.
5. Decide whether the request needs Literature Lineage Mode, Idea Generation Mode, or both.
6. Search and review related literature.
7. Build Paper Evidence Cards for important papers.
8. If Lineage Mode is requested, build closest-paper clusters and per-paper innovation cards before proposing ideas.
9. Build a Claim-Evidence Map for top claims.
10. Build a timeline across roughly the last decade, emphasizing the last five years.
11. Build a trend matrix and saturation map.
12. Audit gaps with evidence labels.
13. If Idea Generation Mode is requested, generate concrete novelty candidates from the lineage, gaps, limitations, trend shifts, and user constraints.
14. Rank novelty ideas as weak, medium, or strong.
15. Run an Idea Reasonableness Audit for each top idea.
16. Route each top idea to a paper type and fallback type.
17. For top ideas, create a Paper Thesis Card.
18. For top ideas, create an Experiment Card.
19. For top ideas, use the baseline decision tree to define minimum and strong baselines.
20. Run reviewer objection pre-mortem.
21. Apply kill / continue criteria.
22. Recommend the best 1-3 directions with the strongest reason for and against each.
23. Give a paper-readiness verdict.
24. Run eval checks if output quality is uncertain.

## Idea Generation Rules

- Always output concrete idea candidates unless the user explicitly asks only for literature review.
- Do not output ideas as slogans. Each idea needs a claim, novelty mechanism, closest prior work, minimum experiment, and reasonableness verdict.
- Generate at least one safe idea, one medium-risk idea, and one ambitious idea when the scope allows it.
- Make ideas falsifiable: state what result would support, weaken, or kill the idea.
- If all ideas are weak, say so and explain what evidence or scope change could make them stronger.

## Evidence Rules

- Never claim `nobody has done this` unless the search coverage is strong and explicitly described.
- When the user asks for closest-paper lineage, every important paper must include explicit innovation points, not only a summary.
- In Lineage Mode, separate each paper's actual contribution from your inferred gap. Do not turn inferred gaps into verified author claims.
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

Choose the answer order from the user's request:

- If the user asks to "先梳理", "先综述", "论文脉络", or "极度相似论文", start with Literature Lineage Mode. Do not put ideas first.
- If the user asks only for "idea", "创新点", or "怎么做", start with the best 1-3 recommended ideas, but include a closest-prior-work snapshot.
- If the user asks for both, output Part A: literature lineage, then Part B: idea generation and reasonableness audit.

Do not hide uncertainty. A useful negative result is better than a fake strong idea.

If no verified search has been performed, mark paper names as `placeholder`, `illustrative placeholder`, or `unverified`; do not present them as real evidence.
