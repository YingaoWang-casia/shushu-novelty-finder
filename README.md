# shushu-novelty-finder

Paste a CS research direction or seed paper.
Get a literature-backed novelty audit, trend matrix, and paper-readiness verdict.

输入一个计算机研究方向或种子论文，输出近十年趋势、研究空白、创新点分级和可投稿性判断。

`shushu-novelty-finder` is a Codex Skill for auditing computer science paper ideas. It helps a student, new researcher, or engineering-oriented researcher turn a vague direction into an evidence-bound research scope, gap analysis, novelty ranking, and paper-readiness decision.

It is designed to behave like a strict CS paper idea auditor / paper-readiness reviewer: lock the task first, check the literature line, separate evidence from inference, then recommend ideas with baselines, risks, and minimum experiments.

This is a prompt-first Skill workflow. It can guide literature search, organize evidence, and enforce paper-readiness checks. The included scripts are lightweight helpers, not a full automatic literature-mining system.

## Who It Is For

- CS students looking for a paper-oriented project direction.
- Research beginners who need help moving from "interesting topic" to scoped research task.
- Engineering researchers who want to test whether an implementation idea has paper potential.
- Users who already have a seed paper and need prior work, follow-up work, sibling work, and gap analysis.

## What It Is Not

- Not a paper summarizer.
- Not a random innovation-point generator.
- Not a replacement for an advisor, reviewer, or literature-search by a domain expert.
- Not a tool that can prove novelty without search coverage and concrete evidence.
- Not a complete citation-graph crawler or fully automatic systematic review engine.

## Core Workflow

1. Route the input into Direction Mode, Seed Paper Mode, Hybrid Mode, or Paper-Readiness Mode.
2. Lock the research scope before broad search.
3. Build a Research Scope Card or Seed Paper Card.
4. Guide and organize prior work, follow-up work, and sibling work search.
5. Build Paper Evidence Cards that bind papers to claims.
6. Build a Literature Timeline for roughly the last decade, with extra attention to the last five years.
7. Build a Trend Matrix that separates task shift, method shift, dataset/metric shift, and open gaps.
8. Audit gaps with evidence labels.
9. Rank novelty candidates as weak, medium, or strong.
10. Attach paper evidence, evidence type, feasibility, risks, baselines, and minimum experiments.
11. Produce a paper-readiness verdict: `not ready`, `pilot-ready`, `workshop-ready`, `main-track candidate`, or `technical-report-only`.

## Usage Modes

### Direction Mode

Use when you only have a direction, such as `RAG evaluation`, `speech turn-taking`, `LLM-as-a-Judge`, or `multimodal agent memory`.

The Skill first checks whether the direction is too broad. If so, it asks up to five scope-locking questions before searching.

### Seed Paper Mode

Use when you provide a paper title, abstract, arXiv link, DOI, URL, or PDF.

The Skill first creates a Seed Paper Card, then searches or plans prior work, follow-up work, and sibling work. It does not treat the seed paper as authoritative just because the user supplied it.

### Paper-Readiness Mode

Use when you already have an idea and want to know whether it can become a paper.

The Skill produces a Paper Thesis Card, Experiment Card, Baseline Plan, Related Work Argument Map, Threats to Validity, and a paper-readiness verdict.

## Shortest Prompt

```text
Use shushu-novelty-finder.
Direction: RAG evaluation.
```

## Complete Prompt

```text
Use shushu-novelty-finder.
Direction: RAG evaluation.
Goal: paper-oriented research project.
Constraints: 2 months, limited compute.
First lock the scope, then produce a literature-backed novelty audit and paper-readiness verdict.
```

For a seed paper:

```text
Use shushu-novelty-finder.
Seed paper: <title / abstract / arXiv / DOI / PDF>.
Goal: find paper-worthy extension ideas.
First build a Seed Paper Card, then search prior work, follow-up work, and sibling work.
Rank ideas as weak / medium / strong and give a paper-readiness verdict.
```

## Output Examples

- [RAG evaluation output](examples/rag-evaluation-output.md)
- [Seed paper output](examples/seed-paper-output.md)
- [Bad output vs good output](examples/bad-output-vs-good-output.md)
- [RAG evaluation request](examples/rag-evaluation-request.md)
- [Seed paper request](examples/seed-paper-request.md)

## Installation

```bash
git clone https://github.com/YingaoWang-casia/shushu-novelty-finder.git
mkdir -p ~/.codex/skills
cp -R shushu-novelty-finder/skills/shushu-novelty-finder ~/.codex/skills/
```

Then use it in Codex:

```text
Use shushu-novelty-finder.
Direction: RAG evaluation.
Goal: paper-oriented research project.
Constraints: 2 months, limited compute.
First lock the scope, then produce a literature-backed novelty audit and paper-readiness verdict.
```

## Repository Layout

- `skills/shushu-novelty-finder/SKILL.md` - main Skill instructions.
- `skills/shushu-novelty-finder/agents/openai.yaml` - agent configuration.
- `skills/shushu-novelty-finder/references/` - workflow references and domain packs.
- `docs/usage.md` - detailed usage guide.
- `examples/` - sample requests and full output examples.
- `evals/` - lightweight quality checks and eval cases.
- `scripts/normalize_papers.py` - converts JSONL paper records into Paper Evidence Cards.
- `scripts/search_arxiv.py` - lightweight arXiv API search helper that emits candidate preprint records.

## Current Capabilities

- Routes input into Direction, Seed Paper, Hybrid, and Paper-Readiness modes.
- Builds Research Scope Cards, Seed Paper Cards, Paper Thesis Cards, and Experiment Cards.
- Uses Paper Evidence Cards instead of title-only citations.
- Separates evidence status from evidence role so candidate papers are not mistaken for verified support.
- Guides literature timeline and trend matrix construction.
- Labels gap evidence as explicit limitation, future work, cross-paper pattern, benchmark absence, implementation absence, or inferred gap.
- Ranks ideas as weak / medium / strong with feasibility, risks, baselines, and minimum experiments.
- Marks preprints separately from accepted papers.
- Provides RAG and speech domain packs for common fake novelty traps, metrics, and minimum baselines.
- Includes eval checklists for catching unsupported novelty claims and missing paper-readiness evidence.

## Roadmap

- Add more domain packs for LLM agents, multimodal learning, ML systems, security, and data engineering.
- Add richer paper metadata normalization for Semantic Scholar, OpenAlex, and DBLP inputs.
- Add automatic report validation against the eval checklist.
- Add more full examples for Seed Paper Mode and Paper-Readiness Mode.
- Add venue-specific readiness rubrics for ACL, EMNLP, SIGIR, CHI, ICML, NeurIPS, ICLR, KDD, and systems venues.

## Philosophy

Good research ideation is not just "find something new." It is a chain of scoped claims, literature evidence, reviewer objections, feasible experiments, and honest uncertainty. This Skill is built to make that chain visible.
