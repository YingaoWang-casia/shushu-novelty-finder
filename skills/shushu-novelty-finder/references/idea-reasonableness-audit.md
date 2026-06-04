# Idea Reasonableness Audit

Use this reference after generating novelty candidates. The goal is not only to produce ideas, but to judge whether each idea is logically defensible, experimentally testable, and worth pursuing.

A good idea should survive both directions:

1. positive construction: why this might be a real contribution;
2. negative stress test: why this might be trivial, already solved, infeasible, or unpublishable.

## Required Audit For Each Top Idea

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
``` 

## Novelty Mechanism

Name the actual mechanism that makes the idea novel. Use one or more of:

- new task definition;
- new evaluation target;
- new benchmark or dataset;
- new method component;
- new system constraint;
- new failure taxonomy;
- new empirical finding;
- new theoretical explanation;
- new application setting with non-trivial constraints;
- negative result that changes practice.

If the mechanism is only `apply existing method to another dataset`, downgrade unless the domain has a strong reason, hard data barrier, or surprising expected failure mode.

## Reasonableness Questions

Ask these before recommending an idea:

- Is the core claim specific enough to falsify?
- Is the idea different from the closest prior work in more than wording?
- Does the proposed experiment actually test the claimed novelty?
- Are the baselines strong enough that reviewers would accept the comparison?
- Can the user run the minimum experiment with available time, data, and compute?
- Would a negative result still teach something useful?
- Is there a clear audience: method researchers, benchmark builders, system builders, application researchers, or practitioners?
- Is the idea too broad to finish, or too narrow to matter?

## Verdict Labels

Use exactly one reasonableness verdict for each top idea:

- `reasonable`: evidence, scope, experiment, and contribution type align.
- `reasonable but underspecified`: promising, but task, metric, data, or baseline must be locked.
- `high-risk but worth piloting`: ambitious or weakly evidenced, but a small experiment could change the decision.
- `weak but useful`: not likely paper-worthy, but useful as a course project, demo, reproduction, or technical report.
- `not reasonable yet`: the idea is too vague, unsupported, infeasible, or likely already solved.

## Downgrade Triggers

Downgrade an idea if any of these hold:

- novelty depends on vague words such as adaptive, robust, efficient, agentic, or human-like without a measurable claim;
- closest prior work is not identified;
- no strong baseline is named;
- the evaluation cannot distinguish the new idea from existing methods;
- the required data or annotation is unrealistic;
- the idea only combines tools without a controlled contribution claim;
- the likely reviewer objection cannot be answered with an experiment;
- the benefit is only engineering convenience but the target is a main-track research paper.

## Upgrade Triggers

Upgrade an idea only when evidence supports it:

- it exposes a gap across multiple papers, benchmarks, or evaluation protocols;
- it makes a falsifiable claim that current baselines plausibly fail;
- it has a minimum experiment that can produce a clear decision;
- it has a fallback paper type if the strongest claim fails;
- it can answer the most likely reviewer objection with data;
- it remains useful even if the result is negative.

## Output Rule

Do not output only a list of ideas. For every recommended idea, include the reasonableness verdict and the strongest reason for and against it.
