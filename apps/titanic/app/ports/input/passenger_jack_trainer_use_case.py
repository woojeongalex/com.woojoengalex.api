from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainSchema
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainResponse


class JackTrainUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: JackTrainSchema) -> JackTrainResponse:
        '''잭 도슨의 자기소개 메소드'''
        pass