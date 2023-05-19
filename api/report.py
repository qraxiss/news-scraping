from script.models.report import Report
from api.connection import interface

def report_to_text(report: Report)->str:
    return f"◼{report.title}\n🔗{report.link}"

def report(report : Report):
    return interface.request(["send-message"], method="post", json={
        "text": report_to_text(report)
    })