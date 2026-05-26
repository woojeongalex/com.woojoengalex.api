"""
분석 화면 3단계 ↔ API 요청 순서.

1) 음정·박자·등급·요약 → `ai_vocal_analyses` 에만 저장
2) 입력 메타 · MR·카탈로그 맥락 → `user_vocal_recordings`
3) 세션 허브 → `sing_evaluations` (user_id 시각 등만; 점수·곡 중복 없음)
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class VocalEvaluationCreateRequest(BaseModel):
    """클라이언트 → 서버 (camelCase 허용). 필드 선언 순서는 화면 카드 순서와 동일."""

    model_config = ConfigDict(populate_by_name=True)

    pitch_score: int = Field(
        ge=0,
        le=100,
        alias="pitchScore",
        description="음정 정확도 (%)",
    )
    rhythm_score: int = Field(
        ge=0,
        le=100,
        alias="rhythmScore",
        description="박자 정확도 (%)",
    )
    vocal_grade: str = Field(
        max_length=32,
        alias="vocalGrade",
        description="AI 피드백 등급 (예: A-)",
    )
    summary: str = Field(max_length=2048, description="AI 피드백 요약")

    catalog_song_id: str | None = Field(
        default=None,
        max_length=64,
        alias="catalogSongId",
        description="선택 곡. mrSearchListId 있으면 MR 행 catalog로 정합 → user_vocal_recordings",
    )
    mr_search_list_id: int | None = Field(
        default=None,
        ge=1,
        alias="mrSearchListId",
        description="녹음에 사용한 song_mr_search_lists.id (uses_mr 정본)",
    )
    input_source: Literal["mic", "video"] = Field(
        alias="inputSource",
        description="mic | video",
    )
    file_name: str = Field(default="", max_length=512, alias="fileName")
    duration_sec: int = Field(default=0, ge=0, alias="durationSec")


class VocalEvaluationResponse(BaseModel):
    id: int = Field(description="sing_evaluations.id")
    ok: bool = True
    message: str = "저장되었습니다."
