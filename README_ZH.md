![Shushu Novelty Finder](https://capsule-render.vercel.app/api?type=waving&height=260&color=0:0f172a,35:2563eb,70:7c3aed,100:ec4899&text=Shushu%20Novelty%20Finder&fontColor=ffffff&fontSize=48&fontAlignY=38&desc=Generate%20research%20ideas.%20Stress-test%20them%20like%20a%20top-tier%20reviewer.&descSize=18&descAlignY=58)

<div align="center">

# 🚀 shushu-novelty-finder

**面向 Codex 的计算机论文创新点生成与可行性审查 Skill。**

给它一个研究方向或种子论文，它会先收敛研究边界，再生成候选创新点，最后用文献证据、最小实验、审稿人反驳和 kill / continue 标准逐条推敲。

[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827?style=for-the-badge&logo=openai&logoColor=white)](skills/shushu-novelty-finder/SKILL.md)
[![创新点生成](https://img.shields.io/badge/Research-Idea%20Generator-2563eb?style=for-the-badge)](#-它能做什么)
[![合理性审查](https://img.shields.io/badge/Reviewer-Reasonableness%20Audit-7c3aed?style=for-the-badge)](skills/shushu-novelty-finder/references/idea-reasonableness-audit.md)
[![可投稿性判断](https://img.shields.io/badge/Paper-Readiness%20Verdict-ec4899?style=for-the-badge)](#-可投稿性判断)

语言 / Languages: [English](README.md) | [中文](README_ZH.md)

[✨ 为什么需要它](#-为什么需要它) · [🔥 核心能力](#-它能做什么) · [🔁 工作闭环](#-工作闭环) · [⚡ 使用示例](#-使用示例) · [🛠️ 安装](#️-安装) · [🎯 判断标准](#-可投稿性判断)

</div>

---

## ✨ 为什么需要它

很多“帮我想论文创新点”的提示词，最大的问题不是不会想，而是太容易把**听起来合理的脑暴**包装成**看起来很新的贡献**。

真正难的是后半段：这个 idea 到底新在哪里？最接近的前人工作是谁？它能不能被实验验证？如果审稿人说“这只是已有方法的组合”，你怎么回答？如果实验结果不显著，应该继续、缩小范围，还是直接停止？

`shushu-novelty-finder` 就是为这种时刻准备的。你可以给它一个模糊方向，例如：

```text
RAG evaluation
LLM-as-a-Judge
speech turn-taking
multimodal agent memory
```

它不会只给你一串时髦 topic，而是帮你判断：

- 这个方向里哪些创新点值得尝试？
- 哪些 idea 只是 weak novelty，哪些有 medium / strong 潜力？
- 哪篇论文是最接近的 prior work？
- 这个 idea 为什么可能站不住？
- 最小实验应该怎么设计，什么结果会支持、削弱或杀掉它？
- 它更适合课程项目、技术报告、workshop，还是有主会候选潜力？

---

## 🔥 它能做什么

<table>
<tr>
<td width="50%">

### 🧠 提出创新点

- 把宽泛方向收敛成具体研究任务；
- 从文献趋势、种子论文和约束条件中提取 gap；
- 生成保守型、中风险型和进取型候选 idea；
- 将候选 idea 分为 weak / medium / strong；
- 判断每个 idea 更适合方法、评测、benchmark、系统、分析还是技术报告。

</td>
<td width="50%">

### 🧪 推敲合理性

- 找出 closest prior work，避免“假创新”；
- 明确 novelty mechanism，而不是只堆流行词；
- 区分文献证据、用户假设和模型推断；
- 设计最小实验、强 baseline 和 falsification test；
- 预演 reviewer objection；
- 给出 continue / narrow / downgrade / kill 条件。

</td>
</tr>
</table>

---

## 🔁 工作闭环

| 阶段 | 做什么 | 输出 |
|---:|---|---|
| 01 | 锁定研究范围或解析种子论文 | Research Scope Card / Seed Paper Card |
| 02 | 梳理 prior、follow-up 和 sibling work | Paper Evidence Cards |
| 03 | 把论文证据绑定到具体 claim | Claim-Evidence Map |
| 04 | 提炼研究趋势、gap 和风险信号 | Literature Timeline + Gap Audit |
| 05 | 生成候选创新点 | Weak / Medium / Strong idea set |
| 06 | 逐条压力测试 idea 是否站得住 | Idea Reasonableness Audit |
| 07 | 设计最小决定性实验 | Baselines + falsification plan |
| 08 | 预演审稿人可能的反驳 | Accept / reject reasons |
| 09 | 给出下一步决策 | Pursue / narrow / verify / downgrade / stop |

它不是只负责说“这个方向很新”。它会把一个研究想法背后的**证据链、实验链、反驳链和决策链**摊开。

---

## ⚡ 使用示例

只有研究方向时：

```text
Use shushu-novelty-finder.
研究方向：RAG evaluation
目标：面向论文的研究项目
约束：2 个月，算力有限
请先锁定范围，再生成创新点，并逐条审查合理性和可投稿性。
```

如果你已经有种子论文：

```text
Use shushu-novelty-finder.
Seed paper: <论文标题 / 摘要 / arXiv / DOI / PDF>.
目标：寻找有论文潜力的扩展方向。
请先构建 Seed Paper Card，再检索 prior work、follow-up work 和 sibling work。
最后按 weak / medium / strong 给出创新点分级，并判断每个 top idea 是否合理。
```

---

## 🧾 输出预览

字段名保留英文，是为了和 Skill 的输出模板保持一致；中文用户可以直接看每个字段后的内容。

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

`Idea Reasonableness Audit` 不是普通打分表，而是用来防止“幻觉式创新点”的压力测试。

每个 top idea 都需要回答：

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

重启 Codex 或打开新的 Codex 会话，然后直接用名字触发：

```text
Use shushu-novelty-finder.
```

检查 Skill 是否安装到正确位置：

```text
~/.codex/skills/shushu-novelty-finder/SKILL.md
%USERPROFILE%\.codex\skills\shushu-novelty-finder\SKILL.md
```

---

## 🎯 可投稿性判断

| Verdict | 含义 |
|---|---|
| `not ready` | 当前 idea 太模糊、证据不足、实验不可行，或很可能已经被解决。 |
| `pilot-ready` | 值得先做最小实验，用数据决定是否继续投入。 |
| `workshop-ready` | 如果证据和实验执行扎实，有机会形成 workshop / short paper 级别贡献。 |
| `main-track candidate` | 具备较强 novelty、证据链、baseline 设计和 reviewer defense 潜力。 |
| `technical-report-only` | 工程实现、复现或负结果有价值，但暂时不足以支撑研究论文。 |

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

## 🧭 设计理念

好的研究 ideation 不是简单地“找一个新东西”。

它是一条可以被审查的链：

```text
scoped problem -> literature evidence -> candidate idea -> reasonableness audit -> experiment -> reviewer defense -> decision
```

这个 Skill 的目标，就是先生成这条链，再测试它到底站不站得住。

![Footer](https://capsule-render.vercel.app/api?type=waving&height=120&section=footer&color=0:ec4899,45:7c3aed,100:2563eb)
