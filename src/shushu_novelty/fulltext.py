"""PDF/HTML acquisition, caching, and page-level extraction."""

from __future__ import annotations

import hashlib
import re
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

from pypdf import PdfReader

from shushu_novelty.errors import RetrievalError
from shushu_novelty.io import write_jsonl
from shushu_novelty.retrieval.multi import write_failures
from shushu_novelty.schemas import FullTextDocument, PageText, PaperRecord

MAX_PDF_BYTES = 50 * 1024 * 1024
MAX_HTML_BYTES = 10 * 1024 * 1024


class _TextHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.ignored_depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in {"script", "style", "noscript", "svg"}:
            self.ignored_depth += 1
        elif tag in {"p", "div", "section", "article", "h1", "h2", "h3", "li", "br"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg"} and self.ignored_depth:
            self.ignored_depth -= 1
        elif tag in {"p", "div", "section", "article", "h1", "h2", "h3", "li"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.ignored_depth:
            self.parts.append(data)


def candidate_pdf_urls(record: PaperRecord) -> list[str]:
    candidates = []
    arxiv_id = record.identifiers.get("arxiv")
    if arxiv_id:
        candidates.append(f"https://arxiv.org/pdf/{arxiv_id}")
    for raw_url in record.urls:
        url = str(raw_url)
        if "arxiv.org/abs/" in url:
            url = url.replace("/abs/", "/pdf/")
        if url.casefold().endswith(".pdf") or "/pdf/" in url:
            candidates.append(url)
    return list(dict.fromkeys(candidates))


def candidate_html_urls(record: PaperRecord) -> list[str]:
    candidates = []
    arxiv_id = record.identifiers.get("arxiv")
    if arxiv_id:
        candidates.append(f"https://arxiv.org/html/{arxiv_id}")
    for raw_url in record.urls:
        url = str(raw_url)
        if "/html/" in url or url.casefold().endswith((".html", ".htm")):
            candidates.append(url)
    return list(dict.fromkeys(candidates))


def _safe_paper_dir(record: PaperRecord) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", record.paper_id)


def download_pdf(
    record: PaperRecord,
    cache_dir: Path,
    timeout: float = 30.0,
    max_bytes: int = MAX_PDF_BYTES,
) -> tuple[Path, str]:
    urls = candidate_pdf_urls(record)
    if not urls:
        raise RetrievalError(f"no public PDF URL for {record.paper_id}")
    failures = []
    for url in urls:
        request = urllib.request.Request(url, headers={"User-Agent": "shushu-novelty-finder/0.2"})
        try:
            deadline = time.monotonic() + timeout
            chunks = []
            total_bytes = 0
            with urllib.request.urlopen(request, timeout=min(timeout, 10.0)) as response:
                content_length = response.headers.get("Content-Length")
                if content_length and int(content_length) > max_bytes:
                    raise RetrievalError(f"PDF exceeds {max_bytes} bytes")
                while True:
                    if time.monotonic() >= deadline:
                        raise RetrievalError(f"PDF download exceeded {timeout} seconds")
                    chunk = response.read(min(65536, max_bytes + 1 - total_bytes))
                    if not chunk:
                        break
                    chunks.append(chunk)
                    total_bytes += len(chunk)
                    if total_bytes > max_bytes:
                        raise RetrievalError(f"PDF exceeds {max_bytes} bytes")
            payload = b"".join(chunks)
            if not payload.startswith(b"%PDF"):
                raise RetrievalError("response is not a PDF")
            digest = hashlib.sha256(payload).hexdigest()
            destination = cache_dir / _safe_paper_dir(record) / f"{digest}.pdf"
            destination.parent.mkdir(parents=True, exist_ok=True)
            if not destination.exists():
                destination.write_bytes(payload)
            return destination, url
        except (OSError, urllib.error.URLError, RetrievalError, ValueError) as exc:
            failures.append(f"{url}: {exc}")
    raise RetrievalError(f"all PDF candidates failed for {record.paper_id}: {'; '.join(failures)}")


def download_html(
    record: PaperRecord,
    cache_dir: Path,
    timeout: float = 30.0,
    max_bytes: int = MAX_HTML_BYTES,
) -> tuple[Path, str]:
    urls = candidate_html_urls(record)
    if not urls:
        raise RetrievalError(f"no public HTML URL for {record.paper_id}")
    failures = []
    for url in urls:
        request = urllib.request.Request(url, headers={"User-Agent": "shushu-novelty-finder/0.2"})
        try:
            deadline = time.monotonic() + timeout
            chunks = []
            total_bytes = 0
            with urllib.request.urlopen(request, timeout=min(timeout, 10.0)) as response:
                content_type = response.headers.get_content_type()
                while True:
                    if time.monotonic() >= deadline:
                        raise RetrievalError(f"HTML download exceeded {timeout} seconds")
                    chunk = response.read(min(65536, max_bytes + 1 - total_bytes))
                    if not chunk:
                        break
                    chunks.append(chunk)
                    total_bytes += len(chunk)
                    if total_bytes > max_bytes:
                        raise RetrievalError(f"HTML exceeds {max_bytes} bytes")
            payload = b"".join(chunks)
            if content_type not in {"text/html", "application/xhtml+xml"}:
                raise RetrievalError(f"response content type is {content_type}, not HTML")
            digest = hashlib.sha256(payload).hexdigest()
            destination = cache_dir / _safe_paper_dir(record) / f"{digest}.html"
            destination.parent.mkdir(parents=True, exist_ok=True)
            if not destination.exists():
                destination.write_bytes(payload)
            return destination, url
        except (OSError, urllib.error.URLError, RetrievalError, ValueError) as exc:
            failures.append(f"{url}: {exc}")
    raise RetrievalError(f"all HTML candidates failed for {record.paper_id}: {'; '.join(failures)}")


def _normalize_text(value: str) -> str:
    return "\n".join(line.rstrip() for line in value.replace("\x00", "").splitlines()).strip()


def _section_hint(text: str) -> str | None:
    for line in text.splitlines()[:12]:
        cleaned = " ".join(line.split())
        if 3 <= len(cleaned) <= 120 and (
            re.match(r"^\d+(?:\.\d+)*\s+\S", cleaned)
            or cleaned.casefold()
            in {"abstract", "introduction", "method", "methods", "results", "limitations"}
        ):
            return cleaned
    return None


def extract_pdf(
    path: Path,
    paper_id: str,
    source_url: str,
    visual_verification: str = "not-run",
) -> FullTextDocument:
    try:
        reader = PdfReader(path)
    except Exception as exc:
        raise RetrievalError(f"failed to read PDF {path}: {exc}") from exc
    pages = []
    warnings = []
    for index, page in enumerate(reader.pages, 1):
        try:
            text = _normalize_text(page.extract_text() or "")
        except Exception as exc:
            text = ""
            warnings.append(f"page {index} extraction failed: {exc}")
        if not text:
            warnings.append(f"page {index} has no extractable text")
        pages.append(
            PageText(
                page_number=index,
                text=text,
                text_sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
                section_hint=_section_hint(text),
            )
        )
    if not pages:
        raise RetrievalError(f"PDF has no pages: {path}")
    return FullTextDocument(
        paper_id=paper_id,
        source_url=source_url,
        pdf_path=str(path.resolve()),
        pdf_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        page_count=len(pages),
        pages=pages,
        extracted_at=datetime.now(timezone.utc).isoformat(),
        visual_verification=visual_verification,
        warnings=warnings,
    )


def extract_html(path: Path, paper_id: str, source_url: str) -> FullTextDocument:
    payload = path.read_bytes()
    parser = _TextHTMLParser()
    try:
        parser.feed(payload.decode("utf-8", errors="replace"))
    except Exception as exc:
        raise RetrievalError(f"failed to parse HTML {path}: {exc}") from exc
    text = _normalize_text("".join(parser.parts))
    if not text:
        raise RetrievalError(f"HTML has no extractable text: {path}")
    page = PageText(
        page_number=1,
        text=text,
        text_sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
        section_hint=_section_hint(text),
    )
    return FullTextDocument(
        paper_id=paper_id,
        source_url=source_url,
        content_path=str(path.resolve()),
        content_sha256=hashlib.sha256(payload).hexdigest(),
        page_count=1,
        pages=[page],
        extraction_method="html",
        extracted_at=datetime.now(timezone.utc).isoformat(),
        visual_verification="not-run",
        warnings=["HTML is represented as one document page for locator compatibility"],
    )


def fetch_and_extract(
    record: PaperRecord, cache_dir: Path, visual_verification: str = "not-run"
) -> FullTextDocument:
    pdf_error = None
    try:
        path, source_url = download_pdf(record, cache_dir)
    except RetrievalError as exc:
        pdf_error = exc
    else:
        return extract_pdf(path, record.paper_id, source_url, visual_verification)
    try:
        path, source_url = download_html(record, cache_dir)
        return extract_html(path, record.paper_id, source_url)
    except RetrievalError as html_error:
        raise RetrievalError(
            f"PDF failed ({pdf_error}); HTML failed ({html_error})"
        ) from html_error


def build_fulltext_ledger(
    records: Iterable[PaperRecord],
    cache_dir: Path,
    failure_log: Path,
    workers: int = 4,
    checkpoint_path: Path | None = None,
) -> tuple[list[FullTextDocument], list[dict[str, str]]]:
    items = list(records)
    documents: list[FullTextDocument] = []
    failures = []
    with ThreadPoolExecutor(max_workers=min(workers, max(len(items), 1))) as executor:
        futures = {executor.submit(fetch_and_extract, item, cache_dir): item for item in items}
        for future in as_completed(futures):
            item = futures[future]
            try:
                documents.append(future.result())
                documents.sort(key=lambda item: item.paper_id)
                if checkpoint_path is not None:
                    write_jsonl(documents, checkpoint_path)
            except Exception as exc:
                failures.append(
                    {
                        "schema_version": "1.0",
                        "source": "fulltext",
                        "query": item.paper_id,
                        "error": str(exc),
                        "occurred_at": datetime.now(timezone.utc).isoformat(),
                    }
                )
            failures.sort(key=lambda item: item["query"])
            write_failures(failures, failure_log)
    documents.sort(key=lambda item: item.paper_id)
    if checkpoint_path is not None:
        write_jsonl(documents, checkpoint_path)
    if not documents:
        raise RetrievalError("no PDF or HTML full text could be acquired and extracted")
    return documents, failures
