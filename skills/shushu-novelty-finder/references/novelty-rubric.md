# Novelty Rubric

Rank novelty by contribution structure, evidence, feasibility, and risk. Do not rank by impressive wording.

## Weak novelty

A weak idea usually keeps the existing task and method family, but changes one controlled factor.

Typical forms:

- apply an existing method to a new dataset or domain;
- add missing ablations;
- compare overlooked baselines;
- improve engineering details;
- evaluate robustness under a narrow condition;
- add a small feature to an existing pipeline.

Weak novelty is useful for course projects, technical reports, early-stage experiments, and safe open-source demos. It is usually not enough for a strong paper unless execution or evidence is unusually good.

## Medium novelty

A medium idea changes the evaluation setting, system framing, benchmark, dataset, or method composition in a meaningful way.

Typical forms:

- build a new benchmark or evaluation protocol;
- define a more realistic task setting;
- combine two research lines with a clear reason;
- create a failure taxonomy and diagnostic toolkit;
- introduce a reproducible system pipeline;
- show that a popular assumption fails under important conditions.

Medium novelty is often the best target for students: feasible, defensible, and useful for papers or strong open-source projects.

## Strong novelty

A strong idea changes the task definition, evaluation paradigm, model architecture, theory, or dominant assumption.

Typical forms:

- define a new task that the field should care about;
- introduce a new benchmark that changes how progress is measured;
- propose a new architecture or training paradigm;
- provide a theoretical explanation for a recurring failure;
- challenge a mainstream route with strong evidence;
- expose a hidden limitation that invalidates common evaluation.

Strong novelty requires strong evidence. Always include failure risk, required resources, and minimum validation plan.

## Scoring dimensions

For every idea, score qualitatively:

- novelty: low / medium / high;
- feasibility: low / medium / high;
- evidence support: weak / moderate / strong;
- expected impact: narrow / useful / field-shaping;
- risk: low / medium / high.

## Required fields for every idea

```text
Idea:
Novelty level:
Evidence:
Evidence type:
Why it is not already solved:
Minimum experiment:
Feasibility:
Risks:
Best target output:
```
