from core.schema import BugBrief, Environment


def test_vague_report_has_missing_fields():
    brief = BugBrief(title="App broken", summary="The app does not work.")
    assert set(brief.missing_fields()) == {
        "steps_to_reproduce",
        "expected_behavior",
        "actual_behavior",
        "environment",
    }


def test_complete_report_has_no_missing_fields():
    brief = BugBrief(
        title="Login button shows blank screen",
        summary="Clicking Login shows a blank white screen instead of the dashboard.",
        steps_to_reproduce=["Open the app", "Enter credentials", "Click Login"],
        expected_behavior="Dashboard loads",
        actual_behavior="Blank white screen",
        environment=Environment(os="macOS 15"),
    )
    assert brief.missing_fields() == []