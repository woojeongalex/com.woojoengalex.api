from typing import Optional

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class AdminModel(SQLModel):
    """관리자 전용 DTO 스텁 (`table=False` — DB 테이블 없음)."""

    model_config = ConfigDict(populate_by_name=True)

    id: Optional[int] = Field(default=None, description="placeholder")
