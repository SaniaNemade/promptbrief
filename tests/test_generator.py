from core.generator import GitHubIssue, to_markdown


def test_markdown_has_title_labels_and_body():
    issue = GitHubIssue(
        title="Login fails with 'Invalid session'",
        labels=["bug", "auth", "severity: high"],
        body="## Summary\nLogin fails on iOS.",
    )
    md = to_markdown(issue)

    assert md.startswith("# Login fails")
    assert "`auth`" in md
    assert "## Summary" in md


def test_markdown_handles_no_labels():
    issue = GitHubIssue(title="Something odd", labels=[], body="## Summary\n_Not provided_")
    assert "_none_" in to_markdown(issue)