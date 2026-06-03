# Paper Type Router

Use this reference to decide what kind of paper an idea can become. Different paper types need different evidence, baselines, and reviewer defenses.

## Router Format

```text
Idea:
Best paper type:
Alternative paper type:
Why this type fits:
Required evidence:
Required baselines:
Main reviewer risk:
Readiness verdict:
```

## Paper Types

### Method Paper

Best when:

- there is a clear algorithmic or modeling change;
- the method can be compared against strong baselines;
- ablations can isolate the contribution.

Needs:

- method delta;
- strong baseline;
- ablation;
- robustness or generalization check.

Reviewer risk:

```text
This is an incremental tweak or an engineering trick.
```

### Benchmark Paper

Best when:

- existing evaluation misses an important failure mode;
- task definition is clear;
- annotation or data construction is reproducible.

Needs:

- task definition;
- dataset or benchmark construction;
- annotation protocol;
- multiple baselines;
- metric justification.

Reviewer risk:

```text
This is a dataset release without insight.
```

### Analysis Paper

Best when:

- the contribution is a surprising empirical finding;
- the experiment isolates a hidden assumption;
- the result changes how researchers evaluate or build systems.

Needs:

- controlled comparison;
- multiple settings;
- contrary hypothesis;
- explanation of why the finding matters.

Reviewer risk:

```text
This is descriptive and does not explain why the pattern happens.
```

### System Paper

Best when:

- the contribution is an end-to-end system under real constraints;
- engineering tradeoffs matter;
- deployment, latency, cost, or reliability is central.

Needs:

- system design;
- workload;
- baseline system;
- failure analysis;
- reproducibility boundary.

Reviewer risk:

```text
This is an engineering report without a generalizable lesson.
```

### Dataset Paper

Best when:

- data is new, useful, and hard to collect;
- annotation quality can be verified;
- the dataset enables a task or evaluation not previously possible.

Needs:

- data collection protocol;
- annotation protocol;
- quality control;
- baseline results;
- licensing and reproducibility notes.

Reviewer risk:

```text
This dataset is too small, too private, or not useful beyond one setting.
```

### Negative Result Paper

Best when:

- a common assumption fails under controlled conditions;
- the negative result changes a design or evaluation decision;
- the failure is reproducible.

Needs:

- strong baseline;
- careful controls;
- clear implication;
- alternative explanations checked.

Reviewer risk:

```text
The failure is caused by weak implementation or unfair setup.
```

### Technical Report

Best when:

- the idea is useful but not research-novel enough;
- baselines are incomplete;
- data is private;
- the output is mostly guidance, tooling, or pilot results.

Needs:

- honest limitations;
- reproducible parts;
- practical value;
- next-step plan.

Reviewer risk:

```text
Do not overclaim this as a main-track paper.
```

## Final Output Requirement

For every top idea, choose one primary paper type and one fallback type. If the paper type is unclear, verdict cannot be above `pilot-ready`.
