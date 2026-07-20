from shushu_novelty.evaluation.structural import validate_report


def test_structural_validator_reports_missing_sections():
    result = validate_report("Mode: idea\nScope card")
    assert not result.ok
    assert "papers" in result.missing


def test_structural_validator_flags_unsupported_novelty_language():
    result = validate_report("No one has ever explored this")
    assert "unsupported_no_one" in result.warnings


def test_structural_validator_does_not_flag_prohibited_example():
    result = validate_report("What must not be claimed: nobody has done this.")
    assert "unsupported_no_one" not in result.warnings


def test_lineage_mode_does_not_require_idea_or_experiment_sections():
    text = """
    Mode: lineage
    Research Scope Card
    Representative Papers
    Trend Matrix
    Gap Audit
    Risk and uncertainty
    """

    result = validate_report(text, workflow_mode="lineage")

    assert result.ok


def test_idea_mode_does_not_require_trend_matrix():
    text = """
    Mode: idea
    Research Scope Card
    Representative Papers
    Gap Audit
    Strong Idea Candidate and novelty
    Risk and failure
    Minimum Experiment and baseline
    """

    result = validate_report(text, workflow_mode="idea")

    assert result.ok
