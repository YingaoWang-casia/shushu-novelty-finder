# Scope Narrowing Playbook

Use this reference when the user gives a broad direction. The Skill should narrow before search, otherwise the literature audit becomes shallow and random.

## Narrowing Dimensions

Use these dimensions in order:

```text
1. Subfield
2. Task
3. Input
4. Output
5. Dataset / benchmark
6. Metric
7. User constraint
8. Paper type
9. Failure mode
10. Excluded directions
```

## Broad-to-Scoped Pattern

```text
Broad direction:
Narrow by task:
Narrow by setting:
Narrow by failure type:
Narrow by metric:
Narrow by resource:
Scoped idea:
Excluded directions:
```

## Example: RAG Evaluation

```text
Broad direction: RAG evaluation
Narrow by task: citation correctness
Narrow by setting: long-form QA with retrieved evidence
Narrow by failure type: unsupported citations and missing evidence coverage
Narrow by metric: citation precision, evidence coverage, answer utility
Narrow by resource: 2 months, limited compute, small annotation budget
Scoped idea: low-cost citation support audit for long-form RAG answers
Excluded directions: retriever training, generic long-context evaluation, agent planning
```

## Example: Speech Turn-Taking

```text
Broad direction: speech turn-taking
Narrow by task: interruption handling
Narrow by setting: real-time spoken dialogue agent
Narrow by failure type: delayed response and false interruption
Narrow by metric: response timing, interruption accuracy, false alarm, miss rate
Narrow by resource: public data only, limited training budget
Scoped idea: evaluation protocol for interruption timing in full-duplex speech agents
Excluded directions: ASR accuracy, diarization, generic dialogue policy
```

## Example: LLM-as-a-Judge

```text
Broad direction: LLM-as-a-Judge
Narrow by task: judging factual consistency in generated explanations
Narrow by setting: pairwise comparison with human-labeled subset
Narrow by failure type: judge bias toward longer answers and confident wording
Narrow by metric: agreement with human labels, calibration, bias score
Narrow by resource: small human annotation budget
Scoped idea: bias-aware judge protocol for factual explanation evaluation
Excluded directions: general chatbot preference ranking, reward modeling
```

## Clarifying Questions

Ask at most five questions:

```text
1. Which task inside this direction do you care about?
2. What is the input and output?
3. What dataset or benchmark can you use?
4. What metric should prove the claim?
5. What time, compute, and annotation limits do you have?
```

If the user does not answer, continue with assumptions and mark them.

## Final Output Requirement

Before any large literature review, output a Research Scope Card and Excluded Directions.
