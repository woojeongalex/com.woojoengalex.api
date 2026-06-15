from pydantic import BaseModel, Field


class SpeechEvaluationResponse(BaseModel):
    id: int = Field(description="speech_evaluations.id")
    ok: bool = True
    message: str = "저장되었습니다."
