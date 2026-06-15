from pydantic import BaseModel, Field


class VocalEvaluationResponse(BaseModel):
    id: int = Field(description="sing_evaluations.id")
    ok: bool = True
    message: str = "저장되었습니다."


SingEvaluationResponse = VocalEvaluationResponse
