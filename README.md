![Shushu Novelty Finder](https://capsule-render.vercel.app/api?type=waving&height=260&color=0:0f172a,35:2563eb,70:7c3aed,100:ec4899&text=Shushu%20Novelty%20Finder&fontColor=ffffff&fontSize=48&fontAlignY=38&desc=Paper%20lineage%20first.%20Novelty%20ideas%20next.&descSize=18&descAlignY=58)

<div align="center">

# 🚀 Shushu Novelty Finder

**面向 Codex 的论文脉络梳理 + 创新点生成 + 审稿式合理性审查 Skill**

先把一个方向里“极度相似”的论文脉络讲透，再从文献 gap 里长出真正能做的 idea。

🌐 语言 / Language: **中文** | [English](README_EN.md)

[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827?style=for-the-badge&logo=openai&logoColor=white)](skills/shushu-novelty-finder/SKILL.md)
[![论文脉络](https://img.shields.io/badge/Literature-Lineage-2563eb?style=for-the-badge)](examples/literature-lineage-mode.md)
[![创新点生成](https://img.shields.io/badge/Idea-Generation-7c3aed?style=for-the-badge)](examples/idea-generation-mode.md)
[![合理性审查](https://img.shields.io/badge/Reviewer-Audit-ec4899?style=for-the-badge)](skills/shushu-novelty-finder/references/idea-reasonableness-audit.md)
[![欢迎 Star](https://img.shields.io/badge/Star-Welcome-ffd700?style=for-the-badge&logo=github)](https://github.com/YingaoWang-casia/shushu-novelty-finder)

⭐ **如果你觉得这个 Skill 好用，欢迎给仓库点一个 Star 支持一下！**

[✨ 它能做什么](#-它能做什么) · [🧭 两种模式](#-两种核心模式) · [⚡ 快速开始](#-快速开始) · [🛠️ 安装教程](#️-安装教程) · [📚 示例](#-完整输入示例) · [🧪 输出质量](#-输出质量检查)

</div>

---

## ✨ 它能做什么

很多“帮我想论文创新点”的回答听起来很热闹，但真正写论文时会卡在这些问题上：

- 这个方向的任务到底是怎么发展来的？
- 哪些论文和我的想法极度相似？
- 每篇关键论文的创新点分别是什么？
- 哪些点已经被做烂了，哪些 gap 还站得住？
- 我的 idea 和 closest prior work 到底差在哪？
- 最小实验怎么设计，什么结果会支持、削弱或杀掉这个 idea？

`shushu-novelty-finder` 就是为这个场景准备的。它不只是 brainstorm，而是把研究 idea 拆成一条能被审查的链：

```text
研究方向 -> 极度相似论文 -> 每篇论文创新点 -> 趋势和饱和点 -> gap -> 候选 idea -> 实验和 baseline -> 审稿人反驳 -> 是否继续
```

为了方便中文和英文读者阅读，仓库提供双语 README：

- 中文版：[`README.md`](README.md)
- English version: [`README_EN.md`](README_EN.md)

---

## 🧭 两种核心模式

| 模式 | 适合什么时候用 | 主要输出 |
| --- | --- | --- |
| 🧾 **Literature Lineage Mode** | 你想先搞清楚某个方向的论文脉络、极度相似论文、每篇论文的新意 | 任务地图、论文分组、每篇论文创新点、趋势矩阵、gap audit |
| 💡 **Idea Generation Mode** | 你已经有一篇论文或一个方向，想生成可以做成论文的创新点 | weak / medium / strong idea、closest prior work、实验、baseline、kill criteria |

最推荐的使用方式是：

```text
先用 Literature Lineage Mode 把方向梳理清楚，
再用 Idea Generation Mode 从 gap 里生成 idea。
```

---

## ⚡ 快速开始

安装完成后，你可以直接在 Codex 里这样说：

```text
Use shushu-novelty-finder.

Mode:
Literature Lineage first, then Idea Generation.

Direction:
organic reaction prediction + RAG + LLM reasoning

请先梳理这个方向极度相似论文的整体脉络：
- 按历史阶段或方法路线分组；
- 输出每篇关键论文的具体创新点；
- 说明 task、input、output、datasets、metrics、assumptions；
- 标出哪些贡献已经饱和，哪些 gap 还可以做。

然后基于这些 gap 输出可以做成论文的创新点：
- weak / medium / strong 分级；
- 每个 idea 的 closest prior work；
- 最小实验和 baseline；
- reviewer objections；
- kill / continue criteria。
```

如果你本地把它安装成了短名 `idea`，也可以像这样启动：

```text
$idea 先梳理 organic reaction prediction + RAG + LLM reasoning 的论文脉络，再给可以做的 idea
```

---

## 🧾 模式一：论文脉络模式

### 什么时候用

当你还没准备好直接做 idea，而是想先看清楚一个方向：

- 当前任务是什么；
- 代表论文按什么路线发展；
- 每篇论文到底新在哪里；
- 哪些工作和你的方向最接近；
- 哪些创新点已经被占掉；
- 还有哪些 gap 能继续做。

### 输入模板

```text
Use shushu-novelty-finder.

Mode:
Literature Lineage first.

Direction:
<你的研究方向>

请先梳理这个方向极度相似论文的整体脉络：
1. 按历史阶段、方法路线或任务分支给论文分组；
2. 找出每组最关键、最相似的论文；
3. 对每篇论文输出具体创新点，不要只写一句摘要；
4. 说明每篇论文的数据集、指标、核心假设和局限；
5. 总结哪些贡献已经饱和，哪些 gap 仍然可以做；
6. 暂时不要急着给 idea，先把文献脉络讲清楚。
```

### 预期输出

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

完整示例：[`examples/literature-lineage-mode.md`](examples/literature-lineage-mode.md)

---

## 💡 模式二：创新点生成模式

### 什么时候用

当你已经有一个方向或一篇种子论文，并且想知道“我能怎么继续做”：

- 想从一篇论文扩展出新论文；
- 想判断某个 idea 是否已经被做过；
- 想要 weak / medium / strong 创新点分级；
- 想要最小实验、baseline 和审稿人反驳；
- 想知道这个 idea 是 `pilot-ready`、`workshop-ready` 还是 `main-track candidate`。

### 输入模板

```text
Use shushu-novelty-finder.

Mode:
Idea Generation.

Seed paper or direction:
<论文标题 / 摘要 / arXiv / DOI / URL / 你的研究方向>

Goal:
根据这篇论文或这个方向，输出可以做成论文的创新点。

请包括：
1. weak / medium / strong 创新点；
2. 每个 idea 的 closest prior work；
3. 为什么它不是已经被解决的问题；
4. novelty mechanism；
5. 最小实验和 strong baseline；
6. reviewer objections；
7. kill / continue criteria；
8. paper-readiness verdict。
```

### 预期输出

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

完整示例：[`examples/idea-generation-mode.md`](examples/idea-generation-mode.md)

---

## 🛠️ 安装教程

### 方法 1：标准安装

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

重启 Codex 后，用下面的方式触发：

```text
Use shushu-novelty-finder.
```

### 方法 2：安装成 `$idea` 短名

如果你想像 `$pua` 那样直接说 `$idea`，可以把 Skill 目录复制成 `idea`：

Windows PowerShell:

```powershell
git clone https://github.com/YingaoWang-casia/shushu-novelty-finder.git
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codex\skills\idea" | Out-Null
Copy-Item -Recurse -Force "shushu-novelty-finder\skills\shushu-novelty-finder\*" "$env:USERPROFILE\.codex\skills\idea\"
```

然后把 `%USERPROFILE%\.codex\skills\idea\SKILL.md` 顶部的 `name` 改成：

```yaml
name: idea
```

重启 Codex 后即可这样用：

```text
$idea 帮我先梳理论文脉络，再给创新点
```

### 方法 3：更新到最新版

如果之前已经安装过，可以重新复制覆盖：

```powershell
git pull
Copy-Item -Recurse -Force "skills\shushu-novelty-finder\*" "$env:USERPROFILE\.codex\skills\idea\"
```

如果你使用的是标准名字，把最后的 `idea` 换成 `shushu-novelty-finder`。

---

## 📚 完整输入示例

### 示例 A：先综述，再给 idea

```text
$idea

Mode:
Literature Lineage first, then Idea Generation.

Direction:
RAG evaluation for long-form question answering with citations

请先梳理这个方向极度相似论文的整体脉络：
- RAG evaluation 是怎么从 QA metric 发展到 citation faithfulness 的；
- 每篇关键论文的新意是什么；
- 哪些 benchmark / metric 已经覆盖；
- 哪些 gap 还可以写成论文。

然后基于 gap 输出 3-5 个可做 idea，并给出最小实验、baseline 和 kill criteria。
```

### 示例 B：基于种子论文找扩展方向

```text
$idea

Mode:
Idea Generation.

Seed paper:
<粘贴论文标题、摘要、arXiv 链接或 PDF 内容>

Goal:
我想基于这篇论文继续做一个 workshop 或 main-track candidate。

请输出：
- 这篇论文已经占掉的贡献点；
- closest prior work；
- 还能做的 weak / medium / strong idea；
- 每个 idea 的 novelty mechanism；
- 最小实验和 baseline；
- reviewer 可能怎么拒；
- 什么结果会支持、削弱或杀掉这个 idea。
```

### 示例 C：只想看论文脉络，不要 idea

```text
$idea

Mode:
Literature Lineage only.

Direction:
speech turn-taking evaluation for full-duplex voice agents

只需要先梳理论文脉络，不要生成 idea。
请重点输出：
- 任务定义怎么变化；
- 极度相似论文分组；
- 每篇论文创新点；
- 数据集和指标；
- 目前最饱和和最缺失的地方。
```

---

## 🧪 输出质量检查

一个合格输出至少应该满足：

- ✅ 有明确的 input mode；
- ✅ 有 scope / task map；
- ✅ 有真实论文名，或明确标注 `candidate / unverified`；
- ✅ 论文脉络模式下，每篇关键论文都有具体创新点；
- ✅ trend matrix 不是论文列表，而是趋势变化；
- ✅ gap 有证据标签；
- ✅ idea 有 closest prior work；
- ✅ idea 有 novelty mechanism；
- ✅ idea 有 minimum experiment 和 baseline；
- ✅ 有 reviewer objection；
- ✅ 有 kill / continue criteria；
- ✅ 不随便说“没人做过”。

完整检查清单：[`evals/checks/output-checklist.md`](evals/checks/output-checklist.md)

---

## 🗂️ 仓库结构

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

## 🔗 相关链接

- 🌐 [English README](README_EN.md)
- 🧠 [Main Skill](skills/shushu-novelty-finder/SKILL.md)
- 📖 [Usage Guide](docs/usage.md)
- ⚡ [Quickstart](docs/quickstart.md)
- 🧾 [Literature Lineage Example](examples/literature-lineage-mode.md)
- 💡 [Idea Generation Example](examples/idea-generation-mode.md)
- 🧪 [Output Checklist](evals/checks/output-checklist.md)

---

## ⭐ Star

如果这个 Skill 帮你更快地看清一个研究方向、找到靠谱的论文 idea，欢迎给仓库点一个 Star ⭐。

这会让我知道它真的有用，也会让我更有动力继续补更多领域模板和示例。

![Footer](https://capsule-render.vercel.app/api?type=waving&height=120&section=footer&color=0:ec4899,45:7c3aed,100:2563eb)
