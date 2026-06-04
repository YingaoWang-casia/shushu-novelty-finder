# Usage Guide

This guide explains how to use `shushu-novelty-finder` as a CS paper idea generator and reasonableness auditor.

The Skill should produce concrete innovation-point candidates, then carefully judge whether each idea is reasonable, feasible, evidence-backed, and paper-worthy. It should prefer scoped, evidence-bound, decision-useful answers over long lists of plausible but unsupported ideas.

## 0. Activate The Skill In Codex

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
Direction: RAG evaluation.
Goal: paper-oriented research project.
First lock the scope, then generate novelty ideas and audit whether each idea is reasonable.
```

Check installation:

```text
~/.codex/skills/shushu-novelty-finder/SKILL.md
%USERPROFILE%\.codex\skills\shushu-novelty-finder\SKILL.md
```

## 1. Direction Mode

Use when the user only has a research direction, for example:

```text
RAG evaluation
speech turn-taking
LLM-as-a-Judge
multimodal agent memory
```

If the direction is too broad, ask at most 5 clarifying questions. Lock subfield, task, input, output, dataset, metric, constraints, and target paper type before broad search.

Expected output:

```text
Mode:
Research Scope Card:
Scope narrowing assumptions:
Paper Evidence Cards:
Claim-Evidence Map:
Literature Timeline:
Trend Matrix:
Gap Audit:
Novelty Candidates:
Idea Reasonableness Audit:
Paper Type Routing:
Baseline Decision:
Reviewer Objection Pre-Mortem:
Kill / Continue Criteria:
Paper-readiness Verdict:
Next Action:
```

## 2. Seed Paper Mode

Use when the user gives a paper title, abstract, arXiv link, DOI, URL, or PDF.

First create a Seed Paper Card:

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

Then search or plan:

- prior work: what the paper builds on;
- follow-up work: what cited, extended, reproduced, or challenged it;
- sibling work: papers solving the same task with different assumptions, methods, data, or metrics;
- contrary evidence: work that may already solve the proposed extension.

The Skill should then generate extension ideas and audit whether each extension is actually different from prior work.

## 3. Hybrid Mode

Use when the user gives both a direction and a seed paper. The direction limits the search space. The paper locks the task boundary.

```text
Use shushu-novelty-finder.
Direction: RAG evaluation for citation correctness.
Seed paper: <paper title and abstract>.
Goal: find a workshop-ready extension.
```

## 4. Paper-Readiness Mode

Use when the user already has an idea and wants to know whether it can become a paper.

Required output:

```text
Paper Thesis Card
Experiment Card
Baseline Decision
Claim-Evidence Map
Idea Reasonableness Audit
Paper Type Routing
Related Work Argument Map
Reviewer Objection Pre-Mortem
Kill / Continue Criteria
Threats to Validity
Paper-readiness Verdict
```

Allowed reasonableness verdicts:

- `not reasonable yet`
- `weak but useful`
- `reasonable but underspecified`
- `reasonable`
- `high-risk but worth piloting`

Allowed paper-readiness verdicts:

- `not ready`
- `pilot-ready`
- `workshop-ready`
- `main-track candidate`
- `technical-report-only`

## 5. Output Levels

```text
Quick Mode: top ideas, reasonableness verdict, key evidence status, next action, and kill / continue checkpoint
Research Mode: timeline / trend matrix / gap audit / novelty candidates / claim-evidence map / reasonableness audit
Paper Mode: thesis / experiment / baseline / reviewer objections / validity / readiness
```

## Evidence Discipline

Every important paper should be represented as a Paper Evidence Card. Every important claim should have a Claim-Evidence Map. Every top idea should include the minimum experiment that could falsify it.

Every recommended idea should include the strongest reason for and strongest reason against pursuing it. If the idea is not reasonable yet, say so directly and explain what must be verified or narrowed.

If the Skill uses placeholders because no real search was performed, it must explicitly mark them as `illustrative placeholder`, `candidate`, or `unverified`.

Candidate or placeholder papers cannot be used as verified support for novelty claims.
