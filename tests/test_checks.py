from core.generator import GitHubIssue
from evaluation.checks import errors_preserved, has_all_sections, needs_info_correct, other_issues_kept

FULL_BODY = (
    "## Summary\nx\n## Steps to Reproduce\n1. x\n## Expected Behavior\nx\n"
    "## Actual Behavior\n`ERR_TOKEN_EXPIRED`\n## Environment\nx\n## Additional Notes\nDark mode looks off."
)


def make_issue(labels=None, body=FULL_BODY):
    return GitHubIssue(title="Test issue", labels=labels or [], body=body)


def test_sections():
    assert has_all_sections(make_issue())
    assert not has_all_sections(make_issue(body="## Summary\nonly this"))


def test_needs_info():
    assert needs_info_correct(make_issue(labels=["needs-info"]), is_complete=False)
    assert not needs_info_correct(make_issue(labels=["needs-info"]), is_complete=True)


def test_errors_and_other_issues():
    assert errors_preserved(make_issue(), ["ERR_TOKEN_EXPIRED"])
    assert errors_preserved(make_issue(), []) is None
    assert other_issues_kept(make_issue(), ["dark mode"])