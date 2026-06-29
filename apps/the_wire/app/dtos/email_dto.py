from dataclasses import dataclass


@dataclass(frozen=True)
class EmailCommand:
    to: str
    subject: str
    topic: str


@dataclass(frozen=True)
class EmailResult:
    success: bool
    detail: str
