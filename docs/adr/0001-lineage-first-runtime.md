# ADR 0001: Separate research judgment from deterministic runtime

- Status: accepted
- Date: 2026-07-16

## Decision

Keep lineage construction, novelty judgment, and reviewer reasoning in the Skill/LLM layer.
Move retrieval, canonicalization, schema validation, artifact persistence, deterministic gates,
and evaluation bookkeeping into an installable Python package.

## Consequences

The same run can be interrupted, inspected, and resumed. Claims and ideas become traceable to
versioned records. The runtime deliberately does not pretend that deterministic validation can
judge scientific truth; benchmark and human evaluation remain necessary.
