from typing import Any

from pydantic import BaseModel, Field


class VideoVocalAnalysisResponse(BaseModel):
    """비디오→오디오 분석 최종 응답."""

    pitch_data: dict[str, Any] = Field(
        description="음정 요약(샘플레이트, 평균 f0, f0 샘플 등)"
    )
    bpm: float = Field(description="추정 BPM")
    duration: float = Field(description="오디오 길이(초)")
    emotions: dict[str, float] = Field(
        description="감정 점수 (0~1 등, 외부 API 연동 시 확장)"
    )
