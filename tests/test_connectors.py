from shushu_novelty.retrieval import semantic_scholar
from shushu_novelty.retrieval.openalex import reconstruct_abstract, record_from_work
from shushu_novelty.retrieval.openreview import parse_search_response
from shushu_novelty.retrieval.semantic_scholar import record_from_paper


def test_openalex_reconstructs_abstract_and_identifiers():
    work = {
        "id": "https://openalex.org/W123",
        "title": "Evidence Graphs",
        "publication_year": 2025,
        "type": "article",
        "doi": "https://doi.org/10.1000/XYZ",
        "abstract_inverted_index": {"Evidence": [0], "matters": [1]},
        "authorships": [{"author": {"display_name": "Ada"}}],
        "primary_location": {
            "landing_page_url": "https://example.org/paper",
            "source": {"display_name": "ExampleConf"},
        },
        "ids": {"openalex": "https://openalex.org/W123"},
        "primary_topic": {"display_name": "Information Retrieval"},
    }
    assert reconstruct_abstract(work["abstract_inverted_index"]) == "Evidence matters"
    record = record_from_work(work, "2026-07-16T00:00:00+00:00")
    assert record.identifiers["doi"] == "10.1000/xyz"
    assert record.venue_or_source == "ExampleConf"
    assert record.verification_level == "abstract"


def test_semantic_scholar_preserves_cross_source_ids():
    record = record_from_paper(
        {
            "paperId": "S2-1",
            "title": "Evidence Graphs",
            "year": 2025,
            "abstract": "Evidence matters.",
            "externalIds": {"DOI": "10.1000/XYZ", "ArXiv": "2501.00001"},
            "authors": [{"name": "Ada"}],
            "publicationTypes": ["Conference"],
        },
        "2026-07-16T00:00:00+00:00",
    )
    assert record.identifiers["doi"] == "10.1000/xyz"
    assert record.identifiers["arxiv"] == "2501.00001"


def test_semantic_scholar_uses_bulk_search_without_key(monkeypatch):
    requests = []

    def fake_get_json(url, **kwargs):
        requests.append((url, kwargs))
        return {"data": [{"paperId": "S2-1", "title": "Evidence Graphs"}]}

    monkeypatch.delenv("SEMANTICSCHOLAR_API_KEY", raising=False)
    monkeypatch.setattr(semantic_scholar, "get_json", fake_get_json)

    records = semantic_scholar.search_semantic_scholar("evidence-graphs", max_results=5)

    assert len(records) == 1
    assert requests[0][0].startswith(semantic_scholar.SEMANTIC_SCHOLAR_BULK_API + "?")
    assert "sort=citationCount%3Adesc" in requests[0][0]
    assert "limit=" not in requests[0][0]
    assert "x-api-key" not in requests[0][1]["headers"]
    assert requests[0][1]["retries"] == 4


def test_semantic_scholar_relaxes_empty_bulk_query_once(monkeypatch):
    requests = []

    def fake_get_json(url, **kwargs):
        requests.append(url)
        if len(requests) == 1:
            return {"data": []}
        return {"data": [{"paperId": "S2-1", "title": "Citation Faithfulness"}]}

    monkeypatch.delenv("SEMANTICSCHOLAR_API_KEY", raising=False)
    monkeypatch.setattr(semantic_scholar, "get_json", fake_get_json)

    records = semantic_scholar.search_semantic_scholar(
        "citation faithfulness metrics long form generation", max_results=5
    )

    assert len(records) == 1
    assert len(requests) == 2
    assert "query=citation+faithfulness+metrics&" in requests[1]


def test_semantic_scholar_uses_relevance_search_with_key(monkeypatch):
    requests = []

    def fake_get_json(url, **kwargs):
        requests.append((url, kwargs))
        return {"data": [{"paperId": "S2-1", "title": "Evidence Graphs"}]}

    monkeypatch.setattr(semantic_scholar, "get_json", fake_get_json)

    semantic_scholar.search_semantic_scholar("evidence graphs", max_results=5, api_key="secret")

    assert requests[0][0].startswith(semantic_scholar.SEMANTIC_SCHOLAR_API + "?")
    assert "/bulk?" not in requests[0][0]
    assert "limit=5" in requests[0][0]
    assert "sort=" not in requests[0][0]
    assert requests[0][1]["headers"]["x-api-key"] == "secret"
    assert "retries" not in requests[0][1]


def test_openreview_collapses_review_notes_by_forum():
    forum = {
        "title": {"value": "Evidence Graphs"},
        "abstract": {"value": "Evidence matters."},
        "authors": {"value": ["Ada"]},
        "venue": {"value": "Submitted to ICLR 2026"},
    }
    payload = {
        "notes": [
            {"id": "review-1", "forum": "forum-1", "forumContent": forum, "cdate": 1760000000000},
            {"id": "review-2", "forum": "forum-1", "forumContent": forum, "cdate": 1760000000000},
        ]
    }
    records = parse_search_response(payload, 10)
    assert len(records) == 1
    assert records[0].paper_id == "P-openreview:forum-1"
