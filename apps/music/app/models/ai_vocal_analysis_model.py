"""AI 보컬 분석 — `ai_vocal_analyses`. 평가 **대상**은 USER가 아니라 `USER_VOCAL_RECORDING`."""

from datetime import datetime
from typing import Optional

from pydantic import ConfigDict
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlmodel import Field, SQLModel


class AiVocalAnalysisEntity(SQLModel, table=True):
    """사용자 녹음·영상 1건에 대한 AI 평가 결과 (`user_vocal_recordings` 1:1)."""

    __tablename__ = "ai_vocal_analyses"

    model_config = ConfigDict(populate_by_name=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    user_vocal_recording_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("user_vocal_recordings.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
            index=True,
        ),
    )
    analysis_engine: str = Field(
        max_length=32,
        description="예: librosa, mic_demo, client",
    )
    pitch_score: int
    rhythm_score: int
    vocal_grade: str = Field(max_length=32)
    summary: str = Field(max_length=2048)
    analyzed_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
    )
