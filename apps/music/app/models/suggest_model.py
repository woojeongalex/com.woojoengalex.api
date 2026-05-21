"""보컬 평가 기반 장르·곡 추천 (`vocal_recommendations`)."""

from datetime import datetime
from typing import Any, Optional

from pydantic import ConfigDict
from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, func
from sqlmodel import Field, SQLModel


class VocalRecommendationEntity(SQLModel, table=True):
    """보컬 평가 1건(`sing_evaluations`)에 대한 추천 장르·곡 스냅샷."""

    __tablename__ = "vocal_recommendations"

    model_config = ConfigDict(populate_by_name=True)

    id: Optional[int] = Field(default=None, primary_key=True)

    sing_evaluation_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("sing_evaluations.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        description="FK → sing_evaluations.id",
    )

    pitch_score_snapshot: int = Field(description="분석 당시 음정 점수(스냅샷)")
    rhythm_score_snapshot: int = Field(description="분석 당시 박자 점수(스냅샷)")
    vocal_grade_snapshot: str = Field(max_length=32, description="등급 스냅샷")
    vocalization_pattern: str = Field(
        max_length=1024,
        description="음정·박자·발성 기준 요약(배너 설명문)",
    )

    recommended_genres: list[Any] = Field(
        default_factory=list,
        sa_column=Column(JSON, nullable=False),
        description='예: ["발라드", "뮤지컬 넘버"]',
    )
    recommended_songs: list[Any] = Field(
        default_factory=list,
        sa_column=Column(JSON, nullable=False),
        description='예: ["밤편지", "Defying Gravity"]',
    )

    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
    )
