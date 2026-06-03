# shushu-novelty-finder

A Codex Skill for computer science paper novelty discovery.

This repository contains a Skill workflow for analyzing a computer science research direction or seed paper, reviewing related work, and producing evidence-grounded novelty candidates.

## Goal

The goal is to help users move from a vague research direction to a scoped research idea. The workflow emphasizes task definition, literature evidence, trend analysis, gap auditing, novelty ranking, and feasibility checking.

This is not a random paper idea generator. It should behave more like a strict senior reviewer: define the task first, verify the literature line, separate evidence from speculation, then recommend possible innovations.

## Workflow

1. Parse the user input.
2. Ask clarifying questions if the direction is too broad.
3. Build a research scope card.
4. Review related papers by time stage.
5. Build a trend matrix.
6. Identify research gaps.
7. Rank novelty ideas as weak, medium, or strong.
8. Provide risks and minimum experiments.

## Core rules

- If the scope is unclear, ask the user before broad search.
- If the user gives a seed paper, first parse the task, data, metric, method, and claim.
- Every trend must be supported by concrete paper names.
- Every gap must be marked as explicit, cross-paper, or inferred.
- Do not claim that nobody has done something without strong search evidence.
- Strong ideas must include failure risks and minimum validation experiments.

## Repository layout

- `skills/shushu-novelty-finder/SKILL.md`
- `skills/shushu-novelty-finder/agents/openai.yaml`
- `skills/shushu-novelty-finder/references/`
- `examples/`

## Example prompt

```text
Use shushu-novelty-finder.
I want to find novelty ideas around real-time speech turn-taking for voice agents.
My constraints are two months, limited compute, and a paper-oriented project.
```

Or:

```text
Use shushu-novelty-finder.
Here is a seed paper: <title / abstract / link>.
Analyze what task it solves, review related work from the last decade, and propose weak / medium / strong novelty ideas.
```

## Philosophy

The Skill is designed to make research ideation more evidence-bound and less random. It cannot guarantee a publishable idea. It can help users avoid shallow novelty, fake gaps, and unsupported claims.
