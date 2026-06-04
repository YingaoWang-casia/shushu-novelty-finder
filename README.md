# shushu-novelty-finder

A Codex Skill for generating and stress-testing CS paper innovation ideas.

输入一个计算机研究方向或种子论文，输出候选创新点、文献证据、合理性推敲和可投稿性判断。

## What It Does

`shushu-novelty-finder` should not only review literature. It should:

1. lock the research scope;
2. inspect prior / follow-up / sibling work;
3. generate concrete novelty candidates;
4. rank them as weak / medium / strong;
5. audit whether each top idea is reasonable;
6. name closest prior work, baselines, risks, reviewer objections, and kill / continue criteria;
7. give a paper-readiness verdict.

## Activate In Codex

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

Restart Codex, then prompt:

```text
Use shushu-novelty-finder.
Direction: RAG evaluation.
Goal: paper-oriented research project.
First lock the scope, then generate novelty ideas and audit whether each idea is reasonable.
```

For details, see [`docs/usage.md`](docs/usage.md) and [`skills/shushu-novelty-finder/SKILL.md`](skills/shushu-novelty-finder/SKILL.md).
