from database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.pg.crew_james_pg_repository import JamesPgRepository
from titanic.app.ports.input.crew_james_use_case import JamesUseCase
from titanic.app.ports.output.crew_james_repository import JamesRepository
from titanic.app.use_cases.crew_james_interactor import JamesInteractor


def get_james_repository(db: AsyncSession = Depends(get_db)) -> JamesRepository:
    return JamesPgRepository(session=db)


def get_james_use_case(
    repository: JamesRepository = Depends(get_james_repository)
) -> JamesUseCase:
    return JamesInteractor(repository=repository)
