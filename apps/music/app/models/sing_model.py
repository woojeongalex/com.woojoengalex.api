from datetime import datetime
from typing import Optional

from pydantic import ConfigDict
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlmodel import Field, SQLModel


class SingEvaluationEntity(SQLModel, table=True):
    """보컬 평가 세션 1건 — 녹음·AI·추천 묶음(허브). 평가 대상은 USER가 아님."""

    __tablename__ = "sing_evaluations"

    model_config = ConfigDict(populate_by_name=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(
        default=None,
        sa_column=Column(
            Integer,
            ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
            index=True,
        ),
        description="평가 세션을 수행한 회원 (로그인 연동 시)",
    )
    catalog_song_id: Optional[str] = Field(
        default=None,
        sa_column=Column(String(64), nullable=True, index=True),
    )
    mr_search_list_id: Optional[int] = Field(
        default=None,
        sa_column=Column(
            Integer,
            ForeignKey("song_mr_search_lists.id", ondelete="SET NULL"),
            nullable=True,
            index=True,
        ),
    )
    input_source: str = Field(max_length=16)
    pitch_score: int
    rhythm_score: int
    vocal_grade: str = Field(max_length=32)
    summary: str = Field(max_length=2048)
    file_name: str = Field(max_length=512)
    duration_sec: int
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
    )
