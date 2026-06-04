![Shushu Novelty Finder](https://capsule-render.vercel.app/api?type=waving&height=260&color=0:0f172a,35:2563eb,70:7c3aed,100:ec4899&text=Shushu%20Novelty%20Finder&fontColor=ffffff&fontSize=48&fontAlignY=38&desc=Generate%20research%20ideas.%20Stress-test%20them%20like%20a%20top-tier%20reviewer.&descSize=18&descAlignY=58)

<div align="center">

# shushu-novelty-finder

**A Codex Skill for generating CS paper innovation ideas, then judging whether they actually stand up.**

输入一个计算机研究方向或种子论文，输出候选创新点、文献证据、合理性推敲、实验方案和可投稿性判断。

[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827?style=for-the-badge&logo=openai&logoColor=white)](skills/shushu-novelty-finder/SKILL.md)
[![Research Ideas](https://img.shields.io/badge/Research-Idea%20Generator-2563eb?style=for-the-badge)](#what-it-does)
[![Reviewer Mode](https://img.shields.io/badge/Reviewer-Reasonableness%20Audit-7c3aed?style=for-the-badge)](skills/shushu-novelty-finder/references/idea-reasonableness-audit.md)
[![Paper Ready](https://img.shields.io/badge/Paper-Readiness%20Verdict-ec4899?style=for-the-badge)](#paper-readiness-verdicts)

</div>

---

## Why This Exists

Most research-idea prompts have the same problem: they sound confident, but they do not tell you whether the idea is actually new, feasible, defensible, or publishable.

`shushu-novelty-finder` is built for the moment when you have a direction like:

```text
RAG evaluation
LLM-as-a-Judge
speech turn-taking
multimodal agent memory
```

and you want something more useful than a list of fashionable topics.

It should help you answer:

- What are the possible innovation points?
- Which ones are weak, medium, or strong?
- What prior work is closest?
- Why might the idea be unreasonable?
- What experiment would support, weaken, or kill it?
- Is this a course project, workshop paper, main-track candidate, or just not ready?

---

## What It Does

<table>
<tr>
<td width="50%">

### Generates Ideas

- turns vague directions into scoped research tasks;
- extracts gaps from literature trends and seed papers;
- proposes safe, medium-risk, and ambitious directions;
- ranks ideas as weak / medium / strong;
- suggests the best paper type for each idea.

</td>
<td width="50%">

### Stress-Tests Ideas

- names closest prior work;
- checks the novelty mechanism;
- separates evidence from inference;
- designs minimum experiments and baselines;
- predicts reviewer objections;
- gives kill / continue criteria.

</td>
</tr>
</table>

---

## The Core Loop

| Stage | What Happens | Output |
|---:|---|---|
| 01 | Scope the user's direction or seed paper | Research Scope Card / Seed Paper Card |
| 02 | Inspect prior, follow-up, and sibling work | Paper Evidence Cards |
| 03 | Bind papers to concrete claims | Claim-Evidence Map |
| 04 | Extract trends, gaps, and weak signals | Literature Timeline + Gap Audit |
| 05 | Generate candidate innovation points | Weak / Medium / Strong idea set |
| 06 | Stress-test whether each idea stands up | Idea Reasonableness Audit |
| 07 | Design the minimum decisive experiment | Baselines + falsification plan |
| 08 | Pre-mortem likely reviewer objections | Accept / reject reasons |
| 09 | Decide what to do next | Pursue / narrow / verify / downgrade / stop |

The Skill is not just trying to say something is novel. It tries to make the whole reasoning chain visible.

---

## Example Prompt

```text
Use shushu-novelty-finder.
Direction: RAG evaluation.
Goal: paper-oriented research project.
Constraints: 2 months, limited compute.
First lock the scope, then generate novelty ideas and audit whether each idea is reasonable.
```

For a seed paper:

```text
Use shushu-novelty-finder.
Seed paper: <paper title / abstract / arXiv / DOI / PDF>.
Goal: find paper-worthy extension ideas.
First build a Seed Paper Card, then search prior work, follow-up work, and sibling work.
Rank ideas as weak / medium / strong, judge whether each top idea is reasonable, and give a paper-readiness verdict.
```

---

## Output Preview

```text
Recommended idea:
Novelty level: medium
Reasonableness verdict: reasonable but underspecified
Paper-readiness verdict: pilot-ready
Best paper type: evaluation / benchmark paper
Closest prior work: <paper names>
Novelty mechanism: new evaluation target
Strongest reason for: exposes a measurable failure mode not covered by current benchmarks
Strongest reason against: may collapse into a narrow benchmark variant
Minimum experiment: compare strong baselines on citation-level faithfulness under controlled retrieval noise
Kill condition: if current metrics already predict the target failure reliably
Next decision: verify closest prior work and run a 2-day pilot
```

---

## Reasonableness Audit

Every top idea should be pushed through this checklist:

```text
Idea:
One-sentence thesis:
Novelty mechanism:
Why now:
Assumptions:
Evidence that supports the idea:
Evidence that weakens the idea:
Closest prior work:
Difference from closest prior work:
Who would care:
Minimum experiment:
What result would support it:
What result would weaken it:
What result would kill it:
Reasonableness verdict:
Strongest reason for:
Strongest reason against:
Decision: pursue / narrow / verify / downgrade / pivot / stop
```

See [`idea-reasonableness-audit.md`](skills/shushu-novelty-finder/references/idea-reasonableness-audit.md) for the full rubric.

---

## Install

### macOS / Linux

```bash
git clone https://github.com/YingaoWang-casia/shushu-novelty-finder.git
mkdir -p ~/.codex/skills
cp -R shushu-novelty-finder/skills/shushu-novelty-finder ~/.codex/skills/
```

### Windows PowerShell

```powershell
git clone https://github.com/YingaoWang-casia/shushu-novelty-finder.git
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force "shushu-novelty-finder\skills\shushu-novelty-finder" "$env:USERPROFILE\.codex\skills\"
```

Restart Codex or open a new Codex session, then trigger the Skill by name:

```text
Use shushu-novelty-finder.
```

Check installation:

```text
~/.codex/skills/shushu-novelty-finder/SKILL.md
%USERPROFILE%\.codex\skills\shushu-novelty-finder\SKILL.md
```

---

## Paper-Readiness Verdicts

| Verdict | Meaning |
|---|---|
| `not ready` | The idea is too vague, unsupported, infeasible, or likely already solved. |
| `pilot-ready` | Worth a small experiment before investing serious time. |
| `workshop-ready` | Has a plausible scoped contribution if evidence and execution are solid. |
| `main-track candidate` | Has strong novelty, evidence, baselines, and reviewer defense potential. |
| `technical-report-only` | Useful engineering or negative result, but not clearly a research paper. |

---

## Repository Map

```text
shushu-novelty-finder/
├─ skills/shushu-novelty-finder/
│  ├─ SKILL.md                         # main skill contract
│  ├─ agents/openai.yaml               # Codex skill metadata
│  └─ references/                      # rubrics, templates, domain packs
├─ docs/usage.md                       # detailed usage guide
├─ examples/                           # prompts and sample outputs
├─ evals/                              # quality checks and eval cases
└─ scripts/                            # lightweight paper-record helpers
```

---

## Useful Links

- [Main Skill](skills/shushu-novelty-finder/SKILL.md)
- [Usage Guide](docs/usage.md)
- [Output Template](skills/shushu-novelty-finder/references/output-template.md)
- [Idea Reasonableness Audit](skills/shushu-novelty-finder/references/idea-reasonableness-audit.md)
- [Output Checklist](evals/checks/output-checklist.md)
- [Verified RAG Mini Audit](examples/verified-rag-mini-audit.md)

---

## Philosophy

Good research ideation is not just "find something new."

It is a chain:

```text
scoped problem -> literature evidence -> candidate idea -> reasonableness audit -> experiment -> reviewer defense -> decision
```

This Skill is built to generate that chain, then test whether it holds.

![Footer](https://capsule-render.vercel.app/api?type=waving&height=120&section=footer&color=0:ec4899,45:7c3aed,100:2563eb)
