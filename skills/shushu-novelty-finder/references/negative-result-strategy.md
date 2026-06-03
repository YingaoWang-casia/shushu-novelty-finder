# Negative Result Strategy

A strong project does not always need a new method. A well-supported negative result can become a valuable paper if it changes what the field believes.

## When to consider a negative-result direction

Use this path when:

- a popular method performs well only under narrow conditions;
- a benchmark hides important failure modes;
- a simple baseline matches or beats complex methods;
- reported gains disappear under fair comparison;
- a common metric disagrees with human or deployment outcomes;
- an assumption appears repeatedly but is rarely tested.

## Negative Result Card

```text
Claim being challenged:
Papers that support the claim:
Controlled condition to test:
Alternative explanation to rule out:
Reproduction setup:
Failure condition:
Evidence needed:
Why the result matters:
What remains true about the original claim:
```

## Strong negative-result patterns

- Reproduce a known claim, then show where it breaks.
- Show benchmark-model ranking changes under realistic settings.
- Show a metric rewards behavior that users or experts reject.
- Show a simple baseline is competitive under fair constraints.
- Show robustness failures are systematic, not anecdotal.

## Weak negative-result patterns

Avoid these:

- failing to reproduce without checking implementation details;
- using a weaker setup than the original paper;
- attacking a strawman baseline;
- testing only one dataset or one model;
- presenting a bug as a research conclusion.

## Required safeguards

- Be fair to the original work.
- State what the original work still gets right.
- Distinguish implementation failure from conceptual failure.
- Include enough controls to make the negative result credible.
