"""추천 배너 API — 분석 결과 ID 기반."""

from pydantic import BaseModel, ConfigDict, Field


class VocalRecommendationCreateRequest(BaseModel):
    """추천 생성: 저장된 보컬 분석 행 ID."""

    model_config = ConfigDict(populate_by_name=True)

    vocal_sing_result_id: int = Field(ge=1, alias="vocalSingResultId")


class VocalRecommendationResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(description="vocal_recommendations.id")
    vocal_sing_result_id: int = Field(alias="vocalSingResultId")
    pitch_score_snapshot: int = Field(alias="pitchScoreSnapshot")
    rhythm_score_snapshot: int = Field(alias="rhythmScoreSnapshot")
    vocal_grade_snapshot: str = Field(alias="vocalGradeSnapshot")
    vocalization_pattern: str = Field(alias="vocalizationPattern")
    recommended_genres: list[str] = Field(alias="recommendedGenres")
    recommended_songs: list[str] = Field(alias="recommendedSongs")
