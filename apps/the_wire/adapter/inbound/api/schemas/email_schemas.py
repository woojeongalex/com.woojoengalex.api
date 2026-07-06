from pydantic import BaseModel


class EmailRequest(BaseModel):
    to: str
    subject: str
    topic: str


class EmailResponse(BaseModel):
    success: bool
    detail: str


class SentEmailSchema(BaseModel):
    id: int
    recipient: str
    subject: str
    body: str
    sent_at: str
    has_embedding: bool


class SentEmailListResponse(BaseModel):
    emails: list[SentEmailSchema]
