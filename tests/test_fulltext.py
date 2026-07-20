import hashlib
import json

from pypdf import PdfWriter

from shushu_novelty import fulltext
from shushu_novelty.fulltext import (
    candidate_html_urls,
    candidate_pdf_urls,
    extract_html,
    extract_pdf,
)
from shushu_novelty.schemas import FullTextDocument, PageText, PaperRecord, Provenance


def test_candidate_urls_prefers_arxiv_pdf():
    record = PaperRecord(
        paper_id="P-arxiv:2501.00001",
        title="Example",
        identifiers={"arxiv": "2501.00001"},
        urls=["https://arxiv.org/abs/2501.00001"],
        provenance=[Provenance(source="arxiv", source_identifier="2501.00001", retrieved_at="now")],
    )
    assert candidate_pdf_urls(record) == ["https://arxiv.org/pdf/2501.00001"]
    assert candidate_html_urls(record) == ["https://arxiv.org/html/2501.00001"]


def test_extract_pdf_records_page_hashes(tmp_path):
    path = tmp_path / "blank.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=100)
    with path.open("wb") as handle:
        writer.write(handle)
    document = extract_pdf(path, "P-arxiv:2501.00001", "https://arxiv.org/pdf/2501.00001")
    assert document.page_count == 1
    assert document.pages[0].text_sha256 == hashlib.sha256(b"").hexdigest()
    assert document.visual_verification == "not-run"
    assert "no extractable text" in document.warnings[0]


def test_extract_html_records_content_and_page_hashes(tmp_path):
    path = tmp_path / "paper.html"
    path.write_text(
        "<html><body><h1>Abstract</h1><p>Evidence matters.</p>"
        "<script>ignore me</script></body></html>",
        encoding="utf-8",
    )

    document = extract_html(
        path, "P-arxiv:2501.00001", "https://arxiv.org/html/2501.00001"
    )

    assert document.extraction_method == "html"
    assert document.page_count == 1
    assert "Evidence matters" in document.pages[0].text
    assert "ignore me" not in document.pages[0].text
    assert document.content_sha256 == hashlib.sha256(path.read_bytes()).hexdigest()


def test_batch_checkpoints_success_before_other_failures(monkeypatch, tmp_path):
    good = PaperRecord(
        paper_id="P-arxiv:good",
        title="Good",
        identifiers={"arxiv": "good"},
        provenance=[Provenance(source="arxiv", source_identifier="good", retrieved_at="now")],
    )
    bad = PaperRecord(
        paper_id="P-openreview:bad",
        title="Bad",
        identifiers={"openreview": "bad"},
        provenance=[Provenance(source="openreview", source_identifier="bad", retrieved_at="now")],
    )
    page_hash = hashlib.sha256(b"text").hexdigest()
    document = FullTextDocument(
        paper_id=good.paper_id,
        source_url="https://arxiv.org/pdf/good",
        pdf_path="/tmp/good.pdf",
        pdf_sha256="a" * 64,
        page_count=1,
        pages=[PageText(page_number=1, text="text", text_sha256=page_hash)],
        extracted_at="now",
    )

    def fake_fetch(record, cache_dir):
        if record.paper_id == bad.paper_id:
            raise RuntimeError("no PDF")
        return document

    monkeypatch.setattr(fulltext, "fetch_and_extract", fake_fetch)
    output = tmp_path / "documents.jsonl"
    failures = tmp_path / "failures.jsonl"
    documents, errors = fulltext.build_fulltext_ledger(
        [good, bad], tmp_path / "cache", failures, checkpoint_path=output
    )
    assert len(documents) == 1
    assert errors[0]["query"] == bad.paper_id
    assert json.loads(output.read_text())["paper_id"] == good.paper_id
    assert json.loads(failures.read_text())["error"] == "no PDF"
