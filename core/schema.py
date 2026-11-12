from typing import Literal
from pydantic import BaseModel, Field


class Environment(BaseModel):
    os: str | None = Field(None, description="Operating system and version, e.g. 'macOS 15.1', 'iOS 18'. None if not mentioned.")
    browser: str | None = Field(None, description="Browser and version, e.g. 'Chrome 131'. None if not mentioned.")
    app_version: str | None = Field(None, description="Version of the app or software. None if not mentioned.")
    device: str | None = Field(None, description="Device, e.g. 'iPhone 15' or 'desktop'. None if not mentioned.")

    def is_sufficient(self) -> bool:
        """A device name alone isn't enough to reproduce a bug; we need an OS, browser or app version."""
        return any([self.os, self.browser, self.app_version])


class BugBrief(BaseModel):
    title: str = Field(description="Short, specific title (under 12 words) describing the bug.")
    summary: str = Field(description="One or two neutral sentences describing the problem.")
    steps_to_reproduce: list[str] = Field(
        default_factory=list,
        description="Ordered steps the user took. Only steps the user stated or clearly implied. Empty list if unknown.",
    )
    expected_behavior: str | None = Field(
        None,
        description=(
            "What the user expected to happen. Fill it only if stated, or if it is the obvious opposite "
            "of a concrete symptom; in that case also record it in 'assumptions'. None otherwise."
        ),
    )
    actual_behavior: str | None = Field(
        None,
        description=(
            "The concrete, observable symptom the user saw (an error, a crash, a spinner, wrong data). "
            "Vague statements like 'broken' or 'doesn't work' are NOT symptoms: use None for those."
        ),
    )
    error_messages: list[str] = Field(default_factory=list, description="Exact error messages or codes the user quoted.")
    environment: Environment = Field(default_factory=Environment)
    frequency: Literal["always", "sometimes", "once", "unknown"] = Field(
        "unknown",
        description=(
            "Use 'always' only if the user says it happens every time (e.g. 'every time', 'always', 'whenever'). "
            "Use 'sometimes' only if they say it is intermittent, and 'once' only if it happened one time. "
            "Otherwise 'unknown'. Do not guess."
        ),
    )
    severity: Literal["critical", "high", "medium", "low", "unknown"] = Field(
        "unknown",
        description=(
            "critical = data loss, security issue or total outage; "
            "high = core feature broken with no workaround; "
            "medium = broken but has a workaround; low = cosmetic. "
            "unknown if unclear."
        ),
    )
    assumptions: list[str] = Field(
        default_factory=list,
        description="Everything you inferred rather than read directly, e.g. 'Assumed the user expected the upload to succeed'.",
    )
    other_issues: list[str] = Field(
        default_factory=list,
        description="Any separate, secondary problems the user mentioned in passing, briefly described.",
    )

    def missing_fields(self) -> list[str]:
        """Plain code (not the LLM) decides what's missing, so it's predictable."""
        missing = []
        if not self.steps_to_reproduce:
            missing.append("steps_to_reproduce")
        if not self.expected_behavior:
            missing.append("expected_behavior")
        if not self.actual_behavior:
            missing.append("actual_behavior")
        if not self.environment.is_sufficient():
            missing.append("environment")
        return missing