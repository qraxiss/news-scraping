from script.models.report import Report
from api.telegram.connection import interface


def report_to_text(report: Report) -> str:
    if report.content:
        f"◼{report.title}\n\n📰{report.content}\n\n{report.link}"

    return f"◼{report.title}\n\n🔗{report.link}"


def report(report: Report):
    return interface.request(["send-message"], method="post", json={
        "text": report_to_text(report)
    })
