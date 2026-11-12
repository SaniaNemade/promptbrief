from core.structurer import structure_report

reports = {
    "slow-09": "dashboard takes like 30 seconds to load since monday. chrome on mac. other pages are fine",
    "payment-08": "charged twice for my order #48213!! paid with visa. need refund asap",
}

for report_id, text in reports.items():
    for attempt in range(1, 4):
        brief = structure_report(text)
        print(f"{report_id} attempt {attempt}: frequency = {brief.frequency}")
        