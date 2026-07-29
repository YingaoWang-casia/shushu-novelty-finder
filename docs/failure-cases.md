# Failure cases and expected behavior

These cases are first-class outputs, not exceptional text that may be omitted from a report.
Every final report must include a failure disclosure and an uncertainty section, even when no
failure occurred.

| Failure case | Required behavior | Enforced by |
|---|---|---|
| A cited paper does not exist | Keep the candidate out of verified evidence; log the failed source lookup. | Citation-existence evaluation and durable retrieval failure logs |
| arXiv and accepted versions are duplicated | Merge them into one canonical paper while retaining both identifiers and provenance records. | Identifier/title deduplication and accepted/preprint merge tests |
| Abstracts look similar but full-text mechanisms differ | Keep the match as a candidate until page-level passages support the mechanism comparison. | Full-text ledger and six-axis collision evidence |
| An idea only combines existing modules | Rank it weak or revise it unless the composition creates a new falsifiable mechanism or assumption. | Collision axes plus reviewer objection gate |
| A recent paper fully covers the idea | Downgrade or abandon it; a pass is forbidden for scoop-level overlap. | Collision decision gate and known-scoop benchmark controls |
| There is not enough evidence | Report the missing evidence and lower confidence; do not promote a strong claim. | Strong-claim full-text invariant and report uncertainty gate |
| One or more retrieval APIs fail | Preserve successful sources, write one failure record per failed source, and disclose partial coverage. | Multi-source retrieval failure JSONL and report manifest |
| The direction is too broad for a falsifiable claim | Stop at scope narrowing and request a narrower task, mechanism, population, or evaluation claim. | P1 scope artifact and deterministic phase gate |
| A 240-run model evaluation is interrupted | Preserve every completed output and its adapter/output hashes; resume only from an immutable matching checkpoint and retain failed-attempt history. | Per-run benchmark checkpoints, provenance fingerprints, and atomic failure history |
| A supposedly blind output reveals its system/profile | Refuse to create the rater package until the answer is repaired or independently redacted and re-hashed. | Blind-package identity-marker gate and opaque copied paths |

The runtime intentionally does not turn an empty or partially failed search into evidence that no
prior work exists.
