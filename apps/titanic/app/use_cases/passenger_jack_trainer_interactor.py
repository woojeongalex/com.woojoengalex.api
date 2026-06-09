from __future__ import annotations

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainSchema
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainQuery, JackTrainResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainUseCase
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainRepository


class JackTrainInteractor(JackTrainUseCase):
    def __init__(self, repository: JackTrainRepository):
        self.repository = repository

    async def introduce_myself(self, schema: JackTrainSchema) -> JackTrainResponse:
        '''잭 도슨의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(JackTrainQuery(
            id=schema.id,
            name=schema.name
        ))
