# Input Router

Classify every request before searching.

## Direction Mode

Use when the user gives only a direction or keywords.

If the scope is broad, ask up to five questions. Good questions:

1. Which CS subfield and task do you mean?
2. Do you want a paper idea, thesis topic, open-source project, or course project?
3. Do you have a target venue or level?
4. What are your time, compute, data, and annotation constraints?
5. Do you prefer safe novelty or high-risk novelty?

Do not ask generic questions. Ask questions that change the search scope.

## Seed Paper Mode

Use when the user gives a paper title, abstract, DOI, arXiv link, PDF, or URL.

Do not ask many questions first. Parse the seed paper into a Seed Paper Card, then ask only if task, dataset, metric, or target scope remains ambiguous.

## Hybrid Mode

Use when the user gives both a direction and a paper. Use the direction to constrain the search and the paper to anchor the task.

## Default assumptions

If the user does not provide constraints, assume:

- time range: last 10 years, with emphasis on the last 5 years;
- output: paper-oriented research idea;
- field: computer science only;
- novelty ideas: 3 weak, 3 medium, 2 strong;
- every idea must include evidence, feasibility, risk, and minimum experiment.
