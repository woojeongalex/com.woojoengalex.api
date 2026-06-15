from typing import Any

from pydantic import BaseModel, Field


class VideoVocalAnalysisResponse(BaseModel):
    pitch_data: dict[str, Any]
    bpm: float
    duration: float
    emotions: dict[str, float] = Field(default_factory=dict)
