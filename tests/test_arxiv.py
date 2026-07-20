from shushu_novelty.retrieval.arxiv import as_legacy_records, parse_feed

ATOM = b"""<?xml version='1.0' encoding='UTF-8'?>
<feed xmlns='http://www.w3.org/2005/Atom' xmlns:arxiv='http://arxiv.org/schemas/atom'>
  <entry>
    <id>http://arxiv.org/abs/2401.01234v2</id>
    <published>2024-01-03T00:00:00Z</published>
    <title>  Evidence-Aware   Retrieval  </title>
    <summary>We test a retrieval method.</summary>
    <author><name>Ada Researcher</name></author>
    <arxiv:primary_category term='cs.IR'/>
  </entry>
</feed>
"""


def test_parse_feed_produces_canonical_record():
    records = parse_feed(ATOM, "2026-07-16T00:00:00+00:00")
    record = records[0]
    assert record.paper_id == "P-arxiv:2401.01234"
    assert record.identifiers == {"arxiv": "2401.01234"}
    assert record.title == "Evidence-Aware Retrieval"
    assert record.verification_level == "abstract"
    assert record.evidence_status == "candidate"


def test_legacy_adapter_preserves_old_contract():
    legacy = as_legacy_records(parse_feed(ATOM, "2026-07-16T00:00:00+00:00"))[0]
    assert legacy["url_or_identifier"] == "2401.01234"
    assert legacy["evidence_status"] == "candidate"
