from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class InstrumentCatalogHit(BaseModel):
    instrument_id: str
    label: str
    description: str
    standard_tuning: str


class InstrumentCatalogResponse(BaseModel):
    query: str = ""
    hits: list[InstrumentCatalogHit]
    count: int


class InstrumentEvaluationCreateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: Literal["guitar", "piano"] = Field(alias="instrumentId")
    tuning_accuracy: int = Field(ge=0, le=100, alias="tuningAccuracy")
    pitch_deviation_cents: int = Field(alias="pitchDeviationCents")
    summary: str = Field(max_length=2048)
    string_readings: list[dict[str, Any]] = Field(
        default_factory=list, alias="stringReadings"
    )
    file_name: str = Field(default="", max_length=512, alias="fileName")
    duration_sec: int = Field(default=0, ge=0, alias="durationSec")


class InstrumentEvaluationResponse(BaseModel):
    id: int = Field(description="instrument_evaluations.id")
    ok: bool = True
    message: str = "저장되었습니다."
