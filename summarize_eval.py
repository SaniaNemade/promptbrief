import json
from pathlib import Path

results = json.loads(Path("results/eval_results.json").read_text())


def pct(values):
    values = [v for v in values if v is not None]  # skip "not applicable"
    if not values:
        return "n/a"
    return f"{100 * sum(values) / len(values):.0f}% ({sum(values)}/{len(values)})"


def summarize(path):
    rows = [r[path] for r in results]
    return {
        "All sections present": pct([r["has_all_sections"] for r in rows]),
        "Correct needs-info label": pct([r["needs_info_correct"] for r in rows]),
        "Error messages kept exactly": pct([r["errors_preserved"] for r in rows]),
        "Secondary issues kept": pct([r["other_issues_kept"] for r in rows]),
        "Issues with invented details (lower is better)": pct([bool(r["invented_details"]) for r in rows]),
        "Avg actionability (1-5)": f"{sum(r['actionability'] for r in rows) / len(rows):.2f}",
    }


raw, brief = summarize("raw"), summarize("brief")
lines = ["| Metric | Raw input | Structured brief |", "|---|---|---|"]
lines += [f"| {metric} | {raw[metric]} | {brief[metric]} |" for metric in raw]
table = "\n".join(lines)
print(table)

print("\nInvented details found by the judge:")
for r in results:
    for path in ("raw", "brief"):
        for detail in r[path]["invented_details"]:
            print(f"- [{r['id']} / {path}] {detail}")

Path("results/eval_summary.md").write_text(
    f"# Evaluation results\n\n{len(results)} bug reports, one run each.\n\n{table}\n"
)