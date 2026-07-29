# Quickstart

This project is a Codex Skill for computer science paper novelty discovery.

## Engineering runtime

Create an editable environment and verify the installed package:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements-dev.lock
.venv/bin/python -m pip install --no-deps --no-build-isolation -e .
.venv/bin/shushu check
```

The lock file includes hashed runtime, test, and build dependencies. Regenerate it after a
dependency declaration changes (install `pip-tools` first if it is not already available):

```bash
.venv/bin/pip-compile pyproject.toml --extra dev --all-build-deps \
  --allow-unsafe --strip-extras --generate-hashes --output-file requirements-dev.lock
```

Start a complete P0–P9 run and ask for the deterministic next artifact:

```bash
run_dir=$(.venv/bin/shushu run "RAG citation robustness" --mode full)
.venv/bin/shushu next --run "$run_dir"
```

`next` never writes research content. Produce the requested artifact, then call it again. P3 uses
both `papers/fulltext.jsonl` and `papers/claims.jsonl`; later gates cross-check those claims against
lineage, idea, collision, reviewer, and report records.

Search and replay canonical records:

```bash
.venv/bin/shushu search "RAG evaluation" \
  --source arxiv --source openreview \
  --output retrieval/papers.jsonl
.venv/bin/shushu replay retrieval/papers.jsonl.manifest.json
```

File output automatically creates a hashed replay manifest and a durable failure JSONL. A partial
API outage remains visible rather than becoming an empty “no prior art” result.

Three complete offline-verifiable runs are included:

```bash
for run in examples/runs/*-known-scoop; do
  .venv/bin/shushu next --run "$run"
done
```

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

For a v0.2 run, validate the final manifest and every cross-artifact reference instead:

```bash
shushu report runs/example/report/manifest.json --run-dir runs/example
```

See [migration-v0.2.md](migration-v0.2.md) for the artifact conventions.
