import json
import time
from pathlib import Path

from core.generator import issue_from_brief, issue_from_raw
from core.structurer import structure_report
from evaluation.checks import errors_preserved, has_all_sections, needs_info_correct, other_issues_kept
from evaluation.judge import judge_issue

PAUSE = 4  # seconds between calls, to be gentle on the free tier
OUT = Path("results/eval_results.json")
OUT.parent.mkdir(exist_ok=True)

cases = json.loads(Path("data/eval_set.json").read_text())


def score(case, issue):
    judgement = judge_issue(case["text"], issue)
    time.sleep(PAUSE)
    return {
        "issue": issue.model_dump(),
        "has_all_sections": has_all_sections(issue),
        "needs_info_correct": needs_info_correct(issue, case["complete"]),
        "errors_preserved": errors_preserved(issue, case["error_messages"]),
        "other_issues_kept": other_issues_kept(issue, case["other_issue_keywords"]),
        "invented_details": judgement.invented_details,
        "actionability": judgement.actionability,
    }


results = []
for i, case in enumerate(cases, start=1):
    print(f"[{i}/{len(cases)}] {case['id']}")

    raw_issue = issue_from_raw(case["text"])
    time.sleep(PAUSE)
    brief = structure_report(case["text"])
    time.sleep(PAUSE)
    brief_issue = issue_from_brief(brief)
    time.sleep(PAUSE)

    results.append({"id": case["id"], "raw": score(case, raw_issue), "brief": score(case, brief_issue)})
    OUT.write_text(json.dumps(results, indent=2))  # save after every case, so a crash doesn't lose everything

print(f"\nSaved {OUT}. Now run: uv run python summarize_eval.py")