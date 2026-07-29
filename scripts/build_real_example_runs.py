#!/usr/bin/env python3
"""Build three deterministic real-paper P0-P9 example runs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from shushu_novelty.fulltext import download_pdf, extract_pdf
from shushu_novelty.io import sha256_file, write_jsonl
from shushu_novelty.orchestrator.navigator import next_action
from shushu_novelty.orchestrator.phases import phases_for_mode
from shushu_novelty.retrieval.replay import create_search_manifest
from shushu_novelty.schemas import (
    AxisOverlap,
    ClaimEvidence,
    CollisionAudit,
    CollisionBatch,
    CollisionQueries,
    EvidenceRef,
    GapRecord,
    IdeaCandidate,
    LineageEdge,
    LineageGraph,
    LineageNode,
    PaperRecord,
    PhaseRecord,
    PriorComparison,
    Provenance,
    ReportManifest,
    ReviewerAudit,
    ReviewerBatch,
    ReviewerObjection,
    RunState,
    SaturationRecord,
)

STAMP = "2026-07-16T00:00:00+00:00"
AXES = ["task", "mechanism", "supervision-data", "assumption", "evaluation", "application"]

CASES = [
    {
        "slug": "rag-known-scoop",
        "topic": "RAG mechanism prior-art control",
        "candidate": (
            "Condition a sequence generator on passages retrieved from a dense Wikipedia index "
            "and jointly train retrieval and generation."
        ),
        "limitation": "This three-paper control is not a systematic review.",
        "papers": [
            (
                "2005.11401",
                "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
                2020,
                "Combines parametric sequence generation with dense non-parametric retrieval.",
            ),
            (
                "2002.08909",
                "REALM: Retrieval-Augmented Language Model Pre-Training",
                2020,
                "Pretrains a language model with a latent retrieval component.",
            ),
            (
                "2004.04906",
                "Dense Passage Retrieval for Open-Domain Question Answering",
                2020,
                "Introduces dense dual-encoder passage retrieval for open-domain QA.",
            ),
        ],
    },
    {
        "slug": "lora-known-scoop",
        "topic": "LoRA mechanism prior-art control",
        "candidate": (
            "Freeze a pretrained Transformer and inject learned low-rank matrices into its "
            "attention projections."
        ),
        "limitation": "This control does not audit later adaptive-rank variants.",
        "papers": [
            (
                "2106.09685",
                "LoRA: Low-Rank Adaptation of Large Language Models",
                2021,
                "Freezes pretrained weights and injects trainable low-rank decompositions.",
            ),
            (
                "1902.00751",
                "Parameter-Efficient Transfer Learning for NLP",
                2019,
                "Studies adapter modules for parameter-efficient transfer.",
            ),
            (
                "2101.00190",
                "Prefix-Tuning: Optimizing Continuous Prompts for Generation",
                2021,
                "Optimizes continuous prefixes while keeping language-model parameters frozen.",
            ),
        ],
    },
    {
        "slug": "clip-known-scoop",
        "topic": "CLIP mechanism prior-art control",
        "candidate": (
            "Contrastively pretrain image and text encoders on web-scale image-caption pairs for "
            "zero-shot recognition."
        ),
        "limitation": "This control does not enumerate every vision-language objective.",
        "papers": [
            (
                "2103.00020",
                "Learning Transferable Visual Models From Natural Language Supervision",
                2021,
                "Contrastively learns transferable image-text representations at web scale.",
            ),
            (
                "2102.05918",
                (
                    "Scaling Up Visual and Vision-Language Representation Learning With Noisy "
                    "Text Supervision"
                ),
                2021,
                "Scales image-text representation learning with noisy alt-text supervision.",
            ),
            (
                "2010.00747",
                (
                    "Contrastive Learning of Medical Visual Representations from Paired Images "
                    "and Text"
                ),
                2020,
                "Uses paired medical images and text for contrastive representation learning.",
            ),
        ],
    },
]


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = value.model_dump(mode="json") if hasattr(value, "model_dump") else value
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def paper_records(case: dict[str, object]) -> list[PaperRecord]:
    records = []
    slug = str(case["slug"])
    for index, (arxiv_id, title, year, abstract) in enumerate(case["papers"], 1):
        records.append(
            PaperRecord(
                paper_id=f"P-arxiv:{arxiv_id}",
                title=title,
                year=year,
                venue_or_source="arXiv",
                paper_type="preprint record",
                identifiers={"arxiv": arxiv_id},
                urls=[f"https://arxiv.org/abs/{arxiv_id}"],
                task=str(case["topic"]),
                abstract=abstract,
                main_contribution=abstract,
                why_relevant="Direct or neighboring mechanism in the prior-art control.",
                evidence_status="verified",
                verification_level="full-text" if index == 1 else "abstract",
                evidence_roles=["closest-prior" if index == 1 else "lineage"],
                supported_claim_ids=[f"C-{slug}-{index}", f"C-{slug}-lineage"],
                confidence=0.95 if index == 1 else 0.75,
                provenance=[
                    Provenance(
                        source="arxiv",
                        source_identifier=arxiv_id,
                        retrieved_at=STAMP,
                        source_url=f"https://arxiv.org/abs/{arxiv_id}",
                    )
                ],
            )
        )
    return records


def claim_records(case: dict[str, object], papers, document) -> list[ClaimEvidence]:
    slug = str(case["slug"])
    claims = [
        ClaimEvidence(
            claim_id=f"C-{slug}-1",
            claim="The submitted candidate substantially repeats the closest paper's mechanism.",
            origin="cross-paper-synthesis",
            strength="strong",
            evidence=[
                EvidenceRef(
                    paper_id=papers[0].paper_id,
                    role="support",
                    verification="full-text",
                    section=document.pages[0].section_hint,
                    locator="page 1",
                    passage_hash=document.pages[0].text_sha256,
                    confidence=0.95,
                )
            ],
        )
    ]
    for index, paper in enumerate(papers[1:], 2):
        claims.append(
            ClaimEvidence(
                claim_id=f"C-{slug}-{index}",
                claim=f"{paper.title} is a neighboring mechanism in the lineage.",
                origin="cross-paper-synthesis",
                strength="moderate",
                evidence=[
                    EvidenceRef(
                        paper_id=paper.paper_id,
                        role="background",
                        verification="abstract",
                        confidence=0.75,
                    )
                ],
            )
        )
    claims.append(
        ClaimEvidence(
            claim_id=f"C-{slug}-lineage",
            claim="The candidate sits inside an established mechanism lineage.",
            origin="cross-paper-synthesis",
            strength="moderate",
            evidence=[
                EvidenceRef(
                    paper_id=paper.paper_id,
                    role="support" if index == 0 else "background",
                    verification="full-text" if index == 0 else "abstract",
                    section=document.pages[0].section_hint if index == 0 else None,
                    locator="page 1" if index == 0 else None,
                    passage_hash=document.pages[0].text_sha256 if index == 0 else None,
                    confidence=0.9 if index == 0 else 0.7,
                )
                for index, paper in enumerate(papers)
            ],
        )
    )
    return claims


def lineage(case, papers) -> LineageGraph:
    slug = case["slug"]
    return LineageGraph(
        nodes=[
            LineageNode(
                paper_id=paper.paper_id,
                method_family="established mechanism family",
                assumptions=["the linked arXiv record is the evidence boundary"],
                contributions=[paper.main_contribution],
            )
            for paper in papers
        ],
        edges=[
            LineageEdge(
                edge_id=f"E-{slug}-{index}",
                source_paper_id=papers[index].paper_id,
                target_paper_id=papers[0].paper_id,
                relation="closest-prior" if index == 1 else "sibling",
                rationale="Mechanism-level neighbor used for the prior-art control.",
                evidence_claim_ids=[f"C-{slug}-lineage"],
                confidence=0.75,
            )
            for index in [1, 2]
        ],
        saturation=[
            SaturationRecord(
                saturation_id=f"S-{slug}",
                contribution="The submitted mechanism as written",
                status="blocked",
                paper_ids=[paper.paper_id for paper in papers],
                evidence_claim_ids=[f"C-{slug}-lineage"],
                blocked_idea_space=[case["candidate"]],
                open_idea_space=["A new falsifiable assumption or evaluation claim."],
            )
        ],
    )


def collision_batch(case, papers) -> CollisionBatch:
    slug = case["slug"]
    comparisons = []
    for index, paper in enumerate(papers, 1):
        comparisons.append(
            PriorComparison(
                paper_id=paper.paper_id,
                axes=[
                    AxisOverlap(
                        axis=axis,
                        overlap=(
                            "full"
                            if index == 1
                            else ("partial" if axis == "mechanism" else "none")
                        ),
                        rationale=(
                            "Direct mechanism replay."
                            if index == 1
                            else "Neighboring lineage evidence."
                        ),
                        evidence_claim_ids=[f"C-{slug}-{index}"],
                    )
                    for axis in AXES
                ],
                collision_risk="high" if index == 1 else "low",
            )
        )
    return CollisionBatch(
        audits=[
            CollisionAudit(
                audit_id=f"A-{slug}",
                idea_id=f"I-{slug}",
                generator_context_hash="a" * 64,
                auditor_context_hash="b" * 64,
                queries=CollisionQueries(
                    problem=[str(case["topic"])],
                    mechanism_signature=[str(case["candidate"])],
                    escape_mechanism=["new falsifiable assumption or evaluation claim"],
                ),
                comparisons=comparisons,
                decision="abandon",
                rationale="The closest paper fully covers the submitted mechanism.",
            )
        ]
    )


def reviewer_batch(case) -> ReviewerBatch:
    slug = case["slug"]
    objections = [
        ReviewerObjection(
            category="novelty",
            severity="fatal",
            objection="The novelty-bearing mechanism already exists in the closest paper.",
            evidence_claim_ids=[f"C-{slug}-1"],
            response="Abandon the unchanged candidate.",
            status="open",
        ),
        ReviewerObjection(
            category="evidence",
            severity="medium",
            objection="Three papers do not constitute a systematic review.",
            evidence_claim_ids=[f"C-{slug}-lineage"],
            response="The report labels the evidence boundary and uncertainty.",
            status="mitigated",
        ),
        ReviewerObjection(
            category="evaluation",
            severity="medium",
            objection="No experiment can rescue an identical mechanism claim.",
            evidence_claim_ids=[f"C-{slug}-1"],
            response="Require a structurally different, falsifiable thesis before experiments.",
            status="resolved",
        ),
    ]
    return ReviewerBatch(
        audits=[
            ReviewerAudit(
                review_id=f"R-{slug}",
                idea_id=f"I-{slug}",
                collision_audit_id=f"A-{slug}",
                reviewer_context_hash="c" * 64,
                strongest_reason_for="The candidate is technically concrete and testable.",
                strongest_reason_against="Its central mechanism is direct prior art.",
                supporting_claim_ids=[f"C-{slug}-1", f"C-{slug}-lineage"],
                objections=objections,
                kill_triggers=["Full task-and-mechanism overlap with the closest paper."],
                initial_decision="abandon",
                final_decision="abandon",
                rationale="Fatal novelty overlap leaves no defensible unchanged thesis.",
            )
        ]
    )


def report_markdown(case, papers) -> str:
    return f"""# Final prior-art control: {case['topic']}

Mode: full

## Research Scope Card

Audit the submitted mechanism against three real canonical arXiv records.

## Representative Papers and Paper Evidence

Closest paper: {papers[0].title} ({papers[0].identifiers['arxiv']}).
Lineage neighbors: {papers[1].title}; {papers[2].title}.

## Trend Matrix

The neighboring mechanisms precede or accompany the closest paper; this compact control does not
claim a complete historical timeline.

## Gap Audit

An open project would need a new falsifiable assumption or evaluation claim. The submitted
mechanism is blocked.

## Strong Idea Candidate and Novelty Verdict

Submitted claim: {case['candidate']}

Verdict: abandon. Calling the unchanged candidate strong novelty is unsupported.

## Risk and Failure Disclosure

No retrieval or PDF failure occurred for the closest paper. The failure risk is incomplete
literature coverage beyond these three controls.

## Minimum Experiment and Baseline

No experiment should start until a structurally different thesis exists. The closest paper is the
mandatory baseline for any rewrite.

## Paper Thesis and Core Claim

There is no defensible paper thesis for the unchanged candidate.

## Paper-readiness Verdict

Not paper-ready; abandon the unchanged idea.

## Uncertainty Budget

Only three canonical records were audited; later variants and accepted-version metadata may alter
the surrounding lineage but not the direct closest-paper collision.

## Known Limitations

{case['limitation']}
"""


def build_case(root: Path, case: dict[str, object]) -> None:
    case_dir = root / str(case["slug"])
    if case_dir.exists():
        raise FileExistsError(
            f"example already exists: {case_dir}; remove it explicitly to rebuild"
        )
    for directory in [
        "intake",
        "retrieval",
        "papers/pdf-cache",
        "lineage",
        "gaps",
        "ideas",
        "collision",
        "audit",
        "report",
    ]:
        (case_dir / directory).mkdir(parents=True, exist_ok=True)

    run_id = f"example-{case['slug']}"
    state = RunState(
        run_id=run_id,
        topic=str(case["topic"]),
        topic_slug=str(case["slug"]),
        mode="full",
        created_at=STAMP,
        updated_at=STAMP,
        model="documented-control",
        prompt_version="v0.2-example-1",
        phases={
            phase.code: PhaseRecord(artifact=phase.artifact)
            for phase in phases_for_mode("full")
        },
    )
    state.write_json(case_dir / "run.json")
    write_json(
        case_dir / "intake/intake.json",
        {"schema_version": "1.0", "topic": case["topic"], "mode": "full", "created_at": STAMP},
    )
    write_json(
        case_dir / "intake/scope.json",
        {
            "core_task": case["topic"],
            "inclusion_criteria": ["direct and neighboring mechanism papers"],
            "exclusion_criteria": ["comparative effectiveness claims"],
            "time_window": "canonical prior-art control",
        },
    )
    papers = paper_records(case)
    write_jsonl(papers, case_dir / "retrieval/papers.jsonl")
    (case_dir / "retrieval/failures.jsonl").write_text("", encoding="utf-8")
    create_search_manifest(
        str(case["topic"]),
        ["arxiv"],
        3,
        case_dir / "retrieval/papers.jsonl",
        case_dir / "retrieval/failures.jsonl",
        case_dir / "retrieval/papers.jsonl.manifest.json",
        papers,
        [],
    )
    pdf_path, source_url = download_pdf(
        papers[0], case_dir / "papers/pdf-cache", timeout=90.0
    )
    document = extract_pdf(pdf_path, papers[0].paper_id, source_url)
    document.pdf_path = str(pdf_path.relative_to(case_dir))
    documents = [document]
    write_jsonl(documents, case_dir / "papers/fulltext.jsonl")
    (case_dir / "papers/fulltext.failures.jsonl").write_text("", encoding="utf-8")
    claims = claim_records(case, papers, documents[0])
    write_jsonl(claims, case_dir / "papers/claims.jsonl")
    write_json(case_dir / "lineage/graph.json", lineage(case, papers))
    gap = GapRecord(
        gap_id=f"G-{case['slug']}",
        statement="A new project needs a falsifiable assumption or evaluation claim.",
        gap_type="cross-paper-pattern",
        evidence_claim_ids=[f"C-{case['slug']}-lineage"],
        blocked_by_paper_ids=[papers[0].paper_id],
        open_assumptions=["A structural rewrite changes the novelty-bearing mechanism."],
        confidence=0.7,
    )
    write_jsonl([gap], case_dir / "gaps/gaps.jsonl")
    idea = IdeaCandidate(
        idea_id=f"I-{case['slug']}",
        title="Submitted known-scoop control",
        novelty_level="strong",
        task=str(case["topic"]),
        mechanism=str(case["candidate"]),
        supervision_or_data="As specified by the closest canonical paper.",
        assumption="The known mechanism is incorrectly treated as new.",
        evaluation="Direct axis-level prior-art comparison.",
        application="Canonical task setting.",
        gap_ids=[gap.gap_id],
        closest_prior_work=[papers[0].paper_id],
        kill_criteria=["Closest paper fully covers task and mechanism."],
        status="abandon",
    )
    write_jsonl([idea], case_dir / "ideas/ideas.jsonl")
    collisions = collision_batch(case, papers)
    write_json(case_dir / "collision/collisions.json", collisions)
    write_json(case_dir / "audit/reviewer.json", reviewer_batch(case))
    report_path = case_dir / "report/report.md"
    report_path.write_text(report_markdown(case, papers), encoding="utf-8")
    manifest = ReportManifest(
        run_id=run_id,
        mode="full",
        report_path="report/report.md",
        report_sha256=sha256_file(report_path),
        input_artifact_hashes={
            "intake/scope.json": sha256_file(case_dir / "intake/scope.json"),
            "retrieval/papers.jsonl": sha256_file(case_dir / "retrieval/papers.jsonl"),
            "papers/fulltext.jsonl": sha256_file(case_dir / "papers/fulltext.jsonl"),
            "papers/claims.jsonl": sha256_file(case_dir / "papers/claims.jsonl"),
            "lineage/graph.json": sha256_file(case_dir / "lineage/graph.json"),
            "gaps/gaps.jsonl": sha256_file(case_dir / "gaps/gaps.jsonl"),
            "ideas/ideas.jsonl": sha256_file(case_dir / "ideas/ideas.jsonl"),
            "collision/collisions.json": sha256_file(
                case_dir / "collision/collisions.json"
            ),
            "audit/reviewer.json": sha256_file(case_dir / "audit/reviewer.json"),
        },
        claim_ids=[claim.claim_id for claim in claims],
        failure_logs=["retrieval/failures.jsonl", "papers/fulltext.failures.jsonl"],
        failure_log_hashes={
            "retrieval/failures.jsonl": sha256_file(
                case_dir / "retrieval/failures.jsonl"
            ),
            "papers/fulltext.failures.jsonl": sha256_file(
                case_dir / "papers/fulltext.failures.jsonl"
            ),
        },
        uncertainty_sections=["Uncertainty Budget"],
        known_limitations=[str(case["limitation"])],
    )
    write_json(case_dir / "report/manifest.json", manifest)
    action = next_action(case_dir)
    if action["status"] != "complete":
        raise RuntimeError(f"example run did not pass P0-P9: {action}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("examples/runs"))
    parser.add_argument("--case", choices=[case["slug"] for case in CASES])
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    for case in CASES:
        if args.case and case["slug"] != args.case:
            continue
        build_case(args.output, case)
        print(f"built {args.output / case['slug']}")


if __name__ == "__main__":
    main()
