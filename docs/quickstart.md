# Quickstart

This project is a Codex Skill for computer science paper novelty discovery.

## Install

Clone the repository and copy the Skill directory into your Codex skills directory.

```bash
git clone https://github.com/YingaoWang-casia/shushu-novelty-finder.git
mkdir -p ~/.codex/skills
cp -R shushu-novelty-finder/skills/shushu-novelty-finder ~/.codex/skills/
```

Restart Codex or start a new session.

## Quick prompt

```text
Use shushu-novelty-finder.

Direction:
RAG evaluation for LLM question answering.

Constraints:
- paper-oriented project
- 2-3 months
- limited compute
- medium-risk novelty

Please run Research Mode first. If the scope is too broad, ask clarifying questions before searching.
```

## Literature Lineage prompt

Use this when you want the Skill to first map the closest papers and their innovation points.

```text
Use shushu-novelty-finder.

Mode:
Literature Lineage first.

Direction:
organic reaction prediction + RAG + LLM reasoning

Please first梳理这个方向极度相似论文的整体脉络:
- group papers by historical stage or method route;
- list each important paper's concrete innovation points;
- explain task, input, output, datasets, metrics, and assumptions;
- mark what has become saturated and what remains open;
- do not propose ideas until the lineage and gap audit are complete.
```

## Idea Generation prompt

Use this when you already have a seed paper or direction and want concrete innovation points.

```text
Use shushu-novelty-finder.

Mode:
Idea Generation.

Seed paper:
<title, abstract, arXiv, DOI, URL, or PDF>

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

## Seed paper prompt

```text
Use shushu-novelty-finder.

Seed paper:
<title, abstract, or link>

Goal:
Find evidence-grounded weak / medium / strong novelty ideas.

Please first build a Seed Paper Card, then review prior work, follow-up work, and sibling work.
```

## Paper Mode prompt

```text
Use shushu-novelty-finder.

I want a paper-ready plan, not only ideas.
For the top ideas, include:
- Paper Thesis Card
- Experiment Card
- Baseline Card
- Related Work Argument Map
- Threats Card
- Paper-readiness verdict
```

## Validate a report

If you save an output report as Markdown, run:

```bash
python scripts/validate_report.py report.md
python scripts/validate_report.py report.md --paper-mode
```
