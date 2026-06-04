# Output Checklist

Use this checklist after a `shushu-novelty-finder` run. It is the human-facing companion to `evals/checks/output-checklist.md`; both should enforce the same standard: the Skill must generate evidence-backed research ideas and then decide whether those ideas are reasonable, not just produce plausible brainstorming.

## Scope and Input Mode

- [ ] The output identifies `Direction Mode`, `Seed Paper Mode`, or `Hybrid Mode`.
- [ ] The output states assumptions if the user did not provide enough detail.
- [ ] The task, input, output, dataset, metric, and target venue level are clear enough to evaluate.
- [ ] The output narrows over-broad topics before claiming novelty.

## Literature and Evidence Hygiene

- [ ] Representative papers include title, year, venue/source, and relevance.
- [ ] Accepted papers, preprints, surveys, benchmark papers, and engineering artifacts are separated.
- [ ] Each key paper has an `Evidence status`: `verified`, `candidate`, `placeholder`, or `user-provided`.
- [ ] Each key paper has an `Evidence role`: foundation, contrast, benchmark, negative result, method component, dataset, evaluation protocol, or reviewer concern.
- [ ] Each key paper states which claim it supports.
- [ ] Candidate or placeholder papers are not used as verified support.
- [ ] The output does not use one paper to support a field-wide claim.

## Claim-Evidence Map

- [ ] The top claims are listed explicitly.
- [ ] Each top claim is connected to supporting, contrasting, or missing evidence.
- [ ] Unsupported claims are marked as hypotheses, not facts.
- [ ] The output names what evidence would change the conclusion.

## Gap Audit

- [ ] Each gap has a gap type.
- [ ] Each gap has an evidence label.
- [ ] Inferred gaps are marked as hypotheses.
- [ ] The output avoids saying "nobody has done this" unless the evidence base justifies it.

## Novelty Candidate Generation

- [ ] The output generates concrete innovation-point candidates, not only literature summary.
- [ ] Ideas are separated into weak, medium, and strong.
- [ ] Each idea has a novelty mechanism.
- [ ] Each idea includes evidence, risk, feasibility, and a minimum experiment.
- [ ] The best 1-3 ideas are recommended with reasons.
- [ ] Weak ideas are not dressed up as paper-ready contributions.

## Idea Reasonableness Audit

- [ ] Each top idea has a one-sentence thesis.
- [ ] Each top idea names the closest prior work.
- [ ] Each top idea explains how it differs from closest prior work.
- [ ] Each top idea explains why it may be unreasonable.
- [ ] Each top idea includes the strongest reason for and strongest reason against pursuing it.
- [ ] Each top idea has a reasonableness verdict: `not reasonable yet`, `weak but useful`, `reasonable but underspecified`, `reasonable`, or `high-risk but worth piloting`.
- [ ] Each top idea states what result would support, weaken, and kill it.

## Paper Type Routing

- [ ] Each top idea is routed to a likely paper type: method, benchmark, dataset, evaluation, analysis, systems, or application paper.
- [ ] The output explains why that paper type fits the evidence and experiment plan.
- [ ] The claimed contribution matches the routed paper type.

## Baseline and Experiment Plan

- [ ] Baselines and ablations are specified for medium and strong ideas.
- [ ] The baseline plan includes strong, fair, and field-relevant comparisons.
- [ ] The experiment card includes minimum viable experiment, robustness check, and falsification test.
- [ ] The output does not call an idea strong without a baseline plan.

## Reviewer Objection Pre-Mortem

- [ ] The output includes at least one likely accept reason.
- [ ] The output includes at least one likely reject reason.
- [ ] The output states how to answer the strongest reviewer objection.
- [ ] Threats to validity are listed and tied to concrete mitigation or evidence needs.

## Kill / Continue Criteria

- [ ] Each top idea has at least one continue condition.
- [ ] Each top idea has at least one downgrade condition.
- [ ] Each top idea has at least one kill condition.
- [ ] The output says what result would make the idea not worth pursuing.

## Paper Readiness

- [ ] Medium and strong ideas include a Paper Thesis Card if Paper Mode is requested.
- [ ] The paper-readiness verdict is explicit.
- [ ] The verdict uses one of: `not ready`, `pilot-ready`, `workshop-ready`, `main-track candidate`, or `technical-report-only`.
- [ ] The final recommendation is decision-oriented: pursue, narrow, verify, pivot, or stop.
