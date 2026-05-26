from pydantic import BaseModel, ConfigDict, Field


class SpeechTopicHit(BaseModel):
    topic_id: str
    label: str
    description: str


class SpeechTopicsResponse(BaseModel):
    hits: list[SpeechTopicHit]
    count: int


class SpeechEvaluationCreateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    topic_id: str = Field(max_length=64, alias="topicId")
    clarity_score: int = Field(ge=0, le=100, alias="clarityScore")
    pace_score: int = Field(ge=0, le=100, alias="paceScore")
    tone_score: int = Field(ge=0, le=100, alias="toneScore")
    summary: str = Field(max_length=2048)
    feedback_points: list[str] = Field(default_factory=list, alias="feedbackPoints")
    file_name: str = Field(default="", max_length=512, alias="fileName")
    duration_sec: int = Field(default=0, ge=0, alias="durationSec")


class SpeechEvaluationResponse(BaseModel):
    id: int = Field(description="speech_evaluations.id")
    ok: bool = True
    message: str = "저장되었습니다."
