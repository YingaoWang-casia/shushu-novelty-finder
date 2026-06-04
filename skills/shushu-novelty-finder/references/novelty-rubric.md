# Novelty Rubric

Use this reference to generate and grade candidate innovation points. Rank novelty by contribution structure, evidence, feasibility, and risk. Do not rank by impressive wording.

The Skill should first create candidate ideas, then grade and stress-test them. A good output is not just a list of possible topics; it is a decision table that helps the user know which ideas deserve time.

## Idea Construction Pattern

Each candidate idea should be built from:

```text
Observed gap or limitation:
Candidate idea:
Core claim:
Novelty mechanism:
Closest prior work:
Difference from closest prior work:
Minimum experiment:
Expected evidence if true:
Reason it might fail:
``` 

The novelty mechanism must be concrete. Prefer mechanisms such as a new task, new benchmark, new evaluation target, new method component, new failure taxonomy, new empirical finding, or useful negative result.

## Weak Novelty

A weak idea usually keeps the existing task and method family, but changes one controlled factor.

Typical forms:

- apply an existing method to a new dataset or domain;
- add missing ablations;
- compare overlooked baselines;
- improve engineering details;
- evaluate robustness under a narrow condition;
- add a small feature to an existing pipeline.

Weak novelty is useful for course projects, technical reports, early-stage experiments, and safe open-source demos. It is usually not enough for a strong paper unless execution or evidence is unusually good.

## Medium Novelty

A medium idea changes the evaluation setting, system framing, benchmark, dataset, or method composition in a meaningful way.

Typical forms:

- build a new benchmark or evaluation protocol;
- define a more realistic task setting;
- combine two research lines with a clear reason;
- create a failure taxonomy and diagnostic toolkit;
- introduce a reproducible system pipeline;
- show that a popular assumption fails under important conditions.

Medium novelty is often the best target for students: feasible, defensible, and useful for papers or strong open-source projects.

## Strong Novelty

A strong idea changes the task definition, evaluation paradigm, model architecture, theory, or dominant assumption.

Typical forms:

- define a new task that the field should care about;
- introduce a new benchmark that changes how progress is measured;
- propose a new architecture or training paradigm;
- provide a theoretical explanation for a recurring failure;
- challenge a mainstream route with strong evidence;
- expose a hidden limitation that invalidates common evaluation.

Strong novelty requires strong evidence. Always include failure risk, required resources, and minimum validation plan.

## Scoring Dimensions

For every idea, score qualitatively:

- novelty: low / medium / high;
- feasibility: low / medium / high;
- evidence support: weak / moderate / strong;
- expected impact: narrow / useful / field-shaping;
- risk: low / medium / high;
- reasonableness: not reasonable yet / weak but useful / reasonable but underspecified / reasonable / high-risk but worth piloting.

## Required Fields For Every Idea

```text
Idea:
Novelty level:
Novelty mechanism:
Core claim:
Evidence:
Evidence type:
Closest prior work:
Why it is not already solved:
Why it may be unreasonable:
Minimum experiment:
Feasibility:
Risks:
Reasonableness verdict:
Best target output:
```

## Sanity Rules

- Do not call an idea strong if the closest prior work is unknown.
- Do not call an idea paper-ready if the minimum experiment cannot falsify the core claim.
- Do not call an engineering pipeline a research contribution unless the controlled comparison isolates what is new.
- Do not upgrade an idea because it sounds fashionable. Upgrade only because the evidence, experiment, and contribution type align.
