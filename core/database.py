"""Neon DB 연결·세션·테이블 초기화 (아웃바운드 인프라)."""

import os
from collections.abc import AsyncGenerator
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import SQLModel

load_dotenv(Path(__file__).resolve().parent / ".env")

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def _database_url() -> str:
    url = os.getenv("DATABASE_URL", "").strip()
    if not url:
        raise RuntimeError(
            "DATABASE_URL이 설정되지 않았습니다. backend/.env를 확인하세요."
        )
    return url


def get_engine() -> AsyncEngine:
    global _engine
    if _engine is None:
        _engine = create_async_engine(
            _database_url(),
            echo=False,
            pool_pre_ping=True,
        )
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    global _session_factory
    if _session_factory is None:
        _session_factory = async_sessionmaker(
            get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _session_factory


def _register_orm_models() -> None:
    """create_all 전에 모든 SQLModel 테이블 메타데이터를 등록."""
    import music.adapter.outbound.orm.ai_vocal_analysis_model  # noqa: F401
    import music.adapter.outbound.orm.evaluation_models  # noqa: F401
    import music.adapter.outbound.orm.instrument_evaluation_model  # noqa: F401
    import music.adapter.outbound.orm.instrument_recording_model  # noqa: F401
    import music.adapter.outbound.orm.instrument_tuning_analysis_model  # noqa: F401
    import music.adapter.outbound.orm.list_model  # noqa: F401
    import music.adapter.outbound.orm.sing_model  # noqa: F401
    import music.adapter.outbound.orm.speech_evaluation_model  # noqa: F401
    import music.adapter.outbound.orm.speech_feedback_analysis_model  # noqa: F401
    import music.adapter.outbound.orm.speech_recording_model  # noqa: F401
    import music.adapter.outbound.orm.suggest_model  # noqa: F401
    import music.adapter.outbound.orm.user_vocal_recording_model  # noqa: F401
    import friday13th.adapter.outbound.orm.user_model  # noqa: F401
    import titanic.adapter.outbound.orm.titanic_passenger_orm  # noqa: F401


async def init_db() -> None:
    _register_orm_models()
    async with get_engine().begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def dispose_engine() -> None:
    global _engine, _session_factory
    if _engine is not None:
        await _engine.dispose()
    _engine = None
    _session_factory = None


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    factory = get_session_factory()
    async with factory() as session:
        yield session
