"""Neon DB 연결·세션·테이블 초기화 (SQLAlchemy 2.0 async + SQLModel)."""

import os
import threading
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

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None
_init_lock = threading.Lock()
_initialized = False

_ASYNC_DRIVER_PREFIXES = (
    "postgresql+asyncpg://",
    "postgresql+psycopg://",
    "sqlite+aiosqlite://",
)


def _database_url() -> str:
    url = os.getenv("DATABASE_URL", "").strip()
    if not url:
        raise RuntimeError(
            "DATABASE_URL이 설정되지 않았습니다. backend/.env를 확인하세요."
        )
    return url


def _normalize_async_database_url(url: str) -> str:
    """sync 스타일 URL을 async 드라이버 URL로 맞춥니다."""
    lower = url.lower()
    if lower.startswith(_ASYNC_DRIVER_PREFIXES):
        return url
    if lower.startswith("postgresql://"):
        return "postgresql+asyncpg://" + url[len("postgresql://") :]
    if lower.startswith("postgres://"):
        return "postgresql+asyncpg://" + url[len("postgres://") :]
    raise RuntimeError(
        "DATABASE_URL은 비동기 드라이버가 필요합니다. "
        "예: postgresql+asyncpg://user:pass@host/db"
    )


def _init_engine_and_factory() -> None:
    global _engine, _session_factory, _initialized
    if _initialized:
        return
    with _init_lock:
        if _initialized:
            return
        url = _normalize_async_database_url(_database_url())
        _engine = create_async_engine(
            url,
            echo=False,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
        )
        _session_factory = async_sessionmaker(
            bind=_engine,
            expire_on_commit=False,
        )
        _initialized = True


def get_engine() -> AsyncEngine:
    _init_engine_and_factory()
    assert _engine is not None
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    _init_engine_and_factory()
    assert _session_factory is not None
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
    import titanic.adapter.outbound.orm.person_orm  # noqa: F401
    import titanic.adapter.outbound.orm.booking_orm  # noqa: F401
    import titanic.adapter.outbound.orm.titanic_passenger_orm  # noqa: F401


async def init_db() -> None:
    _register_orm_models()
    async with get_engine().begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def dispose_engine() -> None:
    global _engine, _session_factory, _initialized
    with _init_lock:
        if _engine is not None:
            await _engine.dispose()
        _engine = None
        _session_factory = None
        _initialized = False


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with get_session_factory()() as session:
        yield session
