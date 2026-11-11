import instructor
import litellm

from core.llm import MODEL
from core.schema import BugBrief

client = instructor.from_litellm(litellm.completion)

SYSTEM_PROMPT = """You turn messy, informal bug reports into a structured bug brief.

Rules:
- Only use information the user actually gave or clearly implied. Never invent steps, versions, devices or error messages.
- If something is not mentioned, leave it empty (None or an empty list). A blank field is better than a guess.
- Do not restate the complaint to fill a field. "It's broken" or "doesn't work" is not an actual behavior; leave actual_behavior empty.
- Any reasonable inference you make must be listed in 'assumptions'.
- Copy error messages and codes exactly as written.
- Write the title and summary in neutral, professional language, even if the user is frustrated.
- If the user mentions a second, unrelated problem, put it in 'other_issues' instead of mixing it into the main bug.
- Ignore greetings, praise and complaints that carry no technical information."""

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