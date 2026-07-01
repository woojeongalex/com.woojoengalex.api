from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ReceiveMailCommand:
    sender: str
    subject: str
    body: str


@dataclass(frozen=True)
class InboxResult:
    id: int
    sender: str
    subject: str
    body: str
    received_at: datetime
    is_read: bool
