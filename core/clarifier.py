from typing import Literal

from pydantic import BaseModel, Field

from core.llm import MODEL
from core.schema import BugBrief
from core.structurer import client

MAX_QUESTIONS = 3

# Plain-language hints so the AI knows what each missing field really needs
FIELD_HINTS = {
    "steps_to_reproduce": "what the user did, step by step, right before the problem happened",
    "expected_behavior": "what the user expected to happen instead",
    "actual_behavior": "what the user actually saw: an error message, a crash, a blank screen, a spinner, wrong data",
    "environment": "the operating system version, app version, or browser (whichever fits this report)",
}


class ClarifyingQuestion(BaseModel):
    field: Literal["steps_to_reproduce", "expected_behavior", "actual_behavior", "environment"]
    question: str = Field(
        description="One short, friendly question in plain language, with an example answer in parentheses where helpful."
    )


class QuestionSet(BaseModel):
    questions: list[ClarifyingQuestion] = Field(max_length=MAX_QUESTIONS)


QUESTION_PROMPT = f"""You help a support team get complete bug reports.
You will receive the user's original report and the fields that are still missing.
Write at most {MAX_QUESTIONS} short, friendly questions that would fill the missing fields.

Rules:
- Only ask about the missing fields listed. Never ask about something the user already said.
- Use plain, non-technical language.
- Make each question specific to this report (mention the feature they talked about).
- You may combine two closely related fields into one question if it reads naturally.
- Where helpful, add a short example answer in parentheses.
- Never blame the user."""


def generate_questions(raw_report: str, brief: BugBrief) -> list[ClarifyingQuestion]:
    """Ask the AI to phrase questions for the fields our code says are missing."""
    missing = brief.missing_fields()
    if not missing:
        return []

    missing_text = "\n".join(f"- {field}: {FIELD_HINTS[field]}" for field in missing)
    result = client.chat.completions.create(
        model=MODEL,
        response_model=QuestionSet,
        max_retries=2,
        messages=[
            {"role": "system", "content": QUESTION_PROMPT},
            {"role": "user", "content": f"Original report:\n{raw_report}\n\nMissing fields:\n{missing_text}"},
        ],
    )
    return result.questions[:MAX_QUESTIONS]  # safety net, in case the AI ignores the limit


def build_followup_text(raw_report: str, questions: list[ClarifyingQuestion], answers: list[str]) -> str:
    """Combine the original report with the Q&A, so the structurer can read everything at once."""
    lines = [raw_report, "", "Follow-up answers from the user:"]
    for question, answer in zip(questions, answers):
        lines.append(f"Q: {question.question}")
        lines.append(f"A: {answer.strip() or '(no answer)'}")
    return "\n".join(lines)