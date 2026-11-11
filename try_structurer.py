import json
import time
from pathlib import Path

from core.structurer import structure_report

reports = json.loads(Path("data/sample_reports.json").read_text())

for report in reports:
    print("=" * 60)
    print(f"[{report['id']}] RAW: {report['text']}\n")
    brief = structure_report(report["text"])
    print(brief.model_dump_json(indent=2))
    print(f"\nMissing: {brief.missing_fields() or 'nothing'}")
    time.sleep(5)  # pause between calls to stay under free-tier rate limits