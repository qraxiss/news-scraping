from dataclasses import dataclass


@dataclass
class Report:
    title: str
    link: str
    content: str = None
