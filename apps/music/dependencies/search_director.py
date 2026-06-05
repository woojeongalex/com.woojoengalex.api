"""Search(Walter) 의존성 조립소 — MR 검색·조회."""

from database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from music.adapter.outbound.pg.list_pg_repository import ListPgRepository
from music.app.ports.input.search_use_case import SearchUseCase
from music.app.ports.output.list_repository_port import ListRepositoryPort
from music.app.use_cases.search_interactor import SearchInteractor


def get_search_use_case(db: AsyncSession = Depends(get_db)) -> SearchUseCase:
    repository: ListRepositoryPort = ListPgRepository(session=db)
    return SearchInteractor(repository=repository)
