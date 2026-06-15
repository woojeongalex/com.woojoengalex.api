from pydantic import BaseModel


class SpeechTopicHit(BaseModel):
    topic_id: str
    label: str
    description: str


class SpeechTopicsResponse(BaseModel):
    hits: list[SpeechTopicHit]
    count: int
