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
