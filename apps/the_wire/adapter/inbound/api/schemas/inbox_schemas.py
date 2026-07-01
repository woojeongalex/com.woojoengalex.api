from datetime import datetime

from pydantic import BaseModel


class ReceiveMailRequest(BaseModel):
    sender: str
    subject: str = ""
    body: str = ""


class InboxMailResponse(BaseModel):
    id: int
    sender: str
    subject: str
    body: str
    received_at: datetime
    is_read: bool


class InboxListResponse(BaseModel):
    mails: list[InboxMailResponse]
