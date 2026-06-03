# shushu-novelty-finder

A Codex Skill for computer science paper novelty discovery.

This repository contains a Skill workflow for analyzing a computer science research direction or seed paper, reviewing related work, and producing evidence-grounded novelty candidates.

## Goal

The goal is to help users move from a vague research direction to a scoped research idea. The workflow emphasizes task definition, literature evidence, trend analysis, gap auditing, novelty ranking, and feasibility checking.

This is not a random paper idea generator. It should behave more like a strict senior reviewer: define the task first, verify the literature line, separate evidence from speculation, then recommend possible innovations.

## Main capabilities

- Route user input into Direction Mode, Seed Paper Mode, or Hybrid Mode.
- Ask clarifying questions when the research scope is too broad.
- Build Research Scope Cards and Seed Paper Cards.
- Select likely CS venue clusters instead of searching all fields.
- Review related work by prior work, follow-up work, and sibling work.
- Build a literature timeline and trend matrix.
- Classify research gaps by dataset, benchmark, metric, method, system, robustness, interpretability, and negative-result gaps.
- Rank novelty ideas as weak, medium, or strong.
- Attach evidence type, feasibility, risk, and minimum experiments to every idea.
- Detect fake gaps, scope drift, shallow novelty, and feasibility blindness.

## Workflow

1. Parse the user input.
2. Ask clarifying questions if the direction is too broad.
3. Build a research scope card.
4. Select likely CS venue clusters.
5. Review related papers by time stage.
6. Build a trend matrix.
7. Identify research gaps.
8. Rank novelty ideas as weak, medium, or strong.
9. Provide risks and minimum experiments.
10. Recommend the best 1-3 directions.

## Core rules

- If the scope is unclear, ask the user before broad search.
- If the user gives a seed paper, first parse the task, data, metric, method, and claim.
- Every trend must be supported by concrete paper names.
- Every gap must be marked as explicit limitation, future work, cross-paper pattern, benchmark absence, implementation absence, or inferred gap.
- Do not claim that nobody has done something without strong search evidence.
- Strong ideas must include failure risks and minimum validation experiments.
- Preprints must be marked separately from accepted conference or journal papers.
- Every recommended idea should include one main reason to accept and one main reason to reject.

## Repository layout

- `skills/shushu-novelty-finder/SKILL.md`
- `skills/shushu-novelty-finder/agents/openai.yaml`
- `skills/shushu-novelty-finder/references/input-router.md`
- `skills/shushu-novelty-finder/references/scope-card.md`
- `skills/shushu-novelty-finder/references/venue-map.md`
- `skills/shushu-novelty-finder/references/search-protocol.md`
- `skills/shushu-novelty-finder/references/trend-matrix.md`
- `skills/shushu-novelty-finder/references/gap-taxonomy.md`
- `skills/shushu-novelty-finder/references/novelty-rubric.md`
- `skills/shushu-novelty-finder/references/reviewer-heuristics.md`
- `skills/shushu-novelty-finder/references/failure-modes.md`
- `skills/shushu-novelty-finder/references/output-template.md`
- `examples/`

## Example prompt

```text
Use shushu-novelty-finder.
I want to find novelty ideas around RAG evaluation.
My constraints are 2-3 months, limited compute, and a paper-oriented project.
First lock the scope, then review related work and propose weak / medium / strong novelty ideas.
```

Or:

```text
Use shushu-novelty-finder.
Here is a seed paper: <title / abstract / link>.
Analyze what task it solves, review related work from the last decade, and propose weak / medium / strong novelty ideas.
```

## Philosophy

The Skill is designed to make research ideation more evidence-bound and less random. It cannot guarantee a publishable idea. It can help users avoid shallow novelty, fake gaps, unsupported claims, and ideas that sound strong but cannot be validated.
