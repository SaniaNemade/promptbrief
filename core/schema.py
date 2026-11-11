from typing import Literal
from pydantic import BaseModel, Field


class Environment(BaseModel):
    os: str | None = Field(None, description="Operating system and version, e.g. 'macOS 15.1'. None if not mentioned.")
    browser: str | None = Field(None, description="Browser and version, e.g. 'Chrome 131'. None if not mentioned.")
    app_version: str | None = Field(None, description="Version of the app or software. None if not mentioned.")
    device: str | None = Field(None, description="Device, e.g. 'iPhone 15' or 'desktop'. None if not mentioned.")

    def is_empty(self) -> bool:
        return not any([self.os, self.browser, self.app_version, self.device])


class BugBrief(BaseModel):
    title: str = Field(description="Short, specific title (under 12 words) describing the bug.")
    summary: str = Field(description="One or two neutral sentences describing the problem.")
    steps_to_reproduce: list[str] = Field(
        default_factory=list,
        description="Ordered steps the user took. Only steps the user stated or clearly implied. Empty list if unknown.",
    )
    expected_behavior: str | None = Field(None, description="What the user expected to happen. None if not stated.")
    actual_behavior: str | None = Field(None, description="What actually happened. None if not stated.")
    error_messages: list[str] = Field(default_factory=list, description="Exact error messages or codes the user quoted.")
    environment: Environment = Field(default_factory=Environment)
    frequency: Literal["always", "sometimes", "once", "unknown"] = "unknown"
    severity: Literal["critical", "high", "medium", "low", "unknown"] = Field(
        "unknown",
        description=(
            "critical = data loss, security issue or total outage; "
            "high = core feature broken with no workaround; "
            "medium = broken but has a workaround; low = cosmetic. "
            "unknown if unclear."
        ),
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
        if self.environment.is_empty():
            missing.append("environment")
        return missing