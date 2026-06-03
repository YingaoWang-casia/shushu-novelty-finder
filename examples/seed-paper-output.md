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

## Prior Work Search Plan

Search for papers that the seed paper builds on:

- task anchors: papers defining the same task;
- method baselines: earlier methods compared by the seed paper;
- benchmark baselines: datasets and metrics used by the seed paper;
- survey support: surveys that map the broader area.

Required evidence format: Paper Evidence Cards with title, year, venue/source, paper type, evidence role, supported claim, and confidence.

## Follow-up Work Search Plan

Search for papers that came after the seed paper:

- papers that cite the seed paper;
- papers that reproduce or challenge the seed claim;
- papers that extend the method, benchmark, dataset, or metric;
- papers that expose limitations or negative results.

The search must separate accepted papers from arXiv preprints.

## Sibling Work Search Plan

Search for papers solving the same task with different assumptions:

- same task, different method;
- same method family, different dataset;
- same benchmark, different metric;
- same claim, different experimental design;
- adjacent subfield with transferable evaluation logic.

Sibling work is important because it prevents overclaiming novelty from a single paper lineage.

## Scope Lock

```text
Mode: Seed Paper Mode
Seed anchor: <paper title>
Research boundary: <specific task and output>
Included: prior work, follow-up work, sibling work in the same task family
Excluded: unrelated broad surveys, generic LLM application papers, work without comparable task / dataset / metric
Assumptions: search not yet performed; all placeholders are unverified
```

## Gap Audit

### Gap 1

```text
Gap: <candidate gap derived from explicit limitation or cross-paper pattern>
Gap type: explicit limitation / future work / cross-paper pattern / benchmark absence / inferred gap
Evidence type: <paper evidence card IDs after verification>
Supporting papers: <verified papers or placeholder until search>
Why it matters: <why the gap affects a claim, benchmark, method, dataset, or deployment setting>
Why it may be a bad idea: <reviewer objection, feasibility issue, or existing-work overlap risk>
Confidence: weak until verified
```

### Gap 2

```text
Gap: <candidate sibling-work gap>
Gap type: inferred gap
Evidence type: sibling-work comparison, requires verification
Supporting papers: <verified sibling papers or placeholder until search>
Why it matters: prevents staying too close to the seed paper
Why it may be a bad idea: may be only an application transfer without research novelty
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
Risks: high annotation or engineering burden; reviewers may reject if the task is not broadly useful
Best target output: main-track candidate only after strong evidence and clean experiments
```

## Paper-readiness Verdict

```text
Verdict: pilot-ready
Reason: a seed paper can anchor a useful project, but current novelty claims are not ready until prior, follow-up, and sibling work are checked.
Upgrade path: workshop-ready if a medium idea survives literature verification and has a baseline-backed experiment.
Downgrade path: technical-report-only if the idea is only a reimplementation, parameter tweak, or application transfer.
Next action: populate Paper Evidence Cards for 8-12 verified papers before writing a thesis claim.
```
