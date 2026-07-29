from shushu_novelty.retrieval.dedup import deduplicate
from shushu_novelty.schemas import PaperRecord, Provenance


def paper(source: str, paper_id: str, identifiers: dict[str, str], paper_type: str) -> PaperRecord:
    return PaperRecord(
        paper_id=paper_id,
        title="Evidence-Aware Retrieval",
        year=2025,
        venue_or_source=source,
        paper_type=paper_type,
        identifiers=identifiers,
        provenance=[
            Provenance(
                source=source,
                source_identifier=next(iter(identifiers.values())),
                retrieved_at="2026-07-16T00:00:00+00:00",
            )
        ],
    )


def test_dedup_merges_preprint_and_accepted_version():
    arxiv = paper("arxiv", "P-arxiv:2501.1", {"arxiv": "2501.1"}, "preprint")
    accepted = paper(
        "semantic-scholar",
        "P-semanticscholar:S2",
        {"arxiv": "2501.1", "doi": "10.1/example"},
        "Conference",
    )
    result = deduplicate([arxiv, accepted])
    assert len(result) == 1
    assert result[0].paper_type == "Conference"
    assert {item.source for item in result[0].provenance} == {"arxiv", "semantic-scholar"}
    assert result[0].identifiers["doi"] == "10.1/example"
