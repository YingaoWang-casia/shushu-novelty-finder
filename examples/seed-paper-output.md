# Example Output: Seed Paper Mode

This is a generic output example. It intentionally uses placeholders and does not invent a concrete paper.

## Input

```text
Seed paper: <paper title>
Abstract: <abstract>
```

## Seed Paper Card

```text
Title: <paper title>
Year: unknown until verified
Venue/source: unknown until verified
Paper type: unknown; classify as method / benchmark / dataset / survey / system / analysis / preprint after verification
Task: <task extracted from abstract>
Input: <input described by the paper>
Output: <output predicted, generated, retrieved, classified, or evaluated>
Dataset: <dataset if stated; otherwise unknown>
Metric: <metric if stated; otherwise unknown>
Main method: <main technical approach>
Claimed contribution: <claim made by the paper>
Limitations: <explicit limitations if stated; otherwise mark not stated>
Expansion keywords: <keywords for prior / follow-up / sibling search>
Excluded directions: <directions outside the user's goal or outside the paper's task>
```

## Scope Lock

```text
Mode: Seed Paper Mode
Seed anchor: <paper title>
Research boundary: <specific task and output>
Included: prior work, follow-up work, sibling work in the same task family
Excluded: unrelated broad surveys, generic LLM application papers, work without comparable task / dataset / metric
Assumptions: search not yet performed; all placeholders are unverified
```

## Search Plan

```text
Prior work: papers that define the task, baselines, datasets, and metrics used by the seed paper.
Follow-up work: papers that cite, extend, reproduce, or challenge the seed paper.
Sibling work: papers solving the same task with different assumptions, methods, datasets, or metrics.
Contrary evidence: papers showing the proposed extension already exists or is unnecessary.
```

## Paper Evidence Card Template

```text
Title: <paper title>
Year: <year>
Venue or source: <venue/source>
Paper type: method / benchmark / dataset / survey / system / analysis / preprint
URL, DOI, or arXiv id: <identifier>
Task: <task>
Dataset: <dataset>
Metric: <metric>
Main contribution: <contribution>
Why it is relevant: <why this paper matters for the seed extension>
Evidence status: placeholder / candidate / verified / rejected / needs follow-up check
Evidence role: task anchor / method baseline / benchmark baseline / limitation evidence / follow-up work / contrary evidence
Used to support which claim: <claim>
Confidence: weak / moderate / strong
```

## Claim-Evidence Map

```text
Claim: <seed-paper extension claim>
Claim type: novelty / feasibility / limitation / baseline / evaluation
Supporting papers: <verified papers or placeholders>
Contrary papers: <verified papers or placeholders>
Background papers: <verified papers or placeholders>
Evidence strength: weak until search is complete
What can be safely claimed: this is a candidate extension idea anchored by the seed paper.
What must not be claimed: the limitation is open or novel before follow-up work is checked.
Confidence: weak
Next verification step: populate Paper Evidence Cards for prior, follow-up, and sibling work.
```

## Gap Audit

```text
Gap: <candidate gap derived from explicit limitation or cross-paper pattern>
Gap type: explicit limitation / future work / cross-paper pattern / benchmark absence / inferred gap
Evidence type: placeholder until verified
Supporting papers: <verified papers or placeholder until search>
Why it matters: <why the gap affects a claim, benchmark, method, dataset, or deployment setting>
Why it may be a bad idea: <reviewer objection, feasibility issue, or existing-work overlap risk>
Confidence: weak until verified
```

## Novelty Ranking

### Weak

```text
Idea: <small extension or re-run of the seed paper>
Novelty level: weak
Evidence: seed paper plus one related line, unverified
Evidence type: extension of existing method
Feasibility: high
Minimum experiment: reproduce the seed setup or one baseline comparison
Baseline plan: seed-paper baseline plus one simple baseline
Risks: too incremental; reviewers may see it as a course project
Best target output: pilot-ready or technical-report-only
```

### Medium

```text
Idea: <scoped extension with a falsifiable claim and baseline plan>
Novelty level: medium
Evidence: seed paper limitation plus follow-up / sibling work contrast
Evidence type: explicit limitation plus cross-paper pattern
Feasibility: medium
Minimum experiment: compare seed method, strongest baseline, and proposed variant on a shared dataset and metric
Baseline plan: seed method, closest follow-up method, strongest sibling baseline
Risks: novelty collapses if follow-up papers already solve the limitation
Best target output: workshop-ready after literature verification
```

### Strong

```text
Idea: <new benchmark, task formulation, or method claim that changes evaluation assumptions>
Novelty level: strong only after contrary-evidence search
Evidence: requires verified absence or weakness in existing benchmarks / methods
Evidence type: benchmark absence plus contrary evidence search
Feasibility: medium-low
Minimum experiment: controlled dataset or benchmark plus baseline suite and ablations
Baseline plan: strongest method baseline, benchmark baseline, ablation, robustness check
Risks: high annotation or engineering burden; reviewers may reject if the task is not broadly useful
Best target output: main-track candidate only after strong evidence and clean experiments
```

## Paper Type Routing

```text
Best paper type: <method / benchmark / analysis / system / dataset / negative result / technical report>
Fallback paper type: technical report or workshop paper
Why this type fits: <reason>
Required evidence: prior, follow-up, sibling, and contrary evidence
Required baselines: seed method, closest prior baseline, strongest feasible sibling baseline
Main reviewer risk: extension may be too incremental or already covered by follow-up work
Readiness verdict: pilot-ready until search is complete
```

## Reviewer Objection Pre-Mortem

```text
Likely reviewer objection: this is just an incremental extension of the seed paper.
Why the objection is plausible: the seed paper already defines the task and method.
Evidence needed to answer it: follow-up work showing the limitation remains open.
Current defense: not enough evidence yet.
Weakness in current defense: no verified follow-up papers.
Action to strengthen: search citing papers and sibling work.
Verdict impact: downgrade if follow-up work already solves it.
```

```text
Likely reviewer objection: baselines are too weak.
Why the objection is plausible: seed-paper baselines may be outdated.
Evidence needed to answer it: strongest recent baseline and reproducible setup.
Current defense: baseline plan exists but is not populated.
Weakness in current defense: no verified baseline list.
Action to strengthen: identify recent accepted baselines.
Verdict impact: not workshop-ready until fixed.
```

```text
Likely reviewer objection: the claim is not falsifiable.
Why the objection is plausible: extension idea may be framed too broadly.
Evidence needed to answer it: clear metric and falsification result.
Current defense: minimum experiment can be defined.
Weakness in current defense: dataset and metric may be unknown.
Action to strengthen: lock dataset and metric.
Verdict impact: not ready if no falsifiable metric exists.
```

## Kill / Continue Criteria

```text
Continue condition: follow-up work has not solved the limitation and the minimum experiment can test the claim.
Narrow condition: the gap is broad but a specific task / metric / dataset remains under-tested.
Downgrade condition: only the seed paper supports the claim or baselines are too weak.
Kill condition: closest follow-up work already solves the claim, or no falsifiable metric exists.
Next checkpoint: verify 8-12 prior / follow-up / sibling papers.
Smallest next action that changes the decision: build a Claim-Evidence Map for the top extension claim.
```

## Paper-readiness Verdict

```text
Verdict: pilot-ready
Reason: a seed paper can anchor a useful project, but current novelty claims are not ready until prior, follow-up, sibling, and contrary work are checked.
Upgrade path: workshop-ready if a medium idea survives literature verification and has a baseline-backed experiment.
Downgrade path: technical-report-only if the idea is only a reimplementation, parameter tweak, or application transfer.
Next action: populate Paper Evidence Cards for 8-12 verified papers before writing a thesis claim.
```
