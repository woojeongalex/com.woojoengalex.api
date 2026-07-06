from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class JudgeCommand:
    sender: str
    subject: str
    body: str
    important_client: bool = False


@dataclass(frozen=True)
class JudgeResult:
    verdict: str  # "CASE_A" | "CASE_B"
    sender: str
    subject: str
    reason: str
    judged_at: datetime
