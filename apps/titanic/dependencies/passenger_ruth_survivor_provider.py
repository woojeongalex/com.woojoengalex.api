from database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.pg.passenger_ruth_survivor_pg_repository import RuthSurvivorPgRepository
from titanic.app.ports.input.passenger_ruth_survivor_use_case import RuthSurvivorUseCase
from titanic.app.ports.output.passenger_ruth_survivor_repository import RuthSurvivorRepository
from titanic.app.use_cases.passenger_ruth_survivor_interactor import RuthSurvivorInteractor


def get_ruth_survivor_repository(db: AsyncSession = Depends(get_db)) -> RuthSurvivorRepository:
    return RuthSurvivorPgRepository(session=db)


def get_ruth_survivor_use_case(
    repository: RuthSurvivorRepository = Depends(get_ruth_survivor_repository)
) -> RuthSurvivorUseCase:
    return RuthSurvivorInteractor(repository=repository)
