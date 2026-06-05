"""Evaluation(James) 의존성 조립소 — 보컬 평가 업로드."""

from database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from music.adapter.outbound.pg.evaluation_pg_repository import EvaluationPgRepository
from music.adapter.outbound.pg.list_pg_repository import ListPgRepository
from music.app.ports.input.evaluation_use_case import EvaluationUseCase
from music.app.ports.output.evaluation_repository_port import EvaluationRepositoryPort
from music.app.ports.output.list_repository_port import ListRepositoryPort
from music.app.use_cases.evaluation_interactor import EvaluationInteractor


def get_evaluation_use_case(db: AsyncSession = Depends(get_db)) -> EvaluationUseCase:
    repository: EvaluationRepositoryPort = EvaluationPgRepository(session=db)
    list_repository: ListRepositoryPort = ListPgRepository(session=db)
    return EvaluationInteractor(
        repository=repository,
        list_repository=list_repository,
    )
