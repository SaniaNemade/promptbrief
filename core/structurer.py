import instructor
import litellm

from core.llm import MODEL
from core.schema import BugBrief

client = instructor.from_litellm(litellm.completion)

SYSTEM_PROMPT = """You turn messy, informal bug reports into a structured bug brief.

Rules:
- Only use information the user actually gave or clearly implied. Never invent steps, versions, devices or error messages.
- If something is not mentioned, leave it empty (None or an empty list). A blank field is better than a guess.
- Copy error messages and codes exactly as written.
- Write the title and summary in neutral, professional language, even if the user is frustrated.
- Ignore greetings, complaints and anything unrelated to the bug."""


def structure_report(raw_report: str) -> BugBrief:
    """Turn a messy bug report into a validated BugBrief."""
    return client.chat.completions.create(
        model=MODEL,
        response_model=BugBrief,
        max_retries=2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Bug report:\n\n{raw_report}"},
        ],
    )