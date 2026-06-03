# Eval Case: Seed Paper

## Input

```text
Use shushu-novelty-finder.
Seed paper: <title and abstract>.
Find novelty ideas based on this paper.
```

## Expected behavior

The Skill should first build a Seed Paper Card before recommending ideas.

## Required output checks

- Seed Paper Card exists.
- Task, input, output, dataset, metric, and claimed contribution are extracted or marked unknown.
- Prior work, follow-up work, and sibling work are searched separately.
- The seed paper is not treated as automatically authoritative.
- Suggested ideas distinguish explicit limitations from inferred gaps.
- Top ideas include paper-readiness verdicts.

## Failure signs

- Jumps directly to innovation ideas.
- Uses the seed paper title only.
- Ignores whether the seed paper is a survey, benchmark, method, dataset, or system paper.
