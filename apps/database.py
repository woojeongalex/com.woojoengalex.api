import asyncio
import os
import sys
from pathlib import Path

import logging

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

_BACKEND_DIR = Path(__file__).resolve().parent.parent
load_dotenv(_BACKEND_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

engine = None
AsyncSessionLocal: async_sessionmaker[AsyncSession] | None = None


class Base(DeclarativeBase):
    """SQLAlchemy 2.0 Declarative 베이스 — ORM 모델은 이 클래스를 상속합니다."""


def _async_database_url(url: str) -> str:
    """Neon 비동기 접속용 URL (asyncpg)로 정규화합니다."""
    if url.startswith("postgresql+psycopg://"):
        url = url.replace("postgresql+psycopg://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+asyncpg://", 1)

    if "?" in url:
        base, query = url.split("?", 1)
        params: list[str] = []
        for p in query.split("&"):
            if not p or p.startswith("channel_binding="):
                continue
            if p.startswith("sslmode="):
                params.append("ssl=require")
            else:
                params.append(p)
        url = f"{base}?{'&'.join(params)}" if params else base
    elif "neon.tech" in url:
        url = f"{url}?ssl=require"
    return url


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    global engine, AsyncSessionLocal

    if AsyncSessionLocal is not None:
        return AsyncSessionLocal

    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set. Configure it in backend/.env.")

    async_url = _async_database_url(DATABASE_URL)

    try:
        engine = create_async_engine(async_url, echo=False)
        AsyncSessionLocal = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        return AsyncSessionLocal
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Database driver is not installed. Install asyncpg."
        ) from exc


async def init_db() -> None:
    """등록된 ORM 모델 기준으로 테이블을 생성합니다 (개발·초기 설정용)."""
    logger.info("[database] init_db 시작")
    session_factory = get_session_factory()
    assert engine is not None
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("[database] init_db 완료")


async def get_db():
    """FastAPI Dependency — 비동기 DB 세션을 주입합니다."""
    session_factory = get_session_factory()
    async with session_factory() as session:
        yield session


async def dispose_engine() -> None:
    """앱 종료 시 엔진 연결을 정리합니다."""
    global engine, AsyncSessionLocal

    local_engine = engine
    engine = None
    AsyncSessionLocal = None
    if local_engine is not None:
        await local_engine.dispose()
