import json
import time
from pathlib import Path

from core.generator import issue_from_brief, issue_from_raw, to_markdown
from core.structurer import structure_report

OUT = Path("results/issues")
OUT.mkdir(parents=True, exist_ok=True)

reports = json.loads(Path("data/sample_reports.json").read_text())

for report in reports:
    print(f"Generating issues for {report['id']}...")

    raw_issue = issue_from_raw(report["text"])
    time.sleep(5)  # stay under free-tier rate limits

    brief = structure_report(report["text"])
    time.sleep(5)

    brief_issue = issue_from_brief(brief)
    time.sleep(5)

    (OUT / f"{report['id']}_from_raw.md").write_text(to_markdown(raw_issue))
    (OUT / f"{report['id']}_from_brief.md").write_text(to_markdown(brief_issue))

print(f"\nDone! Open the files in {OUT}/ to compare.")