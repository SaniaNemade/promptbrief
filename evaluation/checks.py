from core.generator import GitHubIssue

REQUIRED_SECTIONS = [
    "## Summary",
    "## Steps to Reproduce",
    "## Expected Behavior",
    "## Actual Behavior",
    "## Environment",
    "## Additional Notes",
]


def has_all_sections(issue: GitHubIssue) -> bool:
    return all(section in issue.body for section in REQUIRED_SECTIONS)


def needs_info_correct(issue: GitHubIssue, is_complete: bool) -> bool:
    """Correct if it flags incomplete reports, and doesn't flag complete ones."""
    flagged = "needs-info" in issue.labels
    return flagged != is_complete


def errors_preserved(issue: GitHubIssue, expected_errors: list[str]) -> bool | None:
    if not expected_errors:
        return None  # not applicable to this report
    return all(error in issue.body for error in expected_errors)


def other_issues_kept(issue: GitHubIssue, keywords: list[str]) -> bool | None:
    if not keywords:
        return None  # not applicable to this report
    text = (issue.title + " " + issue.body).lower()
    return all(keyword.lower() in text for keyword in keywords)