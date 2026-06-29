from pydantic import BaseModel


class EmailRequest(BaseModel):
    to: str
    subject: str
    topic: str


class EmailResponse(BaseModel):
    success: bool
    detail: str
