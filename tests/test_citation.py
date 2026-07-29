import hashlib

from shushu_novelty.evaluation.citation import validate_ledger
from shushu_novelty.schemas import (
    ClaimEvidence,
    EvidenceRef,
    FullTextDocument,
    PageText,
    PaperRecord,
    Provenance,
)


def fixtures():
    text_hash = hashlib.sha256(b"Evidence text").hexdigest()
    paper = PaperRecord(
        paper_id="P-arxiv:2501.00001",
        title="Evidence",
        identifiers={"arxiv": "2501.00001"},
        provenance=[Provenance(source="arxiv", source_identifier="2501.00001", retrieved_at="now")],
    )
    document = FullTextDocument(
        paper_id=paper.paper_id,
        source_url="https://arxiv.org/pdf/2501.00001",
        pdf_path="/tmp/paper.pdf",
        pdf_sha256="a" * 64,
        page_count=1,
        pages=[PageText(page_number=1, text="Evidence text", text_sha256=text_hash)],
        extracted_at="now",
    )
    claim = ClaimEvidence(
        claim_id="C-001",
        claim="Evidence supports this claim",
        origin="author-statement",
        strength="strong",
        evidence=[
            EvidenceRef(
                paper_id=paper.paper_id,
                role="support",
                verification="full-text",
                locator="page:1",
                passage_hash=text_hash,
                confidence=0.9,
            )
        ],
    )
    return paper, document, claim


def test_valid_ledger_connects_claim_to_page_hash():
    paper, document, claim = fixtures()
    assert validate_ledger([paper], [document], [claim]).ok


def test_ledger_rejects_stale_page_hash():
    paper, document, claim = fixtures()
    claim.evidence[0].passage_hash = "b" * 64
    result = validate_ledger([paper], [document], [claim])
    assert not result.ok
    assert "does not match" in result.errors[0]
