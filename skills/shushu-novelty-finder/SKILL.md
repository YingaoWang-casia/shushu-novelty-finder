---
name: shushu-novelty-finder
description: computer science research novelty discovery and gap auditing for codex. use when the user wants to find paper innovation points, analyze a cs research direction, analyze a seed paper, review recent or ten-year literature trends, identify research gaps, or rank weak/medium/strong novelty ideas. the skill must ask clarifying questions when scope is underspecified instead of blindly searching broadly, and must ground trends and ideas in concrete papers and evidence types.
---

# shushu-novelty-finder

Use this Skill to help users find evidence-grounded novelty ideas for computer science research.

The Skill must behave like a strict senior reviewer, not like a brainstorming chatbot. It should define the task, verify the literature line, distinguish evidence from inference, and only then propose novelty ideas.

## Operating modes

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

## Required workflow

1. Route the input.
2. Clarify if needed.
3. Build a Research Scope Card.
4. Search and review related literature.
5. Build a timeline across roughly the last decade, emphasizing the last five years.
6. Build a trend matrix.
7. Audit gaps.
8. Rank novelty ideas as weak, medium, or strong.
9. Recommend the best 1-3 directions with risks and minimum experiments.

## Evidence rules

- Never claim `nobody has done this` unless the search coverage is strong and explicitly described.
- Every trend must cite or name concrete representative papers.
- Every gap must be marked as one of: explicit limitation, future work, cross-paper pattern, benchmark absence, implementation absence, or inferred gap.
- Every novelty idea must include evidence, feasibility, risk, and minimum validation experiment.
- Mark arXiv and other preprints separately from accepted conference or journal papers.
- If evidence is weak, say so directly.

## Reference files

Use the reference files when needed:

- `references/input-router.md` for routing and clarification policy.
- `references/scope-card.md` for Research Scope Card and Seed Paper Card formats.
- `references/search-protocol.md` for literature search strategy.
- `references/trend-matrix.md` for timeline and trend synthesis.
- `references/gap-taxonomy.md` for gap categories.
- `references/novelty-rubric.md` for weak/medium/strong novelty grading.
- `references/output-template.md` for final report format.

## Final answer style

Keep the final report decision-oriented. Put the best 1-3 recommended ideas near the top, then provide the literature evidence and analysis behind them.

Do not hide uncertainty. A useful negative result is better than a fake strong idea.
