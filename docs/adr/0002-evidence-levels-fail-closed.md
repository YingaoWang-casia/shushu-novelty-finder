# ADR 0002: Evidence levels fail closed

- Status: accepted
- Date: 2026-07-16

## Context

Titles, metadata, abstracts, extracted body text, and visually verified passages provide different
levels of support. Treating them as interchangeable makes novelty collision and lineage conclusions
look more certain than the inspected source permits.

## Decision

Persist the inspection level on paper and claim records. Metadata or abstract inspection can create
a candidate and support recall, but cannot support a strong claim. Strong claims require a
full-text evidence reference whose paper, page locator, and extracted-text hash are present in the
ledger. Missing or failed full text lowers confidence and remains visible in failure logs. Model
inference, cross-paper synthesis, and author-stated limitations remain distinct origins.

## Consequences

The runtime may reject an otherwise polished report when its evidence is weaker than its language.
This is intentional. OCR, semantic entailment, and visual verification remain explicit limitations
rather than being inferred from successful text extraction.
