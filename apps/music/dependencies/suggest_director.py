"""Suggest 의존성 조립소 — 추천 업로드·조회."""

from database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from music.adapter.outbound.pg.suggest_pg_repository import SuggestPgRepository
from music.app.ports.input.suggest_use_case import SuggestUseCase
from music.app.ports.output.suggest_repository_port import SuggestRepositoryPort
from music.app.use_cases.suggest_interactor import SuggestInteractor


def get_suggest_use_case(db: AsyncSession = Depends(get_db)) -> SuggestUseCase:
    repository: SuggestRepositoryPort = SuggestPgRepository(session=db)
    return SuggestInteractor(repository=repository)
