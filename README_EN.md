![Shushu Novelty Finder](https://capsule-render.vercel.app/api?type=waving&height=260&color=0:0f172a,35:2563eb,70:7c3aed,100:ec4899&text=Shushu%20Novelty%20Finder&fontColor=ffffff&fontSize=48&fontAlignY=38&desc=Paper%20lineage%20first.%20Novelty%20ideas%20next.&descSize=18&descAlignY=58)

<div align="center">

# 🚀 Shushu Novelty Finder

**A Codex Skill for paper lineage mapping, novelty idea generation, and reviewer-style reasonableness auditing**

Understand the closest paper lineage first, then grow realistic paper ideas from evidence-backed literature gaps.

🌐 Language / 语言: [中文](README.md) | **English**

[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827?style=for-the-badge&logo=openai&logoColor=white)](skills/shushu-novelty-finder/SKILL.md)
[![Literature Lineage](https://img.shields.io/badge/Literature-Lineage-2563eb?style=for-the-badge)](examples/literature-lineage-mode.md)
[![Idea Generation](https://img.shields.io/badge/Idea-Generation-7c3aed?style=for-the-badge)](examples/idea-generation-mode.md)
[![Reviewer Audit](https://img.shields.io/badge/Reviewer-Audit-ec4899?style=for-the-badge)](skills/shushu-novelty-finder/references/idea-reasonableness-audit.md)
[![Star Welcome](https://img.shields.io/badge/Star-Welcome-ffd700?style=for-the-badge&logo=github)](https://github.com/YingaoWang-casia/shushu-novelty-finder)

⭐ **If this Skill is useful to you, a Star is welcome.**

[✨ What it does](#-what-it-does) · [🧭 Two core modes](#-two-core-modes) · [⚡ Quick start](#-quick-start) · [🛠️ Installation](#️-installation) · [📚 Examples](#-complete-input-examples) · [🧪 Output quality](#-output-quality-checks)

</div>

---

## ✨ What it does

Many answers to “help me find a paper idea” sound active, but actual paper writing often gets stuck on questions like:

- How did this research task evolve?
- Which papers are extremely similar to my idea?
- What is the concrete innovation point of each key paper?
- Which contributions are already saturated, and which gaps are still defensible?
- How is my idea different from the closest prior work?
- What minimum experiment should I run, and what results would support, weaken, or kill the idea?

`shushu-novelty-finder` is designed for this workflow. It is not only a brainstorming helper. It breaks a research idea into an auditable chain:

```text
research direction -> extremely similar papers -> per-paper innovation points -> trends and saturation -> gaps -> candidate ideas -> experiments and baselines -> reviewer objections -> continue or stop
```

For readability, this repository provides bilingual README files:

- Chinese version: [`README.md`](README.md)
- English version: [`README_EN.md`](README_EN.md)

---

## 🧭 Two core modes

| Mode | When to use it | Main outputs |
| --- | --- | --- |
| 🧾 **Literature Lineage Mode** | You want to understand the paper lineage, closest papers, and concrete contribution of each key work before generating ideas. | Task map, paper clusters, per-paper innovation cards, trend matrix, gap audit. |
| 💡 **Idea Generation Mode** | You already have a seed paper or direction and want paper-worthy novelty ideas. | Weak / medium / strong ideas, closest prior work, experiments, baselines, kill criteria. |

Recommended workflow:

```text
Use Literature Lineage Mode first to understand the direction,
then use Idea Generation Mode to generate ideas from defensible gaps.
```

---

## ⚡ Quick start

### Engineering CLI (v0.2 alpha)

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements-dev.lock
.venv/bin/python -m pip install --no-deps --no-build-isolation -e .
run_dir=$(.venv/bin/shushu run "RAG citation robustness" --mode full)
.venv/bin/shushu next --run "$run_dir"
```

`requirements-dev.lock` pins and verifies development and build dependencies. After changing
dependency declarations, regenerate it with
`.venv/bin/pip-compile pyproject.toml --extra dev --all-build-deps --allow-unsafe --strip-extras --generate-hashes --output-file requirements-dev.lock`;
do not edit the lock file manually.

### Effectiveness-claim status

<!-- EFFECTIVENESS_CLAIMS_START -->
There are no public comparative effectiveness claims. All 240 runs in the fixed 60-seed ×
4-system matrix and the two anonymous rater packs are hash-complete, but blind ratings by two
research-experienced reviewers and public aggregate results are pending. Until then, an LLM judge
cannot establish superiority over a baseline.
<!-- EFFECTIVENESS_CLAIMS_END -->

The release gate enforces this block. See [`evals/README.md`](evals/README.md) for the protocol and
[`docs/release-checklist.md`](docs/release-checklist.md) for the publication requirements. Version
changes are recorded in [`CHANGELOG.md`](CHANGELOG.md).

After installation, you can use it in Codex like this:

```text
Use shushu-novelty-finder.

Mode:
Literature Lineage first, then Idea Generation.

Direction:
organic reaction prediction + RAG + LLM reasoning

First map the closest-paper lineage of this direction:
- group papers by historical stage or methodological route;
- list the concrete innovation points of each key paper;
- specify task, input, output, datasets, metrics, and assumptions;
- identify saturated contributions and remaining defensible gaps.

Then generate paper-worthy ideas from those gaps:
- weak / medium / strong ranking;
- closest prior work for each idea;
- minimum experiments and baselines;
- reviewer objections;
- kill / continue criteria.
```

If you installed it locally with the short alias `idea`, you can also invoke it like this:

```text
$idea first map the paper lineage of organic reaction prediction + RAG + LLM reasoning, then suggest viable paper ideas
```

Three real-paper end-to-end prior-art controls for RAG, LoRA, and CLIP are documented in
[`examples/real-end-to-end-cases.md`](examples/real-end-to-end-cases.md). They exercise the
`downgrade/abandon` path and are not comparative-effectiveness evidence.
Their complete P0–P9 run trees, including real PDFs, page hashes, and manifests, are stored in
[`examples/runs/`](examples/runs/README.md).

---

## 🧾 Mode 1: Literature Lineage Mode

### When to use

Use this mode when you are not ready to generate ideas directly and first need to understand a research direction:

- what the current task is;
- how representative papers developed over time;
- what each paper actually contributed;
- which works are closest to your target direction;
- which innovation spaces are already occupied;
- which gaps may still be worth pursuing.

### Input template

```text
Use shushu-novelty-finder.

Mode:
Literature Lineage first.

Direction:
<your research direction>

Please first map the closest-paper lineage of this direction:
1. group papers by historical stage, method route, or task branch;
2. identify the most important and most similar papers in each group;
3. extract concrete innovation points for each paper, not just one-line summaries;
4. specify datasets, metrics, core assumptions, and limitations;
5. summarize saturated contributions and remaining defensible gaps;
6. do not generate ideas yet; first make the literature lineage clear.
```

### Expected output

```text
Scope And Task Map
- Core task
- Subtasks
- Input / output
- Standard datasets
- Standard metrics
- Typical baselines

Closest-Paper Clusters
- Cluster name
- Why this cluster is close
- Representative papers
- Shared assumptions
- Saturated contribution
- Open gap

Per-Paper Innovation Cards
- Paper
- Year / venue
- Relationship to your direction
- Innovation point 1 / 2 / 3
- Dataset and metric
- What it solved
- What it left open
- What idea space it blocks
- What idea space it leaves open

Trend Matrix
Gap Audit
Lineage Verdict
```

Full example: [`examples/literature-lineage-mode.md`](examples/literature-lineage-mode.md)

---

## 💡 Mode 2: Idea Generation Mode

### When to use

Use this mode when you already have a direction or seed paper and want to know what can be done next:

- extend a paper into a new project;
- judge whether an idea has already been solved;
- rank novelty as weak / medium / strong;
- define minimum experiments, baselines, and likely reviewer objections;
- decide whether the idea is `pilot-ready`, `workshop-ready`, or a `main-track candidate`.

### Input template

```text
Use shushu-novelty-finder.

Mode:
Idea Generation.

Seed paper or direction:
<paper title / abstract / arXiv / DOI / URL / your research direction>

Goal:
Generate paper-worthy novelty ideas based on this paper or direction.

Please include:
1. weak / medium / strong novelty ideas;
2. closest prior work for each idea;
3. why it is not already solved;
4. novelty mechanism;
5. minimum experiment and strong baseline;
6. reviewer objections;
7. kill / continue criteria;
8. paper-readiness verdict.
```

### Expected output

```text
Closest-Prior Snapshot
Executive Recommendation
Novelty Candidates
Idea Reasonableness Audit
Paper Type Routing
Paper Thesis Card
Experiment Card
Baseline Decision
Reviewer Objection Pre-Mortem
Kill / Continue Criteria
Paper-readiness Verdict
```

Full example: [`examples/idea-generation-mode.md`](examples/idea-generation-mode.md)

---

## 🛠️ Installation

### Method 1: Standard installation

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

Restart Codex and trigger it with:

```text
Use shushu-novelty-finder.
```

### Method 2: Install as the `$idea` short alias

If you want to invoke it directly with `$idea`, copy the Skill directory as `idea`:

Windows PowerShell:

```powershell
git clone https://github.com/YingaoWang-casia/shushu-novelty-finder.git
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codex\skills\idea" | Out-Null
Copy-Item -Recurse -Force "shushu-novelty-finder\skills\shushu-novelty-finder\*" "$env:USERPROFILE\.codex\skills\idea\"
```

Then edit `%USERPROFILE%\.codex\skills\idea\SKILL.md` and change the top-level name to:

```yaml
name: idea
```

Restart Codex and use:

```text
$idea help me map the literature lineage first, then generate paper ideas
```

### Method 3: Update to the latest version

If you already installed it, copy over the latest files:

```powershell
git pull
Copy-Item -Recurse -Force "skills\shushu-novelty-finder\*" "$env:USERPROFILE\.codex\skills\idea\"
```

If you use the standard name, replace `idea` with `shushu-novelty-finder`.

---

## 📚 Complete input examples

### Example A: Review first, then generate ideas

```text
$idea

Mode:
Literature Lineage first, then Idea Generation.

Direction:
RAG evaluation for long-form question answering with citations

Please first map the closest-paper lineage of this direction:
- how RAG evaluation evolved from QA metrics to citation faithfulness;
- what each key paper contributed;
- which benchmarks / metrics are already covered;
- which gaps may still support a paper.

Then generate 3-5 viable ideas from those gaps, with minimum experiments, baselines, and kill criteria.
```

### Example B: Extend a seed paper

```text
$idea

Mode:
Idea Generation.

Seed paper:
<paste paper title, abstract, arXiv link, or PDF content>

Goal:
I want to build a workshop or main-track candidate based on this paper.

Please output:
- contributions already occupied by this paper;
- closest prior work;
- remaining weak / medium / strong ideas;
- novelty mechanism for each idea;
- minimum experiments and baselines;
- likely reviewer objections;
- what results would support, weaken, or kill each idea.
```

### Example C: Literature lineage only

```text
$idea

Mode:
Literature Lineage only.

Direction:
speech turn-taking evaluation for full-duplex voice agents

Only map the paper lineage. Do not generate ideas yet.
Focus on:
- how the task definition changed;
- extremely similar paper clusters;
- per-paper innovation points;
- datasets and metrics;
- the most saturated and most missing parts.
```

---

## 🧪 Output quality checks

A good output should include at least:

- ✅ clear input mode;
- ✅ scope / task map;
- ✅ real paper names, or explicit `candidate / unverified` labels;
- ✅ concrete innovation points for each key paper in lineage mode;
- ✅ a trend matrix, not just a paper list;
- ✅ evidence-labeled gaps;
- ✅ closest prior work for every idea;
- ✅ novelty mechanism;
- ✅ minimum experiment and baseline;
- ✅ reviewer objection;
- ✅ kill / continue criteria;
- ✅ no casual claim that “nobody has done this.”

Full checklist: [`evals/checks/output-checklist.md`](evals/checks/output-checklist.md)

---

## 🗂️ Repository structure

```text
shushu-novelty-finder/
|- skills/shushu-novelty-finder/
|  |- SKILL.md
|  |- agents/openai.yaml
|  `- references/
|- docs/
|  |- quickstart.md
|  `- usage.md
|- examples/
|  |- literature-lineage-mode.md
|  `- idea-generation-mode.md
|- evals/
`- scripts/
```

---

## 🔗 Links

- 🌐 [中文 README](README.md)
- 🧠 [Main Skill](skills/shushu-novelty-finder/SKILL.md)
- 📖 [Usage Guide](docs/usage.md)
- ⚡ [Quickstart](docs/quickstart.md)
- 🧾 [Literature Lineage Example](examples/literature-lineage-mode.md)
- 💡 [Idea Generation Example](examples/idea-generation-mode.md)
- 🧪 [Output Checklist](evals/checks/output-checklist.md)

---

## ⭐ Star

If this Skill helps you understand a research direction faster and find more defensible paper ideas, a Star is welcome ⭐.

It also helps signal that the project is useful and worth maintaining.

![Footer](https://capsule-render.vercel.app/api?type=waving&height=120&section=footer&color=0:ec4899,45:7c3aed,100:2563eb)
