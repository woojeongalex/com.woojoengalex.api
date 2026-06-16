from database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.pg.passenger_jack_trainer_pg_repository import JackTrainerPgRepository
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository
from titanic.app.use_cases.passenger_jack_trainer_interactor import JackTrainerInteractor


def get_jack_train_repository(db: AsyncSession = Depends(get_db)) -> JackTrainerRepository:
    return JackTrainerPgRepository(session=db)


def get_jack_train_use_case(
    repository: JackTrainerRepository = Depends(get_jack_train_repository)
) -> JackTrainerUseCase:
    return JackTrainerInteractor(repository=repository)

