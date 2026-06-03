# Failure Modes

Use this file to prevent shallow or fake novelty.

## Fake gap

The tool says a problem is unexplored, but it is actually studied under another name.

Mitigation:

- search synonyms;
- search dataset and metric names;
- search adjacent venues;
- check surveys and benchmark papers.

## Scope drift

The tool starts from one task but collects papers from several adjacent tasks, producing a noisy trend summary.

Mitigation:

- lock the Research Scope Card;
- explicitly list excluded directions;
- separate main-line papers from adjacent papers.

## Paper-list syndrome

The output lists many papers but does not explain how the field changed.

Mitigation:

- always build a Trend Matrix;
- group papers by stage;
- compare task, method, dataset, metric, and system setting.

## Preprint inflation

The output treats arXiv preprints as accepted top-venue evidence.

Mitigation:

- mark preprints;
- use preprints for latest signals, not settled trends;
- rely on accepted papers for core claims when possible.

## Novelty overclaim

The output turns a small extension into a strong contribution.

Mitigation:

- apply the novelty rubric;
- check whether the idea changes task, benchmark, metric, method, or system constraint;
- include a reject reason for every strong idea.

## Feasibility blindness

The idea is academically plausible but impossible for the user to execute.

Mitigation:

- check data access;
- check compute and time;
- identify minimum experiment;
- downgrade the idea if validation is unrealistic.

## Benchmark illusion

The idea proposes a benchmark without proving that current benchmarks are insufficient.

Mitigation:

- list existing benchmarks;
- explain why they are misaligned;
- define new input, output, metric, and baseline;
- include a small pilot benchmark plan.

## Reviewer mismatch

The idea may be useful but does not fit the target venue.

Mitigation:

- map the idea to venues;
- check contribution type expected by that community;
- rewrite target output as paper, workshop, dataset, system, or open-source project.
