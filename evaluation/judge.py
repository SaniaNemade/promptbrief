import os

from pydantic import BaseModel, Field

from core.generator import GitHubIssue, to_markdown
from core.llm import MODEL
from core.structurer import client

JUDGE_MODEL = os.getenv("JUDGE_MODEL", MODEL)


class Judgement(BaseModel):
    invented_details: list[str] = Field(
        description=(
            "Every specific detail in the issue that the original report does not support, "
            "e.g. an invented version, step, device, error message or cause. Empty list if none."
        )
    )
    actionability: int = Field(
        ge=1, le=5,
        description="1 = a developer could not act on this; 5 = a developer could start investigating immediately.",
    )


JUDGE_PROMPT = """You are a strict reviewer checking GitHub issues written from user bug reports.
The ORIGINAL report is the only source of truth.

- List every specific detail in the issue that the original report does not support.
  Statements clearly labeled as assumptions do not count. '_Not provided_' does not count.
- Rate actionability from 1 to 5.
- Be consistent, and do not reward length."""


def judge_issue(raw_report: str, issue: GitHubIssue) -> Judgement:
    return client.chat.completions.create(
        model=JUDGE_MODEL,
        response_model=Judgement,
        max_retries=2,
        messages=[
            {"role": "system", "content": JUDGE_PROMPT},
            {"role": "user", "content": f"ORIGINAL REPORT:\n{raw_report}\n\nGITHUB ISSUE:\n{to_markdown(issue)}"},
        ],
    )