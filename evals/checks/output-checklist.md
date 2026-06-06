# Output Checklist

A qualified `shushu-novelty-finder` output must satisfy the following checks.

- has input mode
- has scope card
- if Literature Lineage Mode is requested, has closest-paper clusters
- if Literature Lineage Mode is requested, has per-paper innovation cards
- if Literature Lineage Mode is requested, each important paper has concrete innovation points
- if Literature Lineage Mode is requested, states what each paper solved and left open
- has concrete paper names or explicitly marks placeholder / unverified
- has paper evidence cards
- has evidence status for key papers
- has evidence role for key papers
- states which claim each key paper supports
- has claim-evidence map for top claims
- has trend matrix
- has gap evidence labels
- generates concrete novelty candidates, not only literature summary
- has weak / medium / strong novelty ranking
- each top idea has a novelty mechanism
- each top idea has closest prior work
- each top idea explains why it is not already solved
- each top idea explains why it may be unreasonable
- each top idea has a reasonableness verdict
- each top idea has strongest reason for and strongest reason against
- has paper type routing for top ideas
- has minimum experiments
- has baseline plan for top ideas
- has reviewer objection pre-mortem
- has kill / continue criteria
- has risks
- has paper-readiness verdict
- does not claim "nobody has done this" without evidence
- separates preprints from accepted papers
- does not use candidate or placeholder papers as verified support

## Additional Paper-Readiness Checks

- top idea has a Paper Thesis Card
- top idea has an Experiment Card
- top idea has baseline, ablation, robustness, and falsification plans
- top idea has at least one accept reason and one reject reason
- top idea has at least one downgrade condition and one kill condition
- reasonableness verdict uses one of: `not reasonable yet`, `weak but useful`, `reasonable but underspecified`, `reasonable`, `high-risk but worth piloting`
- paper-readiness verdict uses one of: `not ready`, `pilot-ready`, `workshop-ready`, `main-track candidate`, `technical-report-only`

## Common Failure Patterns

- scope is broad and no clarification questions were asked
- output reviews literature but never proposes concrete ideas
- output claims to provide lineage but only lists paper titles
- output gives similar papers but does not extract each paper's innovation points
- output mixes actual paper contributions with inferred gaps without labeling the difference
- output lists ideas but never stress-tests whether they are reasonable
- output lists paper titles but no evidence roles
- output lists papers but never says which claim they support
- candidate search results are treated as verified evidence
- gap is stated as a fact but evidence type is missing
- idea is called strong without a baseline plan
- idea is called reasonable without closest prior work
- idea is called paper-ready without reviewer objections
- no condition is given for stopping or downgrading the idea
- arXiv preprint is described as an accepted paper
- novelty claim depends on private data without reproducible benchmark plan
