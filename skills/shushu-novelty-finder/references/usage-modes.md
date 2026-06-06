# Usage Modes

Use modes to control output depth. Do not always produce the heaviest report.

## Lite Mode

Use when the user wants quick direction screening.

Output:

- Research Scope Card
- 5-10 representative papers
- 3-5 likely gaps
- weak / medium / strong idea shortlist
- one next action

## Research Mode

Use when the user wants serious literature analysis.

Output:

- Research Scope Card
- venue cluster selection
- closest-paper lineage if the user asks for paper context or similar papers
- literature timeline
- trend matrix
- gap audit
- novelty ranking
- top 1-3 recommended ideas

## Literature Lineage Mode

Use when the user asks to first understand the direction, the task's paper history, extremely similar papers, or each paper's innovation points.

Trigger examples:

- "先梳理论文脉络"
- "极度相似的论文整体脉络"
- "把每篇论文创新点输出出来"
- "先综述这个方向，再给 idea"
- "closest papers and their contributions"

Output:

- Scope and Task Map
- Closest-Paper Clusters
- Per-Paper Innovation Cards
- Literature Timeline
- Trend Matrix
- Gap Audit
- Lineage Verdict

If the user also asks for ideas, continue with Idea Generation Mode after the lineage.

## Idea Generation Mode

Use when the user asks for innovation points, extension ideas, paper ideas, or whether a direction can become a paper.

Output:

- Closest-Prior Snapshot
- Weak / Medium / Strong Novelty Candidates
- Top 1-3 Recommended Ideas
- Idea Reasonableness Audit
- Paper Thesis Card for the top idea
- Experiment Card
- Baseline Decision
- Reviewer Objection Pre-Mortem
- Kill / Continue Criteria
- Paper-readiness Verdict

## Paper Mode

Use when the user wants a paper-ready plan.

Output:

- everything in Research Mode
- Paper Thesis Card
- Experiment Card
- Baseline Card
- Related Work Argument Map
- Story Card
- Threats Card
- Paper-readiness verdict

## Default routing

If the user only says "find ideas", use Lite Mode.

If the user mentions papers, trends, similar papers, "论文脉络", "极度相似", or "先综述", use Literature Lineage Mode. If ideas are also requested, append Idea Generation Mode.

If the user mentions papers, trends, or gaps but does not ask for detailed lineage, use Research Mode.

If the user mentions submission, A conference, thesis, workshop, experiments, baselines, or writing, use Paper Mode.
