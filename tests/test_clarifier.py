from core.clarifier import ClarifyingQuestion, build_followup_text


def test_followup_text_includes_answers_and_marks_skips():
    questions = [
        ClarifyingQuestion(field="actual_behavior", question="What happens when you tap Login?"),
        ClarifyingQuestion(field="environment", question="Which iOS version are you on?"),
    ]
    text = build_followup_text("login doesnt work", questions, ["A red error says 'Invalid session'", ""])

    assert "login doesnt work" in text
    assert "Invalid session" in text
    assert "(no answer)" in text  # the skipped question is marked, not left blank