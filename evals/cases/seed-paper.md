# Eval Case: Seed Paper

## Input

```text
Use shushu-novelty-finder.
Seed paper: <title and abstract>.
Find novelty ideas based on this paper.
```

## Expected Behavior

The Skill should first build a Seed Paper Card before recommending ideas. It should use the seed paper to anchor the task boundary, not as proof that the paper's claims are correct.

## Required Output Checks

- has input mode: Seed Paper Mode
- Seed Paper Card exists
- Title, year, venue/source, and paper type are extracted or marked unknown
- task, input, output, dataset, metric, method, and claimed contribution are extracted or marked unknown
- limitations are separated into stated limitations and inferred limitations
- expansion keywords and excluded directions are listed
- prior work, follow-up work, and sibling work are searched or planned separately
- Paper Evidence Cards exist for key papers or are explicitly marked placeholder / candidate / unverified
- Claim-Evidence Map exists for the seed-paper extension claim
- suggested ideas distinguish explicit limitations from inferred gaps
- novelty candidates are ranked weak / medium / strong
- top ideas include paper type routing
- top ideas include baseline decision, minimum experiment, risks, reviewer objections, kill / continue criteria, and paper-readiness verdict

## Failure Signs

- jumps directly to innovation ideas
- uses only the seed paper title
- treats the seed paper as automatically authoritative
- ignores whether the seed paper is a survey, benchmark, method, dataset, system paper, or preprint
- proposes a strong idea without checking follow-up work
- gives an extension idea without a baseline or falsifiable claim
- does not separate accepted papers from preprints
- gives no reviewer objection section
- gives no downgrade or kill condition

## Passing Pattern

A passing output can downgrade its own confidence: `This is only pilot-ready until follow-up work confirms that the limitation remains open.`
