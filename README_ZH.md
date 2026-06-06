# Shushu Novelty Finder

**一个面向 Codex 的研究论文脉络梳理、相似论文创新点提取、论文 idea 生成与合理性审查 Skill。**

**中文** | [English](README.md)

[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827?style=for-the-badge&logo=openai&logoColor=white)](skills/shushu-novelty-finder/SKILL.md)
[![论文脉络](https://img.shields.io/badge/Literature-Lineage-2563eb?style=for-the-badge)](examples/literature-lineage-mode.md)
[![创新点生成](https://img.shields.io/badge/Idea-Generation-7c3aed?style=for-the-badge)](examples/idea-generation-mode.md)
[![合理性审查](https://img.shields.io/badge/Reviewer-Audit-ec4899?style=for-the-badge)](skills/shushu-novelty-finder/references/idea-reasonableness-audit.md)

`shushu-novelty-finder` 现在明确支持两种主要输出：

1. **论文脉络模式**：先梳理某个方向里极度相似的论文整体脉络，把每篇关键论文的具体创新点、数据集、指标、假设、局限和剩余空间讲清楚。
2. **创新点生成模式**：根据一篇种子论文或用户想做的方向，输出 weak / medium / strong 创新点，并逐条审查这个 idea 是否真的站得住。

它不是简单头脑风暴，而是像一个严格但愿意帮你找方向的 senior reviewer：检查最近工作、文献证据、baseline、风险、审稿人反驳和 kill / continue 条件。

## 它能做什么

| 需求 | 输出 |
| --- | --- |
| 先理解一个方向 | Scope and Task Map、Closest-Paper Clusters、Per-Paper Innovation Cards |
| 看每篇相似论文到底新在哪里 | 每篇论文的创新点、贡献类型、数据集、指标、局限 |
| 找真正还能做的 gap | Trend Matrix、Saturation Map、带证据标签的 Gap Audit |
| 生成论文创新点 | Weak / Medium / Strong Novelty Candidates |
| 判断 idea 是否合理 | Idea Reasonableness Audit、baseline、审稿人反驳、kill criteria |
| 把 idea 变成论文计划 | Paper Thesis Card、Experiment Card、Paper-readiness Verdict |

## 模式 1：论文脉络模式

当你想先把方向和相似论文搞清楚时，用这个模式。

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

预期输出结构：

```text
Scope And Task Map
Closest-Paper Clusters
Per-Paper Innovation Cards
Literature Timeline
Trend Matrix
Gap Audit
Lineage Verdict
```

完整示例：[examples/literature-lineage-mode.md](examples/literature-lineage-mode.md)

## 模式 2：创新点生成模式

当你已经有一篇论文或一个方向，想要具体可做的论文创新点时，用这个模式。

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

预期输出结构：

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

完整示例：[examples/idea-generation-mode.md](examples/idea-generation-mode.md)

## 安装

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

重启 Codex 或打开新的 Codex 会话，然后用名称触发：

```text
Use shushu-novelty-finder.
```

## 仓库结构

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

## 相关链接

- [Main Skill](skills/shushu-novelty-finder/SKILL.md)
- [Usage Guide](docs/usage.md)
- [Quickstart](docs/quickstart.md)
- [Output Template](skills/shushu-novelty-finder/references/output-template.md)
- [论文脉络示例](examples/literature-lineage-mode.md)
- [创新点生成示例](examples/idea-generation-mode.md)
- [Output Checklist](evals/checks/output-checklist.md)

## 设计理念

好的研究 ideation 不是简单地“找一个新东西”，而是一条能被审查的链：

```text
研究范围 -> 极度相似论文 -> 每篇论文创新点 -> gap -> 候选 idea -> 合理性审查 -> 实验 -> 决策
```

这个 Skill 的目标，就是先生成这条链，再测试它到底站不站得住。
