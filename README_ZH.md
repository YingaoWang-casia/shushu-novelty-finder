![Shushu Novelty Finder](https://capsule-render.vercel.app/api?type=waving&height=260&color=0:0f172a,35:2563eb,70:7c3aed,100:ec4899&text=Shushu%20Novelty%20Finder&fontColor=ffffff&fontSize=48&fontAlignY=38&desc=Generate%20research%20ideas.%20Stress-test%20them%20like%20a%20top-tier%20reviewer.&descSize=18&descAlignY=58)

<div align="center">

# 🚀 shushu-novelty-finder

**一个用于 Codex 的论文创新点生成与合理性审查 Skill。**

输入一个计算机研究方向或种子论文，输出候选创新点、文献证据、合理性推敲、实验方案和可投稿性判断。

[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827?style=for-the-badge&logo=openai&logoColor=white)](skills/shushu-novelty-finder/SKILL.md)
[![创新点生成](https://img.shields.io/badge/Research-Idea%20Generator-2563eb?style=for-the-badge)](#-它能做什么)
[![合理性审查](https://img.shields.io/badge/Reviewer-Reasonableness%20Audit-7c3aed?style=for-the-badge)](skills/shushu-novelty-finder/references/idea-reasonableness-audit.md)
[![可投稿性判断](https://img.shields.io/badge/Paper-Readiness%20Verdict-ec4899?style=for-the-badge)](#-可投稿性判断)

语言 / Languages: [English](README.md) | [中文](README_ZH.md)

[✨ 为什么需要它](#-为什么需要它) · [🔥 核心能力](#-它能做什么) · [🔁 工作闭环](#-工作闭环) · [⚡ 使用示例](#-使用示例) · [🛠️ 安装](#️-安装) · [🎯 判断标准](#-可投稿性判断)

</div>

---

## ✨ 为什么需要它

很多“帮我想论文创新点”的提示词都会犯同一个问题：听起来很自信，但并不告诉你这个 idea 到底新不新、能不能做、能不能被实验支撑、能不能扛住审稿人质疑。

`shushu-novelty-finder` 适合这种场景：你手里只有一个方向，比如：

```text
RAG evaluation
LLM-as-a-Judge
speech turn-taking
multimodal agent memory
```

但你不想要一串看起来很潮、实际上落不了地的 topic。你真正想知道的是：

- 这个方向里有哪些可能的创新点？
- 哪些是 weak / medium / strong？
- 最接近的前人工作是什么？
- 这个 idea 为什么可能不合理？
- 什么实验能支持、削弱或杀掉它？
- 它更像课程项目、workshop、主会候选，还是根本没准备好？

---

## 🔥 它能做什么

<table>
<tr>
<td width="50%">

### 🧠 生成创新点

- 把模糊方向收敛成可研究的任务边界；
- 从文献趋势、种子论文和限制条件中抽取 gap；
- 生成 safe / medium-risk / ambitious 三类候选方向；
- 将 idea 分成 weak / medium / strong；
- 判断每个 idea 更适合什么论文类型。

</td>
<td width="50%">

### 🧪 推敲合理性

- 找出 closest prior work；
- 检查真正的 novelty mechanism；
- 区分“文献证据”和“模型推断”；
- 设计最小实验、baseline 和 falsification test；
- 预判 reviewer objection；
- 给出 continue / narrow / downgrade / kill 条件。

</td>
</tr>
</table>

---

## 🔁 工作闭环

| 阶段 | 做什么 | 输出 |
|---:|---|---|
| 01 | 锁定用户方向或种子论文边界 | Research Scope Card / Seed Paper Card |
| 02 | 检查 prior / follow-up / sibling work | Paper Evidence Cards |
| 03 | 把论文证据绑定到具体 claim | Claim-Evidence Map |
| 04 | 抽取趋势、gap 和弱信号 | Literature Timeline + Gap Audit |
| 05 | 生成候选创新点 | Weak / Medium / Strong idea set |
| 06 | 推敲每个 idea 是否站得住 | Idea Reasonableness Audit |
| 07 | 设计最小决定性实验 | Baselines + falsification plan |
| 08 | 预演审稿人反驳 | Accept / reject reasons |
| 09 | 给出下一步决策 | Pursue / narrow / verify / downgrade / stop |

它不是只负责说“这个很新”。它会把一条研究想法背后的证据链、实验链和风险链都摊开。

---

## ⚡ 使用示例

```text
Use shushu-novelty-finder.
Direction: RAG evaluation.
Goal: paper-oriented research project.
Constraints: 2 months, limited compute.
First lock the scope, then generate novelty ideas and audit whether each idea is reasonable.
```

如果你有种子论文：

```text
Use shushu-novelty-finder.
Seed paper: <paper title / abstract / arXiv / DOI / PDF>.
Goal: find paper-worthy extension ideas.
First build a Seed Paper Card, then search prior work, follow-up work, and sibling work.
Rank ideas as weak / medium / strong, judge whether each top idea is reasonable, and give a paper-readiness verdict.
```

---

## 🧾 输出预览

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

## 🧩 合理性审查

每个 top idea 都要过这张表：

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

完整规则见 [`idea-reasonableness-audit.md`](skills/shushu-novelty-finder/references/idea-reasonableness-audit.md)。

---

## 🛠️ 安装

### 🍎 macOS / Linux

```bash
git clone https://github.com/YingaoWang-casia/shushu-novelty-finder.git
mkdir -p ~/.codex/skills
cp -R shushu-novelty-finder/skills/shushu-novelty-finder ~/.codex/skills/
```

### 🪟 Windows PowerShell

```powershell
git clone https://github.com/YingaoWang-casia/shushu-novelty-finder.git
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force "shushu-novelty-finder\skills\shushu-novelty-finder" "$env:USERPROFILE\.codex\skills\"
```

重启 Codex 或打开一个新的 Codex 会话，然后用名字触发：

```text
Use shushu-novelty-finder.
```

检查安装位置：

```text
~/.codex/skills/shushu-novelty-finder/SKILL.md
%USERPROFILE%\.codex\skills\shushu-novelty-finder\SKILL.md
```

---

## 🎯 可投稿性判断

| Verdict | 含义 |
|---|---|
| `not ready` | idea 太模糊、证据不足、不可行，或很可能已经被解决。 |
| `pilot-ready` | 值得先做一个小实验，再决定是否继续投入。 |
| `workshop-ready` | 如果证据和执行扎实，有机会形成 scoped contribution。 |
| `main-track candidate` | 具备较强 novelty、证据、baseline 和 reviewer defense 潜力。 |
| `technical-report-only` | 工程或负结果有价值，但不一定构成研究论文。 |

---

## 🗺️ 仓库结构

```text
shushu-novelty-finder/
├─ skills/shushu-novelty-finder/
│  ├─ SKILL.md                         # Skill 主体说明
│  ├─ agents/openai.yaml               # Codex Skill 元数据
│  └─ references/                      # 规则、模板、领域包
├─ docs/usage.md                       # 详细使用说明
├─ examples/                           # 示例 prompt 和输出
├─ evals/                              # 质量检查与 eval case
└─ scripts/                            # 轻量论文记录处理脚本
```

---

## 🔗 相关链接

- [Main Skill](skills/shushu-novelty-finder/SKILL.md)
- [Usage Guide](docs/usage.md)
- [Output Template](skills/shushu-novelty-finder/references/output-template.md)
- [Idea Reasonableness Audit](skills/shushu-novelty-finder/references/idea-reasonableness-audit.md)
- [Output Checklist](evals/checks/output-checklist.md)
- [Verified RAG Mini Audit](examples/verified-rag-mini-audit.md)

---

## 🧭 Philosophy

好的研究 ideation 不是简单地“找一个新东西”。

它是一条链：

```text
scoped problem -> literature evidence -> candidate idea -> reasonableness audit -> experiment -> reviewer defense -> decision
```

这个 Skill 的目标，就是先生成这条链，再测试它到底站不站得住。

![Footer](https://capsule-render.vercel.app/api?type=waving&height=120&section=footer&color=0:ec4899,45:7c3aed,100:2563eb)
