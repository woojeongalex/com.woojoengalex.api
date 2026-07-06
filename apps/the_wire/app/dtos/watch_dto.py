from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class WatchStatusResult:
    history_id: str
    expiration: datetime
    updated_at: datetime


@dataclass(frozen=True)
class PolicyFilterCommand:
    sender: str
    subject: str
    body: str


@dataclass(frozen=True)
class PolicyFilterResult:
    verdict: str  # "PASS" | "BLOCK"
    score: float  # BLOCK 확률 (0.0 ~ 1.0)
    reason: str
