# Shushu Novelty Finder

**A Codex Skill for mapping research-paper lineages, extracting prior-paper innovation points, and generating defensible CS paper ideas.**

[中文](README_ZH.md) | **English**

[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827?style=for-the-badge&logo=openai&logoColor=white)](skills/shushu-novelty-finder/SKILL.md)
[![Literature Lineage](https://img.shields.io/badge/Literature-Lineage-2563eb?style=for-the-badge)](examples/literature-lineage-mode.md)
[![Idea Generation](https://img.shields.io/badge/Idea-Generation-7c3aed?style=for-the-badge)](examples/idea-generation-mode.md)
[![Reasonableness Audit](https://img.shields.io/badge/Reviewer-Audit-ec4899?style=for-the-badge)](skills/shushu-novelty-finder/references/idea-reasonableness-audit.md)

`shushu-novelty-finder` is designed for two common research workflows:

1. **Literature Lineage Mode**: first map the extremely similar papers in a direction, explain the task history, and extract each paper's concrete innovation points.
2. **Idea Generation Mode**: based on a seed paper or user direction, generate weak / medium / strong novelty candidates and stress-test whether each idea can become a paper.

It is meant to behave like a strict senior reviewer who still wants to help you find a viable direction: it checks closest prior work, evidence, baselines, risks, reviewer objections, and kill / continue criteria.

## What It Does

| Need | Output |
| --- | --- |
| Understand a direction before proposing ideas | Scope and Task Map, Closest-Paper Clusters, Per-Paper Innovation Cards |
| Know what each similar paper actually contributed | Per-paper innovation points, contribution type, datasets, metrics, limitations |
| Find defensible gaps | Trend Matrix, Saturation Map, Gap Audit with evidence labels |
| Generate paper ideas | Weak / Medium / Strong Novelty Candidates |
| Decide whether an idea stands up | Idea Reasonableness Audit, baselines, reviewer objections, kill criteria |
| Turn an idea into a paper plan | Paper Thesis Card, Experiment Card, Paper-readiness Verdict |

## Mode 1: Literature Lineage

Use this when you want a detailed paper-context map first.

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

Expected output shape:

```text
Scope And Task Map
Closest-Paper Clusters
Per-Paper Innovation Cards
Literature Timeline
Trend Matrix
Gap Audit
Lineage Verdict
```

Full example: [examples/literature-lineage-mode.md](examples/literature-lineage-mode.md)

## Mode 2: Idea Generation

Use this when you want concrete innovation points based on a paper or direction.

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

Expected output shape:

```text
Closest-Prior Snapshot
Executive Recommendation
Novelty Candidates
Idea Reasonableness Audit
Paper Thesis Card
Experiment Card
Baseline Decision
Reviewer Objection Pre-Mortem
Kill / Continue Criteria
Paper-readiness Verdict
```

Full example: [examples/idea-generation-mode.md](examples/idea-generation-mode.md)

## Install

macOS / Linux:

```bash
git clone https://github.com/YingaoWang-casia/shushu-novelty-finder.git
mkdir -p ~/.codex/skills
cp -R shushu-novelty-finder/skills/shushu-novelty-finder ~/.codex/skills/
```

Windows PowerShell:

```powershell
git clone https://github.com/YingaoWang-casia/shushu-novelty-finder.git
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force "shushu-novelty-finder\skills\shushu-novelty-finder" "$env:USERPROFILE\.codex\skills\"
```

Restart Codex or open a new Codex session, then trigger the Skill by name:

```text
Use shushu-novelty-finder.
```

## Repository Map

```text
shushu-novelty-finder/
|- skills/shushu-novelty-finder/
|  |- SKILL.md
|  |- agents/openai.yaml
|  `- references/
|- docs/
|- examples/
|- evals/
`- scripts/
```

## Useful Links

- [Main Skill](skills/shushu-novelty-finder/SKILL.md)
- [Usage Guide](docs/usage.md)
- [Quickstart](docs/quickstart.md)
- [Output Template](skills/shushu-novelty-finder/references/output-template.md)
- [Literature Lineage Example](examples/literature-lineage-mode.md)
- [Idea Generation Example](examples/idea-generation-mode.md)
- [Output Checklist](evals/checks/output-checklist.md)

## Philosophy

Good research ideation is not just "find something new". It is a chain:

```text
scope -> closest papers -> per-paper innovation points -> gaps -> candidate ideas -> audit -> experiments -> decision
```

This Skill is built to generate that chain, then test whether it holds.
