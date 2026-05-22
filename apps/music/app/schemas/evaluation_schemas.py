"""
분석 화면 3단계(음정·박자·AI 피드백) ↔ API ↔ DB 필드 순서.

1) 음정 정확도 (pitch_score)
2) 박자 정확도 (rhythm_score)
3) AI 피드백 등급 (vocal_grade)
4) 요약 텍스트 (summary)
5) MR·곡 맥락 + 입력 메타 (catalog_song_id, mr_search_list_id → USER_VOCAL_RECORDING, input_source, file_name, duration_sec)
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
        description="녹음·분석 시 선택 곡. mrSearchListId 있으면 MR 행 catalog로 정합 → user_vocal_recordings·sing_evaluations",
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
