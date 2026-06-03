# Paper Story Checklist

A paper idea must become a coherent story before it is paper-ready.

## Introduction logic

A strong introduction usually follows this chain:

1. The problem matters.
2. Existing work appears to solve it.
3. Existing work actually misses a specific setting, metric, assumption, or failure mode.
4. This miss changes the conclusion or limits deployment.
5. The paper proposes a method, benchmark, dataset, or analysis that directly addresses it.
6. The experiments verify the claim.

## Story Card

```text
Opening motivation:
Why the problem matters now:
What prior work has achieved:
Key missing piece:
Core insight:
Our contribution:
Why the contribution is timely:
Main experiment that proves the story:
Most likely reviewer objection:
```

## Contribution statement

Produce 3-4 contribution bullets in this format:

```text
- We identify ...
- We introduce ...
- We show ...
- We release / analyze / benchmark ...
```

Avoid vague bullets such as:

- We propose a novel framework.
- We improve performance.
- We conduct extensive experiments.

## Story failure cases

Downgrade the idea if:

- the motivation depends on hype rather than a concrete technical failure;
- the gap does not change evaluation or system behavior;
- the proposed solution does not directly test the claimed gap;
- the contribution bullets could apply to many unrelated papers.
