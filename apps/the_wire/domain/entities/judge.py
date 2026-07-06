from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Verdict(str, Enum):
    CASE_A = "CASE_A"  # 일반 업무 — Holmes 자체 종결
    CASE_B = "CASE_B"  # VIP/에스컬레이션 — StarCraft → Faker


@dataclass(frozen=True)
class JudgeEntity:
    """Watson Triage 판정 결과 엔티티."""

    sender: str
    subject: str
    body: str
    verdict: Verdict
    important_client: bool = False
    escalation_keywords: list[str] = field(default_factory=list)
    judged_at: datetime = field(default_factory=datetime.utcnow)
