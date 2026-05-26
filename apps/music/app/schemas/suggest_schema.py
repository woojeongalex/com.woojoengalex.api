"""추천 배너 API — 보컬 평가 ID 기반."""

from pydantic import BaseModel, ConfigDict, Field


class VocalRecommendationCreateRequest(BaseModel):
    """추천 생성: 저장된 보컬 평가 행 ID."""

    model_config = ConfigDict(populate_by_name=True)

    sing_evaluation_id: int = Field(ge=1, alias="singEvaluationId")


class VocalRecommendationResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(description="vocal_recommendations.id")
    sing_evaluation_id: int = Field(alias="singEvaluationId")
    pitch_score_snapshot: int = Field(
        alias="pitchScoreSnapshot",
        description="DB 비저장 · ai_vocal_analyses 조인값",
    )
    rhythm_score_snapshot: int = Field(
        alias="rhythmScoreSnapshot",
        description="DB 비저장 · ai_vocal_analyses 조인값",
    )
    vocal_grade_snapshot: str = Field(
        alias="vocalGradeSnapshot",
        description="DB 비저장 · ai_vocal_analyses 조인값",
    )
    vocalization_pattern: str = Field(alias="vocalizationPattern")
    recommended_genres: list[str] = Field(alias="recommendedGenres")
    recommended_songs: list[str] = Field(alias="recommendedSongs")
