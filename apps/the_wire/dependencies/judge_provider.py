from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

try:
    from database import get_db
except ModuleNotFoundError:
    from apps.database import get_db

from the_wire.adapter.outbound.repositories.judge_pg_repository import JudgePgRepository
from the_wire.app.ports.input.judge_use_case import JudgeUseCase
from the_wire.app.ports.output.judge_repository_port import JudgeRepositoryPort
from the_wire.app.use_cases.judge_interactor import JudgeInteractor


def get_judge_repository(
    db: AsyncSession = Depends(get_db),
) -> JudgeRepositoryPort:
    return JudgePgRepository(session=db)


def get_judge_use_case(
    repository: JudgeRepositoryPort = Depends(get_judge_repository),
) -> JudgeUseCase:
    return JudgeInteractor(repository=repository)
