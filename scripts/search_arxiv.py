#!/usr/bin/env python3
"""Search arXiv and emit JSONL records compatible with normalize_papers.py.

This script uses only the Python standard library. arXiv records are marked as
preprints with weak confidence by default; they must not be treated as accepted
conference or journal papers without separate verification.
"""

import argparse
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

ARXIV_API = "https://export.arxiv.org/api/query"
ATOM_NS = "{http://www.w3.org/2005/Atom}"
ARXIV_NS = "{http://arxiv.org/schemas/atom}"


def text_of(parent, tag, default=""):
    node = parent.find(tag)
    if node is None or node.text is None:
        return default
    return " ".join(node.text.split())


def first_year(entry):
    published = text_of(entry, ATOM_NS + "published", "")
    if published:
        try:
            return str(datetime.fromisoformat(published.replace("Z", "+00:00")).year)
        except ValueError:
            match = re.search(r"\d{4}", published)
            if match:
                return match.group(0)
    return "unknown"


def arxiv_identifier(entry):
    entry_id = text_of(entry, ATOM_NS + "id", "")
    if not entry_id:
        return "unknown"
    return entry_id


def main_contribution(entry):
    summary = text_of(entry, ATOM_NS + "summary", "unknown")
    if len(summary) <= 500:
        return summary
    return summary[:497].rstrip() + "..."


def record_from_entry(entry):
    title = text_of(entry, ATOM_NS + "title", "unknown")
    primary_category = entry.find(ARXIV_NS + "primary_category")
    task = "unknown"
    if primary_category is not None:
        task = primary_category.attrib.get("term", "unknown")

    return {
        "title": title,
        "year": first_year(entry),
        "venue_or_source": "arXiv",
        "paper_type": "preprint",
        "url_or_identifier": arxiv_identifier(entry),
        "task": task,
        "dataset": "unknown",
        "metric": "unknown",
        "main_contribution": main_contribution(entry),
        "why_relevant": "matched arXiv query; must be verified before use as evidence",
        "evidence_status": "candidate",
        "evidence_role": "task anchor",
        "used_to_support_which_claim": "candidate only; do not use to support a claim until verified",
        "confidence": "weak",
    }


def search_arxiv(query, max_results, start, sort_by, sort_order):
    params = {
        "search_query": "all:" + query,
        "start": str(start),
        "max_results": str(max_results),
        "sortBy": sort_by,
        "sortOrder": sort_order,
    }
    url = ARXIV_API + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"User-Agent": "shushu-novelty-finder/0.1"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def main():
    parser = argparse.ArgumentParser(description="Search arXiv and output JSONL paper records.")
    parser.add_argument("query", help="arXiv search query")
    parser.add_argument("--max-results", type=int, default=10, help="maximum results to return")
    parser.add_argument("--start", type=int, default=0, help="start offset")
    parser.add_argument("--sort-by", default="relevance", choices=["relevance", "lastUpdatedDate", "submittedDate"])
    parser.add_argument("--sort-order", default="descending", choices=["ascending", "descending"])
    args = parser.parse_args()

    try:
        payload = search_arxiv(args.query, args.max_results, args.start, args.sort_by, args.sort_order)
        root = ET.fromstring(payload)
    except Exception as exc:  # network and XML errors should be visible to CLI users
        raise SystemExit(f"arXiv request failed: {exc}") from exc

    for entry in root.findall(ATOM_NS + "entry"):
        print(json.dumps(record_from_entry(entry), ensure_ascii=False))


if __name__ == "__main__":
    main()
