import hashlib
import json

from shushu_novelty.orchestrator.navigator import next_action
from shushu_novelty.orchestrator.state import create_run, load_state, save_state
from shushu_novelty.retrieval.replay import create_search_manifest
from shushu_novelty.schemas import PaperRecord


def _advance_through_p2(tmp_path):
    run_dir = create_run("RAG citation robustness", "full", tmp_path)
    (run_dir / "intake" / "scope.json").write_text(
        json.dumps(
            {
                "core_task": "RAG citation verification",
                "inclusion_criteria": ["citation claims"],
                "exclusion_criteria": ["generic QA"],
                "time_window": "2020-2026",
            }
        ),
        encoding="utf-8",
    )
    paper = PaperRecord.model_validate(
        {
            "paper_id": "P-example:1",
            "title": "Example",
            "identifiers": {"example": "1"},
            "provenance": [
                {"source": "fixture", "source_identifier": "1", "retrieved_at": "now"}
            ],
        }
    )
    records_path = run_dir / "retrieval" / "papers.jsonl"
    failures_path = run_dir / "retrieval" / "failures.jsonl"
    records_path.write_text(paper.model_dump_json() + "\n", encoding="utf-8")
    failures_path.write_text("", encoding="utf-8")
    create_search_manifest(
        "RAG fixture",
        ["arxiv"],
        1,
        records_path,
        failures_path,
        run_dir / "retrieval" / "papers.jsonl.manifest.json",
        [paper],
        [],
    )
    assert next_action(run_dir)["phase"] == "P3"
    return run_dir


def test_new_run_resumes_at_scope_narrowing(tmp_path):
    run_dir = create_run("RAG citation robustness", "full", tmp_path)
    action = next_action(run_dir)
    assert action["status"] == "ready"
    assert action["phase"] == "P1"
    assert action["artifact"].endswith("intake/scope.json")
    state = load_state(run_dir)
    assert state.phases["P0"].status == "complete"
    assert state.phases["P0"].input_hash
    assert state.phases["P0"].output_hash
    assert state.phases["P1"].status == "ready"
    assert state.phases["P1"].input_hash == state.phases["P0"].output_hash


def test_invalid_existing_artifact_fails_gate_without_overwrite(tmp_path):
    run_dir = create_run("RAG citation robustness", "full", tmp_path)
    scope = run_dir / "intake" / "scope.json"
    scope.write_text(json.dumps({"core_task": "RAG"}), encoding="utf-8")
    before = scope.read_text(encoding="utf-8")
    action = next_action(run_dir)
    assert action["status"] == "failed"
    assert action["phase"] == "P1"
    assert scope.read_text(encoding="utf-8") == before


def test_failed_phase_can_be_repaired_and_resumed_without_restarting(tmp_path):
    run_dir = create_run("RAG citation robustness", "full", tmp_path)
    scope = run_dir / "intake" / "scope.json"
    scope.write_text(json.dumps({"core_task": "RAG"}), encoding="utf-8")
    assert next_action(run_dir)["status"] == "failed"
    scope.write_text(
        json.dumps(
            {
                "core_task": "RAG citation verification",
                "inclusion_criteria": ["citation claims"],
                "exclusion_criteria": ["generic QA"],
                "time_window": "2020-2026",
            }
        ),
        encoding="utf-8",
    )

    action = next_action(run_dir)

    assert action["status"] == "ready"
    assert action["phase"] == "P2"
    assert load_state(run_dir).phases["P1"].status == "complete"


def test_completed_artifact_tampering_is_not_silently_rehashed(tmp_path):
    run_dir = create_run("RAG citation robustness", "full", tmp_path)
    scope = run_dir / "intake" / "scope.json"
    scope.write_text(
        json.dumps(
            {
                "core_task": "RAG citation verification",
                "inclusion_criteria": ["citation claims"],
                "exclusion_criteria": ["generic QA"],
                "time_window": "2020-2026",
            }
        ),
        encoding="utf-8",
    )
    assert next_action(run_dir)["phase"] == "P2"
    scope.write_text(scope.read_text(encoding="utf-8") + "\n", encoding="utf-8")

    action = next_action(run_dir)

    assert action["status"] == "failed"
    assert action["phase"] == "P1"
    assert "changed after validation" in action["error"]


def test_legacy_complete_state_backfills_missing_input_hashes(tmp_path):
    run_dir = create_run("RAG citation robustness", "full", tmp_path)
    scope = run_dir / "intake" / "scope.json"
    scope.write_text(
        json.dumps(
            {
                "core_task": "RAG citation verification",
                "inclusion_criteria": ["citation claims"],
                "exclusion_criteria": ["generic QA"],
                "time_window": "2020-2026",
            }
        ),
        encoding="utf-8",
    )
    assert next_action(run_dir)["phase"] == "P2"
    state = load_state(run_dir)
    state.phases["P0"].input_hash = None
    state.phases["P1"].input_hash = None
    save_state(run_dir, state)

    assert next_action(run_dir)["phase"] == "P2"

    migrated = load_state(run_dir)
    assert migrated.phases["P0"].input_hash
    assert migrated.phases["P1"].input_hash == migrated.phases["P0"].output_hash


def test_completed_auxiliary_artifact_tampering_is_not_silently_rehashed(tmp_path):
    run_dir = _advance_through_p2(tmp_path)
    (run_dir / "retrieval" / "failures.jsonl").write_text(
        '{"error":"late mutation"}\n', encoding="utf-8"
    )

    action = next_action(run_dir)

    assert action["status"] == "failed"
    assert action["phase"] == "P2"
    assert "auxiliary artifact changed after validation" in action["error"]


def test_legacy_complete_state_backfills_auxiliary_bundle_hashes(tmp_path):
    run_dir = _advance_through_p2(tmp_path)
    state = load_state(run_dir)
    state.phases["P2"].auxiliary_hashes = {}
    state.phases["P3"].input_hash = state.phases["P2"].output_hash
    save_state(run_dir, state)

    assert next_action(run_dir)["phase"] == "P3"

    migrated = load_state(run_dir)
    assert set(migrated.phases["P2"].auxiliary_hashes) == {
        "retrieval/papers.jsonl.manifest.json",
        "retrieval/failures.jsonl",
    }
    assert migrated.phases["P3"].input_hash != migrated.phases["P2"].output_hash


def test_paper_verification_gate_requires_claim_ledger(tmp_path):
    run_dir = create_run("RAG citation robustness", "full", tmp_path)
    (run_dir / "intake" / "scope.json").write_text(
        json.dumps(
            {
                "core_task": "RAG",
                "inclusion_criteria": ["retrieval plus generation"],
                "exclusion_criteria": ["retrieval-only"],
                "time_window": "2020-2026",
            }
        ),
        encoding="utf-8",
    )
    paper = {
        "paper_id": "P-example:1",
        "title": "Example",
        "identifiers": {"example": "1"},
        "provenance": [
            {"source": "fixture", "source_identifier": "1", "retrieved_at": "now"}
        ],
    }
    (run_dir / "retrieval" / "papers.jsonl").write_text(
        json.dumps(paper) + "\n", encoding="utf-8"
    )
    (run_dir / "retrieval" / "failures.jsonl").write_text("", encoding="utf-8")
    create_search_manifest(
        "RAG fixture",
        ["arxiv"],
        1,
        run_dir / "retrieval" / "papers.jsonl",
        run_dir / "retrieval" / "failures.jsonl",
        run_dir / "retrieval" / "papers.jsonl.manifest.json",
        [PaperRecord.model_validate(paper)],
        [],
    )
    page_text = "fixture page"
    document = {
        "paper_id": "P-example:1",
        "source_url": "https://example.com/paper.pdf",
        "pdf_path": "cache/paper.pdf",
        "pdf_sha256": "a" * 64,
        "page_count": 1,
        "pages": [
            {
                "page_number": 1,
                "text": page_text,
                "text_sha256": hashlib.sha256(page_text.encode()).hexdigest(),
            }
        ],
        "extracted_at": "now",
    }
    (run_dir / "papers" / "fulltext.jsonl").write_text(
        json.dumps(document) + "\n", encoding="utf-8"
    )

    action = next_action(run_dir)

    assert action["status"] == "failed"
    assert action["phase"] == "P3"
    assert "claims.jsonl" in action["error"]
