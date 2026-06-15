from pydantic import BaseModel, Field


class InstrumentEvaluationResponse(BaseModel):
    id: int = Field(description="instrument_evaluations.id")
    ok: bool = True
    message: str = "저장되었습니다."
