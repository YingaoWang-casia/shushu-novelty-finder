"""Full-text extraction and page-locator records."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import Field, HttpUrl, model_validator

from shushu_novelty.schemas.base import StrictModel


class PageText(StrictModel):
    page_number: int = Field(ge=1)
    text: str
    text_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    section_hint: Optional[str] = None


class FullTextDocument(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    paper_id: str = Field(pattern=r"^P-[A-Za-z0-9._:-]+$")
    source_url: HttpUrl
    pdf_path: Optional[str] = Field(default=None, min_length=1)
    pdf_sha256: Optional[str] = Field(default=None, pattern=r"^[a-f0-9]{64}$")
    content_path: Optional[str] = Field(default=None, min_length=1)
    content_sha256: Optional[str] = Field(default=None, pattern=r"^[a-f0-9]{64}$")
    page_count: int = Field(ge=1)
    pages: list[PageText] = Field(min_length=1)
    extraction_method: Literal["pypdf", "html"] = "pypdf"
    extracted_at: str = Field(min_length=1)
    visual_verification: Literal["not-run", "passed", "failed"] = "not-run"
    warnings: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def pages_match_count(self) -> FullTextDocument:
        expected = list(range(1, self.page_count + 1))
        actual = [page.page_number for page in self.pages]
        if actual != expected:
            raise ValueError("page numbers must be contiguous and match page_count")
        if self.extraction_method == "pypdf" and (not self.pdf_path or not self.pdf_sha256):
            raise ValueError("pypdf extraction requires pdf_path and pdf_sha256")
        if self.extraction_method == "html" and (
            not self.content_path or not self.content_sha256
        ):
            raise ValueError("HTML extraction requires content_path and content_sha256")
        return self
