# Strong User Prompts

Use these prompts when you want `shushu-novelty-finder` to produce a decision-useful novelty audit instead of a broad brainstorm.

## 1. I Only Have A Direction

```text
Use shushu-novelty-finder.
Direction: RAG evaluation.
Goal: find a workshop-ready research idea.
Constraints: 2 months, limited compute, small annotation budget.
First narrow the scope. Ask at most 5 questions if needed.
Then produce a literature-backed novelty audit with claim-evidence map, baseline plan, reviewer objections, and paper-readiness verdict.
```

## 2. I Have A Seed Paper

```text
Use shushu-novelty-finder.
Seed paper: <title / abstract / arXiv / DOI / PDF>.
Goal: find extension ideas that could become a paper.
First build a Seed Paper Card.
Then search or plan prior work, follow-up work, and sibling work.
For each candidate idea, give evidence status, evidence role, used-to-support claim, baseline plan, kill criteria, and readiness verdict.
```

## 3. I Have A Direction And A Seed Paper

```text
Use shushu-novelty-finder.
Direction: citation correctness in RAG evaluation.
Seed paper: <paper title and abstract>.
Use the direction to limit the search space and the paper to anchor the task boundary.
Do not drift into general RAG, long-context evaluation, or agent evaluation.
Return a scoped idea with claim-evidence map, reviewer objection pre-mortem, and minimum experiment.
```

## 4. I Already Have An Idea

```text
Use shushu-novelty-finder.
Idea: <my idea>.
I want to know whether this can become a workshop paper, main-track candidate, technical report, or only a pilot idea.
Please produce:
- Paper Thesis Card
- Experiment Card
- Baseline Decision Tree output
- Claim-Evidence Map
- Reviewer Objection Bank output
- Kill / Continue Criteria
- Paper-readiness Verdict
```

## 5. My Advisor Says The Novelty Is Weak

```text
Use shushu-novelty-finder.
My current idea is: <idea>.
Advisor feedback: the innovation is not clear enough.
Please diagnose whether the problem is scope, related work, baseline weakness, metric mismatch, or lack of falsifiable claim.
Then rewrite the idea into weak / medium / strong versions and say what evidence would upgrade it.
```

## 6. I Have Experimental Results

```text
Use shushu-novelty-finder.
Idea: <idea>.
Experimental result: <summary of result>.
Baselines run: <baselines>.
Datasets and metrics: <datasets and metrics>.
Please judge whether the result supports a paper claim.
Map each result to a claim, list reviewer objections, identify missing baselines, and give a paper-readiness verdict.
```

## 7. I Need To Decide Whether To Stop

```text
Use shushu-novelty-finder.
Idea: <idea>.
What I have checked: <papers / baselines / pilot results>.
What failed: <failure details>.
Use kill / continue criteria to decide whether I should continue, narrow, downgrade, or kill this idea.
Give the smallest next action that would change the decision.
```

## 8. I Want A Paper Type Recommendation

```text
Use shushu-novelty-finder.
Idea: <idea>.
Possible output types: method paper, benchmark paper, analysis paper, system paper, dataset paper, negative result paper, technical report.
Route this idea to the best paper type and fallback type.
For each type, list required evidence, required baselines, reviewer risk, and readiness verdict.
```
