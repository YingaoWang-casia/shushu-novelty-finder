# Three real end-to-end prior-art controls

These compact cases exercise the full decision path with real canonical papers. They are
**prior-art controls**, not claims that Shushu discovered new research. Paper-level statements are
limited to the linked arXiv records; the examples explicitly abandon ideas whose core mechanisms
already exist.

## Case 1 — RAG mechanism replay

**P0–P1 Intake and scope.** Audit the candidate “condition a sequence generator on passages from a
dense Wikipedia index and train retrieval and generation together.” Scope is knowledge-intensive
NLP, not every use of retrieval.

**P2–P4 Retrieval, verification, and lineage.** The closest paper is
[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401),
which combines parametric seq2seq memory with a dense Wikipedia index and studies two conditioning
schemes. Relevant ancestors include
[REALM](https://arxiv.org/abs/2002.08909) and
[Dense Passage Retrieval](https://arxiv.org/abs/2004.04906). The safe claim is that the proposed
task/mechanism pair substantially repeats the RAG paper; this is not an absence claim.

**P5–P7 Gap, candidate, and collision.** A defensible gap would need to change an assumption or
evaluation claim, such as auditable evidence use under corpus updates. Merely restating the dense
retriever plus generator is full overlap on task, mechanism, supervision/data, and application.
Collision decision: `abandon`.

**P8–P9 Review and report.** Strongest reject reason: the novelty-bearing mechanism is already the
paper’s central contribution. No structural rewrite is attempted because the submitted idea has no
independent thesis. Failure disclosure: the three-paper control is not a systematic review.
Uncertainty: later variants are intentionally outside this minimal control.

## Case 2 — LoRA mechanism replay

**P0–P1 Intake and scope.** Audit the candidate “freeze a pretrained Transformer and inject learned
low-rank matrices into attention projections.” Scope is parameter-efficient adaptation.

**P2–P4 Retrieval, verification, and lineage.** The proposal directly matches
[LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685). Its nearby
adaptation lineage includes
[Parameter-Efficient Transfer Learning for NLP](https://arxiv.org/abs/1902.00751) and
[Prefix-Tuning](https://arxiv.org/abs/2101.00190). The evidence supports a collision judgment, not a
claim that every later low-rank method has been enumerated.

**P5–P7 Gap, candidate, and collision.** Changing rank, dataset, or application without a new
mechanism is insufficient for strong novelty. A structural alternative would need a falsifiable
allocation, optimization, or systems claim that survives later-work search. The unchanged
candidate fully overlaps LoRA on mechanism and adaptation assumption. Collision decision:
`abandon`.

**P8–P9 Review and report.** Fatal objection: the candidate is a description of the known method.
Final decision: `abandon`; zero revisions. Failure disclosure: no claim is made about the novelty of
specific adaptive-rank variants. Uncertainty: accepted-version metadata is not evaluated here.

## Case 3 — CLIP mechanism replay

**P0–P1 Intake and scope.** Audit the candidate “contrastively pretrain image and text encoders on
web-scale image-caption pairs for zero-shot recognition.” Scope is transferable visual
representation learning from natural-language supervision.

**P2–P4 Retrieval, verification, and lineage.** The candidate directly matches
[Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020).
Nearby work includes
[ALIGN](https://arxiv.org/abs/2102.05918) and
[ConVIRT](https://arxiv.org/abs/2010.00747). Application to a new image domain alone does not erase
the mechanism overlap.

**P5–P7 Gap, candidate, and collision.** A new scientific claim could arise from a domain-specific
failure model, supervision assumption, or evaluation protocol, but the submitted contrastive
pretraining recipe overlaps the canonical paper on task, mechanism, data, and evaluation intent.
Collision decision: `abandon`.

**P8–P9 Review and report.** Fatal objection: no contribution remains after subtracting the closest
prior mechanism. Final decision: `abandon`; zero revisions. Failure disclosure: this control does
not compare every vision-language objective. Uncertainty: domain-specific transfer claims require
their own closest-paper search.

## What these cases prove—and do not prove

They are deterministic regression cases for downgrade/abandon behavior and honest uncertainty
reporting. They do not establish comparative effectiveness. The public 60-seed, four-system,
two-human evaluation remains the only allowed basis for a README quality claim.
