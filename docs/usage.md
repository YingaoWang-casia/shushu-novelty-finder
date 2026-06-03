# Usage Guide

This guide explains how to use `shushu-novelty-finder` as a CS paper idea auditor rather than a generic brainstorming prompt.

The Skill should always prefer a scoped, evidence-bound answer over a long list of plausible but unsupported ideas.

## 1. Direction Mode

Use Direction Mode when the user only has a research direction, for example:

```text
RAG evaluation
speech turn-taking
LLM-as-a-Judge
multimodal agent memory
```

The Skill must first decide whether the direction is too broad. If it is too broad, ask at most 5 clarifying questions before broad search. Good questions lock:

- subfield and concrete task;
- target output: workshop paper, main-track paper, technical report, thesis topic, or project;
- resource constraints: time, compute, data, annotation budget;
- target venue family or review standard;
- novelty appetite: safe, medium-risk, or ambitious.

If the user does not answer, continue with explicit assumptions and mark the uncertainty in the Research Scope Card.

Expected Direction Mode output:

```text
Mode:
Research Scope Card:
Search Plan:
Literature Timeline:
Trend Matrix:
Gap Audit:
Novelty Candidates:
Paper-readiness Verdict:
Next Action:
```

## 2. Seed Paper Mode

Use Seed Paper Mode when the user gives a paper title, abstract, arXiv link, DOI, URL, or PDF.

The Skill must first create a Seed Paper Card:

```text
Title:
Year:
Venue/source:
Paper type:
Task:
Input:
Output:
Dataset:
Metric:
Main method:
Claimed contribution:
Limitations:
Expansion keywords:
Excluded directions:
```

Only after that should it search:

- prior work: what the paper builds on;
- follow-up work: what cited, extended, reproduced, or challenged it;
- sibling work: papers solving the same task with different assumptions, methods, data, or metrics.

The seed paper is an anchor, not proof. If the seed paper is a preprint, survey, benchmark, dataset, method, or system paper, mark that status and adjust the evidence role.

## 3. Hybrid Mode

Use Hybrid Mode when the user gives both a direction and a seed paper.

The direction limits the search space. The paper locks the task boundary.

Example:

```text
Use shushu-novelty-finder.
Direction: RAG evaluation for citation correctness.
Seed paper: <paper title and abstract>.
Goal: find a workshop-ready extension.
```

Hybrid Mode should avoid two failure modes:

- following the seed paper so narrowly that no adjacent gaps are considered;
- using the broad direction so loosely that the seed paper no longer constrains the task.

## 4. Paper-Readiness Mode

Use Paper-Readiness Mode when the user already has an idea and wants to know whether it can become a paper.

Required output:

```text
Paper Thesis Card
Experiment Card
Baseline Plan
Related Work Argument Map
Threats to Validity
Paper-readiness Verdict
```

The verdict must use one of these labels:

- `not ready`
- `pilot-ready`
- `workshop-ready`
- `main-track candidate`
- `technical-report-only`

The Skill should explain both why a reviewer might accept the idea and why a reviewer might reject it.

## 5. Output Levels

The user can request different depths.

```text
Quick Mode: 只要 top ideas 和 next action
Research Mode: 要 timeline / trend matrix / gap audit
Paper Mode: 要 thesis / experiment / baseline / validity / readiness
```

### Quick Mode

Use when the user needs fast triage. It should still include scope, evidence status, risk, and next action. It must not invent strong novelty without literature evidence.

### Research Mode

Use when the user wants a real novelty audit. It should include a timeline, trend matrix, gap evidence labels, and weak / medium / strong idea ranking.

### Paper Mode

Use when the user wants to write or test a paper. It should include thesis, experiments, baselines, ablations, robustness checks, falsification results, threats to validity, and a readiness verdict.

## Evidence Discipline

Every important paper should be represented as a Paper Evidence Card. Every gap should have an evidence type. Every top idea should include the minimum experiment that could falsify it.

If the Skill uses placeholders because no real search was performed, it must explicitly mark them as `illustrative placeholder` or `unverified`.
