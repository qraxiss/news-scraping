from api.wordpress.connection import interface as wordpressApi
from script.models.report import Report


def send_report(report: Report):
    return wordpressApi.request(
        ["createAiPost"],
        json={
            "title": report.title,
            "content": report.content
        },
        method="post"
    )
