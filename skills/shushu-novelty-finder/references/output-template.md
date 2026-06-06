# Output Template

Use this report format for full novelty-finding tasks. The output should read like a compact literature review plus a strict paper-idea audit, not a generic brainstorm.

The Skill has two primary output modes:

- **Literature Lineage Mode**: first map the closest papers and their concrete innovation points.
- **Idea Generation Mode**: generate and stress-test paper-worthy innovation points from a seed paper or user direction.

If the user asks for both, output Mode 1 first, then Mode 2.

## Mode 1. Literature Lineage Output

Use this mode when the user asks for paper lineage, very similar papers, current task map, trend review, or "先梳理再给 idea".

### 0. Scope And Task Map

```text
User direction or seed paper:
Research field:
Core task:
Subtasks:
Canonical input:
Canonical output:
Standard datasets:
Standard metrics:
Typical baselines:
Deployment or system setting:
What counts as meaningful progress:
Directions intentionally excluded:
Search status: verified / partial / placeholder-only / not searched
```

### 1. Closest-Paper Clusters

Group papers by method route, task framing, benchmark route, or historical stage.

```text
Cluster:
Why this cluster is close to the user's direction:
Representative papers:
Shared assumption:
Shared contribution type:
What became saturated:
What remains open:
```

### 2. Per-Paper Innovation Cards

For every important extremely similar paper, include a card. Do not only summarize the paper. Extract its innovation points.

```text
Paper:
Year:
Venue/source:
URL / DOI / arXiv:
Evidence status: verified / partial / candidate / unverified
Relationship to user direction: ancestor / closest prior / sibling / follow-up / benchmark / contrary evidence
Task:
Input:
Output:
Datasets:
Metrics:
Main method:
Innovation point 1:
Innovation point 2:
Innovation point 3:
Contribution type: method / dataset / benchmark / metric / system / analysis / application
What it solved:
What it did not solve:
Why it matters for the user's direction:
What idea space it blocks:
What idea space it leaves open:
```

### 3. Literature Timeline

```text
Stage:
Years:
Representative papers:
Main task definition:
Main method family:
Dataset / metric pattern:
What changed from previous stage:
What became saturated:
What remained weak:
```

### 4. Trend Matrix

```text
Time period | Representative papers | Task shift | Method shift | Dataset/metric shift | Saturated contribution | Open gap
```

### 5. Gap Audit

For each gap:

```text
Gap:
Gap type: explicit limitation / future work / cross-paper pattern / benchmark absence / implementation absence / inferred gap
Evidence type:
Supporting papers:
Why this matters:
Why it may be a bad idea:
Confidence:
```

### 6. Lineage Verdict

```text
Most saturated idea:
Most defensible gap:
Most dangerous overlap risk:
Best direction to continue:
What must be verified next:
```

## Mode 2. Idea Generation Output

Use this mode when the user asks for innovation points, paper ideas, extension directions, or whether a direction can become a paper.

### 0. Closest-Prior Snapshot

```text
Seed paper or direction:
Closest prior work:
What those papers already did:
What cannot be claimed as new:
Open space for ideas:
Evidence status:
```

### 1. Executive Recommendation

Give the best 1-3 recommended ideas.

```text
Recommended idea:
Novelty level: weak / medium / strong
Reasonableness verdict: not reasonable yet / weak but useful / reasonable but underspecified / reasonable / high-risk but worth piloting
Paper-readiness verdict: not ready / pilot-ready / workshop-ready / main-track candidate / technical-report-only
Best paper type:
Fallback paper type:
Why this is the best option:
Evidence basis:
Strongest reason for:
Strongest reason against:
Minimum experiment:
Baseline plan:
Main risk:
Likely accept reason:
Likely reject reason:
Continue / narrow / downgrade / kill:
```

### 2. Novelty Candidates

Generate concrete ideas and separate them into weak, medium, and strong.

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
Feasibility:
Minimum experiment:
Baseline plan:
Risks:
Reasonableness verdict:
Best target output:
```

### 3. Idea Reasonableness Audit

For each top idea, test whether the idea actually stands up.

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
Strongest reason for:
Strongest reason against:
Decision: pursue / narrow / verify / downgrade / pivot / stop
```

### 4. Paper Type Routing

For each top idea:

```text
Best paper type:
Fallback paper type:
Why this type fits:
Required evidence:
Required baselines:
Main reviewer risk:
Readiness verdict:
```

### 5. Paper Thesis Card

For the top idea:

```text
Working title:
Paper type:
Core claim:
Why now:
What existing work assumes:
What breaks that assumption:
What evidence supports the claim:
What reviewers may reject:
```

### 6. Experiment Card

For the top idea:

```text
Claim:
Independent variable:
Dependent variable:
Datasets:
Metrics:
Baselines:
Ablations:
Robustness checks:
Falsification result:
```

### 7. Baseline Decision

```text
Minimum baselines:
Strong baselines:
Why each baseline is necessary:
What result would make the idea look weak:
What result would make the idea publishable:
```

### 8. Related Work Argument Map

```text
Closest prior work:
Follow-up work:
Sibling work:
Contrary evidence:
How the proposed idea differs:
What should not be claimed:
```

### 9. Reviewer Objection Pre-Mortem

For each top idea, include at least three objections.

```text
Likely reviewer objection:
Why the objection is plausible:
Evidence needed to answer it:
Current defense:
Weakness in current defense:
Action to strengthen:
Verdict impact: no change / downgrade / kill
```

### 10. Kill / Continue Criteria

```text
Continue condition:
Narrow condition:
Downgrade condition:
Kill condition:
Next checkpoint:
Smallest next action that changes the decision:
```

### 11. Threats To Validity

```text
Internal validity:
External validity:
Dataset validity:
Metric validity:
Reproducibility risk:
Reviewer concern:
```

### 12. Next-Step Plan

Give a concrete plan:

- papers to verify next;
- datasets or benchmarks to inspect;
- baseline to reproduce;
- first experiment;
- decision checkpoint.

### 13. Uncertainty And Search Limits

State what the search may have missed. Do not hide weak evidence. If no verified search has been performed, mark all paper names as `placeholder`, `candidate`, or `unverified`.
