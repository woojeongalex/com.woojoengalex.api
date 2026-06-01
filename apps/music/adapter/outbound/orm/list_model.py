from datetime import datetime
from typing import Optional

from pydantic import ConfigDict
from sqlalchemy import Column, DateTime, Integer, String, func
from sqlmodel import Field, SQLModel


class SongMrSearchListEntity(SQLModel, table=True):
    """노래 MR 검색 1회·일치 곡 1행 (검색할 때마다 INSERT)."""

    __tablename__ = "song_mr_search_lists"

    model_config = ConfigDict(populate_by_name=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    search_query: str = Field(max_length=512, index=True)
    catalog_song_id: str = Field(max_length=64, index=True)
    title: str = Field(max_length=255)
    artist: str = Field(max_length=255)
    bpm: int
    song_key: str = Field(sa_column=Column("song_key", String(64)))
    range_label: str = Field(max_length=255)
    mr_track_name: str = Field(max_length=512)
    mr_description: str = Field(max_length=1024)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
    )
