from datetime import datetime

from pydantic import BaseModel


class WatchStatusResponse(BaseModel):
    history_id: str
    expiration: datetime
    updated_at: datetime


class PolicyFilterResponse(BaseModel):
    verdict: str  # "PASS" | "BLOCK"
    score: float
    reason: str
