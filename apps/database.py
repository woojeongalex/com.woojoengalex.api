import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

load_dotenv()


# Neon DB URL 가져오기
DATABASE_URL = os.getenv("DATABASE_URL")
engine = None
AsyncSessionLocal = None

Base = declarative_base()


def get_session_factory():
    global engine, AsyncSessionLocal

    if AsyncSessionLocal is not None:
        return AsyncSessionLocal

    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set. Configure it in .env.")

    try:
        engine = create_async_engine(DATABASE_URL, echo=True)
        AsyncSessionLocal = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        return AsyncSessionLocal
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Database driver is not installed. Install psycopg[binary]."
        ) from exc


# Dependency: DB 세션 주입
async def get_db():
    try:
        session_factory = get_session_factory()
        async with session_factory() as session:
            yield session
    except Exception as exc:
        raise RuntimeError(f"Database session error: {exc}") from exc
