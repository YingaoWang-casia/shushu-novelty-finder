![Shushu Novelty Finder](https://capsule-render.vercel.app/api?type=waving&height=260&color=0:0f172a,35:2563eb,70:7c3aed,100:ec4899&text=Shushu%20Novelty%20Finder&fontColor=ffffff&fontSize=48&fontAlignY=38&desc=Paper%20lineage%20first.%20Novelty%20ideas%20next.&descSize=18&descAlignY=58)

<div align="center">

# 🚀 Shushu Novelty Finder

**面向 Codex 的论文脉络梳理 + 创新点生成 + 审稿式合理性审查 + 中英文互转 Skill**

先把一个方向里“极度相似”的论文脉络讲透，再从文献 gap 里长出真正能做的 idea，也支持科研文本的中英文互转。

🌐 语言 / Language: **中文** | [English](README_EN.md)

[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827?style=for-the-badge&logo=openai&logoColor=white)](skills/shushu-novelty-finder/SKILL.md)
[![论文脉络](https://img.shields.io/badge/Literature-Lineage-2563eb?style=for-the-badge)](examples/literature-lineage-mode.md)
[![创新点生成](https://img.shields.io/badge/Idea-Generation-7c3aed?style=for-the-badge)](examples/idea-generation-mode.md)
[![中英文互转](https://img.shields.io/badge/ZH--EN-Translation-10b981?style=for-the-badge)](#-模式三中英文互转)
[![合理性审查](https://img.shields.io/badge/Reviewer-Audit-ec4899?style=for-the-badge)](skills/shushu-novelty-finder/references/idea-reasonableness-audit.md)
[![欢迎 Star](https://img.shields.io/badge/Star-Welcome-ffd700?style=for-the-badge&logo=github)](https://github.com/YingaoWang-casia/shushu-novelty-finder)

⭐ **如果你觉得这个 Skill 好用，欢迎给仓库点一个 Star 支持一下！**

[✨ 它能做什么](#-它能做什么) · [🧭 三种模式](#-三种核心模式) · [⚡ 快速开始](#-快速开始) · [🛠️ 安装教程](#️-安装教程) · [📚 示例](#-完整输入示例) · [🧪 输出质量](#-输出质量检查)

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
- 中文 idea、摘要、rebuttal 怎么翻成自然的英文论文表达？英文 review / related work 又怎么翻回中文理解？

`shushu-novelty-finder` 不是简单 brainstorm，而是把研究 idea 拆成一条能被审查的链：

```text
研究方向 -> 极度相似论文 -> 每篇论文创新点 -> 趋势和饱和点 -> gap -> 候选 idea -> 实验和 baseline -> 审稿人反驳 -> 是否继续
```

同时也可以辅助科研文本中英文互转：

```text
中文研究想法 / 摘要 / rebuttal -> 英文学术表达
English abstract / related work / review -> 中文理解版
```

---

## 🧭 三种核心模式

| 模式 | 适合什么时候用 | 主要输出 |
| --- | --- | --- |
| 🧾 **Literature Lineage Mode** | 你想先搞清楚某个方向的论文脉络、极度相似论文、每篇论文的新意 | 任务地图、论文分组、每篇论文创新点、趋势矩阵、gap audit |
| 💡 **Idea Generation Mode** | 你已经有一篇论文或一个方向，想生成可以做成论文的创新点 | weak / medium / strong idea、closest prior work、实验、baseline、kill criteria |
| 🌐 **Chinese-English Translation Mode** | 你想在中文和英文之间转换科研文本、摘要、related work、review response 或 prompt | 中译英、英译中、双语对照、术语保留、学术表达润色 |

---

## ⚡ 快速开始

```text
Use shushu-novelty-finder.

Mode:
Literature Lineage first, then Idea Generation.

Direction:
organic reaction prediction + RAG + LLM reasoning

请先梳理这个方向极度相似论文的整体脉络，然后基于 gap 输出可以做成论文的创新点。
```

中英文互转示例：

```text
$idea 请把下面中文 idea 翻译成英文学术表达，并保留 RAG、baseline、faithfulness 等术语：
<粘贴文本>
```

---

## 🧾 模式一：论文脉络模式

```text
Use shushu-novelty-finder.

Mode:
Literature Lineage first.

Direction:
<你的研究方向>

请先梳理这个方向极度相似论文的整体脉络：
1. 按历史阶段、方法路线或任务分支给论文分组；
2. 找出每组最关键、最相似的论文；
3. 对每篇论文输出具体创新点；
4. 说明每篇论文的数据集、指标、核心假设和局限；
5. 总结哪些贡献已经饱和，哪些 gap 仍然可以做。
```

完整示例：[`examples/literature-lineage-mode.md`](examples/literature-lineage-mode.md)

---

## 💡 模式二：创新点生成模式

```text
Use shushu-novelty-finder.

Mode:
Idea Generation.

Seed paper or direction:
<论文标题 / 摘要 / arXiv / DOI / URL / 你的研究方向>

请输出 weak / medium / strong 创新点、closest prior work、最小实验、baseline、reviewer objections 和 kill / continue criteria。
```

完整示例：[`examples/idea-generation-mode.md`](examples/idea-generation-mode.md)

---

## 🌐 模式三：中英文互转

```text
Use shushu-novelty-finder.

Mode:
Chinese-English Translation.

请把下面的中文翻译成自然、准确的英文学术表达：
<粘贴中文文本>
```

英译中也可以这样：

```text
$idea 请把下面英文 related work 翻译成中文，保留 benchmark、dataset、metric、citation：
<粘贴英文文本>
```

---

## 🛠️ 安装教程

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

如果你想像 `$pua` 那样直接说 `$idea`，可以把 Skill 目录复制成 `idea`，并把 `SKILL.md` 顶部改成：

```yaml
name: idea
```

---

## 🧪 输出质量检查

- ✅ 有明确的 input mode；
- ✅ 论文脉络模式下，每篇关键论文都有具体创新点；
- ✅ idea 有 closest prior work、novelty mechanism、minimum experiment 和 baseline；
- ✅ 有 reviewer objection 和 kill / continue criteria；
- ✅ 中英文互转时不增加新 claim，保留关键术语、引用、公式和数据集 / metric 名。

完整检查清单：[`evals/checks/output-checklist.md`](evals/checks/output-checklist.md)

---

## 🔗 相关链接

- 🧠 [Main Skill](skills/shushu-novelty-finder/SKILL.md)
- 📖 [Usage Guide](docs/usage.md)
- ⚡ [Quickstart](docs/quickstart.md)
- 🧾 [Literature Lineage Example](examples/literature-lineage-mode.md)
- 💡 [Idea Generation Example](examples/idea-generation-mode.md)
- 🧪 [Output Checklist](evals/checks/output-checklist.md)

---

## ⭐ Star

如果这个 Skill 帮你更快地看清一个研究方向、找到靠谱的论文 idea，欢迎给仓库点一个 Star ⭐。

![Footer](https://capsule-render.vercel.app/api?type=waving&height=120&section=footer&color=0:ec4899,45:7c3aed,100:2563eb)
