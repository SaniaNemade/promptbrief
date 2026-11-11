import os

import litellm
from dotenv import load_dotenv

load_dotenv()  # reads .env so GEMINI_API_KEY and MODEL become available

MODEL = os.getenv("MODEL", "gemini/gemini-2.5-flash")


def ask(prompt: str) -> str:
    """Send a plain text prompt and return the text reply."""
    response = litellm.completion(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content