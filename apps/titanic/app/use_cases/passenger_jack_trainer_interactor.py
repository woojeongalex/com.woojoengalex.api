from __future__ import annotations

from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository


class JackTrainerInteractor(JackTrainerUseCase):
    def __init__(self, repository: JackTrainerRepository):
        self.repository = repository

    async def introduce_myself(self, request) -> JackTrainerResponse:
        return await self.repository.introduce_myself(JackTrainerQuery(
            id=request.id,
            name=request.name,
        ))
