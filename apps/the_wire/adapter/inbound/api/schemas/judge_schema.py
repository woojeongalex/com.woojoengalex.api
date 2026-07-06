from pydantic import BaseModel


class JudgeRequest(BaseModel):
    sender: str
    subject: str
    body: str
    important_client: bool = False


class JudgeResponse(BaseModel):
    verdict: str  # "CASE_A" | "CASE_B"
    sender: str
    subject: str
    reason: str
    judged_at: str
