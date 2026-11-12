from typing import Literal

from pydantic import BaseModel, Field

from core.llm import MODEL
from core.schema import BugBrief
from core.structurer import client

Label = Literal[
    "bug", "crash", "ui", "performance", "auth", "payments", "search", "settings", "upload",
    "needs-info",
    "severity: critical", "severity: high", "severity: medium", "severity: low",
]


class GitHubIssue(BaseModel):
    title: str = Field(description="Clear, specific issue title under 12 words.")
    labels: list[Label] = Field(
        description=(
            "Only labels that fit. Add 'needs-info' if steps, expected behavior, actual behavior "
            "or environment are missing. Add one severity label only if severity is known."
        )
    )
    body: str = Field(
        description=(
            "Issue body in GitHub Markdown with these sections in order: "
            "## Summary, ## Steps to Reproduce (numbered list), ## Expected Behavior, "
            "## Actual Behavior, ## Environment, ## Additional Notes. "
            "Write _Not provided_ under any section with no information."
        )
    )


ISSUE_PROMPT = """You are a senior QA engineer writing GitHub issues for a development team.

Rules:
- Use only the information provided. Never invent steps, versions, error messages or causes.
- If a section has no information, write _Not provided_ under it.
- Put error messages in backticks, exactly as given.
- Under Additional Notes, mention any assumptions and any other issues, if provided.
- In a structured brief, 'unknown', null and empty lists mean the user did not say. Never replace them with a guess.
- Be concise and neutral. No greetings or sign-offs."""


def _generate(source_label: str, content: str) -> GitHubIssue:
    """Shared by both paths, so the only difference between them is the input."""
    return client.chat.completions.create(
        model=MODEL,
        response_model=GitHubIssue,
        max_retries=2,
        messages=[
            {"role": "system", "content": ISSUE_PROMPT},
            {"role": "user", "content": f"{source_label}:\n\n{content}"},
        ],
    )


def issue_from_raw(raw_report: str) -> GitHubIssue:
    """Path A (baseline): straight from the messy text."""
    return _generate("Raw bug report from a user", raw_report)


def issue_from_brief(brief: BugBrief) -> GitHubIssue:
    """Path B (ours): from the structured brief."""
    return _generate("Structured bug brief (JSON)", brief.model_dump_json(indent=2))


def to_markdown(issue: GitHubIssue) -> str:
    """Turn an issue into one Markdown document. Plain Python, so it's easy to test."""
    labels = ", ".join(f"`{label}`" for label in issue.labels) or "_none_"
    return f"# {issue.title}\n\n**Labels:** {labels}\n\n{issue.body}\n"