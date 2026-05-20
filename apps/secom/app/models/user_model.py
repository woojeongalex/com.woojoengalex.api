import logging
from datetime import datetime
from typing import Optional

import bcrypt
from pydantic import ConfigDict
from sqlalchemy import Column, DateTime, String, func, text
from sqlmodel import Field, SQLModel

logger = logging.getLogger(__name__)


def hash_password(plain: str) -> str:
    # bcrypt는 레이어 6 — DEBUG만 (요청마다 INFO 스팸 방지)
    logger.debug("[AUTH-FLOW][signup][6/model] bcrypt hash")
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    logger.debug("[AUTH-FLOW][login][6/model] bcrypt verify")
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


class UserEntity(SQLModel, table=True):
    """회원 테이블 — ENTITY_RULE: 시스템 PK는 `id` 단일."""

    __tablename__ = "users"

    model_config = ConfigDict(populate_by_name=True)

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="시스템 내부 자동 증가 PK",
    )
    username: str = Field(
        max_length=64,
        unique=True,
        index=True,
        description="로그인 아이디",
    )
    nickname: str = Field(max_length=64)
    email: str = Field(max_length=255)
    password_hash: str = Field(max_length=255)
    role: str = Field(
        default="user",
        sa_column=Column(
            String(16),
            nullable=False,
            server_default=text("'user'"),
        ),
    )
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
    )
