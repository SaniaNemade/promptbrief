from core.clarifier import build_followup_text, generate_questions
from core.structurer import structure_report
from core.generator import issue_from_brief, to_markdown

MAX_ROUNDS = 2


def main():
    report = input("Describe the bug:\n> ")
    brief = structure_report(report)

    for _ in range(MAX_ROUNDS):
        if not brief.missing_fields():
            break

        questions = generate_questions(report, brief)
        print("\nA few quick questions (press Enter to skip any):")
        answers = [input(f"\n{q.question}\n> ") for q in questions]

        if not any(answer.strip() for answer in answers):
            print("\nNo answers given, so we'll stop here.")
            break

        report = build_followup_text(report, questions, answers)
        brief = structure_report(report)

    print("\n" + "=" * 60)
    print(brief.model_dump_json(indent=2))
    print(f"\nStill missing: {brief.missing_fields() or 'nothing'}")


if __name__ == "__main__":
    main()

    issue = issue_from_brief(brief)
    print("\n" + "=" * 60)
    print("GITHUB ISSUE")
    print("=" * 60)
    print(to_markdown(issue))