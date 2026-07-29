# Shushu Novelty Finder — AI 接手与后续执行手册

> 最后核验日期：2026-07-29（Asia/Shanghai）
>
> 面向对象：后续接手本项目的 AI 编程代理、维护者或评测协调者。
>
> 本文记录当前真实状态、已经完成的工作、尚未完成的硬门槛、目录结构、关键产物、
> 安全边界和可直接执行的命令。不要仅凭聊天记录或旧分支判断项目状态。

## 0. 先读结论

- 工程化 Alpha 已完成、合并并公开发布。
- 当前公开版本是 GitHub prerelease `v0.2.0a1`。
- 主分支、安装包、四源检索、P0–P9 状态机、60-seed benchmark、240 次系统运行、
  双人盲评包和自动化评测工具链均已完成。
- **稳定版 `v0.2.0` 唯一未完成的硬性证据是两名真实科研评审者的盲评。**
- 不得让 LLM 冒充真人评审者，不得伪造科研经验，不得在真人结果完成前宣称
  v0.2 优于 baseline。
- 本机存在预解盲材料，部分目录受 `.gitignore` 保护，不能在盲评锁定前提交或公开。

## 1. 仓库与发布状态

| 项目 | 当前状态 |
|---|---|
| 本地仓库 | `/Users/admin/Desktop/idea/shushu-novelty-finder` |
| GitHub | `YingaoWang-casia/shushu-novelty-finder` |
| 默认分支 | `main` |
| 本文编写时 `origin/main` | `199c7487a066472d85904e3cfd0423087686d687` |
| 工程 Alpha Release | [`v0.2.0a1`](https://github.com/YingaoWang-casia/shushu-novelty-finder/releases/tag/v0.2.0a1) |
| Release 源提交 | `2cfa010c24d7bc72ff1686c0383584e71fe95763` |
| 最新主分支 CI | [run 30429442829](https://github.com/YingaoWang-casia/shushu-novelty-finder/actions/runs/30429442829) |
| Python 支持 | 3.9+；CI 覆盖 3.9 和 3.12 |
| 自动测试 | 117 项 |
| 当前包版本 | `0.2.0a1` |

已合并的主要 PR：

1. [PR #1](https://github.com/YingaoWang-casia/shushu-novelty-finder/pull/1)：
   完整工程化运行时、评测与 CI。
2. [PR #2](https://github.com/YingaoWang-casia/shushu-novelty-finder/pull/2)：
   README 顶部 Alpha 证据边界和 Changelog 对齐。
3. [PR #3](https://github.com/YingaoWang-casia/shushu-novelty-finder/pull/3)：
   Alpha Release、远端安装和主分支 CI 审计记录。

Release 附件：

| 附件 | SHA-256 |
|---|---|
| `shushu_novelty_finder-0.2.0a1-py3-none-any.whl` | `b007e94afb7420b48a50dc33c1b76ed3da213e88971719cec2d287a15915f198` |
| `shushu_novelty_finder-0.2.0a1.tar.gz` | `a759eebc2128d71d9f59e848c529476fdccedfdbb4a293a1095d8e0780a4f030` |

该 wheel 已从 GitHub Release 重新下载，在全新 Python 3.9 环境安装，并通过：

```text
shushu --version  -> shushu 0.2.0a1
shushu check      -> status: ok
```

## 2. 已经完成的工作

### 2.1 包、CLI 与基础质量体系

- 使用 `pyproject.toml` 和 `src/` layout 的可安装 Python 包。
- 哈希锁定的 `requirements-dev.lock`。
- 主 CLI：`shushu`；评审侧匿名 CLI：`blind-eval`。
- 保留旧版三个脚本的兼容入口。
- Ruff、pytest、Python 3.9/3.12 GitHub Actions。
- CI 仅由 Python 3.9 重建和校验 canonical dependency lock，避免跨解释器假漂移。
- GitHub Actions 使用 Node 24 运行时的 `actions/checkout@v7` 和
  `actions/setup-python@v7`。

### 2.2 P0–P9 可恢复工作流

阶段如下：

```text
P0 Intake
→ P1 Scope Narrowing
→ P2 Literature Retrieval
→ P3 Paper Verification
→ P4 Lineage Construction
→ P5 Gap Audit
→ P6 Idea Portfolio Generation
→ P7 Novelty Collision Check
→ P8 Reviewer Audit
→ P9 Final Report
```

已实现：

- `lineage`、`idea`、`full` 三种模式。
- `shushu run` 创建运行目录。
- `shushu next` 确定性返回唯一下一阶段。
- 中断恢复、幂等、禁止覆盖已验证产物。
- 每阶段主产物及辅助产物 SHA-256 绑定。
- Schema gate、篡改检测和旧状态迁移。
- 报告绑定正文、输入、失败日志和公开评测证据。

### 2.3 四源论文检索与重放

已实现四个真实来源：

- arXiv；
- OpenAlex；
- Semantic Scholar；
- OpenReview。

包括：

- retry、timeout、backoff；
- 并发检索与限流；
- DOI、arXiv ID、OpenReview ID 和标题级 canonical dedup；
- accepted paper 与 preprint 合并；
- provenance 和失败日志；
- 无结果不得静默成功；
- 可序列化记录和离线 replay manifest。

保留的无凭证 20-topic 联合实跑结果：

- 四个来源均为 `20/20` 成功；
- `395` 条原始记录；
- 去重后 `380` 条 canonical records；
- `0` 个来源失败；
- `0` 个剩余重复；
- `20` 个 replay manifests 均离线校验通过；
- report SHA-256：
  `acabc854490418f6a645caa83446d5dd479efa2d15a2a3a92df428f24cd33c74`。

OpenAlex Key 不是 Alpha 的阻塞项：

- 小规模 smoke/evaluation 可使用 bounded anonymous path；
- 重复或生产级运行仍建议使用调用者自己的免费 `OPENALEX_API_KEY`。

### 2.4 全文证据、Lineage 与 Novelty Collision

已实现：

- PDF/HTML 获取；
- PDF 大小和 magic 校验；
- content-addressed cache；
- 文本抽取、页级 hash、失败 checkpoint；
- Claim-Evidence Ledger；
- `strong` claim 必须由 full-text support；
- abstract-only 不能冒充全文证据；
- lineage graph、七类关系、时间顺序警告；
- contribution saturation；
- gap 与 claim 的跨记录绑定；
- idea 的 closest prior work 和 kill criterion；
- 独立六轴 novelty collision；
- 3–7 篇危险 prior；
- pass / revise / downgrade / abandon；
- abandon 后最多一次结构性重写；
- 独立 reviewer audit 和 fatal objection gate。

### 2.5 Benchmark 与系统执行

固定 Benchmark v1：

- 60 个 seed；
- 20 broad direction；
- 20 seed paper；
- 10 known-scoop；
- 10 mechanism-transfer；
- 覆盖 8 个 CS/AI 子领域。

四个系统：

- bare model；
- bare model + self-reflection；
- Shushu v0.1；
- Shushu v0.2。

执行状态：

- `240/240` 真实 `gpt-5.6-sol` 运行已完成；
- 每个系统 60 个；
- final run-matrix SHA-256：
  `bbfee19d4466f168b482593e38e0145b0cf2acb7bcd0cb54a6ad0b71e88cbbc2`；
- adapter、prompt、model、CLI/runtime、输出路径和输出 hash 已绑定；
- 支持失败落盘、断点恢复、shard merge 和 quota/auth/429 circuit breaker。

### 2.6 双人盲评设计与工具

采用 preregistered `balanced-overlap`：

- 每位评审者 36 个 seed；
- 每人 144 条 scalar judgment；
- 每人 216 条 pairwise judgment；
- 两人共享 12 个分层 seed；
- 两人的并集覆盖全部 60 个 seed；
- 共享 seed 覆盖全部 8 个领域；
- 总计 288 scalar + 432 pairwise；
- 相比两人完整重复评价减少 40% 工作量；
- 共享 seed 在系统总指标中按 seed 归一化，不会获得双倍权重。

已实现：

- opaque system labels；
- pairwise 左右随机化；
- 评审侧去品牌化 provenance；
- rater assignment/output/guide/schema 全量 hash 绑定；
- `blind-eval init/status/lock`；
- unfinished judgment 使用 `null`，不能静默过关；
- response lock；
- coordinator `collect-responses`；
- deterministic unblind；
- tamper、foreign pack、missing lock、coverage drift、identity drift 拒绝；
- scalar 与 pairwise Cohen’s kappa；
- human-primary aggregate；
- LLM judge 只能作为辅助且被排除出 primary metrics。

当前本机盲评包：

```text
evals/blind-balanced-v1/
├── MANIFEST-COMMITMENT.txt
├── coordinator/
│   ├── blind-key.jsonl
│   └── manifest.json
└── raters/
    ├── rater-a/
    └── rater-b/
```

coordinator manifest commitment：

```text
552dfbd1ef0517bd632ea0540beca3505674229ddaf856f5b2f82073e63a6c40
```

该包已准备好，但**当前没有任何真人 response 或 judgment**。

### 2.7 示例、文档与发布

- 三个完整真实论文 P0–P9 known-scoop 示例：RAG、LoRA、CLIP。
- 示例包含 PDF、页级证据、失败日志、hash manifest 和最终报告。
- failure cases 页面。
- Quick Start、使用手册、迁移说明、架构文档、4 个 ADR。
- 中英文 README。
- README release gate：没有 human-primary 公开报告时禁止 comparative claim。
- `v0.2.0a1` GitHub prerelease 已发布。

## 3. 尚未完成的工作

### 3.1 唯一硬阻塞：两名真实科研评审者

必须招募两名满足以下条件的真人：

- 具有 CS、AI、IR、data mining 或相关方向的研究经历；
- 能检查论文、引用、baseline、novelty 和实验声明；
- 未参与本仓库或四个系统配置；
- 在双方响应锁定前相互独立；
- 如实填写科研经验年限和利益冲突。

不能使用以下替代：

- LLM 冒充人类；
- 项目作者自己复制出两个身份；
- 未支付的专业能力筛选；
- 先看 system identity 再评分；
- 手工修改独立评分以提高一致性。

### 3.2 真人结果到位后仍需执行的闭环

1. 验证两个 rater directory 和 response lock。
2. 使用 `collect-responses` 合并，禁止手工拼接 JSONL。
3. deterministic unblind。
4. 生成 `public-results.json`。
5. 检查两类 Cohen’s kappa。
6. 检查所有 retrieval/evidence/lineage/idea/calibration metric families。
7. 确认报告为 `human-primary` 且 `publishable: true`。
8. 将公开报告 SHA-256 写入 README claim block。
9. 运行三语 `release-check`。
10. 完成稳定版版本号、Changelog、最终 CI、tag、GitHub Release。

## 4. 后续 AI 的精确执行顺序

### Step 0：先同步并验证环境

不要在旧 feature branch 上继续：

```bash
cd /Users/admin/Desktop/idea/shushu-novelty-finder
git status -sb
git fetch origin
git switch main
git pull --ff-only origin main
git rev-parse HEAD
```

如果存在用户未提交改动，不得覆盖、reset 或 checkout 丢弃。

创建新分支：

```bash
git switch -c agent/complete-human-evaluation
```

环境验证：

```bash
.venv/bin/shushu --version
.venv/bin/shushu check
.venv/bin/ruff check .
.venv/bin/pytest -q
```

### Step 1：招募与付费 pilot

完整要求和可复制招募文案：

- [`docs/rater-recruitment.md`](rater-recruitment.md)

建议渠道：

- Prolific custom screening；
- Upwork academic research freelancers；
- 大学实验室邮件列表；
- 无利益冲突的专业推荐。

先做一个**付费** pilot seed，确认候选人会：

- 区分 metadata / abstract / full text；
- 检查引用和证据；
- 使用 rubric；
- 判断 novelty、feasibility、falsifiability；
- 不尝试识别系统。

pilot 是否计入最终数据必须提前声明，默认不计入。

### Step 2：安全分发评审包

协调者保留，绝不能发给评审者：

```text
evals/blind-balanced-v1/coordinator/
evals/completed-run-matrix.jsonl
evals/execution/codex-gpt-5.6-sol/
任何带 system name 的原始输出
```

只发送：

```text
rater-a <- evals/blind-balanced-v1/raters/rater-a/
rater-b <- evals/blind-balanced-v1/raters/rater-b/
```

同时单独发送 manifest commitment：

```text
552dfbd1ef0517bd632ea0540beca3505674229ddaf856f5b2f82073e63a6c40
```

发送前再次验证：

```bash
shasum -a 256 evals/blind-balanced-v1/coordinator/manifest.json
```

结果必须等于上述 commitment。若任意 rater-side 文件变化，必须废弃旧 commitment，
重新生成 pack 和新 commitment，不能继续沿用旧值。

### Step 3：评审者本地操作

每位评审者在自己的 pack 目录上执行：

```bash
blind-eval init /path/to/rater-pack --experience-years <真实年数>
blind-eval status /path/to/rater-pack
```

评审者填写由 `init` 创建的 scalar 和 pairwise response drafts。所有 `null` 必须由
真实判断替换，且不能修改 assignment、output hash 或其他 immutable fields。

完成后先看状态，再锁定：

```bash
blind-eval status /path/to/rater-pack

blind-eval lock /path/to/rater-pack \
  --scalar /path/to/rater-pack/scalar-responses.jsonl \
  --pairwise /path/to/rater-pack/pairwise-responses.jsonl \
  --manifest-sha256 \
    552dfbd1ef0517bd632ea0540beca3505674229ddaf856f5b2f82073e63a6c40 \
  --output /path/to/rater-pack/response-lock.json
```

以实际由 `blind-eval init` 创建的文件名为准；如果文件名不同，先用
`blind-eval status` 和 pack README 核对，不要猜。

每个 pack 必须恰好完成：

- 144 scalar；
- 216 pairwise；
- 36 seeds；
- 单一 rater ID；
- 单一且真实的 research-experience years。

### Step 4：协调者安全回收

两份已锁定目录返回后，先复制到受控备份位置，不要直接编辑原件。

在仓库根目录执行：

```bash
shushu benchmark collect-responses \
  evals/blind-balanced-v1/raters/rater-a \
  --rater-dir evals/blind-balanced-v1/raters/rater-b \
  --blind-manifest-sha256 \
    552dfbd1ef0517bd632ea0540beca3505674229ddaf856f5b2f82073e63a6c40 \
  --blind-manifest evals/blind-balanced-v1/coordinator/manifest.json \
  --blind-key evals/blind-balanced-v1/coordinator/blind-key.jsonl \
  --output evals/blind-scalar-responses.jsonl \
  --pairwise-output evals/blind-pairwise-responses.jsonl
```

若命令失败：

- 不要手工删除字段；
- 不要重新计算一个假 lock；
- 不要拼接 JSONL；
- 逐字检查错误，定位是 hash、coverage、immutable field、rater identity、
  commitment 还是 response lock 不一致；
- 让对应评审者在原独立记录基础上修复程序性错误并重新锁定；
- 不得修改其科研判断来“让测试通过”。

### Step 5：解盲

仅在两份 response 都成功锁定并被 `collect-responses` 接受后：

```bash
shushu benchmark unblind evals/blind-scalar-responses.jsonl \
  --blind-pairwise evals/blind-pairwise-responses.jsonl \
  --blind-key evals/blind-balanced-v1/coordinator/blind-key.jsonl \
  --blind-manifest evals/blind-balanced-v1/coordinator/manifest.json \
  --output evals/judgments.jsonl \
  --pairwise-output evals/pairwise-judgments.jsonl
```

保留 pre-adjudication 原始结果。若之后需要讨论分歧，adjudication 必须另存，不能覆盖
用于 Cohen’s kappa 的独立结果。

### Step 6：评分并生成公开报告

```bash
shushu benchmark score evals/judgments.jsonl \
  --pairwise evals/pairwise-judgments.jsonl \
  --blind-scalar evals/blind-scalar-responses.jsonl \
  --blind-pairwise evals/blind-pairwise-responses.jsonl \
  --blind-key evals/blind-balanced-v1/coordinator/blind-key.jsonl \
  --blind-manifest evals/blind-balanced-v1/coordinator/manifest.json \
  --benchmark-seeds evals/benchmark-v1.jsonl \
  --run-matrix evals/completed-run-matrix.jsonl \
  --execution-manifest evals/execution/codex-gpt-5.6-sol/manifest.json \
  --results-root . \
  --output evals/public-results.json
```

必须人工检查 `evals/public-results.json`：

- `publishable` 必须为 `true`；
- primary evidence 必须是 human；
- 至少两名 research-experienced human raters；
- collective coverage 为 60；
- shared complete seeds 至少 12；
- scalar judgments 为 288；
- pairwise judgments 为 432；
- scalar Cohen’s kappa 已报告；
- pairwise Cohen’s kappa 已报告；
- retrieval、evidence、lineage、idea、calibration 指标族齐全；
- benchmark、run matrix、execution manifest、blind responses、key、manifest 和 judgments
  的 hash 全部存在且匹配。

若效果并未优于 baseline：

- 仍然公开真实结果；
- README 不得写“新版更优”；
- 将 negative/neutral result 和不确定性写清楚；
- 稳定版是否发布由证据和产品定位决定，不得美化指标。

### Step 7：README 效果声明门槛

在修改任何 effectiveness claim 前先运行：

```bash
shushu release-check \
  --readme README.md \
  --public-evaluation evals/public-results.json
```

然后同步更新：

- `README.md`；
- `README_EN.md`；
- `README_ZH.md`；
- `docs/acceptance-audit.md`；
- `docs/implementation-status.md`；
- `docs/release-checklist.md`；
- `CHANGELOG.md`。

三语门槛：

```bash
shushu release-check \
  --readme README.md \
  --public-evaluation evals/public-results.json

shushu release-check \
  --readme README_EN.md \
  --public-evaluation evals/public-results.json

shushu release-check \
  --readme README_ZH.md \
  --public-evaluation evals/public-results.json
```

README 中的数值必须能在同一份 hash-bound public report 中逐项找到，禁止：

- cherry-pick 单个有利指标；
- 用 LLM judge 代替 human-primary；
- 把缺失评价写成零失败；
- 用“显著提升”等措辞而没有相应统计证据。

### Step 8：稳定版发布

发布前：

```bash
.venv/bin/ruff check .
.venv/bin/pytest -q
.venv/bin/shushu check
.venv/bin/shushu benchmark validate evals/benchmark-v1.jsonl

.venv/bin/python -m build --no-isolation
.venv/bin/python scripts/check_distribution.py dist
```

然后：

1. 将版本从 `0.2.0a1` 更新为稳定版版本。
2. 更新 Changelog 日期和稳定版限制。
3. 确认 distribution 不含不应公开的 pre-unblinding artifacts。
4. 提交到新分支，开 PR。
5. 等待 Python 3.9/3.12 CI 全绿。
6. 合并后在最终 main commit 上构建。
7. 创建 GitHub stable Release。
8. 上传 wheel 和 sdist。
9. 在 Release notes 中记录两个 SHA-256 和 public report SHA-256。
10. 从 GitHub 重新下载 wheel，在干净环境安装并运行 `shushu check`。

## 5. 代码目录结构

```text
shushu-novelty-finder/
├── .github/workflows/
│   └── ci.yml                         # PR/main 的 Python 3.9/3.12 CI
├── docs/
│   ├── AI-HANDOFF.md                  # 本交接文档
│   ├── acceptance-audit.md            # 14 条最终验收与实证记录
│   ├── architecture.md                # 产品边界、运行时和 phase model
│   ├── evaluation-protocol.md         # 盲评、回收、解盲、评分协议
│   ├── rater-recruitment.md           # 真人评审招募、pilot 和工作量
│   ├── release-checklist.md            # Alpha/稳定版发布门槛
│   ├── implementation-status.md        # 当前实现状态和限制
│   ├── failure-cases.md                # 必须披露的失败案例
│   ├── migration-v0.2.md               # v0.1 -> v0.2 迁移
│   ├── quickstart.md
│   ├── usage.md
│   └── adr/
│       ├── 0001-lineage-first-runtime.md
│       ├── 0002-evidence-levels-fail-closed.md
│       ├── 0003-human-primary-public-claims.md
│       └── 0004-balanced-overlap-human-rating.md
├── evals/
│   ├── benchmark-v1.jsonl              # 固定 60-seed benchmark
│   ├── retrieval-topics-v1.jsonl       # 固定 20-topic live retrieval suite
│   ├── adapters.codex-gpt-5.6-sol.json # 已完成矩阵使用的 pinned adapter
│   ├── completed-run-matrix.jsonl       # 240 个 hash-complete outputs（忽略）
│   ├── execution/                       # 执行 manifest/checkpoints（忽略）
│   ├── blind-balanced-v1/               # 当前双人盲评包（忽略）
│   ├── live-retrieval-*/                # 保留的真实检索运行和失败证据
│   ├── judgment.example.jsonl           # 仅 schema 示例，不是人类证据
│   ├── pairwise-judgment.example.jsonl  # 仅 schema 示例，不是人类证据
│   ├── prompts/
│   ├── cases/
│   └── checks/
├── examples/
│   ├── runs/
│   │   ├── rag-known-scoop/
│   │   ├── lora-known-scoop/
│   │   └── clip-known-scoop/
│   ├── evidence-ledger/
│   ├── lineage-mini/
│   └── *.md                             # 使用、好坏输出和真实案例
├── scripts/
│   ├── build_real_example_runs.py
│   ├── check_distribution.py
│   ├── normalize_papers.py
│   ├── search_arxiv.py
│   └── validate_report.py
├── skills/
│   └── shushu-novelty-finder/
│       ├── SKILL.md                     # LLM 行为策略和研究判断流程
│       ├── agents/openai.yaml
│       └── references/                  # rubric、baseline、领域规则等
├── src/shushu_novelty/
│   ├── cli.py                           # 主 CLI 路由
│   ├── errors.py                        # 统一异常/退出码
│   ├── io.py                            # 安全 I/O 与 hash 辅助
│   ├── normalization.py                 # 元数据规范化
│   ├── fulltext.py                      # PDF/HTML 获取和文本证据
│   ├── orchestrator/
│   │   ├── state.py                     # RunState 持久化
│   │   ├── phases.py                    # P0–P9 定义和 gate
│   │   └── navigator.py                 # next/resume/非覆盖导航
│   ├── retrieval/
│   │   ├── arxiv.py
│   │   ├── openalex.py
│   │   ├── semantic_scholar.py
│   │   ├── openreview.py
│   │   ├── multi.py                     # 四源统一入口
│   │   ├── dedup.py                     # canonical dedup
│   │   ├── replay.py                    # manifest/replay
│   │   └── http.py                      # retry/timeout/backoff
│   ├── schemas/
│   │   ├── base.py
│   │   ├── paper.py
│   │   ├── claim.py
│   │   ├── fulltext.py
│   │   ├── lineage.py
│   │   ├── gap.py
│   │   ├── idea.py
│   │   ├── collision.py
│   │   ├── reviewer.py
│   │   ├── report.py
│   │   ├── run_state.py
│   │   ├── benchmark.py
│   │   ├── benchmark_adapter.py
│   │   ├── blind_evaluation.py
│   │   ├── evaluation.py
│   │   └── retrieval_benchmark.py
│   └── evaluation/
│       ├── benchmark.py                 # plan/collect/merge/blind/unblind
│       ├── runner.py                    # 外部系统执行和 resume
│       ├── codex_adapter.py             # pinned Codex adapter
│       ├── blinding.py                  # pack、manifest、lock、collect
│       ├── rater_cli.py                 # blind-eval
│       ├── metrics.py                   # aggregate 和 kappa
│       ├── release.py                   # README/public claim gate
│       ├── report.py
│       ├── retrieval_benchmark.py
│       ├── citation.py
│       ├── lineage.py
│       ├── gap.py
│       ├── idea.py
│       ├── collision.py
│       ├── reviewer.py
│       └── structural.py
├── tests/                               # 117 项自动测试
├── pyproject.toml
├── requirements-dev.lock
├── README.md
├── README_EN.md
├── README_ZH.md
├── CHANGELOG.md
└── .gitignore
```

## 6. 关键模块与修改影响范围

| 修改目标 | 主要文件 | 必须联动检查 |
|---|---|---|
| CLI 参数/命令 | `src/shushu_novelty/cli.py` | `pyproject.toml` entry points、CLI tests、docs |
| P0–P9 阶段 | `orchestrator/phases.py`, `navigator.py`, `state.py` | schemas、example runs、report gate |
| 检索连接器 | `retrieval/*.py` | replay、dedup、live benchmark、failure logs |
| Paper/Claim schema | `schemas/paper.py`, `claim.py`, `fulltext.py` | P3 gate、examples、JSONL fixtures |
| Lineage/Gap/Idea | 对应 schemas + `evaluation/*.py` | collision、reviewer、metrics |
| 盲评包 | `evaluation/blinding.py`, `rater_cli.py` | manifest commitment、pack hashes、tests |
| 公开评分 | `evaluation/metrics.py`, `report.py` | release gate、README claims、protocol |
| 发布门槛 | `evaluation/release.py` | 三语 README、release tests |
| 依赖 | `pyproject.toml` | Python 3.9 重建 lock、CI、clean build |

任何 schema 变更都应考虑：

- 是否需要提升 `schema_version`；
- 是否会让已有运行产物无法 replay；
- 是否影响 blind manifest；
- 是否影响 `public-results.json` 的可发布性；
- 是否需要迁移或向后兼容。

## 7. 不能公开或随意修改的材料

`.gitignore` 明确忽略：

```text
evals/blind-*/
evals/completed-run-matrix.jsonl
evals/execution/
```

原因不是这些文件不重要，而是它们组合起来可能泄露 system identity。

在两位评审者锁定响应前：

- 不提交 `coordinator/blind-key.jsonl`；
- 不提交带 system name 的原始输出；
- 不把 coordinator 目录发给评审者；
- 不把两个 rater pack 发给同一个人；
- 不修改已 commitment 的 rater-side 文件；
- 不公布能由 output hash 反查 system identity 的映射。

公开结果前应审查 distribution：

```bash
python scripts/check_distribution.py dist
```

## 8. 常用验证命令

完整本地门槛：

```bash
.venv/bin/ruff check .
.venv/bin/pytest -q
.venv/bin/shushu check
.venv/bin/shushu benchmark validate evals/benchmark-v1.jsonl
.venv/bin/shushu validate evals/retrieval-topics-v1.jsonl \
  --schema retrieval-benchmark-topic
.venv/bin/shushu release-check --readme README.md
.venv/bin/shushu release-check --readme README_EN.md
.venv/bin/shushu release-check --readme README_ZH.md

for run in examples/runs/*-known-scoop; do
  .venv/bin/shushu next --run "$run"
done

.venv/bin/python -m build --no-isolation
.venv/bin/python scripts/check_distribution.py dist
```

GitHub 状态：

```bash
gh auth status
gh pr list
gh run list --branch main --workflow CI --limit 5
gh release view v0.2.0a1
```

## 9. 当前已知限制

- 真人盲评尚未完成。
- OpenAlex anonymous path 适合 bounded smoke/eval，不适合长期生产配额。
- raw HTTP response cache 未实现；当前 replay 基于 canonical records 和 failure logs。
- PDF 抽取不提供 OCR，也不会自动完成语义蕴含判断。
- lineage relation classification 仍有 LLM-assisted 部分。
- ResearchStudio-Idea 仅在许可和环境允许时作为外部参考，不是必选 baseline。
- v0.2 非目标：Web UI、图数据库、向量数据库服务、自动论文写作、自由多 Agent 框架。

## 10. 完成定义

Alpha 已完成。只有以下全部为真，才可说完整稳定版工程升级完成：

- 两名真实科研评审者完成并锁定独立盲评；
- `collect-responses`、unblind、score 全部通过；
- `public-results.json` 为 human-primary 且 `publishable: true`；
- scalar 和 pairwise Cohen’s kappa 已公开；
- 所有 metric families 完整；
- README 的每个 comparative claim 都有同一份公开报告支持；
- 三语 release gate 全部通过；
- 最终版本、Changelog、CI、wheel、sdist、distribution audit 和远端安装验证通过；
- stable GitHub Release 已发布；
- 公开内容未泄露不应公开的 coordinator 或 pre-unblinding 资料。

## 11. 接手 AI 的第一条回复建议

接手时不要先重跑 240 个系统，也不要重新生成盲评包。先报告：

```text
我已确认工程 Alpha、240-run matrix 和 balanced-overlap blind pack 已完成。
当前任务是接收两名真实评审者的已锁定目录，验证 manifest commitment，
执行 collect-responses → unblind → score → release-check，并根据真实结果决定
README comparative claim 和 stable v0.2.0 发布。
```

如果还没有真人目录，应转入招募/协调流程，而不是伪造评分或重复工程实现。

